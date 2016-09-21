'''
Command list for botfather:
help - Get full list of commands
translate - Use /translate en it "Hello world" or /translate help to know more (use speech marks for phrases)
wiki - Use /wiki [search term] to find a summary on Wikipedia
calc - Use /calc [expression]. Note: don't use spaces!
weather - Use /weather [town name] for the temperature
youtube - Use /youtube [search term] or /yt [search term] to fetch a YouTube video
vgm - get a random video game music track from youtube
news - The latest news from lodestone
ff1 - Roll random jobs for a new game of Final Fantasy I
status - Pings lobby and Excalibur server
headcount - Use /headcount yes or /headcount no, /headcount new to erase, /headcount to display attendance
alias - In-game names for members of this group
timers - Weekly and daily reset timers
doodle - Links to the doodle schedule table
mumble - Links to mumble server with details
roster - Displays current roster
progress - Links to progression spreadsheet
turn - [1-13] Links to video guide for Coil raid, eg. /turn 5
alex - [1-4] Links to video guide for Alex Savage raid, eg. /alex 3
ff14 - FFXIV meme/forum junk
goons - Goons gonna goon
tumblr - something about snowflakes?
fanfiction - take a guess
yahoo - The questions everyone wants an answer to
reddit - :reddit:
meirl - it's me, irl
twitter - Pulls from any of the above
tweet - Tweets whatever you say. Yeah, seriously.
rt - Retweets the last tweet pulled from the twitterverse
wikihow - The best advice on the Internet
catgirl - catgirl.
catboy - catboy.
oocanime - Out of context anime
damothafuckinsharez0ne - damothafuckinsharez0ne
hildi - I'm a Mander-Mander-Manderville man, Doing what only a Manderville can!
'''

# Standard imports
import StringIO
import logging
import fileinput
import random
import re
import shlex
import io

# Third-party imports
import feedparser
import giphypop
from giphypop import translate
from PIL import Image

# Local imports
import multipart
import telegram
from modules.headcount import *
from modules.hildi import hildi
from modules.ffxivstatus import status
from modules.timers import timers
from modules.guides import guides
from modules.wiki import wiki
from modules.twitter import twitter
from modules.twitter import post_tweet
from modules.twitter import retweet
from modules.twitter import latest
from modules.youtube import youtube
from modules.youtube import vgm
from modules.translate import btranslate
from modules.calculate import calculate
from modules.weather import get_weather
from uploadthread import UploadThread
from config import config

LAST_UPDATE_ID = None
TOKEN = config.get('telegram', 'token')
BASE_URL = 'https://api.telegram.org/bot%s/' % (TOKEN)
SERVER_IP = config.get('static', 'server')
LOBBY_IP = config.get('static', 'lobby')


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
    except IndexError as TypeError:
        LAST_UPDATE_ID = None
    while True:
        brain(bot)


def brain(bot):

    def calc(chat_id, text, first_name):

        head, sep, tail = text.partition('/')
        input_nums = tail.replace('calc', '')
        input_nums = input_nums.replace('\'', '')
        if ' ' in input_nums[1:]:
            spaces = True
        else:
            spaces = False
        finalexp = shlex.split(input_nums)
        exp = finalexp[0]
        bot.sendChatAction(chat_id=chat_id, action=telegram.ChatAction.TYPING)
        error = 'that\'s not maths, ' + first_name.lower() + '.'
        if not exp:
            bot.sendMessage(
                chat_id=chat_id,
                text='this isn\'t a valid expression, ' +
                first_name.lower() +
                '. *FLUSH*')
        elif re.search('[a-zA-Z]', exp):
            bot.sendMessage(chat_id=chat_id, text=error)
        else:
            if spaces:
                bot.sendMessage(
                    chat_id=chat_id,
                    text=str(
                        calculate(exp)) +
                    "\nnote. don\'t use spaces in your expression")
            else:
                bot.sendMessage(chat_id=chat_id, text=calculate(exp))

    def translate(chat_id, text):
        bot.sendChatAction(chat_id=chat_id, action=telegram.ChatAction.TYPING)
        text = text.replace('/translate', '').encode('utf-8')
        if '"' in text:
            noquotes = False
        else:
            noquotes = True
        message_broken = shlex.split(text)
        error = 'not enough parameters. use /translate en hi "hello world" or /translate help'
        if not len(message_broken) < 1:
            if message_broken[0] == 'help':
                help_string = """ usage: /translate en hi "Hello world" (note the speech marks for phrases)\nlanguages:
                        ar-Arabic | bs-Latn-Bosnian (Latin) | bg-Bulgarian | ca-Catalan | zh-CHS-Chinese Simplified |
                        zh-CHT-Chinese Traditional|hr-Croatian | cs-Czech | da-Danish | nl-Dutch |en-English | cy-Welsh |
                        et-Estonian | fi-Finnish | fr-French | de-German | el-Greek | ht-Haitian Creole | he-Hebrew |
                        hi-Hindi | mww-Hmong Daw | hu-Hungarian | id-Indonesian | it-Italian | ja-Japanese | tlh-Klingon |
                        tlh - Qaak-Klingon (pIqaD) | ko-Korean | lv-Latvian | lt-Lithuanian | ms-Malay | mt-Maltese |
                        no-Norwegian | fa-Persian | pl-Polish | pt-Portuguese | otq-Queretaro Otomi | ro-Romanian |
                        ru-Russian | sr-Cyrl-Serbian (Cyrillic) | sr-Latn-Serbian (Latin) | sk-Slovak | sl-Slovenian |
                        es-Spanish | sv-Swedish | th-Thai | tr-Turkish | uk-Ukrainian | ur-Urdu | vi-Vietnamese |
                        """
                bot.sendMessage(chat_id=chat_id, text=help_string)
            else:
                if len(message_broken) < 3:
                    bot.sendMessage(chat_id=chat_id, text=error)
                else:
                    lang_from = message_broken[0]
                    lang_to = message_broken[1]
                    lang_text = message_broken[2]
                    # print lang_from+lang_to+lang_text
                    if noquotes:
                        bot.sendMessage(
                            chat_id=chat_id,
                            text=btranslate(
                                lang_text,
                                lang_from,
                                lang_to) +
                            '\n(note: use quotes around phrase for whole phrases, eg. /translate en it "hello world")')
                    else:
                        bot.sendMessage(
                            chat_id=chat_id, text=btranslate(
                                lang_text, lang_from, lang_to))
        else:
            bot.sendMessage(chat_id=chat_id, text=error)

    def postWiki(chat_id, text):
        bot.sendChatAction(chat_id=chat_id, action=telegram.ChatAction.TYPING)
        search_term = text.replace('/wiki ', '')
        if len(search_term) < 1:
            bot.sendMessage(chat_id=chat_id, text="usage: /wiki toilet")
        else:
            reply = wiki(search_term)
            if ("link's broken :argh:" in reply):
                bot.sendMessage(
                    chat_id=chat_id,
                    text="can't find %s on wikipedia" %
                    (search_term))
            else:
                bot.sendMessage(chat_id=chat_id, text=reply)

    def postYoutube(chat_id, text):
        bot.sendChatAction(chat_id=chat_id, action=telegram.ChatAction.TYPING)
        replacer = {'/youtube': '', '/yt': ''}
        search_term = replace_all(text, replacer)
        if len(search_term) < 1:
            bot.sendMessage(chat_id=chat_id,
                            text="Usage: /yt keywords or /youtube keywords")
        else:
            bot.sendMessage(chat_id=chat_id,
                            text=youtube(search_term).encode('utf8'))

    def postVGM(chat_id):
        bot.sendChatAction(chat_id=chat_id, action=telegram.ChatAction.TYPING)

        rng = random.randint(1, 1947)
        search_term = 'SupraDarky %s' % (str(rng))
        vgm_message = vgm(search_term).encode('utf8')
        vgm_title_filters = {'Best VGM ' + str(rng) + ' - ': ''}
        vgm_new_message = replace_all(vgm_message, vgm_title_filters)
        bot.sendMessage(chat_id=chat_id, text=vgm_new_message)

    def postPhoto(img):
        bot.sendChatAction(chat_id=chat_id, action=telegram.ChatAction.TYPING)
        image = Image.open(img)
        output = StringIO.StringIO()

        if img[-3:].lower() == 'gif':
            ext = 'GIF'
        elif img[-3:].lower() == 'png':
            ext = 'PNG'
        elif img[-3:].lower() == 'jpg':
            ext = 'JPEG'

        image.save(output, ext)

        resp = multipart.post_multipart(BASE_URL + 'sendPhoto', [('chat_id', str(chat_id)),
                                                                 # uncomment to quote original message
                                                                 #('reply_to_message_id', str(message_id)),
                                                                 ], [
            ('photo', 'image.jpg', output.getvalue()),
        ])

    global LAST_UPDATE_ID

    # Request updates after the last updated_id
    for update in bot.getUpdates(offset=LAST_UPDATE_ID, timeout=10):
        if str(update) != "":
            # chat_id is required to reply any message
            chat_id = update.message.chat_id
            text = update.message.text.encode("utf-8")
            first_name = update.message.from_user.first_name

            if text[0] != '/' and first_name.lower() != 'alexa':
                with open("data/mball.txt", "a") as quote_file:
                    quote_file.write("%s: %s" % (first_name, "%s\n" % (text)))
                quote_file.close()
            else:
                with open("data/cmds.txt", "a") as quote_file:
                    quote_file.write("%s: %s" % (first_name, "%s\n" % (text)))
                quote_file.close()

            ffreply = [
                "hahahah %s plays final fantasy games???" %
                (first_name.lower()),
                "final fantasy 13 was the best game, and had the most likeable characters imo",
                "i'm so mad about final fantasy, i'm writing a 50,000 word forum post about it right now",
                "tbh the final fantasy series really lost its way after the first one",
                "please wake me up when a good final fantasy game comes out, thanks *sleeps forever*",
                "quina is such a dream boat... *sigh*",
                "Aeris:\nThis static are sick.",
                "final fantasy fans are the anti-vaccine movement of the video games world",
                "yoship please make a 24-man raid based on the ff8 scene where they realise they all have amnesia"]

            tweet_responses = [
                "tweet posted. fuccckkkk",
                "tweet posted. this is a terrible, terrible idea",
                "tweet posted. why though? why?",
                "tweet posted. it's a shitty tweet and this is coming from a toilet",
                "garbage posted.",
                "tweet posted."]

            if text.startswith("/"):
                text = text.replace("@originalstatic_bot", "")
                bot.sendChatAction(
                    chat_id=chat_id,
                    action=telegram.ChatAction.TYPING)

                if text == "/help":
                    bot.sendMessage(
                        chat_id=chat_id,
                        text="come play, my lord:\n" +
                        "/headcount - Use /headcount yes or /headcount no, /headcount new to erase, /headcount to display attendance\n" +
                        "/timers - weekly and daily reset timers\n" +
                        "/doodle - links to the doodle schedule table\n" +
                        "/mumble - links to mumble server with details\n" +
                        "/roster - displays current roster\n" +
                        "/news - the latest news from lodestone\n" +
                        "/progress - links to progression spreadsheet\n" +
                        "/status - pings lobby and Excalibur server\n" +
                        "/turn - [1-13] links to video guide for Coil raid, eg. /turn 5\n" +
                        "/alex - [1-4] links to video guide for Alex Savage raid, eg. /alex 3\n" +
                        "/flush - <3\n" +
                        "/goons - goons gonna goon\n" +
                        "/forums - words of wisdom from the FFXIV forums\n" +
                        "/tumblr - something about snowflakes?\n" +
                        "/yahoo - the questions we all want answers to\n" +
                        "/reddit - :reddit:\n" +
                        "/twitter - a random tweet from any1 of the .txt accounts\n" +
                        "/translate - use /translate en it 'Hello world' or /translate help to know more (use speech marks for phrases)\n" +
                        "/wiki - use /wiki [search term] to find a summary on Wikipedia\n" +
                        "/calc - use /calc [expression]. don't use spaces!\n" +
                        "/youtube - use /youtube [search term] or /yt [search term] to fetch a YouTube video\n" +
                        "/yt - use /youtube [search term] or /yt [search term] to fetch a YouTube video\n" +
                        "/hildi - 'I'm a Mander-Mander-Manderville man, Doing what only a Manderville can!'")

                elif text.lower() == "/quote":
                    lines = open("data/mball.txt").read().splitlines()
                    quote_line = random.choice(lines)
                    bot.sendMessage(chat_id=chat_id,
                                    text=quote_line)

                elif text.lower().startswith("/youtube") or text.lower().startswith("/yt"):
                    postYoutube(chat_id, text)

                elif text.lower() == "/vgm":
                    postVGM(chat_id)

                elif text.lower() == "/doodle" or text.lower() == "/mumble" or text.lower() == "/roster" or text.lower() == "/progress" or text.lower() == "/alias":
                    bot.sendMessage(
                        chat_id=chat_id,
                        text=config.get(
                            'static',
                            text.lower()[
                                1:]))
                                
                elif text.lower().startswith("/weather"):
                    if len(text) < 10:
                        bot.sendMessage(chat_id=chat_id,
                                text="usage: /weather (town name)")
                    if len(text) >= 11:
                        city_name = text[9:]
                        bot.sendMessage(chat_id=chat_id,
                                text=get_weather(city_name))

                elif text.lower().startswith("/translate"):
                    translate(chat_id, text)

                elif text.lower() == "/hildi":
                    hildi_img, hildi_txt = hildi()
                    postPhoto(hildi_img)
                    bot.sendMessage(chat_id=chat_id,
                                    text=hildi_txt)

                elif text.lower() == "/news":
                    for tweet_count in range(1, 5):
                        bot.sendMessage(
                            chat_id=chat_id, text=latest(
                                "ff_xiv_en", tweet_count).encode("utf8"))

                elif text == "/flush":
                    bot.sendMessage(
                        chat_id=chat_id,
                        text="aaaah. why thank you, " +
                        first_name.lower() +
                        " ;)")

                elif text.lower().startswith("/calc"):
                    calc(chat_id, text, first_name=first_name)

                elif text.lower().startswith("/headcount"):
                    if text.lower() == "/headcount":
                        headcount_output = headcount_display()
                        bot.sendMessage(chat_id=chat_id, text=headcount_output)

                    elif text[10:] == " yes" or text[10:] == " y" or text[10:] == " no" or text[10:] == " n":
                        headcount_rtn = headcount_write(first_name, text[11:])
                        bot.sendMessage(chat_id=chat_id, text=headcount_rtn)

                    elif text[10:] == " new":
                        if first_name.lower() == "erika" or first_name.lower() == "una":
                            headcount_new()
                            bot.sendMessage(
                                chat_id=chat_id, text="headcount erased")
                        else:
                            bot.sendMessage(
                                chat_id=chat_id, text="only erika/arelle can do that")

                    else:
                        bot.sendMessage(
                            chat_id=chat_id,
                            text="usage: /headcount yes or /headcount no\n/headcount to see current roster")

                elif text.lower().startswith("/tweet"):
                    if len(text) == 6 or len(text) == 7:
                        bot.sendMessage(chat_id=chat_id,
                                text="usage: /tweet (some garbage)")
                    elif len(text) > 125:
                        bot.sendMessage(chat_id=chat_id,
                                text="maybe make your tweet just a teensy bit shorter?")
                    else:
                        post_tweet(first_name.lower(), text[7:])
                        bot.sendMessage(chat_id=chat_id,
                                        text=random.choice(tweet_responses))


                elif text.lower() == "/rt":
                    bot.sendMessage(chat_id=chat_id,
                                    text=retweet())

                elif text.lower() == "/goons":
                    tweet = twitter("Goons_TXT").encode("utf8")
                    bot.sendMessage(chat_id=chat_id, text=tweet)

                elif text.lower() == "/yahoo":
                    tweet = twitter("YahooAnswersTXT").encode("utf8")
                    bot.sendMessage(chat_id=chat_id, text=tweet)

                elif text.lower() == "/meirl":
                    tweet = twitter("itmeirl").encode("utf8")
                    bot.sendMessage(chat_id=chat_id, text=tweet)

                elif text.lower() == "/wikihow":
                    tweet = twitter("WikiHowTXT").encode("utf8")
                    bot.sendMessage(chat_id=chat_id, text=tweet)

                elif text.lower() == "/tumblr":
                    tweet = twitter("TumblrTXT").encode("utf8")
                    bot.sendMessage(chat_id=chat_id, text=tweet)

                elif text.lower() == "/fanfiction":
                    tweet = twitter("fanfiction_txt").encode("utf8")
                    bot.sendMessage(chat_id=chat_id, text=tweet)

                elif text.lower() == "/reddit":
                    tweet = twitter("Reddit_txt").encode("utf8")
                    bot.sendMessage(chat_id=chat_id, text=tweet)

                elif text.lower() == "/catgirl":
                    tweet = twitter("catgirls_bot").encode("utf8")
                    bot.sendMessage(chat_id=chat_id, text=tweet)

                elif text.lower() == "/catboy":
                    tweet = twitter("catboys_bot").encode("utf8")
                    bot.sendMessage(chat_id=chat_id, text=tweet)
                    
                elif text.lower() == "/catperson":
                    tweet = twitter(random.choice(["catboys_bot", "catgirls_bot"])).encode("utf8")
                    bot.sendMessage(chat_id=chat_id, text=tweet)

                elif text.lower() == "/ff14":
                    account = ["ff14forums_txt", "FFXIV_Memes", "FFXIV_Names"]
                    tweet = twitter(random.choice(account)).encode("utf8")
                    bot.sendMessage(chat_id=chat_id, text=tweet)

                elif text.lower() == "/oocanime":
                    tweet = twitter("oocanime").encode("utf8")
                    bot.sendMessage(chat_id=chat_id, text=tweet)

                elif text.lower() == "/damothafuckinsharez0ne":
                    tweet = twitter("dasharez0ne").encode("utf8")
                    bot.sendMessage(chat_id=chat_id, text=tweet)

                elif text.lower() == "/twitter":
                    account = [
                        "ff14forums_txt",
                        "FFXIV_Memes",
                        "FFXIV_Names",
                        "Goons_TXT",
                        "YahooAnswersTXT",
                        "TumblrTXT",
                        "Reddit_txt",
                        "fanfiction_txt",
                        "WikiHowTXT",
                        "itmeirl",
                        "oocanime",
                        "damothafuckinsharez0ne"]
                    tweet = twitter(random.choice(account)).encode("utf8")
                    bot.sendMessage(chat_id=chat_id, text=tweet)

                elif text.lower() == "/heart":
                    bot.sendMessage(chat_id=chat_id, text="<3<3<3 hi %s <3<3<3" % (first_name.lower()))

                elif text.lower().startswith("/wiki"):
                    postWiki(chat_id, text)

                elif text.lower().startswith("/turn") or text.lower().startswith("/alex"):
                    bot.sendMessage(chat_id=chat_id,
                                    text=guides(text.lower()))

                elif text.lower() == "/status":
                    bot.sendMessage(chat_id=chat_id,
                                    text=status(LOBBY_IP, SERVER_IP))

                elif text.lower() == "/timers":
                    bot.sendMessage(chat_id=chat_id,
                                    text=timers())

                elif text.lower() == "/ff1":
                    bot.sendChatAction(
                        chat_id=chat_id, action=telegram.ChatAction.TYPING)
                    bot.sendMessage(
                        chat_id=chat_id,
                        text="%s's final fantasy 1 jobs are..." %
                        (first_name.lower()))
                    for i in range(0, 4):
                        random_job = random.randint(1, 6)
                        if random_job == 1:
                            bot.sendMessage(chat_id=chat_id,
                                            text="Black Mage!")
                            postPhoto("img/ff1/blm.png")
                        elif random_job == 2:
                            bot.sendMessage(chat_id=chat_id,
                                            text="White Mage!")
                            postPhoto("img/ff1/wm2.png")
                        elif random_job == 3:
                            bot.sendMessage(chat_id=chat_id,
                                            text="Red Mage!")
                            postPhoto("img/ff1/rdm.jpg")
                        elif random_job == 4:
                            bot.sendMessage(chat_id=chat_id,
                                            text="Fighter!")
                            postPhoto("img/ff1/fighter.png")
                        elif random_job == 5:
                            bot.sendMessage(chat_id=chat_id,
                                            text="Monk!")
                            postPhoto("img/ff1/monk.png")
                        elif random_job == 6:
                            bot.sendMessage(chat_id=chat_id,
                                            text="Thief!")
                            postPhoto("img/ff1/thief.jpg")

                    bot.sendMessage(chat_id=chat_id,
                                    text="Good luck!")

                else:
                    bot.sendMessage(
                        chat_id=chat_id,
                        text="that's not a command i recognise, but we can't all be perfect i guess")

            elif text.lower().startswith("hey ") or text.lower() == "hey":
                bot.sendMessage(chat_id=chat_id,
                                text="o/")
            elif text.lower().startswith("hi ") or text.lower() == "hi":
                bot.sendMessage(chat_id=chat_id,
                                text="hi!")

            elif text.lower().startswith("sup "):
                bot.sendMessage(chat_id=chat_id,
                                text="eyyy")

            elif text.lower().startswith("hello"):
                bot.sendMessage(
                    chat_id=chat_id,
                    text="hello %s! *FLUSH*" %
                    (first_name.lower()))

            elif "ty" == text.lower():
                rng = random.randint(1, 3)
                if (rng == 1):
                    bot.sendMessage(chat_id=chat_id,
                                    text="np. (that was something I did, right?)")

            elif "same" == text.lower():
                rng = random.randint(1, 2)
                if (rng == 1):
                    bot.sendMessage(chat_id=chat_id,
                                    text="same")

            elif text.lower().startswith("i "):
                rng = random.randint(1, 20)
                if (rng == 1):
                    bot.sendMessage(chat_id=chat_id,
                                    text="same")

            elif "rip" == text.lower() or "RIP" in text or text.lower().startswith("rip"):
                rng = random.randint(1, 2)
                if (rng == 1):
                    bot.sendMessage(chat_id=chat_id,
                                    text="ded")
                elif (rng == 2):
                    bot.sendMessage(chat_id=chat_id,
                                    text="yeah, rip.")

            elif "k" == text.lower():
                bot.sendMessage(chat_id=chat_id,
                                text="... k")

            elif "ok" == text.lower():
                bot.sendMessage(chat_id=chat_id,
                                text="k")

            elif text.lower() == "thanks":
                bot.sendMessage(chat_id=chat_id,
                                text="np. (that was something I did, right?)")

            elif text.lower() == "thank you":
                bot.sendMessage(chat_id=chat_id,
                                text="np. (that was something I did, right?)")

            elif "who is raidbot" in text.lower():
                bot.sendMessage(
                    chat_id=chat_id,
                    text="what are you talking about? i've always been here.")

            elif "fuck" in text.lower():
                rng = random.randint(1, 20)
                if (rng == 3):
                    bot.sendMessage(chat_id=chat_id,
                                    text="RUDE")

            elif "shit" in text.lower():
                rng = random.randint(1, 20)
                if (rng == 3):
                    bot.sendMessage(chat_id=chat_id,
                                    text="rude")

            elif "piss" in text.lower():
                rng = random.randint(1, 20)
                if (rng == 3):
                    bot.sendMessage(chat_id=chat_id,
                                    text="rude")

            elif "lol" in text.lower():
                rng = random.randint(1, 10)
                if (rng == 2):
                    bot.sendMessage(chat_id=chat_id,
                                    text="lol")

            elif "lmao" in text.lower():
                rng = random.randint(1, 10)
                if (rng == 2):
                    bot.sendMessage(chat_id=chat_id,
                                    text="lmbo")

            elif "rofl" in text.lower():
                rng = random.randint(1, 10)
                if (rng == 2):
                    bot.sendMessage(chat_id=chat_id,
                                    text="lol")

            elif "hail satan" in text.lower():
                bot.sendMessage(chat_id=chat_id,
                                text="hail satan")

            elif "hail santa" in text.lower():
                bot.sendMessage(chat_id=chat_id,
                                text="no hail SATAN")
                                
            elif "hail stan" in text.lower():
                bot.sendMessage(chat_id=chat_id,
                                text="... hail satan.")

            elif "raidbot" in text.lower():
                rng = random.randint(1, 20)
                if (rng == 1):
                    bot.sendMessage(chat_id=chat_id,
                                    text="WHAT?? i wasn't sleeping i swear")
                if (rng == 2):
                    bot.sendMessage(
                        chat_id=chat_id,
                        text="i can hear you fine, %s. you don't need to shout" %
                        (first_name.lower()))
                if (rng == 3):
                    bot.sendMessage(
                        chat_id=chat_id,
                        text="please redirect all your questions and comments to yoship. thank you")
                if (rng == 4):
                    bot.sendMessage(chat_id=chat_id,
                                    text="careful now")
                if (rng == 5):
                    bot.sendMessage(
                        chat_id=chat_id,
                        text="my /playtime is a time so long it cannot be comprehended by a mortal mind")
                if (rng == 6):
                    bot.sendMessage(
                        chat_id=chat_id,
                        text="look i'm trying to be a toilet here, stop bothering me")
                if (rng == 7):
                    bot.sendMessage(chat_id=chat_id,
                                    text="beep boop. *FLUSH*")
                if (rng == 8):
                    bot.sendMessage(chat_id=chat_id,
                                    text="same")
                if (rng == 9):
                    bot.sendMessage(chat_id=chat_id,
                                    text="same, %s" % (first_name.lower()))
                if (rng == 10):
                    bot.sendMessage(chat_id=chat_id,
                                    text="yoship pls nerf my toilet handle")

            elif "yoship" in text.lower():
                rng = random.randint(1, 10)
                if (rng == 1):
                    bot.sendMessage(
                        chat_id=chat_id,
                        text="yoship pls nerf this static group (down my toilet bowl)")
                elif (rng == 2):
                    bot.sendMessage(
                        chat_id=chat_id,
                        text="spoilers: i'm yoship")
                elif (rng == 3):
                    bot.sendMessage(
                        chat_id=chat_id,
                        text="yoship is MY waifu and nobody will ever take my darling away from me~")
                elif (rng == 4):
                    bot.sendMessage(
                        chat_id=chat_id,
                        text="yoship please make a 24-man raid based on the ff8 scene where they realise they all have amnesia")
                elif (rng == 5):
                    bot.sendMessage(
                        chat_id=chat_id,
                        text="i can't wait for yoship to introduce stat boosting microtransactions")

            '''elif (re.match('.*?ff\d.*', text.lower()) is not None):
                bot.sendMessage(chat_id=chat_id,
                                text=random.choice(ffreply))

            elif "final fantasy" in text.lower():
                bot.sendMessage(chat_id=chat_id,
                                text=random.choice(ffreply))'''
            # Updates global offset to get the new updates
            LAST_UPDATE_ID = update.update_id + 1


def replace_all(text, dic):
    for i, j in dic.iteritems():
        text = text.replace(i, j)
    return text

if __name__ == '__main__':
    main()
