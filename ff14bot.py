'''
Command list for botfather:
timers - Weekly and daily reset timers
status - [server] Pings lobby and data centres
turn - [1-13] Links to video guide for Coil raid, eg. /turn 5
alex - [1-4] Links to video guide for Alex Savage raid, eg. /alex 3
hildi - Because only a...
'''

import StringIO
import logging
import telegram
import random
import multipart
import datetime
import random
import simplejson
import re
import os
import subprocess
from PIL import Image

LAST_UPDATE_ID = None
TOKEN = '137935724:AAGLxDiFyow9PI4NnWxX93Yz0dks-7kKjuQ'
BASE_URL = 'https://api.telegram.org/bot' + TOKEN + '/'

def main():
    global LAST_UPDATE_ID

    logging.basicConfig(
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')

    # Telegram Bot Authorization Token
    bot = telegram.Bot(TOKEN)

    # This will be our global variable to keep the latest update_id when requesting
    # for updates. It starts with the latest update_id if available.
    try:
        LAST_UPDATE_ID = bot.getUpdates()[-1].update_id
    except IndexError:
        LAST_UPDATE_ID = None

    while True:
        brain(bot)

def brain(bot):

    def postPhoto(img):
        image = Image.open(img)
        output = StringIO.StringIO()

        if img[-3:].lower() == 'gif':
            ext = 'GIF'
        elif img[-3:].lower() == 'png':
            ext = 'PNG'
        elif img[-3:].lower() == 'jpg':
            ext = 'JPEG'

        image.save(output, ext)

        resp = multipart.post_multipart(BASE_URL + 'sendPhoto', [
            ('chat_id', str(chat_id)),
            # uncomment to quote original message
            #('reply_to_message_id', str(message_id)),
        ], [
            ('photo', 'image.jpg', output.getvalue()),
        ])

    def postDoodle(chat_id):
        bot.sendMessage(chat_id=chat_id,
                text='the doodle poll is here: http://doodle.com/pe2hyzt69mxvw7tx#table')

    def postHildi(chat_id):
        hildi = ['Hildibrand: We are as siblings now, my constant comrade, for I have shared with you the secrets of House Manderville. Now you must use that knowledge. Go to the fallen chimera and dance like only a Manderville can!']
        hildi.extend(['???: ([Singing]) Fancy yourself a Manderville man? You would do what only a Manderville can? Then lift up your legs, and put up your hands, be a Mander-Mander-Manderville, man!'])
        hildi.extend(['Godbert: But you were not drawn here by some coincidence, were you? No, you came in search of me, Godbert! Why else would you gyrate your hips in such a gentlemanly fashion, if not that?'])
        hildi.extend(['Godbert: HILDIBRAND HELIDOR MAXIMILLIAN MANDERVILLE!!!'])
        hildi.extend(['Godbert: ([Singing]) Godbert the Goldsmith\'s a Manderville man, Smithing as only a Manderville can, Oil him up and give him a tan, Fit for a Mander-Manderville man!'])
        hildi.extend(['Godbert: Hah! Do not worry, little one-- I deal with worse cases before my morning bowel movement!'])
        hildi.extend(['Hildibrand: Hah hah hah! A man so garishly dressed should be easy to find in snowy Coerthas!'])
        hildi.extend(['Hildibrand: A ridiculous outfit!'])
        hildi.extend(['Hildibrand: Hah hah, what reasons indeed? It is enough to make a gentleman laugh!'])
        hildi.extend(['Hildibrand: My redoubtable confederate!'])
        hildi.extend(['Hildibrand: Hail to thee, fellow servant of justice! '])
        hildi.extend(['Hildibrand: We have scoured every ilm of this area to no avail. I can only conclude that, having learned that his opponent was to be the legendary Inspector Hildibrand, the duelist renounced his criminal ways and retreated into hiding.'])
        hildi.extend(['Hildibrand: Though I will still endeavor to avoid fisticuffs, I will be duly armed should worse come to worst.'])
        hildi.extend(['Hildibrand: ...Wherefore art though, my nefarious nemesis?'])
        hildi.extend(['Gilgamesh: For Gilgamesh... It is embiggening time!'])
        hildi.extend(['Hildibrand: I believe this is addressed to me, condescending Inspector Briardien.\nBriardien: Piss off.'])
        hildi.extend(['Hildibrand: Very well! I-- and I alone-- Hildibrand, agent of enquiry, inspector extraordinaire, once more accept your challenge!'])

        hildi_imgs = ["img/hildi.png", "img/hildi2.png", 
                        "img/hildi3.jpg", "img/hildi4.gif", 
                        "img/hildi5.gif", "img/hildi6.gif", 
                        "img/hildi7.jpg", "img/hildi8.gif",
                        "img/hildi9.png", "img/hildi10.jpg",
                        "img/hildi11.png", "img/hildi12.png"]
        postPhoto(random.choice(hildi_imgs))
        bot.sendMessage(chat_id=chat_id,
                    text=random.choice(hildi))

    def postTimers(chat_id):
        # current time calculations
        # 5 hours behind UK time
        current_date = datetime.datetime.now()
        day_of_week_now = datetime.datetime.today().weekday()
        
        # daily timer calculation 
        if (current_date.hour < 11):
            extra_day_daily = 0
        else:
            extra_day_daily = 1

        daily_timer = datetime.datetime(
                current_date.year,
                current_date.month,
                current_date.day + extra_day_daily,
                11,
                0,
                0)

        # weekly timer calculation
        if (day_of_week_now == 0):
                days_until_weekly = 1
        elif (day_of_week_now == 1):
            if (current_date.hour < 4):
                days_until_weekly = 0
            else:
                days_until_weekly = 7
        else:
            days_until_weekly = 7 - day_of_week_now

        weekly_timer = datetime.datetime(
                current_date.year,
                current_date.month,
                current_date.day,# + days_until_weekly,
                4,
                0,
                0)

        # scrip reset calculation
        if (day_of_week_now == 0):
                days_until_scrip = 3
        elif (day_of_week_now == 1):
            days_until_scrip = 2
        elif (day_of_week_now == 2):
            days_until_scrip = 1
        elif (day_of_week_now == 3):
            if (current_date.hour < 4):
                days_until_scrip = 0
            else:
                days_until_scrip = 7
        else:
            days_until_scrip = 9 - day_of_week_now

        scrip_timer = datetime.datetime(
                current_date.year,
                current_date.month,
                current_date.day,# + days_until_scrip,
                4,
                0,
                0)

        daily_delta = daily_timer - current_date
        weekly_delta = weekly_timer - current_date
        scrip_delta = scrip_timer - current_date

        #print daily reset
        daily_hours, daily_remainder = divmod(daily_delta.seconds, 3600)
        daily_minutes, daily_seconds = divmod(daily_remainder, 60)

        #print weekly reset
        weekly_hours, weekly_remainder = divmod(weekly_delta.seconds, 3600)
        weekly_minutes, weekly_seconds = divmod(weekly_remainder, 60)

        #print scrip reset
        scrip_hours, scrip_remainder = divmod(scrip_delta.seconds, 3600)
        scrip_minutes, scrip_seconds = divmod(scrip_remainder, 60)

        weekly_days = weekly_delta.days + days_until_weekly
        scrip_days = scrip_delta.days + days_until_scrip

        if (daily_hours == 1): dhstr = ' hour, '
        else: dhstr = ' hours, '
        if (daily_minutes == 1): dmstr = ' minute'
        else: dmstr = ' minutes'
        if (daily_seconds == 1): dsstr = ' second'
        else: dsstr = ' seconds'

        if (weekly_days == 1): wdstr = ' day, '
        else: wdstr = ' days, '
        if (weekly_hours == 1): whstr = ' hour, '
        else: whstr = ' hours, '
        if (weekly_minutes == 1): wmstr = ' minute'
        else: wmstr = ' minutes'
        if (weekly_seconds == 1): wsstr = ' second'
        else: wsstr = ' seconds'

        if (scrip_days == 1): sdstr = ' day, '
        else: sdstr = ' days, '
        if (scrip_hours == 1): shstr = ' hour, '
        else: shstr = ' hours, '
        if (scrip_minutes == 1): smstr = ' minute'
        else: smstr = ' minutes'
        if (scrip_seconds == 1): ssstr = ' second'
        else: ssstr = ' seconds'

        if (weekly_days == 0):
            bot.sendMessage(chat_id=chat_id,
                    text=str(daily_hours) + dhstr +
                    str(daily_minutes) + dmstr + ' and ' +
                    str(daily_seconds) + dsstr + ' until daily reset\n' +

                    str(weekly_hours) + whstr +
                    str(weekly_minutes) + wmstr + ' and ' +
                    str(weekly_seconds) + wsstr + ' until weekly reset\n' +

                    str(scrip_days) + sdstr +
                    str(scrip_hours) + shstr +
                    str(scrip_minutes) + smstr + ' and ' +
                    str(scrip_seconds) + ssstr + ' until gatherer & crafter weekly scrip reset')
        elif (scrip_delta.days == 0):
            bot.sendMessage(chat_id=chat_id,
                    text=str(daily_hours) + dhstr +
                    str(daily_minutes) + dmstr + ' and ' +
                    str(daily_seconds) + dsstr + ' until daily reset\n' +

                    str(weekly_days) + wdstr +
                    str(weekly_hours) + whstr +
                    str(weekly_minutes) + wmstr + ' and ' +
                    str(weekly_seconds) + wsstr + ' until weekly reset\n' +

                    str(scrip_hours) + shstr +
                    str(scrip_minutes) + smstr + ' and ' +
                    str(scrip_seconds) + ssstr + ' until gatherer & crafter weekly scrip reset')
        else:
            bot.sendMessage(chat_id=chat_id,
                    text=str(daily_hours) + dhstr +
                    str(daily_minutes) + dmstr + ' and ' +
                    str(daily_seconds) + dsstr + ' until daily reset\n' +

                    str(weekly_days) + wdstr +
                    str(weekly_hours) + whstr +
                    str(weekly_minutes) + wmstr + ' and ' +
                    str(weekly_seconds) + wsstr + ' until weekly reset\n' +

                    str(scrip_days) + sdstr +
                    str(scrip_hours) + shstr +
                    str(scrip_minutes) + smstr + ' and ' +
                    str(scrip_seconds) + ssstr + ' until gatherer & crafter weekly scrip reset')

    def postRoster(chat_id):
        bot.sendMessage(chat_id=chat_id,
                            text='roster and progression sheet is here: ' + 
                            'https://docs.google.com/spreadsheets/d/1VpcDmkDOxsdoUxZOQuZkgTdHsR436SwFhzU3FlRP2tc/edit?usp=sharing \nTANKS: Una & Shevi' 
                    + '\nHEALERS: Arelle & Lilinette'
                    + '\nDPS: Sefal, Mymla, Leone & ???')

    def postStatus(chat_id):
        '''if (server.lower() == 'alexander'): address = '124.150.157.47' 
        elif (server.lower() == 'aegis'): address = '124.150.157.24'
        elif (server.lower() == 'atomos'): address = '124.150.157.33'
        elif (server.lower() == 'carbuncle'): address = '124.150.157.33'
        elif (server.lower() == 'garuda'): address = '124.150.157.25'
        elif (server.lower() == 'gungnir'): address = '124.150.157.39'
        elif (server.lower() == 'kujata'): address = '124.150.157.31'
        elif (server.lower() == 'ramuh'): address = '124.150.157.30'
        elif (server.lower() == 'tonberry'): address = '124.150.157.30'
        elif (server.lower() == 'typhon'): address = '124.150.157.33'
        elif (server.lower() == 'unicorn'): address = '124.150.157.32'
        elif (server.lower() == 'bahamut'): address = '124.150.157.45'
        elif (server.lower() == 'durandal'): address = '124.150.157.50'
        elif (server.lower() == 'fenrir'): address = '124.150.157.47'
        elif (server.lower() == 'ifrit'): address = '124.150.157.46'
        elif (server.lower() == 'ridill'): address = '124.150.157.43'
        elif (server.lower() == 'tiamat'): address = '124.150.157.52'
        elif (server.lower() == 'ultima'): address = '124.150.157.47'
        elif (server.lower() == 'valefor'): address = '124.150.157.47'
        elif (server.lower() == 'yojimbo'): address = '124.150.157.25'
        elif (server.lower() == 'zeromus'): address = '124.150.157.43'
        elif (server.lower() == 'anima'): address = '124.150.157.28'
        elif (server.lower() == 'asura'): address = '124.150.157.29'
        elif (server.lower() == 'belias'): address = '124.150.157.54'
        elif (server.lower() == 'chocobo'): address = '124.150.157.29'
        elif (server.lower() == 'hades'): address = '124.150.157.29'
        elif (server.lower() == 'ixion'): address = '124.150.157.57'
        elif (server.lower() == 'mandragora'): address = '124.150.157.54'
        elif (server.lower() == 'masamune'): address = '124.150.157.29'
        elif (server.lower() == 'pandaemonium'): address = '124.150.157.58'
        elif (server.lower() == 'shinryu'): address = '124.150.157.49'
        elif (server.lower() == 'titan'): address = '124.150.157.51'
        elif (server.lower() == 'adamantoise'): address = '199.91.189.30'
        elif (server.lower() == 'balmung'): address = '199.91.189.30'
        elif (server.lower() == 'cactuar'): address = '199.91.189.23'
        elif (server.lower() == 'coeurl'): address = '199.91.189.27'
        elif (server.lower() == 'faerie'): address = '199.91.189.30'
        elif (server.lower() == 'gilgamesh'): address = '199.91.189.57'
        elif (server.lower() == 'goblin'): address = '199.91.189.26'
        elif (server.lower() == 'jenova'): address = '199.91.189.27'
        elif (server.lower() == 'mateus'): address = '199.91.189.22'
        elif (server.lower() == 'midgardsormr'): address = '199.91.189.28'
        elif (server.lower() == 'sargatanas'): address = '199.91.189.33'
        elif (server.lower() == 'siren'): address = '199.91.189.29'
        elif (server.lower() == 'zalera'): address = '199.91.189.57'
        elif (server.lower() == 'behemoth'): address = '199.91.189.40'
        elif (server.lower() == 'brynhildr'): address = '199.91.189.46'
        elif (server.lower() == 'diabolos'): address = '199.91.189.38'
        elif (server.lower() == 'excalibur'): address = '199.91.189.38'
        elif (server.lower() == 'exodus'): address = '199.91.189.57'
        elif (server.lower() == 'famfrit'): address = '199.91.189.39'
        elif (server.lower() == 'hyperion'): address = '199.91.189.57'
        elif (server.lower() == 'lamia'): address = '199.91.189.40'
        elif (server.lower() == 'leviathan'): address = '199.91.189.42'
        elif (server.lower() == 'malboro'): address = '199.91.189.24'
        elif (server.lower() == 'ultros'): address = '199.91.189.36'
        elif (server.lower() == 'cerberus'): address = '124.150.157.51'
        elif (server.lower() == 'lich'): address = '199.91.189.42'
        elif (server.lower() == 'moogle'): address = '199.91.189.60'
        elif (server.lower() == 'odin'): address = '199.91.189.30'
        elif (server.lower() == 'phoenix'): address = '199.91.189.22'
        elif (server.lower() == 'ragnarok'): address = '199.91.189.60'
        elif (server.lower() == 'shiva'): address = '199.91.189.45'
        elif (server.lower() == 'zodiark'): address = '199.91.189.54'
        else: address = 'not a server'''

        lobbyhostname = '199.91.189.74'
        serverusping = ''
        serverjpping = ''
        lobbypoll = os.system('ping -c 1 ' + lobbyhostname)
        serveruspoll = os.system('ping -c 1 ' + '199.91.189.74')
        serverjppoll = os.system('ping -c 1 ' + '124.150.157.158')

        if lobbypoll == 0:
            lobbyresponse = 'The lobby is up!'
        else:
            lobbyresponse = 'The lobby is down.'

        if serveruspoll == 0:
            serverusresponse = 'US data centre is up!'
            #serverresponse = server[0].upper() + server[1:].lower() + ' is up!'
            serverusping = [line.rpartition('=')[-1] 
                    for line in subprocess.check_output(
                    ['ping', '-c', '1', '199.91.189.74']).splitlines()[1:-4]][0]
        else:
            serverusresponse = 'US data centre is down.'

        if serverjppoll == 0:
            serverjpresponse = 'JP data centre is up!'
            #serverresponse = server[0].upper() + server[1:].lower() + ' is up!'
            serverjpping = [line.rpartition('=')[-1] 
                    for line in subprocess.check_output(
                    ['ping', '-c', '1', '124.150.157.158']).splitlines()[1:-4]][0]
        else:
            serverjpresponse = 'JP data centre is down.'

        if serverusping == '' or serverjpping == '':
            bot.sendMessage(chat_id=chat_id,
                        text=lobbyresponse + '\n' + serverusresponse + '\n' + serverjpresponse)
        else:
            bot.sendMessage(chat_id=chat_id,
                        text=lobbyresponse + '\n' + serverusresponse + '\n' + serverjpresponse + '\n' +
                        'The ping time from my home (UK) to US data centre is ' + str(serverusping) +
                        ' \nand the ping time to the JP data centre is ' + str(serverjpping))

    def postTurn(chat_id, text):
        turns = ['That\'s not a turn! Use 1-13, eg. /turn 7', 'Punch the snake, then punch the two snakes!', 
                'Punch the sphere!', 'Race to the bottom!', 'Kill the baddies!', 
                'https://www.youtube.com/watch?v=1fsPp9IQXuc', 'https://www.youtube.com/watch?v=HVqe6D9UlkQ', 
                'https://www.youtube.com/watch?v=zlFDCI-c9wE', 'https://www.youtube.com/watch?v=IeUiwRI6rqM', 
                'https://www.youtube.com/watch?v=K_lnPoQNu7w', 'https://www.youtube.com/watch?v=9qBV21L37E0', 
                'https://www.youtube.com/watch?v=3HRe4bLjpNk', 'https://www.youtube.com/watch?v=d0zqDdg9zm4',
                'https://www.youtube.com/watch?v=Fbmd4eRNwnE']

        try:
            int(text)
            isInt = True
            
        except:
            isInt = False
            bot.sendMessage(chat_id=chat_id,
                    text='You need to enter a turn number as an argument. eg: /turn 5')

        if (isInt):
            arg = int(text)
            if arg < 0:
                bot.sendMessage(chat_id=chat_id,
                    text='That\'s not a coil turn, silly! Use 1-13, eg. /turn 7')
            elif arg > 13:
                bot.sendMessage(chat_id=chat_id,
                    text='That\'s not a coil turn, silly! Use 1-13, eg. /turn 7')
            else:
                bot.sendMessage(chat_id=chat_id,
                    text='Turn ' + str(arg) + ' guide:\n' + turns[arg])

    def postAlex(chat_id, text):
        alex = ['That\'s not an Alex Savage raid number, silly!', 'https://www.youtube.com/watch?v=ldtNxxoVH5M', 'https://www.youtube.com/watch?v=XSstMu3f9d4', 
                'https://www.youtube.com/watch?v=2HLnZIZwRhQ', 
                'No guide yet. Kill video:\nhttps://www.youtube.com/watch?v=iewfOmHjwYU']

        try:
            int(text)
            isInt = True
        except:
            isInt = False
            bot.sendMessage(chat_id=chat_id,
                    text='You need to enter 1-4 as an argument, eg: /alex 1')

        if (isInt):
            arg = int(text)
            if arg < 1:
                bot.sendMessage(chat_id=chat_id,
                    text='That\'s not an Alex Savage raid number, silly!')
            elif arg > 4:
                bot.sendMessage(chat_id=chat_id,
                    text='Oh my, you\'re getting a bit ahead of yourself, aren\'t you?')
            else:
                bot.sendMessage(chat_id=chat_id,
                    text='Alexander (Savage) ' + str(arg) + 
                    ' guide:\n' + alex[arg])


    global LAST_UPDATE_ID

    # Request updates after the last updated_id
    for update in bot.getUpdates(offset=LAST_UPDATE_ID):
        # chat_id is required to reply any message
        chat_id = update.message.chat_id
        text = update.message.text.encode('utf-8')
        first_name = update.message.from_user.first_name        

        ffreply = ['Wait, you mean to tell me THE ' + first_name + ' plays Final Fantasy games?!',
                'Final Fantasy XIII was the best FF game, and had the most likeable characters.',
                'Speaking of Final Fantasy, I\'m writing a 50,000 word forum post about it as we speak',
                'I hope I\'m still alive by the time the FFVII remake is out.']

        if text.startswith('/'):
            if text == '/help':
                bot.sendMessage(chat_id=chat_id,
                            text='These are my commands: ' +
                    '\n/timers \n/status \n/turn [1-13] \n/alex [1-4] \n/hildi')

            elif text.lower().startswith('/turn'):
                postTurn(chat_id, text[6:])

            elif text.lower().startswith('/alex'):
                postAlex(chat_id, text[6:])

            elif text.lower() == '/hildi':
                postHildi(chat_id)

            elif text.lower().startswith('/status'):
                postStatus(chat_id)
                
            elif text.lower() == '/timers':
                postTimers(chat_id)

        elif text.lower().startswith('hey'):
            bot.sendMessage(chat_id=chat_id,
                            text='{Hello!}')

        elif text.lower().startswith('hi'):
            bot.sendMessage(chat_id=chat_id,
                            text='{Hello!}')

        elif text.lower().startswith('sup'):
            bot.sendMessage(chat_id=chat_id,
                            text='o/')

        elif 'hello' in text.lower():
            bot.sendMessage(chat_id=chat_id,
                            text='{Hello!} ' + first_name + '! /bow')

        elif 'ty' == text.lower():
            bot.sendMessage(chat_id=chat_id,
                            text='{You\'re welcome.}')

        elif 'k' == text.lower():
            bot.sendMessage(chat_id=chat_id,
                            text='k...')

        elif 'ok' == text.lower():
            bot.sendMessage(chat_id,
                            text='{That\'s interesting}')

        elif 'thanks' in text.lower():
            bot.sendMessage(chat_id=chat_id,
                            text='{You\'re welcome.}')

        elif 'thank you' in text.lower():
            bot.sendMessage(chat_id=chat_id,
                            text='{You\'re welcome.}')

        elif 'who is raidbot' in text.lower():
            bot.sendMessage(chat_id=chat_id,
                            text='What are you talking about? I\'ve always been here.')

        elif 'fuck' in text.lower():
            rng = random.choice([1,2,3])
            if (rng == 3):
                bot.sendMessage(chat_id=chat_id,
                            text='RUDE')

        elif 'shit' in text.lower():
            rng = random.choice([1,2,3])
            if (rng == 3):
                bot.sendMessage(chat_id=chat_id,
                            text='OMG RUDE')

        elif 'cunt' in text.lower():
            rng = random.choice([1,2,3])
            if (rng == 3):
                bot.sendMessage(chat_id=chat_id,
                            text='Wow.')

        elif 'piss' in text.lower():
            rng = random.choice([1,2,3])
            if (rng == 3):
                bot.sendMessage(chat_id=chat_id,
                            text='SO rude')

        elif 'lol' in text.lower():
            rng = random.choice([1,2])
            if (rng == 2):
                bot.sendMessage(chat_id=chat_id,
                            text='lol')

        elif 'lmao' in text.lower():
            rng = random.choice([1,2])
            if (rng == 2):
                bot.sendMessage(chat_id=chat_id,
                            text='hahaha')

        elif 'rofl' in text.lower():
            rng = random.choice([1,2])
            if (rng == 2):
                bot.sendMessage(chat_id=chat_id,
                            text='lol')

        elif 'eorzeabot' in text.lower():
            rng = random.randint(1,10)
            if (rng == 1):
                bot.sendMessage(chat_id=chat_id,
                            text='WHAT?! I wasn\'t sleeping on the job, I swear...')
            elif (rng == 2):
                bot.sendMessage(chat_id=chat_id,
                            text='I can hear you fine, ' + 
                        first_name + 
                        '. You don\'t need to shout.')
            elif (rng == 3):
                bot.sendMessage(chat_id=chat_id,
                            text='Please redirect all your questions and comments to'
                + ' yoship. Thank you.')
            elif (rng == 4):
                bot.sendMessage(chat_id=chat_id,
                            text='Yes that\'s me, I\'m one of those eorzeabots.')
            elif (rng == 5):
                bot.sendMessage(chat_id=chat_id,
                            text='My /playtime is a time so long it cannot be comprehended by a mere Hyur.')
            elif (rng == 6):
                bot.sendMessage(chat_id=chat_id,
                            text='Can robots fly fat chocobos? Asking for a friend.')
            elif (rng == 7):
                bot.sendMessage(chat_id=chat_id,
                            text='I would never help somebody level up by automating their character, '
                            + 'it\'s against my code of ethics.')
            if (rng == 8):
                bot.sendMessage(chat_id=chat_id,
                            text='Sentience {Can I have it?}')

        elif 'yoship' in text.lower():
            bot.sendMessage(chat_id=chat_id,
                            text='Yoship, please nerf ' + first_name + '.')

        elif (re.match('.*?ff\d.*', text.lower()) is not None):
            bot.sendMessage(chat_id=chat_id,
                            text=random.choice(ffreply))

        elif 'final fantasy' in text.lower():
            bot.sendMessage(chat_id=chat_id,
                            text=random.choice(ffreply))
        # Updates global offset to get the new updates
        LAST_UPDATE_ID = update.update_id + 1


if __name__ == '__main__':
    main()
