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
chown -R $NB_UID:$NB_GID /home/$NB_USER

# (verify|export) conda-env clone
if [ "${EXPORTMODE}" == "VERIFY" ]; then
    su -c "${CONDAEVAL};"'conda create --clone "$SRCENVNAME" -p /opt/conda/pubenvs/"${DSTENVNAME}";' $NB_USER
    su -c "${CONDAEVAL};python /opt/condaenv-export-validation.py ${SRCENVNAME} ${DSTENVNAME};" $NB_USER
    su -c "rm -rf /opt/conda/pubenvs/${DSTENVNAME};" $NB_USER
elif [ "${EXPORTMODE}" == "EXPORT" ]; then
    su -c "${CONDAEVAL};"'conda create --clone "$SRCENVNAME" -p /opt/conda/pubenvs/"${DSTENVNAME}";' $NB_USER
elif [ "${EXPORTMODE}" == "QUERYENVS" ]; then
    su -c "${CONDAEVAL};python /opt/condaenv-adapter.py conda env list;" $NB_USER
elif [ "${EXPORTMODE}" == "QUERYPKGS" ]; then
    su -c "${CONDAEVAL};python /opt/condaenv-adapter.py conda list -n ${SRCENVNAME};" $NB_USER
elif [ "${EXPORTMODE}" == "WETRUN" ]; then
    su -c "${CONDAEVAL};python /opt/condaenv-adapter.py "'${WETRUNARGS};' $NB_USER
else
    echo 
fi
