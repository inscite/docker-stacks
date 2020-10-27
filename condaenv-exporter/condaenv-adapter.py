import os
import sys
import subprocess
from functools import partial

"""Copyright (c) 2020 Seungkyun Hong. <nah@kakao.com>
   Distributed under the terms of the 3-Clause BSD License.
"""


def main():

    try:
        logfile_path = os.environ['LOGFILE']
    except KeyError:
        logfile_path = None
    print("os.environ['LOGFILE']: {:}".format(logfile_path))
    print("Exec: {:}".format(str(sys.argv)))
    if len(sys.argv) > 1:
        try:
            fn_subproc = partial(subprocess.run, check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, encoding='UTF-8')
            subproc = fn_subproc(sys.argv[1:])
            print("[D] STDOUT:\n{:}".format(subproc.stdout))
            print("[D] STDERR:\n{:}".format(subproc.stderr))
            if logfile_path is not None:
                with open(logfile_path, mode='w') as f:
                    f.write(subproc.stdout)
                    f.flush()
                    f.close()
        except (subprocess.SubprocessError, subprocess.CalledProcessError) as e:
            print("[E] error occurred while running:\nExec: {:}\n{:}".format(str(sys.argv[1:]), str(e)))
    else:
        pass

    # fin
    sys.exit(0)


if __name__ == "__main__":
    main()
