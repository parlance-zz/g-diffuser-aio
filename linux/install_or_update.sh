#!/bin/bash
cd ..
chmod +x ./micromamba/micromamba-`uname`
export PIP_EXTRA_INDEX_URL=https://download.pytorch.org/whl/cu116
[ -d "./env" ] ||  ./micromamba/micromamba-`uname` -r ./env -y create -f ./environment.yaml
./micromamba/micromamba-`uname` -r ./env -y update -f ./environment.yaml
./micromamba/micromamba-`uname` -r ./env -n sd-grpc-server run python ./scripts/install_or_update.py
