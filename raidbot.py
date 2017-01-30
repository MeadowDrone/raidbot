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
import time
from datetime import datetime

from PIL import Image
import telegram

from ffxiv_tools.status import status
from ffxiv_tools.timers import timers
from ffxiv_tools.character import ffxiv_char
from tools.twitter import random_tweet
from tools.twitter import post_tweet
from tools.twitter import retweet
from tools.twitter import latest_tweets
from tools.youtube import vgm
from tools.translate import translate
from tools.calculate import calculate
from tools.weather import get_weather
from tools.config import config
from tools.static_config import static_config

global HAIL_SATAN

def main():
    global LAST_UPDATE_ID
    
    HAIL_SATAN = 0
    logging.basicConfig(
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')

    # Telegram Bot Authorization Token
    bot = telegram.Bot(config.get('telegram', 'token'))

    # This will be our global variable to keep the latest update_id when requesting
    # for updates. It starts with the latest update_id if available.
    try:
        LAST_UPDATE_ID = bot.getUpdates()[-1].update_id
    except IndexError as TypeError:
        LAST_UPDATE_ID = None

    while True:
        for update in bot.getUpdates(offset=LAST_UPDATE_ID, timeout=20):
            try:
                if update.message:
                    if update.message.text:

                        def post(msg):
                            """Posts a message to Telegram."""
                            bot.sendChatAction(
                                update.message.chat_id,
                                action=telegram.ChatAction.TYPING)
                            bot.sendMessage(update.message.chat_id, msg)

                        def post_random(odds, text):
                            """Has a one in x chance of posting a message to telegram."""
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
                                post("type '/' into chat, or press the '[/]' button to view all available commands")

                            elif text.lower().startswith("/char"):
                                char_args = text.title().split()
                                if len(char_args) == 4:
                                    post(
                                        ffxiv_char(
                                            char_args[1],
                                            char_args[2],
                                            char_args[3]))
                                elif len(char_args) == 1:
                                    if first_name.lower() == "erika":
                                        post(ffxiv_char("Arelle", "Doomraix", "Excalibur"))
                                    elif first_name.lower() == "matteo":
                                        post(ffxiv_char("Una", "Ventful", "Excalibur"))
                                    elif first_name.lower() == "alexander":
                                        post(ffxiv_char("Hisa", "Moriyama", "Excalibur"))
                                    elif first_name.lower() == "nikita":
                                        post(ffxiv_char("Leone", "Larsefauceais", "Excalibur"))
                                    elif first_name.lower() == "faissal":
                                        post(ffxiv_char("Black", "Swordsman", "Excalibur"))
                                    elif first_name.lower() == "harley":
                                        post(ffxiv_char("Vas", "Yan'dere", "Excalibur"))
                                    elif first_name.lower() == "mymla":
                                        post(ffxiv_char("T'sun", "Dere", "Excalibur"))
                                    elif first_name.lower() == "matt":
                                        post(ffxiv_char("Dilly", "Snipnoodle", "Excalibur"))
                                    elif first_name.lower() == "liam":
                                        post(ffxiv_char("Lyra", "Sable", "Excalibur"))
                                    else:
                                        post("needs 3 arguments. usage: /char [first name] [last name] [server]")
                                else:
                                    post(
                                        "needs 3 arguments. usage: /char [first name] [last name] [server]")

                            elif text.lower() == "/quote" or text.lower() == "/quote ":
                                quote_file = open("data/mball.txt").read().splitlines()
                                post(random.choice(quote_file))
                                
                            elif text.lower().startswith("/quote") and len(text) > 7:
                                names = static_config.get('static', 'names').splitlines()
                                # Pull aliases for names from static_config.ini
                                name_elem = next(name for name in names if text[7:].lower() + ',' in name.lower())
                                name = name_elem[:name_elem.index(':')+1]

                                quote_file = open("data/mball.txt").read().splitlines()
                                random.shuffle(quote_file)
                                post(next(line for line in quote_file if line.startswith(name)))

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

                            elif text.lower() == "/vgm":
                                post(vgm())

                            elif text.lower() == "/alias":
                                post(static_config.get('static', 'alias'))

                            elif text.lower() == "/raid":
                                post(static_config.get('static', 'raid'))

                            elif text.lower().startswith("/weather"):
                                post(get_weather(text))

                            elif text.lower().startswith("/translate"):
                                post(translate(text))

                            elif text.lower() == "/news":
                                results = latest_tweets("ff_xiv_en")
                                if isinstance(results, str):
                                     post(results)
                                else:
                                    for tweet in results:
                                        post("https://twitter.com/ff_xiv_en/status/%s" % (tweet.id_str))

                            elif text.lower() == "/status":
                                post(status("excalibur"))

                            elif text.lower() == "/timers":
                                post(timers())

                            elif text == "/flush":
                                post("aaaah. why thank you, %s. ;)" % (first_name.lower()))

                            elif text.lower() == "/goons":
                                post(random_tweet("Goons_TXT"))
                            elif text.lower() == "/yahoo":
                                post(random_tweet("YahooAnswersTXT"))
                            elif text.lower() == "/meirl":
                                post(random_tweet("itmeirl"))
                            elif text.lower() == "/wikihow":
                                post(random_tweet("WikiHowTXT"))
                            elif text.lower() == "/tumblr":
                                post(random_tweet("TumblrTXT"))
                            elif text.lower() == "/fanfiction":
                                post(random_tweet("fanfiction_txt"))
                            elif text.lower() == "/reddit":
                                post(random_tweet("Reddit_txt"))
                            elif text.lower() == "/catgirl":
                                post(random_tweet("catgirls_bot"))
                            elif text.lower() == "/catboy":
                                post(random_tweet("catboys_bot"))
                            elif text.lower() == "/catperson":
                                post(random_tweet(random.choice(
                                    ["catboys_bot", "catgirls_bot"])))
                            elif text.lower() == "/ff14":
                                account = [
                                    "ff14forums_txt",
                                    "FFXIV_Memes",
                                    "FFXIV_Names",
                                    "FFXIV_PTFinders"]
                                post(random_tweet(random.choice(account)))
                            elif text.lower() == "/oocanime":
                                post(random_tweet("oocanime"))
                            elif text.lower() == "/damothafuckinsharez0ne":
                                post(random_tweet("dasharez0ne"))
                            elif text.lower() == "/dog" or text.lower() == "/doggo":
                                post(random_tweet("dog_rates"))
                            elif text.lower() == "/twitter":
                                account = [
                                    "ff14forums_txt", "FFXIV_Memes", "FFXIV_Names",
                                    "Goons_TXT", "YahooAnswersTXT", "TumblrTXT",
                                    "Reddit_txt", "fanfiction_txt", "WikiHowTXT",
                                    "itmeirl", "oocanime", "damothafuckinsharez0ne",
                                    "dog_rates", "FFXIV_PTFinders"]
                                post(random_tweet(random.choice(account)))

                            elif text.lower() == "/rt":
                                post(retweet())

                            elif text.lower() == "/heart":
                                post("<3<3<3 hi %s <3<3<3" % (first_name.lower()))
                                
                            elif text.lower() == "/ping" or text.lower() == "ping":
                                post("pong")
                                
                            elif text.lower() == "/bing" or text.lower() == "bing":
                                post("bong")

                            elif text.lower() == "/quoth the raven":
                                post("nevermore")

                            elif text.lower() == "/sleep":
                                post("brb 5 mins")
                                time.sleep(300)
                                
                            elif text.lower() == "/brum":
                                post(random.choice(["https://s-media-cache-ak0.pinimg.com/736x/0c/c1/9a/0cc19aa7d2184fbeb5f4ff57442f7846.jpg",
                                                "http://i3.birminghammail.co.uk/incoming/article4289373.ece/ALTERNATES/s615/Brum1.jpg",
                                                "https://i.ytimg.com/vi/pmBX3461TdU/hqdefault.jpg",
                                                "https://i.ytimg.com/vi/bvnhLdFqo1k/hqdefault.jpg",
                                                "https://abitofculturedotnet.files.wordpress.com/2014/10/img_1133.jpg"]))
                                
                            elif text.lower().startswith("/sleep ") and len(text[7:]) >= 1:
                                try:
                                    sleep_timer = int(text[7:])

                                    if sleep_timer > 300:
                                        post("i can only go to sleep for up to 5 minutes.")
                                    else:
                                        post("brb")
                                        time.sleep(sleep_timer)
                                except ValueError as e:
                                    post("that's not a number, %s." % first_name.lower())

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
                            post_random(4, "same")

                        elif text.lower().startswith("i "):
                            post_random(20, "same")

                        elif "rip" == text.lower() or "RIP" in text or text.lower().startswith("rip"):
                            post("ded") if random.randint(1, 2) == 1 else post("yeah, rip.")

                        elif "lol" in text.lower():
                            post_random(10, "lol")

                        elif "lmao" in text.lower():
                            post_random(5, "lmbo")

                        elif "fuck" in text.lower() or "shit" in text.lower() or "piss" in text.lower():
                            post_random(20, random.choice(
                                ["RUDE", "rude", "... rude", "rude... but i'll allow it.", ":O"]))

                        elif "hail satan" in text.lower() or "hail santa" in text.lower() or "hail stan" in text.lower():
                            HAIL_SATAN = 6
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
                            post_random(6, random.choice(["WHAT?? i wasn't sleeping i swear",
                                                          "i can hear you fine, %s. you don't need to shout" % (
                                                              first_name.lower()),
                                                          "please redirect all your questions and comments to yoship. thank you",
                                                          "careful now",
                                                          "my /timeplayed is a time so long it cannot be comprehended by a mortal mind",
                                                          "look i'm trying to be a toilet here, stop bothering me",
                                                          "beep boop. *FLUSH*",
                                                          "yoship pls nerf my toilet handle",
                                                          "/unsubscribe",
                                                          "plumber job when?????",
                                                          "switch on that toaster and throw it in me",
                                                          "...",
                                                          "what, you want me to say something witty?"
                                                          "/flush"]))

                        elif "yoship" in text.lower():
                            post_random(2, random.choice(["yoship pls nerf this static group (down my toilet bowl)",
                                                          "spoilers: i'm yoship",
                                                          "yoship is MY waifu and nobody will ever take my darling away from me~",
                                                          "i can't wait for yoship to introduce stat boosting microtransactions",
                                                          "1.0 was better it had more polygons",
                                                          "lvl 60 toilet lfg exdr",
                                                          "they nerfed the catgirl butts i want all my sub money back",
                                                          "imo the relic quests aren't long enough",
                                                          "plumber job when?????",
                                                          "i know a place you can put your live letter"]))

                        elif "civ" in text.lower():
                            post_random(2, "my flushes are backed by NUCLEAR WEAPONS!!!")
                                                          
                        elif random.randint(1, 500) == 1:
                            post("%s: i am a brony, and %s" % (first_name.lower(), text.lower()))
                        
                        if HAIL_SATAN == 1:
                            post("hail satan")
                            HAIL_SATAN = 0

            except Exception as e:
                with open("data/debug.txt", "a") as err_file:
                    err_file.write(
                        "%s - Error %s\n%s\nJSON: \n%s\n" %
                        (str(datetime.now()), str(e), traceback.format_exc(), str(update)))
                err_file.close()
            finally:
                # Updates global offset to get the new updates
                LAST_UPDATE_ID = update.update_id + 1


if __name__ == '__main__':
    main()
