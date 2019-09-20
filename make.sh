#!/bin/bash

mkdir -p build
cd build   
if [ $(gcc -dumpmachine | cut -f1 -d -) = "aarch64" ]
then
  CFLAGS=-DPLATFORM_TEGRA
fi
cmake \
-D DS_SDK_ROOT=/home/test/Downloads/deepstream_sdk_v4.0_jetson \
-D CFLAGS=${CFLAGS} . ..
make clean
make -j 2 VERBOSE=1
cd -