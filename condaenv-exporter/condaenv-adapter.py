import os
import signal
import sys
from subprocess import Popen, PIPE as spPIPE, STDOUT as spSTDOUT, CalledProcessError, SubprocessError, TimeoutExpired
from functools import partial

"""Copyright (c) 2020 Seungkyun Hong. <nah@kakao.com>
   Distributed under the terms of the 3-Clause BSD License.
"""


def sig_handler(signum, frame):
    # fin
    sys.exit(0)
    return


def main():

    print("Exec: {:}".format(str(sys.argv)))
    try:
        logfile_path = os.environ['LOGFILE']
    except KeyError:
        logfile_path = None
    print("os.environ['LOGFILE']: {:}".format(logfile_path))

    # handling current pid of wrapper
    pid = os.getpid()
    print("PID: {:d}".format(pid))
    with open('/var/run/wetrun.pid', 'w') as f:
        f.write("{:d}".format(pid))
        f.flush()
        f.close()

    # set sigkill handling as main thread termination
    t_signals = (signal.SIGHUP, signal.SIGINT, signal.SIGTERM) # code 1, 2, 15
    for t_sig in t_signals:
        signal.signal(t_sig, sig_handler)

    if len(sys.argv) > 1:
        try:
            fn_subproc = partial(Popen, stdout=spPIPE, stderr=spSTDOUT, encoding='UTF-8')
            subproc_result = fn_subproc(sys.argv[1:])
            callfail = False
        except (CalledProcessError, SubprocessError, TimeoutExpired) as e:
            print("[E] error occurred while running:\nExec: {:}\n{:}".format(str(sys.argv[1:]), str(e)))
            subproc_result = e
            callfail = False
        except OSError as e:
            subproc_result = str(e)
            callfail = True

        if logfile_path is not None and logfile_path != '' and logfile_path != '-':
            try:
                with open(logfile_path, mode='w') as f:
                    if not callfail:
                        comm = subproc_result  # Popen.communicate()
                        # only for valid spawned process which was executed by all means
                        for comm_stdout_inst in comm.stdout:
                            f.write(comm_stdout_inst)
                            f.flush()
                    else:
                        # the process was not spawned
                        f.write(subproc_result + '\n')
                        f.flush()
                    f.flush()
                    f.close()
            except Exception as e:
                # reserved for further exception handling
                pass
        else:
            pass

        # print("[D] STDOUT:\n{:}".format(subproc_result.stdout))
        # print("[D] STDERR:\n{:}".format(subproc_result.stderr))
        #
        # if logfile_path is not None and logfile_path != '' and logfile_path != '-':
        #     with open(logfile_path, mode='w') as f:
        #         f.write("=====[STDOUT]=====\n")
        #         f.write(subproc_result.stdout)
        #         f.flush()
        #         f.write("=====[STDERR]=====\n")
        #         f.write(subproc_result.stderr)
        #         f.flush()
        #         f.close()
    else:
        pass

    return


if __name__ == "__main__":
    main()
