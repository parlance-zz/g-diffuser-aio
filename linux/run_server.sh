#!/bin/bash
cd ..
chmod +x ./micromamba/micromamba-`uname`
./micromamba/micromamba-`uname` -r ./env -n sd-grpc-server run python ./scripts/run.py