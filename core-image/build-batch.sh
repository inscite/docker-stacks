#!/usr/bin/env bash
# comment and uncomment this file as you need

# pure cpu images
#docker build --no-cache -t inscite/base-conda:0.4 -f ./Dockerfile .
#docker build --no-cache -t inscite/base-conda:0.4-gcc4.8 -f ./Dockerfile.gcc4.8 .

# cuda 10.0 images
#docker build --no-cache -t inscite/base-conda:0.4-cuda10.0 -f ./Dockerfile.cuda10.0 .
#docker build --no-cache -t inscite/base-conda:0.4-cuda10.0-gcc4.8 -f ./Dockerfile.cuda10.0_gcc4.8 .

# cuda 10.1 images
#docker build --no-cache -t inscite/base-conda:0.4-cuda10.1 -f ./Dockerfile.cuda10.1 .
#docker build --no-cache -t inscite/base-conda:0.4-cuda10.1-gcc4.8 -f ./Dockerfile.cuda10.1_gcc4.8 .

# cuda 10.2 images
#docker build --no-cache -t inscite/base-conda:0.4-cuda10.2 -f ./Dockerfile.cuda10.2 .
#docker build --no-cache -t inscite/base-conda:0.4-cuda10.2-gcc4.8 -f ./Dockerfile.cuda10.2_gcc4.8 .

docker images | grep inscite/base-conda | grep 0.4
