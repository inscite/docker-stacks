import sys
import subprocess

"""Copyright (c) 2020 Seungkyun Hong. <nah@kakao.com>
   Distributed under the terms of the 3-Clause BSD License.
"""

def main():

    if len(sys.argv) > 1:
        subproc = subprocess.run(sys.argv[1:], capture_output=True)
        print(subproc.stdout.decode('UTF-8'), file=sys.stdout)
        print(subproc.stderr.decode('UTF-8'), file=sys.stderr)
    else:
        pass

    return

if __name__ == "__main__":
    main()
