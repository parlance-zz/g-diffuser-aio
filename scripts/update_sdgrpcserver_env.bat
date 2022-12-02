REM cwd should be g-diffuser-aio\stable-diffusion-grpcserver
"..\env\micromamba.exe" run -r "..\env" -n sd-grpc-server python -m flit install --pth-file
pause