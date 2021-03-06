# Copyright (c) Jupyter Development Team.
# Copyright (c) Seungkyun Hong. <nah@kakao.com>
# Distributed under the terms of the Modified BSD License.

# Ubuntu 18.04 (bionic) -> condaenv-exporter:0.4
# https://hub.docker.com/_/ubuntu/?tab=tags&name=bionic
# OS/ARCH: linux/amd64
ARG ROOT_CONTAINER=inscite/base-conda:0.4
ARG BASE_CONTAINER=$ROOT_CONTAINER
FROM $BASE_CONTAINER

LABEL maintainer="Seungkyun Hong <nah@kakao.com>"

# conda clean-up
RUN conda clean --all -f -y && \
    rm -rf /home/$NB_USER/.cache/yarn && \
    echo "colorscheme delek" >> /home/$NB_USER/.vimrc && \
    fix-permissions $CONDA_DIR && \
    fix-permissions /home/$NB_USER

# Copy local files as late as possible to avoid cache busting
COPY bootstrap.sh /usr/local/bin/
COPY chk_py_ver.py condaenv-export-validation.py condaenv-adapter.py /opt/

# remember, working directory is root of container
USER root
WORKDIR /

# Configure container startup
ENTRYPOINT ["tini", "-g", "--"]
CMD ["bootstrap.sh"]
