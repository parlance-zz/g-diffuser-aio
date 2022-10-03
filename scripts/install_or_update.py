from os import path
import subprocess, os, shutil

def main():
    base=path.dirname(path.dirname(__file__))

    # Create config if it doesn't exist
    
    if not path.exists(path.join(base, "config")):
        shutil.copy(path.join(base, "config.dist"), path.join(base, "config"))

    # Update this repo, and any submodules

    if not path.exists(path.join(base, ".git")):
        subprocess.run(("git", "init"), cwd=base)
        subprocess.run(("git", "remote", "add", "origin", "../idea2art-aio/"), cwd=base)

    subprocess.run(("git", "fetch"), cwd=base)
    subprocess.run(("git", "reset", "--hard", "origin/main"), cwd=base)
    subprocess.run(("git", "submodule", "update", "--init", "--recursive"), cwd=base)
    
    # Install the server dependencies

    subprocess.run(("flit","install","--pth-file"), cwd=os.path.join(base, "stable-diffusion-grpcserver"))

if __name__ == "__main__":
    main()