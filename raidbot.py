# Standard imports
import StringIO
import logging
import fileinput
import random
import re
import shlex
import io
import os
import traceback
from datetime import datetime

# Third-party imports
from PIL import Image

# Local imports
import telegram

from modules import multipart
from modules.ffxivstatus import status
from modules.timers import timers
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
from modules.ffxivchar import ffxiv_char

LAST_UPDATE_ID = None
BASE_URL = 'https://api.telegram.org/bot%s/' % (
    config.get('telegram', 'token'))


def main():
    global LAST_UPDATE_ID
    logging.basicConfig(
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')

    # Telegram Bot Authorization Token
    bot = telegram.Bot(config.get('telegram', 'token'))
    #bot = Updater(config.get('telegram', 'token'))

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
    for update in bot.getUpdates(offset=LAST_UPDATE_ID, timeout=20):
        try:
            if update.message:
                if update.message.text:

                    def post(msg):
                        bot.sendChatAction(
                            update.message.chat_id,
                            action=telegram.ChatAction.TYPING)
                        bot.sendMessage(update.message.chat_id, msg)

                    def post_random(odds, text):
                        if random.randint(1, odds) == odds:
                            post(text)

                    text = update.message.text.encode("utf-8")
                    first_name = update.message.from_user.first_name.encode(
                        "utf-8")

                    # logging for quotable data
                    if update.message.chat.title.encode(
                            "utf-8") == "May Be A Little Late" and text[0] != '/':
                        with open("data/mball.txt", "a") as quote_file:
                            quote_file.write("%s: %s\n" % (first_name, text))
                        quote_file.close()
                    else:
                        with open("data/cmds.txt", "a") as quote_file:
                            quote_file.write("%s: %s\n" % (first_name, text))
                        quote_file.close()

                    if text.startswith("/"):
                        text = text.replace("@originalstatic_bot", "")

                        if text == "/help":
                            post(
                                "type '/' into chat, or press the '[/]' button to view all available commands")

                        elif text.lower().startswith("/char"):
                            char_args = text.title().split()
                            if len(char_args) == 4:
                                post(
                                    ffxiv_char(
                                        char_args[1],
                                        char_args[2],
                                        char_args[3]))
                            else:
                                post(
                                    "needs 3 arguments. usage: /char [first name] [last name] [server]")

                        elif text.lower() == "/quote":
                            quote_file = open("data/mball.txt").read().splitlines()
                            post(random.choice(quote_file))

                        elif text.lower().startswith("/calc"):
                            post(calculate(text, first_name))

                        elif text.lower().startswith("/tweet"):
                            if len(text) < 7:
                                post("usage: /tweet (some garbage)")
                            elif len(text) >= 140:
                                post("maybe make your tweet just a teensy bit shorter?")
                            else:
                                post_tweet(text[7:])
                                post(random.choice([
                                    "tweet posted. fuccckkkk", "tweet posted. this is a terrible, terrible idea",
                                    "tweet posted. why though? why?", "garbage posted.", "tweet posted.",
                                    "tweet posted. it's a shitty tweet and this is coming from a toilet"
                                ]) + " (http://twitter.com/raidbot)")

                        elif text.lower().startswith("/wiki"):
                            post(get_wiki(text))

                        elif text.lower().startswith("/youtube") or text.lower().startswith("/yt"):
                            post(youtube(text))

                        elif text.lower() == "/vgm":
                            post(vgm())

                        elif text.lower() == "/alias":
                            post(config.get('static', 'alias'))

                        elif text.lower() == "/raid":
                            post(config.get('static', 'raid'))

                        elif text.lower().startswith("/weather"):
                            post(
                                "usage: /weather (town name)") if len(text) < 10 else post(get_weather(text[9:]))

                        elif text.lower().startswith("/translate"):
                            post(translate(text))

                        elif text.lower() == "/news":
                            tweets = latest("ff_xiv_en")
                            if isinstance(tweets, str):
                                 post(tweets)
                            else:
                                for tweet in tweets:
                                    post(tweet)
                                    
                        elif text.lower() == "/status":
                            post(
                                status(
                                    config.get(
                                        'static', 'lobby'), config.get(
                                        'static', 'server')))

                        elif text.lower() == "/timers":
                            post(timers())

                        elif text == "/flush":
                            post(
                                "aaaah. why thank you, " +
                                first_name.lower() +
                                " ;)")

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
                            post(twitter(random.choice(
                                ["catboys_bot", "catgirls_bot"])))
                        elif text.lower() == "/ff14":
                            account = [
                                "ff14forums_txt",
                                "FFXIV_Memes",
                                "FFXIV_Names"]
                            post(twitter(random.choice(account)))
                        elif text.lower() == "/oocanime":
                            post(twitter("oocanime"))
                        elif text.lower() == "/damothafuckinsharez0ne":
                            post(twitter("dasharez0ne"))
                        elif text.lower() == "/dog" or text.lower() == "/doggo":
                            post(twitter("dog_rates"))
                        elif text.lower() == "/twitter":
                            account = [
                                "ff14forums_txt", "FFXIV_Memes", "FFXIV_Names",
                                "Goons_TXT", "YahooAnswersTXT", "TumblrTXT",
                                "Reddit_txt", "fanfiction_txt", "WikiHowTXT",
                                "itmeirl", "oocanime", "damothafuckinsharez0ne",
                                "dog_rates"]
                            post(twitter(random.choice(account)))

                        elif text.lower() == "/rt":
                            post(retweet())

                        elif text.lower() == "/heart":
                            post("<3<3<3 hi %s <3<3<3" % (first_name.lower()))

                        else:
                            post(
                                "that's not a command i recognise, but we can't all be perfect i guess")

                    elif (text.lower().startswith("hey ") or text.lower() == "hey"
                            or text.lower().startswith("hi ") or text.lower() == "hi"
                            or text.lower().startswith("sup ") or text.lower().startswith("hello")
                            or text.lower().startswith("good morning")):
                        post(random.choice(["hi", "hi!", "hey", "yo", "eyyyy", "*flush*", "sup",
                                            "hey %s... *flush* ;)" % (
                                                first_name.lower()),
                                            "hello %s! *FLUSH*" % (
                                                first_name.lower()),
                                            "hello %s" % (first_name.lower())]))

                    elif "robot" in text.lower():
                        post_random(2, "robutt")

                    elif "same" == text.lower():
                        post_random(2, "same")

                    elif text.lower().startswith("i "):
                        post_random(20, "same")

                    elif "rip" == text.lower() or "RIP" in text or text.lower().startswith("rip"):
                        post("ded") if random.randint(
                            1, 2) == 1 else post("yeah, rip.")

                    elif "lol" in text.lower():
                        post_random(10, "lol")

                    elif "lmao" in text.lower():
                        post_random(5, "lmbo")

                    elif "fuck" in text.lower() or "shit" in text.lower() or "piss" in text.lower():
                        post_random(20, random.choice(
                            ["RUDE", "rude", "... rude", "rude... but i'll allow it.", ":O"]))

                    elif "hail satan" in text.lower() or "hail santa" in text.lower() or "hail stan" in text.lower():
                        post("hail satan")

                    elif (text.lower() == "thanks" or text.lower() == "ty" or text.lower() == "thank you"):
                        post_random(2, random.choice(
                            ["np", "anytime", "my... *flush* pleasure.", "no problem, now sit on my face"]))

                    elif "k" == text.lower() or "ok" == text.lower():
                        post(random.choice(["... k", "k"]))
                        
                    elif "nice" == text.lower() or "noice" == text.lower():
                        post_random(4, "noice")
                        
                    elif "69" in text.lower() or "420" in text.lower():
                        post("nice")

                    elif "raidbot" in text.lower():
                        post_random(4, random.choice(["WHAT?? i wasn't sleeping i swear",
                                                      "i can hear you fine, %s. you don't need to shout" % (
                                                          first_name.lower()),
                                                      "please redirect all your questions and comments to yoship. thank you",
                                                      "careful now",
                                                      "my /playtime is a time so long it cannot be comprehended by a mortal mind",
                                                      "look i'm trying to be a toilet here, stop bothering me",
                                                      "beep boop. *FLUSH*",
                                                      "same",
                                                      "same, %s",
                                                      "yoship pls nerf my toilet handle"]))

                    elif "yoship" in text.lower():
                        post_random(2, random.choice(["yoship pls nerf this static group (down my toilet bowl)",
                                                      "spoilers: i'm yoship",
                                                      "yoship is MY waifu and nobody will ever take my darling away from me~",
                                                      "yoship please make a 24-man raid based on the ff8 scene where they realise they all have amnesia",
                                                      "i can't wait for yoship to introduce stat boosting microtransactions"]))

        except Exception as e:
            print(
                "exception: message %s\n%s" %
                (str(e), traceback.format_exc()))
            with open("data/debug.txt", "a") as err_file:
                err_file.write(
                    "Error %s\n-------\n%s\n-------\nupdate:\n%s\n%s" %
                    (str(e), traceback.format_exc(), str(update), str(
                        datetime.now())))
            err_file.close()
        finally:
            # Updates global offset to get the new updates
            LAST_UPDATE_ID = update.update_id + 1


def replace_all(text, dic):
    for i, j in dic.iteritems():
        text = text.replace(i, j)
    return text

if __name__ == '__main__':
    main()
