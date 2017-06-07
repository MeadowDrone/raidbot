import os
import subprocess
import bs4
import requests
import re

from tools.static_config import static_config

def arrstatus():
    session = requests.Session()
    headers = {
        'Accept-Language': 'en-us,en;q=0.5',
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_8_4) Chrome/27.0.1453.116 Safari/537.36',
    }
    session.headers.update(headers)
    req = session.get('http://eu.finalfantasyxiv.com/lodestone/worldstatus/')

    if not req:
        return None

    status_soup = bs4.BeautifulSoup(req.content, "html5lib")
    '''with open("data/status_soup.txt", "a") as soup_file:
        soup_file.write(str(status_soup))
    soup_file.close()'''

    status_dict = dict()
    for tag in status_soup.select('.item-list__worldstatus'):
        server_status = re.sub('\n+', ' ', tag.text.strip().replace('\t', ''))
        status_dict[server_status.split(' ')[0]] = server_status.split(' ')[1]
    
    return status_dict

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
