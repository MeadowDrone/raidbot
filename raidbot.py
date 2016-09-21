# Standard imports
import StringIO
import logging
import fileinput
import random
import re
import shlex
import io
import os
import configparser

# Third-party imports
import feedparser
import giphypop
from giphypop import translate
from PIL import Image

# Local imports
import telegram

from modules import multipart
from modules.headcount import *
from modules.hildi import hildi
from modules.ffxivstatus import status
from modules.timers import timers
from modules.guides import guides
from modules.wiki import get_wiki
from modules.twitter import twitter
from modules.twitter import post_tweet
from modules.twitter import retweet
from modules.twitter import latest
from modules.youtube import youtube
from modules.youtube import vgm
from modules.translate import translate
from modules.calculate import calculate
from modules.weather import get_weather
from modules.config import config

LAST_UPDATE_ID = None
TOKEN = config.get('telegram', 'token')
BASE_URL = 'https://api.telegram.org/bot%s/' % (TOKEN)

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
    global LAST_UPDATE_ID

    # Request updates after the last updated_id
    for update in bot.getUpdates(offset=LAST_UPDATE_ID, timeout=10):
        if str(update) != "":
        
            def post(msg):
                bot.sendChatAction(update.message.chat_id, action=telegram.ChatAction.TYPING)
                bot.sendMessage(update.message.chat_id, msg)
            
            text = update.message.text.encode("utf-8")
            first_name = update.message.from_user.first_name

            if text[0] != '/' and first_name.lower() != 'alexa':
                with open("data/mball.txt", "a") as quote_file:
                    quote_file.write("%s: %s\n" % (first_name, text))
                quote_file.close()
            else:
                with open("data/cmds.txt", "a") as quote_file:
                    quote_file.write("%s: %s\n" % (first_name, text))
                quote_file.close()

            tweet_responses = [
                "tweet posted. fuccckkkk", "tweet posted. this is a terrible, terrible idea",
                "tweet posted. why though? why?", "garbage posted.", "tweet posted.",
                "tweet posted. it's a shitty tweet and this is coming from a toilet"
                ]

            if text.startswith("/"):
                text = text.replace("@originalstatic_bot", "")
                

                if text == "/help":
                    post(
                        "come play, my lord:\n" +
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
                    post(quote_line)

                elif text.lower().startswith("/youtube") or text.lower().startswith("/yt"):
                    post(youtube(text))
                    
                elif text.lower() == "/vgm":
                    post(vgm())

                elif text.lower() == "/doodle" or text.lower() == "/mumble" or text.lower() == "/roster" or text.lower() == "/progress" or text.lower() == "/alias":
                    post(config.get('static',text.lower()[1:]))
                                
                elif text.lower().startswith("/weather"):
                    if len(text) < 10:
                        post("usage: /weather (town name)")
                    else:
                        city_name = text[9:]
                        post(get_weather(city_name))

                elif text.lower().startswith("/translate"):
                    post(translate(text))

                elif text.lower() == "/hildi":
                    hildi_img, hildi_txt = hildi()
                    image = Image.open(hildi_img)
                    output = StringIO.StringIO()
                    if hildi_img[-3:].lower() == 'gif':
                        ext = 'GIF'
                    elif hildi_img[-3:].lower() == 'png':
                        ext = 'PNG'
                    elif hildi_img[-3:].lower() == 'jpg':
                        ext = 'JPEG'
                    image.save(output, ext)
                    resp = multipart.post_multipart(BASE_URL + 'sendPhoto',
                            [('chat_id', str(update.message.chat_id))],
                            [('photo', 'image.jpg', output.getvalue())])
                    post(hildi_txt)

                elif text.lower() == "/news":
                    for tweet_count in range(1, 5):
                        post(latest("ff_xiv_en", tweet_count))

                elif text == "/flush":
                    post("aaaah. why thank you, " + first_name.lower() + " ;)")

                elif text.lower().startswith("/calc"):
                    post(calculate(text, first_name))

                elif text.lower().startswith("/headcount"):
                    if text.lower() == "/headcount":
                        headcount_output = headcount_display()
                        post(headcount_output)

                    elif text[10:] == " yes" or text[10:] == " y" or text[10:] == " no" or text[10:] == " n":
                        headcount_rtn = headcount_write(first_name, text[11:])
                        post(headcount_rtn)

                    elif text[10:] == " new":
                        if first_name.lower() == "erika" or first_name.lower() == "una":
                            headcount_new()
                            post("headcount erased")
                        else:
                            post("only erika/arelle can do that")

                    else:
                        post("usage: /headcount yes or /headcount no\n/headcount to see current roster")

                elif text.lower().startswith("/tweet"):
                    if len(text) == 6 or len(text) == 7:
                        post("usage: /tweet (some garbage)")
                    elif len(text) > 125:
                        post("maybe make your tweet just a teensy bit shorter?")
                    else:
                        post_tweet(first_name.lower(), text[7:])
                        post(random.choice(tweet_responses))

                elif text.lower() == "/rt":
                    post(retweet())
                elif text.lower() == "/goons":
                    post(twitter("Goons_TXT"))
                elif text.lower() == "/yahoo":
                    post(twitter("YahooAnswersTXT"))
                elif text.lower() == "/meirl":
                    post(twitter("itmeirl"))
                elif text.lower() == "/wikihow":
                    post(twitter("WikiHowTXT"))
                elif text.lower() == "/tumblr":
                    post(twitter("TumblrTXT"))
                elif text.lower() == "/fanfiction":
                    post(twitter("fanfiction_txt"))
                elif text.lower() == "/reddit":
                    post(twitter("Reddit_txt"))
                elif text.lower() == "/catgirl":
                    post(twitter("catgirls_bot"))
                elif text.lower() == "/catboy":
                    post(twitter("catboys_bot"))                    
                elif text.lower() == "/catperson":
                    post(twitter(random.choice(["catboys_bot", "catgirls_bot"])))
                elif text.lower() == "/ff14":
                    account = ["ff14forums_txt", "FFXIV_Memes", "FFXIV_Names"]
                    post(twitter(random.choice(account)))
                elif text.lower() == "/oocanime":
                    post(twitter("oocanime"))
                elif text.lower() == "/damothafuckinsharez0ne":
                    post(twitter("dasharez0ne"))
                elif text.lower() == "/twitter":
                    account = [
                        "ff14forums_txt", "FFXIV_Memes", "FFXIV_Names",
                        "Goons_TXT", "YahooAnswersTXT", "TumblrTXT",
                        "Reddit_txt", "fanfiction_txt", "WikiHowTXT",
                        "itmeirl", "oocanime", "damothafuckinsharez0ne"]
                    post(twitter(random.choice(account)))

                elif text.lower() == "/heart":
                    post("<3<3<3 hi %s <3<3<3" % (first_name.lower()))

                elif text.lower().startswith("/wiki"):
                    post(get_wiki(text))

                elif text.lower().startswith("/turn") or text.lower().startswith("/alex"):
                    post(guides(text.lower()))

                elif text.lower() == "/status":
                    post(status(config.get('static', 'lobby'), config.get('static', 'server')))

                elif text.lower() == "/timers":
                    post(timers())

                    post("Good luck!")

                else:
                    post("that's not a command i recognise, but we can't all be perfect i guess")

            elif text.lower().startswith("hey ") or text.lower() == "hey":
                post("o/")
            elif text.lower().startswith("hi ") or text.lower() == "hi":
                post("hi!")

            elif text.lower().startswith("sup "):
                post("eyyy")

            elif text.lower().startswith("hello"):
                post("hello %s! *FLUSH*" % (first_name.lower()))

            elif "ty" == text.lower():
                rng = random.randint(1, 3)
                if (rng == 1):
                    post("np. (that was something I did, right?)")

            elif "same" == text.lower():
                rng = random.randint(1, 2)
                if (rng == 1):
                    post("same")

            elif text.lower().startswith("i "):
                rng = random.randint(1, 20)
                if (rng == 1):
                    post("same")

            elif "rip" == text.lower() or "RIP" in text or text.lower().startswith("rip"):
                rng = random.randint(1, 2)
                if (rng == 1):
                    post("ded")
                elif (rng == 2):
                    post("yeah, rip.")

            elif "k" == text.lower():
                post("... k")

            elif "ok" == text.lower():
                post("k")

            elif text.lower() == "thanks":
                post("np. (that was something I did, right?)")

            elif text.lower() == "thank you":
                post("np. (that was something I did, right?)")

            elif "who is raidbot" in text.lower():
                post("what are you talking about? i've always been here.")

            elif "fuck" in text.lower():
                rng = random.randint(1, 20)
                if (rng == 3):
                    post("RUDE")

            elif "shit" in text.lower():
                rng = random.randint(1, 20)
                if (rng == 3):
                    post("rude")

            elif "piss" in text.lower():
                rng = random.randint(1, 20)
                if (rng == 3):
                    post("rude")

            elif "lol" in text.lower():
                rng = random.randint(1, 10)
                if (rng == 2):
                    post("lol")

            elif "lmao" in text.lower():
                rng = random.randint(1, 10)
                if (rng == 2):
                    post("lmbo")

            elif "rofl" in text.lower():
                rng = random.randint(1, 10)
                if (rng == 2):
                    post("lol")

            elif "hail satan" in text.lower():
                post("hail satan")

            elif "hail santa" in text.lower():
                post("no hail SATAN")
                                
            elif "hail stan" in text.lower():
                post("... hail satan.")

            elif "raidbot" in text.lower():
                rng = random.randint(1, 20)
                if (rng == 1):
                    post("WHAT?? i wasn't sleeping i swear")
                if (rng == 2):
                    post("i can hear you fine, %s. you don't need to shout" % (first_name.lower()))
                if (rng == 3):
                    post("please redirect all your questions and comments to yoship. thank you")
                if (rng == 4):
                    post("careful now")
                if (rng == 5):
                    post("my /playtime is a time so long it cannot be comprehended by a mortal mind")
                if (rng == 6):
                    post("look i'm trying to be a toilet here, stop bothering me")
                if (rng == 7):
                    post("beep boop. *FLUSH*")
                if (rng == 8):
                    post("same")
                if (rng == 9):
                    post("same, %s" % (first_name.lower()))
                if (rng == 10):
                    post("yoship pls nerf my toilet handle")

            elif "yoship" in text.lower():
                rng = random.randint(1, 10)
                if (rng == 1):
                    post("yoship pls nerf this static group (down my toilet bowl)")
                elif (rng == 2):
                    post("spoilers: i'm yoship")
                elif (rng == 3):
                    post("yoship is MY waifu and nobody will ever take my darling away from me~")
                elif (rng == 4):
                    post("yoship please make a 24-man raid based on the ff8 scene where they realise they all have amnesia")
                elif (rng == 5):
                    post("i can't wait for yoship to introduce stat boosting microtransactions")
                
            # Updates global offset to get the new updates
            LAST_UPDATE_ID = update.update_id + 1


def replace_all(text, dic):
    for i, j in dic.iteritems():
        text = text.replace(i, j)
    return text

if __name__ == '__main__':
    main()
