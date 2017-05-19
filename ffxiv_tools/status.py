import os
import subprocess

from tools.static_config import static_config

def status(server):
    lobbyhostname = static_config.get('static', 'lobby')
    serverhostname = static_config.get('static', server)
    excalping = ''

    if os.system('ping -c 1 ' + lobbyhostname) != 0:
        return "lobby is down :("
    else:
        serverpoll = os.system('ping -c 1 ' + serverhostname)
    
    if serverpoll != 0:
        return "{} is down :(".format(serverhostname)
    else:
        excalping = [line.rpartition('=')[-1]
                     for line in subprocess.check_output(
            ['ping', '-c', '1', serverhostname]).splitlines()[1:-4]][0]
        return("{} is up. ping from the UK is {}".format(server, str(excalping)))
