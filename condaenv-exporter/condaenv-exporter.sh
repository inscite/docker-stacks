#!/bin/bash

# Copyright (c) 2020 Seungkyun Hong. <nah@kakao.com>
# Distributed under the terms of the 3-Clause BSD License.

export NB_USER=$1
export NB_UID=$2
export NB_GID=$3
export EXPORTMODE=$4
export SRCENVNAME=$5
export DSTENVNAME=$6

export BASE_YAML="job-condaenv-exporter.yaml"

sed -e 's/\$NB_USER/"'"${NB_USER}"'"/g;' \
    -e 's/\$NB_UID/"'"${NB_UID}"'"/g;' \
    -e 's/\$NB_GID/"'"${NB_GID}"'"/g;' \
    -e 's/\$EXPORTMODE/"'"${EXPORTMODE}"'"/g;' \
    -e 's/\$SRCENVNAME/"'"${SRCENVNAME}"'"/g;' \
    -e 's/\$DSTENVNAME/"'"${DSTENVNAME}"'"/g;' \
    $BASE_YAML | kubectl apply -f -
