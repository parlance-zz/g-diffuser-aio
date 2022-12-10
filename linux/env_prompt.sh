#!/bin/bash
chmod +x ../micromamba/micromamba-`uname`
../micromamba/micromamba-`uname` shell init --prefix=../env
../micromamba/micromamba-`uname` activate sd-grpc-server