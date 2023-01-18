#!/bin/bash
cd ..
./micromamba/micromamba-`uname` -r ./env -n sd-grpc-server run python ./scripts/run.py