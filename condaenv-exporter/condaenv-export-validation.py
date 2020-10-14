import os
import sys
import subprocess

"""Copyright (c) 2020 Seungkyun Hong. <nah@kakao.com>
   Distributed under the terms of the 3-Clause BSD License.
"""

def refine_pkgs_info(inst, join=True):
    if not inst.startswith('#'):
        result = list(filter(None, inst.split(' ')))
        return ' '.join(result) if join else result
    else:
        return None

def main():
    
    SRCENVNAME = sys.argv[1]
    DSTENVNAME = sys.argv[2]

    # 00. get-prefix
    prefix_info = {}
    prefix_src = subprocess.run("conda env list".split(' '), capture_output=True)
    for env in prefix_src.stdout.decode('utf-8').strip().split('\n'):
        if env.startswith('#') or env.startswith('base'):
            pass
        else:
            env_info = list(filter(None, env.split(' ')))
            prefix_info.update({env_info[0]: env_info[-1]})
        continue

    # 01. conda-list
    condaenv_src = {"cmd": "conda list -n {:}".format(SRCENVNAME).split(' ')}
    condaenv_dst = {"cmd": "conda list -n {:}".format(DSTENVNAME).split(' ')}

    condaenv_src.update({"proc": subprocess.run(condaenv_src["cmd"], capture_output=True)})
    condaenv_dst.update({"proc": subprocess.run(condaenv_dst["cmd"], capture_output=True)})

    condaenv_src.update({
        "stdout": condaenv_src["proc"].stdout.decode("utf-8").strip(),
        "stderr": condaenv_src["proc"].stderr.decode("utf-8").strip(),
    })

    condaenv_dst.update({
        "stdout": condaenv_dst["proc"].stdout.decode("utf-8").strip(),
        "stderr": condaenv_dst["proc"].stderr.decode("utf-8").strip(),
    })

    src_conda_set = set(filter(None, [refine_pkgs_info(inst) for inst in condaenv_src["stdout"].split('\n')]))
    dst_conda_set = set(filter(None, [refine_pkgs_info(inst) for inst in condaenv_dst["stdout"].split('\n')]))
    chk01 = src_conda_set==dst_conda_set
    print("conda#src:{:}, conda#dst:{:}, conda-equal?{:}".format(len(src_conda_set), len(dst_conda_set), chk01))

    # 02. pip-freeze
    pip_src = {"cmd": "{:}/bin/pip freeze".format(prefix_info[SRCENVNAME]).split(' ')}
    pip_dst = {"cmd": "{:}/bin/pip freeze".format(prefix_info[DSTENVNAME]).split(' ')}

    pip_src.update({"proc": subprocess.run(pip_src["cmd"], capture_output=True)})
    pip_dst.update({"proc": subprocess.run(pip_dst["cmd"], capture_output=True)})

    pip_src.update({
        "stdout": pip_src["proc"].stdout.decode("utf-8").strip(),
        "stderr": pip_dst["proc"].stderr.decode("utf-8").strip(),
    })

    pip_dst.update({
        "stdout": pip_src["proc"].stdout.decode("utf-8").strip(),
        "stderr": pip_dst["proc"].stderr.decode("utf-8").strip(),
    })

    src_pip_set = set(filter(None, [refine_pkgs_info(inst) for inst in pip_src["stdout"].split('\n')]))
    dst_pip_set = set(filter(None, [refine_pkgs_info(inst) for inst in pip_dst["stdout"].split('\n')]))
    chk02 = src_pip_set==dst_pip_set
    print("pip#src:{:}, pip#dst:{:}, pip-equal?{:}".format(len(src_pip_set), len(dst_pip_set), chk02))

    # 03. python-ver-check
    py_src = {"cmd": "{:}/bin/python /opt/chk_py_ver.py".format(prefix_info[SRCENVNAME]).split(' ')}
    py_dst = {"cmd": "{:}/bin/python /opt/chk_py_ver.py".format(prefix_info[DSTENVNAME]).split(' ')}

    py_src.update({"proc": subprocess.run(py_src["cmd"], capture_output=True)})
    py_dst.update({"proc": subprocess.run(py_dst["cmd"], capture_output=True)})

    py_src.update({
        "stdout": py_src["proc"].stdout.decode("utf-8").strip(),
        "stderr": py_src["proc"].stderr.decode("utf-8").strip(),
    })

    py_dst.update({
        "stdout": py_dst["proc"].stdout.decode("utf-8").strip(),
        "stderr": py_dst["proc"].stderr.decode("utf-8").strip(),
    })

    chk03 = py_src["stdout"] == py_dst["stdout"]
    print("pychk-equal?{:}".format(chk03))

    # 04. aggregation
    print("valid-condaenv-clone?{:}".format(chk01 and chk02 and chk03))

    return

if __name__ == "__main__":
    main()
