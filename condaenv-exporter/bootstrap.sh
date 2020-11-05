#!/bin/bash

# Copyright (c) 2020 Seungkyun Hong. <nah@kakao.com>
# Distributed under the terms of the 3-Clause BSD License.

groupadd -g $NB_GID $NB_USER
useradd -u $NB_UID -g $NB_GID $NB_USER -s /bin/bash
usermod -aG 100 $NB_USER
cp -R /home/dataon /home/$NB_USER
chown -R $NB_UID:$NB_GID /home/$NB_USER

CONDAEVAL='eval "$(/opt/conda/bin/conda shell.bash hook)"'
su -c "${CONDAEVAL};conda config --prepend envs_dirs /opt/conda/pubenvs" $NB_USER
su -c "${CONDAEVAL};conda config --prepend envs_dirs /home/${NB_USER}/miniconda3/envs" $NB_USER

# threading
# reference: https://github.com/conda/conda/releases/tag/4.7.11
if [[ ! -z ${CONDA_DEFAULT_THREADS} ]]; then
    su -c "${CONDAEVAL};conda config --set default_threads ${CONDA_DEFAULT_THREADS}" $NB_USER
fi

# ownership take
chown -R $NB_UID:$NB_GID /home/$NB_USER

if [ "${LAP}" == "TRUE" ]; then
    EXECMD="time su -c"
else
    EXECMD="su -c"
fi

# (verify|export) conda-env clone
if [ "${EXPORTMODE}" == "VERIFY" ]; then
    ${EXECMD} "${CONDAEVAL};"'conda create --clone "$SRCENVNAME" -p /opt/conda/pubenvs/"${DSTENVNAME}";' $NB_USER
    ${EXECMD} "${CONDAEVAL};python /opt/condaenv-export-validation.py ${SRCENVNAME} ${DSTENVNAME};" $NB_USER
    ${EXECMD} "rm -rf /opt/conda/pubenvs/${DSTENVNAME};" $NB_USER
elif [ "${EXPORTMODE}" == "EXPORT" ]; then
    ${EXECMD} "${CONDAEVAL};"'ls -alh /opt/conda/pubenvs/;df -h;conda create --clone "$SRCENVNAME" -p /opt/conda/pubenvs/"${DSTENVNAME}";' $NB_USER
elif [ "${EXPORTMODE}" == "QUERYENVS" ]; then
    ${EXECMD} "${CONDAEVAL};python /opt/condaenv-adapter.py conda env list;" $NB_USER
elif [ "${EXPORTMODE}" == "QUERYPKGS" ]; then
    ${EXECMD} "${CONDAEVAL};python /opt/condaenv-adapter.py conda list -n ${SRCENVNAME};" $NB_USER
elif [ "${EXPORTMODE}" == "WETRUN" ]; then
    ${EXECMD} "${CONDAEVAL};conda activate ${SRCENVNAME};LOGFILE="${LOGFILE}" python /opt/condaenv-adapter.py "'${WETRUNARGS};' $NB_USER
else
    echo 
fi
