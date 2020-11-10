import os
import sys
from subprocess import run as sprun, PIPE as spPIPE, CalledProcessError, SubprocessError, TimeoutExpired
from functools import partial

"""Copyright (c) 2020 Seungkyun Hong. <nah@kakao.com>
   Distributed under the terms of the 3-Clause BSD License.
"""


def main():

    print("Exec: {:}".format(str(sys.argv)))
    try:
        logfile_path = os.environ['LOGFILE']
    except KeyError:
        logfile_path = None
    print("os.environ['LOGFILE']: {:}".format(logfile_path))

    # subproc_result = None
    if len(sys.argv) > 1:
        try:
            fn_subproc = partial(sprun, check=True, stdout=spPIPE, stderr=spPIPE, encoding='UTF-8')
            subproc_result = fn_subproc(sys.argv[1:])

        except (CalledProcessError, SubprocessError, TimeoutExpired) as e:
            print("[E] error occurred while running:\nExec: {:}\n{:}".format(str(sys.argv[1:]), str(e)))
            subproc_result = e

        print("[D] STDOUT:\n{:}".format(subproc_result.stdout))
        print("[D] STDERR:\n{:}".format(subproc_result.stderr))

        if logfile_path is not None and logfile_path != '' and logfile_path != '-':
            with open(logfile_path, mode='w') as f:
                f.write("=====[STDOUT]=====\n")
                f.write(subproc_result.stdout)
                f.flush()
                f.write("=====[STDERR]=====\n")
                f.write(subproc_result.stderr)
                f.flush()
                f.close()
    else:
        pass

    sys.exit(0)


if __name__ == "__main__":
    main()
