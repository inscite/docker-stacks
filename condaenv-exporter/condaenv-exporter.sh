#!/bin/bash

# Copyright (c) 2020 Seungkyun Hong. <nah@kakao.com>
# Distributed under the terms of the 3-Clause BSD License.

# condaenv-exporter launcher
# req. container: dataon.kr/condaenv-exporter:0.2

export SU_USR=$1
export SU_UID=$2
export SU_GID=$3
export EXPORTMODE=$4
export SRCENVNAME=$5
export DSTENVNAME=$6
export WETRUNARGS=$7

export BASE_YAML="job-condaenv-exporter.yaml"

sed -e 's/\$NB_USER/"'"${SU_USR}"'"/g;' \
    -e 's/\$NB_UID/"'"${SU_UID}"'"/g;' \
    -e 's/\$NB_GID/"'"${SU_GID}"'"/g;' \
    -e 's/\$EXPORTMODE/"'"${EXPORTMODE}"'"/g;' \
    -e 's/\$SRCENVNAME/"'"${SRCENVNAME}"'"/g;' \
    -e 's/\$DSTENVNAME/"'"${DSTENVNAME}"'"/g;' \
    -e 's/\$WETRUNARGS/"'"${WETRUNARGS}"'"/g;' \
    $BASE_YAML | kubectl apply -f -
