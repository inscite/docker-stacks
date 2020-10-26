import sys
import subprocess

"""Copyright (c) 2020 Seungkyun Hong. <nah@kakao.com>
   Distributed under the terms of the 3-Clause BSD License.
"""

def main():

    print("Exec: {:}".format(str(sys.argv)))
    if len(sys.argv) > 1:
        try:
            subproc = subprocess.run(sys.argv[1:], check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, encoding="UTF-8")
#            print(subproc.stdout, file=sys.stdout)
#            print(subproc.stderr, file=sys.stderr)
            print("[D] STDOUT:\n{:}".format(subproc.stdout))
            print("[D] STDERR:\n{:}".format(subproc.stderr))
        except (subprocess.SubprocessError, subprocess.CalledProcessError) as e:
            print("[E] error occurred while running:\nExec: {:}\n{:}".format(str(sys.argv[1:]), str(e)))
    else:
        pass

    sys.exit(0)
    return

if __name__ == "__main__":
    main()
