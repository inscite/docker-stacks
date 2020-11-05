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
$ docker build -t kisti.rdp/dataon.kr/condaenv-exporter:0.3.3 --no-cache .

# apply container image on localhost docker
$ docker push kisti.rdp/dataon.kr/condaenv-exporter:0.3.3

# optional: container image dump
$ docker save -o condaenv-exporter_0_3_3.tar kisti.rdp/dataon.kr/condaenv-exporter:0.3.3

# optional: loading dumped container image
$ docker load < condaenv-exporter_0_3_3.tar
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
* **LOGFILE**: destination for logfile as a result of **WETRUN**
* **LAP**: debug flag for benchmarking each execution of condaenv-exporter (TRUE or FALSE, default:FALSE)
* **CONDA_DEFAULT_THREADS**: number of conda internal threadpool size (default: 10)

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

---
##Revisions
* 0.3.3 **(latest)** #73e790d : multi-threaded tasking in conda internals and clean-up
* 0.3.2 *(bypass)* #1a50be5a : multi-threaded tasking in conda internals
* 0.3 (baseline) #08b0346b : baseline for beta showcase
---
##Only for fun
###  Launch demo condaenv-exporter instance with current user
```console
./condaenv-exporter.sh $(whoami) $(id -u) $(id -g) VERIFY <srcenvname> <dstenvname>
```
### Get log of launched pods
```console
kubectl logs -f $(kubectl describe job condaenv-exporter | grep Created | tr -s ' ' | cut -d' ' -f8)
```
### Remove specific c8s image on current node
```console
docker rmi <registry>/dataon.kr/condaenv-exporter:<version>
```

### Rebuild specific c8s image
```console
docker build -t <registry>/dataon.kr/condaenv-exporter:<version> --no-cache .
docker push <registry>/dataon.kr/condaenv-exporter:<version>
```