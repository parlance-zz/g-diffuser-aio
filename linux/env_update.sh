#!/bin/bash
cd ..
chmod +x ./micromamba/micromamba-`uname`
./micromamba/micromamba-`uname` -r ./env -y update -f ./environment.yaml
cd stable-diffusion-grpcserver
../micromamba/micromamba-`uname` -r ../env -n sd-grpc-server run python -m flit install --pth-file
