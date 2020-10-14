# condaenv-exporter

conda environment exporter and user-condaenv subtitution

Author: Seungkyun Hong (<nah@kakao.com>)

---

## execution tree

condaenv-exporter.sh -> job-condaenv-exporter.yaml -> | k8s-cluster | -> bootstrap.sh

**You must edit job-condaenv-exporter.yaml appropriately for production environment,**
**especially storage mount options.**


## container build

```console
# fresh build of container image
$ docker build -t <docker-registry>/dataon.kr/condaenv-exporter:0.2 --no-cache .

# apply container image on localhost docker
$ docker push <docker-registry>/dataon.kr/condaenv-exporter:0.2

# optional: container image dump
$ docker save -o condaenv-exporter_0_2.tar <docker-registry>/dataon.kr/condaenv-exporter:0.2

# optional: loading dumped container image
$ docker load < condaenv-exporter_0_2.tar
```

## how-to-use

```console
$ condaenv-exporter.sh <SU_USR> <SU_UID> <SU_GID> <EXPORTMODE> <SRCENVNAME> <DSTENVNAME> <WETRUNARGS>
```

* **SU_USR**: username of subtituting user
* **SU_UID**: uid (user-id) of subtituting user
* **SU_GID**: gid (group-id) of subtituting user
* **EXPORTMODE**: runtime mode of this tool
 * **VERIFY**: testing and verification of condaenv export on temporary location
 * **EXPORT**: actual condaenv export (no verification mode of VERIFY)
 * **QUERYENVS**: same as `conda env list` with user-condaenv substitution
 * **QUERYPKGS**: same as `conda list -n <env>` with user-condaenv substitution
 * **WETRUN**: command execution (similar with `su -c`) with user-condaenv substitution
* **SRCENVNAME**: source condaenv name
* **DSTENVNAME**: destination condaenv name (for environment export)
* **WETRUNARGS**: arguments for user-condaenv substitution **(only used for EXPORTMODE: WETRUN)**

**Example: EXPORTMODE/VERIFY**

```console
# verifying condaenv export of meta02 (in usrenvs) -> meta03 (into pubenvs),
# with username xo (uid: 606200001, gid: 606300000)
$ condaenv-exporter.sh xo 606200001 606300000 VERIFY meta02 meta03
```

**Example: EXPORTMODE/EXPORT**
```console
# actual condaenv export of meta02 (in usrenvs) -> meta03 (into pubenvs),
# with username xo (uid: 606200001, gid: 606300000)
$ condaenv-exporter.sh xo 606200001 606300000 VERIFY meta02 meta03
```

**Example: EXPORTMODE/QUERYENVS**
```console
# condaenv listing with username xo (uid: 606200001, gid: 606300000)
$ condaenv-exporter.sh xo 606200001 606300000 QUERYENVS
```

**Example: EXPORTMODE/QUERYPKGS**
```console
# package listing of condaenv meta02 with username xo (uid: 606200001, gid: 606300000)
$ condaenv-exporter.sh xo 606200001 606300000 QUERYPKGS meta02
```

**Example: EXPORTMODE/WETRUN**
```console
# command substitution of condaenv meta02 with username xo (uid: 606200001, gid: 606300000)
$ condaenv-exporter.sh xo 606200001 606300000 WETRUN meta02 - "python -V"
```