pushd %0\..\
cd ..
.\env\micromamba.exe update -r .\env -n sd-grpc-server -y -f .\environment.yaml
cd stable-diffusion-grpcserver
..\env\micromamba.exe run -r ..\env -n sd-grpc-server python -m flit install --pth-file
popd
pause