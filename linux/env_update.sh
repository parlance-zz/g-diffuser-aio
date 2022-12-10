#!/bin/bash
chmod +x ../micromamba/micromamba-`uname`
../micromamba/micromamba-`uname` -r ../env -y update -f ../environment.yaml
../micromamba/micromamba-`uname` -r ../env -n sd-grpc-server python -m flit install --pth-file ../stable-diffusion-grpcserver
