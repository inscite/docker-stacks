#!/bin/bash
# Copyright (c) Jupyter Development Team.
# Distributed under the terms of the Modified BSD License.

set -e

wrapper=""
if [[ "${RESTARTABLE}" == "yes" ]]; then
    wrapper="run-one-constantly"
fi

if [[ ! -z "${JUPYTERHUB_API_TOKEN}" ]]; then
    # launched by JupyterHub, use single-user entrypoint
    # confirmed as base routine from base Dockerfile by inscite (20200820)
    conda config --prepend envs_dirs /opt/conda/pubenvs
    conda config --prepend envs_dirs /home/${NB_USER}/miniconda3/envs
    exec /usr/local/bin/start-singleuser.sh "$@"
elif [[ ! -z "${JUPYTER_ENABLE_LAB}" ]]; then
    . /usr/local/bin/start.sh $wrapper jupyter lab "$@"
else
    . /usr/local/bin/start.sh $wrapper jupyter notebook "$@"
fi
