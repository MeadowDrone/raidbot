import os
import subprocess


def status(lobbyhostname, excalhostname):
    excalping = ''
    lobbypoll = os.system('ping -c 1 ' + lobbyhostname)

    if lobbypoll != 0:
        return("primal data centre is down :(")
    else:
        excalpoll = os.system('ping -c 1 ' + excalhostname)
        if excalpoll != 0:
            return("excalibur is down :(")
        else:
            excalping = [line.rpartition('=')[-1]
                         for line in subprocess.check_output(
                ['ping', '-c', '1', excalhostname]).splitlines()[1:-4]][0]
            return("servers are up. ping from the UK to excalibur is %s" % str(excalping))
