#!/bin/bash
cd ..
./micromamba/micromamba-`uname` -r ./env -n sd-grpc-server run python ./g-diffuser/g_diffuser_cli.py
