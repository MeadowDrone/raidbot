'''
Command list for botfather:
timers - Weekly and daily reset timers
doodle - Links to the doodle schedule table
mumble - Links to mumble server with details
roster - Displays current roster
progress - Links to progression spreadsheet
status - Pings lobby and Excalibur server
turn - [1-13] Links to video guide for Coil raid, eg. /turn 5
alex - [1-4] Links to video guide for Alex Savage raid, eg. /alex 3
flush - <3
goons - Goons gonna goon
forums - Words of wisdom from the FFXIV forums
translate - Use /translate en it "Hello world" or /translate help to know more (use speech marks for phrases)
wiki - Use /wiki [search term] to find a summary on Wikipedia
gif - Use /gif [search term] for a gif
calculate - Use /calc [expression]. Note: don't use spaces!
youtube - Use /youtube [search term] or /yt [search term] to fetch a YouTube video
hildi - Because only a...
'''

import StringIO
import logging
import fileinput
import random
import multipart
import datetime
import random
import re
import shlex
import os
import subprocess
import giphypop
from giphypop import translate
from PIL import Image

import telegram
from uploadthread import UploadThread
from config import config
from telegram.twitter import twitter,twittertrends,twittersearch
from telegram.translate import btranslate
from telegram.wiki import wiki
from telegram.youtube import youtube
from telegram.calculate import calculate

LAST_UPDATE_ID = None
TOKEN = '129105114:AAGnEDiL6N0duZBDgEvY0aFfMaI8pW1Xeeg'
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
    except IndexError, TypeError:
        LAST_UPDATE_ID = None
    while True:
        brain(bot)

def brain(bot):

    def postForums(chat_id):
         bot.sendMessage(chat_id=chat_id,text=twitter('ff14forums_txt').encode('utf8'))

    def postGoons(chat_id):
         bot.sendMessage(chat_id=chat_id,text=twitter('Goons_TXT').encode('utf8'))

    def calc(chat_id, text, first_name):
        if ' ' in text:
            spaces = True
        else:
            spaces = False
        head, sep, tail = text.partition('/')
        input_nums = tail.replace('calc','')
        input_nums = input_nums.replace('\'','')
        finalexp = shlex.split(input_nums)
        exp = finalexp[0]
        bot.sendChatAction(chat_id=chat_id, action=telegram.ChatAction.TYPING)
        error = 'that\'s not maths, ' + first_name.lower() + '.'
        if not exp:
            bot.sendMessage(chat_id=chat_id,text='this isn\'t a valid expression, ' + first_name.lower() + '. *FLUSH*')
        elif re.search('[a-zA-Z]', exp):
            bot.sendMessage(chat_id=chat_id,text=error)
        else:
            if spaces:
                bot.sendMessage(chat_id=chat_id,text=str(calculate(exp)) + "\nnote. don\'t use spaces in your expression")
            else:
                bot.sendMessage(chat_id=chat_id,text=calculate(exp))

    def translate(chat_id, text):
        text = text.replace('/translate','').encode('utf8')
        if '"' in text:
            noquotes = False
        else:  
            noquotes = True
        message_broken = shlex.split(text)
        error = 'Not enough parameters. Use, /translate en hi "Hello world" or /translate help to know more'
        if not len(message_broken)<1:
            if message_broken[0] == 'help':
                help_string = """ Example, /translate en hi "Hello world"
                        ar-Arabic | bs-Latn-Bosnian (Latin) | bg-Bulgarian | ca-Catalan | zh-CHS-Chinese Simplified | 
                        zh-CHT-Chinese Traditional|hr-Croatian | cs-Czech | da-Danish | nl-Dutch |en-English | cy-Welsh |
                        et-Estonian | fi-Finnish | fr-French | de-German | el-Greek | ht-Haitian Creole | he-Hebrew | 
                        hi-Hindi | mww-Hmong Daw | hu-Hungarian | id-Indonesian | it-Italian | ja-Japanese | tlh-Klingon | 
                        tlh - Qaak-Klingon (pIqaD) | ko-Korean | lv-Latvian | lt-Lithuanian | ms-Malay | mt-Maltese |
                        no-Norwegian | fa-Persian | pl-Polish | pt-Portuguese | otq-Queretaro Otomi | ro-Romanian |
                        ru-Russian | sr-Cyrl-Serbian (Cyrillic) | sr-Latn-Serbian (Latin) | sk-Slovak | sl-Slovenian | 
                        es-Spanish | sv-Swedish | th-Thai | tr-Turkish | uk-Ukrainian | ur-Urdu | vi-Vietnamese |
                        """
                bot.sendMessage(chat_id=chat_id,text=help_string)
            else:
                if len(message_broken)<3:
                    bot.sendMessage(chat_id=chat_id,text=error)
                else:
                    lang_from = message_broken[0]
                    lang_to = message_broken[1]
                    lang_text = message_broken[2]
                    #print lang_from+lang_to+lang_text
                    if noquotes:
                        bot.sendMessage(chat_id=chat_id,text=btranslate(lang_text,lang_from,lang_to)+
                                '\n(note: use quotes around phrase for whole phrases, eg. /translate en it "hello world")')
                    else:
                        bot.sendMessage(chat_id=chat_id,text=btranslate(lang_text,lang_from,lang_to))
        else:
            bot.sendMessage(chat_id=chat_id,text=error)

    def postWiki(chat_id, text):
        search_term = text.replace('/wiki ','')
        if len(search_term)<1:
            bot.sendMessage(chat_id=chat_id,text='Use it like: /wiki Anaconda')
        else:
            reply=wiki(search_term)
            if ("Cannot acces link!" in reply):
                #reply="No wikipedia article on that but got some google results for you \n"+google(text)
                bot.sendMessage(chat_id=chat_id,text="can\'t find " + search_term + " on wikipedia")
            else:
                bot.sendMessage(chat_id=chat_id,text=reply)

    def postGif(chat_id, text):
        replacer = {'/gif':''}
        search_term = replace_all(text,replacer)
        if len(search_term)<1:
            bot.sendMessage(chat_id=chat_id,text='usage: /gif keyword')
        else:
            img = giphypop.translate(search_term)
            #print img.fixed_height.downsampled.url
            #bot.sendMessage(chat_id=chat_id,text='Hang in there. Fetching gif..-Powered by GIPHY!')
            bot.sendChatAction(chat_id=chat_id, action=telegram.ChatAction.UPLOAD_PHOTO)
            threadobjgiphy = UploadThread(bot,chat_id,img.fixed_height.downsampled.url.encode('utf-8'))
            threadobjgiphy.setName('giphythread')
            threadobjgiphy.start()

    def postYoutube(chat_id, text):
            bot.sendChatAction(chat_id=chat_id, action=telegram.ChatAction.TYPING)
            replacer = {'/youtube':'','/yt':''}
            search_term = replace_all(text,replacer)
            if len(search_term)<1:
               bot.sendMessage(chat_id=chat_id,text='Usage: /yt keywords') 
            else:
               bot.sendMessage(chat_id=chat_id,text=youtube(search_term).encode('utf8'))

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

    def postMumble(chat_id):
        bot.sendMessage(chat_id=chat_id,
                text='mumble details: \naddress: ffgoons.com \n' +
                'port: 64738 \n' +
                'password: fishercat')

    def postDoodle(chat_id):
        bot.sendMessage(chat_id=chat_id,
                #text='the schedule poll is here: http://doodle.com/pe2hyzt69mxvw7tx#table' +
                text='the general schedule (days of the week) poll is here: http://doodle.com/poll/gcb63gh9x6p322wy#table')

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

    # WIP
    '''def writeToSchedule(chat_id, days_in, group_name, first_name):
        full_path = '/root/telegram_bots/'
        group_filename = group_name.lower().replace(" ", "_") + '_schedule'
        print(first_name + ' entered ' + days_in + ' to ' + group_filename)
        
        if not os.path.isfile(full_path + group_filename):
            bot.sendMessage(chat_id=chat_id,
                            text='creating schedule for ' + group_name)
            schedule = open(group_filename, 'w').close()

        schedule = open(group_filename, 'r+')
        
        for line in schedule.readlines():
            schedule.write(line.replace(first_name + 'blah', first_name + ' ' + days_in)) # needs regex '''

    def postSchedule(chat_id):
        bot.sendMessage(chat_id=chat_id,
                        text='TUESDAY:\nRoyce + Shevi\nArelle + Lili?\nT\'sun + Velcio + ')

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

    def postProgress(chat_id):
        bot.sendMessage(chat_id=chat_id,
                        text='progression sheet:\n' +
                        'https://docs.google.com/spreadsheets/d/1VpcDmkDOxsdoUxZOQuZkgTdHsR436SwFhzU3FlRP2tc/edit?usp=sharing\n')

    def postRoster(chat_id):
        bot.sendMessage(chat_id=chat_id,
                        text='roster: ' + 
                        ' \nTUESDAY:\nTANKS: Royce Zouks / Shevi Ventus' + 
                        ' \nHEALERS: Arelle Doomraix / Velcio' +
                        ' \nDPS: Black Swordsman / T\'sun Dere / Leone Larcefauceais / Alethea Morne \n\n' +
                        'THURSDAY:\nTANKS: Royce Zouks / Shevi Ventus' + 
                        ' \nHEALERS: Arelle Doomraix / Lilinette Rhyd' +
                        ' \nDPS: Una Ventful / T\'sun Dere / Leone Larcefauceais / Alethea Morne \n\n' +
                        ' SATURDAY:\nTANKS: Royce Zouks / Shevi Ventus' + 
                        ' \nHEALERS: Arelle Doomraix / Lilinette Rhyd' +
                        ' \nDPS: Black Swordsman / T\'sun Dere / Leone Larcefauceais / Una Ventful \n\n')

    def postStatus(chat_id):
        lobbyhostname = '199.91.189.74'
        excalhostname = '199.91.189.47'
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
            bot.sendMessage(chat_id=chat_id,
                        text=lobbyresponse + '\n' + excalresponse)
        else:
            bot.sendMessage(chat_id=chat_id,
                        text=lobbyresponse + '\n' + excalresponse + '\n' + 
                        'ping (UK) is ' + str(excalping))

    def postTurn(chat_id, text):
        turns = ['that\'s not a turn, silly', '... really?', 'punch the sphere', 'zoom zoom', 'kill the baddies', 
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
                    text='you need to enter a turn number as an argument. eg: /turn 5')

        if (isInt):
            arg = int(text)
            if arg < 0:
                bot.sendMessage(chat_id=chat_id,
                    text='that\'s not a coil turn, silly')
            elif arg > 13:
                bot.sendMessage(chat_id=chat_id,
                    text='that\'s not a coil turn, silly')
            else:
                bot.sendMessage(chat_id=chat_id,
                    text='turn ' + str(arg) + ' guide:\n' + turns[arg])

    def postAlex(chat_id, text):
        alex = ['that\'s not a raid number, silly',
                'https://www.youtube.com/watch?v=ldtNxxoVH5M', 
                'xeno: https://www.youtube.com/watch?v=ooNCi_9VL3Y&feature=youtu.be \nmtq: https://www.youtube.com/watch?v=XSstMu3f9d4 \ntext: http://www.dtguilds.com/forum/m/6563292/viewthread/23552103-alexander-gordia-savage-a2s-cuff-father-strategy-guide' , 
                'mtq: https://www.youtube.com/watch?v=2HLnZIZwRhQ \ntext: http://www.dtguilds.com/forum/m/6563292/viewthread/23022915-alexander-gordia-normal-arm-father-a3-strategy-guide', 
                'No guide yet. Kill video:\nhttps://www.youtube.com/watch?v=iewfOmHjwYU']

        try:
            int(text)
            isInt = True
        except:
            isInt = False
            bot.sendMessage(chat_id=chat_id,
                    text='you need to enter a number as an argument. eg: /alex 1')

        if (isInt):
            arg = int(text)
            if arg < 0:
                bot.sendMessage(chat_id=chat_id,
                    text='that\'s not an alex savage raid, silly')
            elif arg > 4:
                bot.sendMessage(chat_id=chat_id,
                    text='getting a bit ahead of yourself, aren\'t you?')
            else:
                bot.sendMessage(chat_id=chat_id,
                    text='alexander (savage) ' + str(arg) + 
                    ' guide:\n' + alex[arg])


    global LAST_UPDATE_ID

    # Request updates after the last updated_id
    for update in bot.getUpdates(offset=LAST_UPDATE_ID, timeout=10):
        if str(update) != '':
            # chat_id is required to reply any message
            chat_id = update.message.chat_id
            text = update.message.text.encode('utf-8')
            first_name = update.message.from_user.first_name

            ffreply = ['hahahah ' + first_name.lower() + ' plays final fantasy games???',
                    'final fantasy 13 was the best game, and had the most likeable characters imo',
                    'i\'m so mad about final fantasy, i\'m writing a 50,000 word forum post about it right now',
                    'tbh the final fantasy series really lost its way after the first one',
                    'please wake me up when a good final fantasy game comes out, thanks *sleeps forever*',
                    'quina is such a dream boat... *sigh*',
                    'Aeris:\nThis static are sick.',
                    'final fantasy fans are the anti-vaccine movement of the video games world',
                    'yoship please make a 24-man raid based on the ff8 scene where they realise they all have amnesia']

            if text.startswith('/'):
                if text == '/flush':
                    bot.sendMessage(chat_id=chat_id,
                                text='aaaah. why thank you, ' + first_name.lower() + ' ;)')

                elif text == '/help':
                    bot.sendMessage(chat_id=chat_id,
                                text='a comprehensive, technical list of my commands: ' +
                        '\n/timers \n/doodle \n/roster \n/turn [#] \n/alex [#] \n/flush \n/hildi \nthat is all.')

                elif text.lower() == '/doodle':
                    postDoodle(chat_id)

                elif text.lower() == '/forums':
                    postForums(chat_id)

                elif text.lower().startswith('/calc'):
                    calc(chat_id, text, first_name=first_name)

                elif text.lower() == '/goons':
                    postGoons(chat_id)

                elif text.lower().startswith('/wiki'):
                    postWiki(chat_id, text)

                elif text.lower().startswith('/youtube') or text.lower().startswith('/yt'):
                    postYoutube(chat_id, text)

                elif text.lower().startswith('/translate'):
                    translate(chat_id, text)

                elif text.lower() == '/mumble':
                    postMumble(chat_id)

                elif text.lower().startswith('/gif'):
                    postGif(chat_id, text)

                elif text.lower().startswith('/turn'):
                    postTurn(chat_id, text[6:])

                elif text.lower().startswith('/alex'):
                    postAlex(chat_id, text[6:])                

                elif text.lower() == '/roster':
                    postRoster(chat_id)

                elif text.lower() == '/hildi':
                    postHildi(chat_id)

                elif text.lower() == '/status':
                    postStatus(chat_id)
                    
                elif text.lower() == '/timers':
                    postTimers(chat_id)

                elif text.lower() == '/progress':
                    postProgress(chat_id)

                elif text.lower().startswith('/schedule'):
                    postSchedule(chat_id=chat_id)

            elif text.lower().startswith('hey ') or text.lower() == 'hey':
                bot.sendMessage(chat_id=chat_id,
                                text='o/')
            elif text.lower().startswith('hi ') or text.lower() == 'hi':
                bot.sendMessage(chat_id=chat_id,
                                text='hi!')

            elif text.lower().startswith('sup'):
                bot.sendMessage(chat_id=chat_id,
                                text='eyyy')

            elif text.lower().startswith('hello'):
                bot.sendMessage(chat_id=chat_id,
                                text='hello ' + first_name.lower() + '! *FLUSH*')

            elif 'ty' == text.lower():
                bot.sendMessage(chat_id=chat_id,
                                text='np. (that was something I did, right?)')

            elif 'same' == text.lower():
                rng = random.randint(1,2)
                if (rng == 1):
                    bot.sendMessage(chat_id=chat_id,
                                    text='same')

            elif 'k' == text.lower():
                bot.sendMessage(chat_id=chat_id,
                                text='k')

            elif 'ok' == text.lower():
                bot.sendMessage(chat_id=chat_id,
                                text='k')

            elif 'thanks' in text.lower():
                bot.sendMessage(chat_id=chat_id,
                                text='np. (that was something I did, right?)')

            elif 'thank you' in text.lower():
                bot.sendMessage(chat_id=chat_id,
                                text='np. (that was something I did, right?)')

            elif 'who is raidbot' in text.lower():
                bot.sendMessage(chat_id=chat_id,
                                text='what are you talking about? i\'ve always been here.')

            elif 'fuck' in text.lower():
                rng = random.randint(1,20)
                if (rng == 3):
                    bot.sendMessage(chat_id=chat_id,
                                text='RUDE')

            elif 'shit' in text.lower():
                rng = random.randint(1,20)
                if (rng == 3):
                    bot.sendMessage(chat_id=chat_id,
                                text='rude')

            elif 'piss' in text.lower():
                rng = random.randint(1,20)
                if (rng == 3):
                    bot.sendMessage(chat_id=chat_id,
                                text='rude')

            elif 'lol' in text.lower():
                rng = random.randint(1,10)
                if (rng == 2):
                    bot.sendMessage(chat_id=chat_id,
                                text='lol')

            elif 'lmao' in text.lower():
                rng = random.randint(1,10)
                if (rng == 2):
                    bot.sendMessage(chat_id=chat_id,
                                text='lmbo')

            elif 'rofl' in text.lower():
                rng = random.randint(1,10)
                if (rng == 2):
                    bot.sendMessage(chat_id=chat_id,
                                text='lol')

            elif 'raidbot' in text.lower():
                rng = random.randint(1,10)
                if (rng == 1):
                    bot.sendMessage(chat_id=chat_id,
                                text='WHAT?? i wasn\'t sleeping i swear')
                if (rng == 2):
                    bot.sendMessage(chat_id=chat_id,
                                text='i can hear you fine, ' + 
                            first_name.lower() + 
                            '. you don\'t need to shout')
                if (rng == 3):
                    bot.sendMessage(chat_id=chat_id,
                                text='please redirect all your questions and comments to'
                    + ' yoship. thank you')
                if (rng == 4):
                    bot.sendMessage(chat_id=chat_id,
                                text='careful now')
                if (rng == 5):
                    bot.sendMessage(chat_id=chat_id,
                                text='my /playtime is a time so long it cannot be comprehended by a mortal mind')
                if (rng == 6):
                    bot.sendMessage(chat_id=chat_id,
                                text='look i\'m trying to be a toilet here, stop bothering me')
                if (rng == 7):
                    bot.sendMessage(chat_id=chat_id,
                                text='beep boop. *FLUSH*')
                if (rng == 8):
                    bot.sendMessage(chat_id=chat_id,
                                text='same')
                if (rng == 9):
                    bot.sendMessage(chat_id=chat_id,
                                text='same, ' + first_name.lower())
                if (rng == 10):
                    bot.sendMessage(chat_id=chat_id,
                                text='yoship pls nerf my toilet handle')        

            elif 'yoship' in text.lower():
                rng = random.randint(1,5)
                if (rng == 1):
                    bot.sendMessage(chat_id=chat_id,
                                    text='yoship pls nerf this static group (down my toilet bowl)')
                elif (rng == 2):
                    bot.sendMessage(chat_id=chat_id,
                                    text='spoilers: i\'m yoship')
                elif (rng == 3):
                    bot.sendMessage(chat_id=chat_id,
                                    text='yoship is MY waifu and nobody will ever take my darling away from me~')
                elif (rng == 4):
                    bot.sendMessage(chat_id=chat_id,
                                    text='yoship please make a 24-man raid based on the ff8 scene where they realise they all have amnesia')
                elif (rng == 5):
                    bot.sendMessage(chat_id=chat_id,
                                    text='i can\'t wait for yoship to introduce stat boosting microtransactions')
                    

            elif (re.match('.*?ff\d.*', text.lower()) is not None):
                bot.sendMessage(chat_id=chat_id,
                                text=random.choice(ffreply))

            elif 'final fantasy' in text.lower():
                bot.sendMessage(chat_id=chat_id,
                                text=random.choice(ffreply))
            # Updates global offset to get the new updates
            LAST_UPDATE_ID = update.update_id + 1

def replace_all(text, dic):
    for i, j in dic.iteritems():
        text = text.replace(i, j)
    return text

if __name__ == '__main__':
    main()
