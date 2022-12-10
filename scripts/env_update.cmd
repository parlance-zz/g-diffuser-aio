"..\env\micromamba.exe" run -r "..\env" -y update -f "..\environment.yaml"
"..\env\micromamba.exe" run -r "..\env" -n sd-grpc-server python -m flit install --pth-file "..\stable-diffusion-grpcserver"
pause