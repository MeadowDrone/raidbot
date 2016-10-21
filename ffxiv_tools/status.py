import os
import subprocess

from tools.config import config

def status(server):
    lobbyhostname = config.get('static', 'lobby')
    serverhostname = config.get('static', server)
    excalping = ''

    if os.system('ping -c 1 ' + lobbyhostname) != 0:
        return "lobby is down :("
    else:
        serverpoll = os.system('ping -c 1 ' + serverhostname)
    
    if serverpoll != 0:
        return "%s is down :(" % (serverhostname)
    else:
        excalping = [line.rpartition('=')[-1]
                     for line in subprocess.check_output(
            ['ping', '-c', '1', serverhostname]).splitlines()[1:-4]][0]
        return("%s is up. ping from the UK is %s" % (server, str(excalping)))
