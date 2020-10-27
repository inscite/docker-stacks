import os
import sys
import subprocess
from functools import partial

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

    fn_subproc = partial(subprocess.run, check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, encoding='UTF-8')

    # 00. get-prefix
    prefix_info = {}
    prefix_src = subprocess.run("conda env list".split(' '), capture_output=True)
    print("[D] conda env list:\n{:}".format(prefix_src.stdout.decode("utf-8")))
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

    try:
        condaenv_src.update({'proc': fn_subproc(condaenv_src['cmd'])})
        condaenv_src.update({
            'stdout': condaenv_src['proc'].stdout,
            'stderr': condaenv_src['proc'].stderr,
        })
    except (subprocess.SubprocessError, subprocess.CalledProcessError) as e:
        condaenv_src.update({
            'stdout': '',
            'stderr': "[E] error occurred while retrieving condaenv-src\nExec: {:}\n{:}".format(condaenv_src['cmd'],
                                                                                                str(e)),
        })

    try:
        condaenv_dst.update({'proc': fn_subproc(condaenv_dst['cmd'])})
        condaenv_dst.update({
            'stdout': condaenv_dst['proc'].stdout,
            'stderr': condaenv_dst['proc'].stderr,
        })
    except (subprocess.SubprocessError, subprocess.CalledProcessError) as e:
        condaenv_dst.update({
            'stdout': '',
            'stderr': "[E] error occurred while retrieving condaenv-dst\nExec: {:}\n{:}".format(condaenv_dst['cmd'],
                                                                                                str(e)),
        })

    src_conda_set = set(filter(None, [refine_pkgs_info(inst) for inst in condaenv_src["stdout"].split('\n')]))
    dst_conda_set = set(filter(None, [refine_pkgs_info(inst) for inst in condaenv_dst["stdout"].split('\n')]))
    chk01 = src_conda_set == dst_conda_set and len(src_conda_set) > 0 and len(dst_conda_set) > 0
    print("conda#src:{:}, conda#dst:{:}, conda-equal?{:}".format(len(src_conda_set), len(dst_conda_set), chk01))

    # 02. pip-freeze
    pip_src = {"cmd": "{:}/bin/pip freeze".format(prefix_info[SRCENVNAME]).split(' ')}
    pip_dst = {"cmd": "{:}/bin/pip freeze".format(prefix_info[DSTENVNAME]).split(' ')}

    try:
        pip_src.update({'proc': fn_subproc(pip_src['cmd'])})
        pip_src.update({
            'stdout': pip_src['proc'].stdout,
            'stderr': pip_src['proc'].stderr,
        })
    except (subprocess.SubprocessError, subprocess.CalledProcessError) as e:
        pip_src.update({
            'stdout': '',
            'stderr': "[E] error occurred while retrieving pipfreeze-src\nExec: {:}\n{:}".format(pip_src['cmd'],
                                                                                                 str(e)),
        })

    try:
        pip_dst.update({'proc': fn_subproc(pip_dst['cmd'])})
        pip_dst.update({
            'stdout': pip_dst['proc'].stdout,
            'stderr': pip_dst['proc'].stderr,
        })
    except (subprocess.SubprocessError, subprocess.CalledProcessError) as e:
        pip_dst.update({
            'stdout': '',
            'stderr': "[E] error occurred while retrieving pipfreeze-dst\nExec: {:}\n{:}".format(pip_dst['cmd'],
                                                                                                 str(e)),
        })

    src_pip_set = set(filter(None, [refine_pkgs_info(inst) for inst in pip_src["stdout"].split('\n')]))
    dst_pip_set = set(filter(None, [refine_pkgs_info(inst) for inst in pip_dst["stdout"].split('\n')]))
    chk02 = src_pip_set == dst_pip_set and len(src_pip_set) > 0 and len(dst_pip_set) > 0
    print("pip#src:{:}, pip#dst:{:}, pip-equal?{:}".format(len(src_pip_set), len(dst_pip_set), chk02))

    # 03. python-ver-check
    py_src = {"cmd": "{:}/bin/python /opt/chk_py_ver.py".format(prefix_info[SRCENVNAME]).split(' ')}
    py_dst = {"cmd": "{:}/bin/python /opt/chk_py_ver.py".format(prefix_info[DSTENVNAME]).split(' ')}

    try:
        py_src.update({'proc': fn_subproc(py_src['cmd'])})
        py_src.update({
            'stdout': py_src['proc'].stdout,
            'stderr': py_src['proc'].stderr,
        })
    except (subprocess.SubprocessError, subprocess.CalledProcessError) as e:
        py_src.update({
            'stdout': 'py-chk-src-err',
            'stderr': "[E] error occurred while retrieving pychk-src\nExec: {:}\n{:}".format(py_src['cmd'], str(e)),
        })

    try:
        py_dst.update({'proc': fn_subproc(py_dst['cmd'])})
        py_dst.update({
            'stdout': py_dst['proc'].stdout,
            'stderr': py_dst['proc'].stderr,
        })
    except (subprocess.SubprocessError, subprocess.CalledProcessError) as e:
        py_dst.update({
            'stdout': 'py-chk-dst-err',
            'stderr': "[E] error occurred while retrieving pychk-dst\nExec: {:}\n{:}".format(py_dst['cmd'], str(e)),
        })

    chk03 = py_src["stdout"] == py_dst["stdout"]
    print("pychk-equal?{:}".format(chk03))

    # 04. aggregation
    chkAgg = chk01 and chk02 and chk03
    print("valid-condaenv-clone?{:}".format(chkAgg))

    sys.exit(0)
    return


if __name__ == "__main__":
    main()
