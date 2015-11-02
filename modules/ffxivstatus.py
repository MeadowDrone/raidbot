import os
import subprocess

def status(lobbyhostname, excalhostname):
    excalping = ''
    lobbypoll = os.system('ping -c 1 ' + lobbyhostname)
    excalpoll = os.system('ping -c 1 ' + excalhostname)

    if lobbypoll == 0:
        lobbyresponse = 'lobby is up'
    else:
        lobbyresponse = 'lobby is down'

    if excalpoll == 0:
        excalresponse = 'excalibur is up'
        excalping = [line.rpartition('=')[-1] 
                for line in subprocess.check_output(
                ['ping', '-c', '1', excalhostname]).splitlines()[1:-4]][0]
    else:
        excalresponse = 'excalibur is down'

    #print(excalping)
    if excalping == "":
        return('%s\n%s' % (lobbyresponse, excalresponse))
    else:
        return('%s\n%s\nping (UK) is %s' % (lobbyresponse, excalresponse, str(excalping)))