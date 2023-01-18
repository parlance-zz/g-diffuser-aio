#!/bin/bash
cd ..
chmod +x ./micromamba/micromamba-`uname`
eval "$(./micromamba shell hook -s posix --prefix=../env)"
#./micromamba/micromamba-`uname` shell init --prefix=../env
./micromamba/micromamba-`uname` activate sd-grpc-server