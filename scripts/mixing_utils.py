from diffusers import StableDiffusionInpaintPipeline
from diffusers import StableDiffusionPipeline
import torch
import argparse

def merge_difference(merged_pipe, target_pipe, base_pipe, alpha=0.5, merge_modules=["vae", "unet", "text_encoder"]):

    for mod_type in merge_modules:

        params1 = list(getattr(merged_pipe, mod_type).parameters())
        params2 = list(getattr(target_pipe, mod_type).parameters())
        params3 = list(getattr(base_pipe, mod_type).parameters())

        if not (len(params1) == len(params2) == len(params3)):
            print(f"Module: '{mod_type}' - skipping, parameter count mismatch")
            continue

        for p1, p2, p3 in zip(params1, params2, params3):
            assert(p2.shape == p3.shape)
            with torch.no_grad():
                if p1.shape != p2.shape:
                    min_shape = min(p1.shape, p2.shape)
                    assert(min_shape != p1.shape)
                    p1[tuple(slice(dim) for dim in min_shape)] += (p2 - p3) * alpha
                else:
                    p1 += (p2 - p3) * alpha

        print(f"Merged module: '{mod_type}'")

    return merged_pipe

def merge_mix(merged_pipe, target_pipe, alpha=0.5, merge_modules=["vae", "unet", "text_encoder"]):

    for mod_type in merge_modules:

        params1 = list(getattr(merged_pipe, mod_type).parameters())
        params2 = list(getattr(target_pipe, mod_type).parameters())

        if not (len(params1) == len(params2)):
            print(f"Module: '{mod_type}' - skipping, parameter count mismatch")
            continue

        for p1, p2 in zip(params1, params2):
            with torch.no_grad():
                if p1.shape != p2.shape:
                    min_shape = min(p1.shape, p2.shape)
                    assert(min_shape != p1.shape)
                    p1[tuple(slice(dim) for dim in min_shape)] = p1[tuple(slice(dim) for dim in min_shape)] * (1. - alpha) + p2 * alpha
                else:
                    p1[:] = p1 * (1. - alpha) + p2 * alpha

        print(f"Merged module: '{mod_type}'")

    return merged_pipe

def get_module_difference(mod1, mod2):
    
        params1 = list(mod1.parameters())
        params2 = list(mod2.parameters())
    
        if not (len(params1) == len(params2)):
            print(f"Warning: tensor parameter count mismatch (p1: {len(params1)}, p2: {len(params2)})")

        total_params = 0
        for p1, p2 in zip(params1, params2):
            if p1.shape != p2.shape:
                min_shape = min(p1.shape, p2.shape)
                print(p1.shape, p2.shape)
                assert(min_shape != p1.shape)
                total_params += p1[tuple(slice(dim) for dim in min_shape)].numel()
            else:
                total_params += p1.numel()
            
        diff = torch.zeros(total_params)
    
        with torch.no_grad():
            i = 0
            for p1, p2 in zip(params1, params2):
                if p1.shape != p2.shape:
                    min_shape = min(p1.shape, p2.shape)
                    p_size = p1[tuple(slice(dim) for dim in min_shape)].numel()
                    diff[i:i+p_size] = (p1[tuple(slice(dim) for dim in min_shape)] - p2).flatten()
                else:
                    p_size = p1.numel()
                    diff[i:i+p_size] = (p1 - p2).flatten()
                i += p_size

        print(f"diff abs min:  {diff.abs().min().item()}")
        print(f"diff abs max:  {diff.abs().max().item()}")
        print(f"diff abs mean: {diff.abs().mean().item()}")
        print(f"diff abs std:  {diff.abs().std().item()}")

        return diff

def get_model_difference(pipe1, pipe2, merge_modules=["vae", "unet", "text_encoder"]):
    for mod_type in merge_modules:
        print(f"Module: '{mod_type}'")
        get_module_difference(getattr(pipe1, mod_type), getattr(pipe2, mod_type))
        print()

    return
        
def main(args):

    target_pipe = StableDiffusionPipeline.from_pretrained(args.target_model_id)
    if args.merge_model_is_inpainting:
        merge_pipe = StableDiffusionInpaintPipeline.from_pretrained(args.merge_model_id)
    else:
        merge_pipe = StableDiffusionPipeline.from_pretrained(args.merge_model_id)

    if args.base_model_id is not None:
        base_pipe = StableDiffusionPipeline.from_pretrained(args.base_model_id)
        print(f"{args.target_model_id} - {args.base_model_id}:")
        if args.show_stats: get_model_difference(target_pipe, base_pipe, merge_modules=args.merge_modules)
        merge_difference(merge_pipe, target_pipe, base_pipe, args.alpha, merge_modules=args.merge_modules)
    else:
        print(f"{args.merge_model_id} - {args.target_model_id}:")
        if args.show_stats: get_model_difference(merge_pipe, target_pipe, merge_modules=args.merge_modules)
        merge_mix(merge_pipe, target_pipe, args.alpha, merge_modules=args.merge_modules)

    merge_pipe.save_pretrained(args.output_path)
    print(f"Saved merged model to: {args.output_path}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--merge_model_id", type=str)
    parser.add_argument("--target_model_id", type=str)
    parser.add_argument("--base_model_id", type=str, default=None)
    parser.add_argument("--alpha", type=float, default=0.5)
    parser.add_argument("--output_path", type=str)
    parser.add_argument("--show_stats", type=bool, default=True)
    parser.add_argument("--merge_model_is_inpainting", type=bool, default=False)
    parser.add_argument('--merge_modules', nargs='+', default=["vae", "unet", "text_encoder"])

    args = parser.parse_args()

    main(args)