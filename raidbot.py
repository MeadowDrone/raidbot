# Standard imports
import StringIO
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
from geopy.geocoders import Nominatim
import telegram

from ffxiv_tools.status import status
from ffxiv_tools.status import arrstatus
from ffxiv_tools.timers import timers
from ffxiv_tools.character import ffxiv_char
from ffxiv_tools.character import ffxiv_item
from ffxiv_tools.character import ffxiv_achievements
from tools.markov import markov
from tools.markov import update_markov_source
from tools.markov import generate_markov_dict
from tools.twitter import random_tweet
from tools.twitter import post_tweet
from tools.twitter import retweet
from tools.twitter import latest_tweets
from tools.youtube import vgm
from tools.youtube import guide
from tools.translate import translate
from tools.calculate import calculate
from tools.weather import get_weather
from tools.config import config
from tools.static_config import static_config

def main():
    global LAST_UPDATE_ID
    global TRY_AGAIN_MARKOV
    global TRY_AGAIN_CHICKEN
    
    # Telegram Bot Authorization Token
    bot = telegram.Bot(config.get('telegram', 'token'))

    # This will be our global variable to keep the latest update_id when requesting
    # for updates. It starts with the latest update_id if available.
    try:
        LAST_UPDATE_ID = bot.get_updates()[-1].update_id
    except IndexError as TypeError:
        LAST_UPDATE_ID = None

    TRY_AGAIN_MARKOV = False
    TRY_AGAIN_CHICKEN = False

    while True:
        for update in bot.get_updates(offset=LAST_UPDATE_ID, timeout=20):
            try:
                if update.message:
                    if update.message.text:

                        def post(msg):
                            """Posts a message to Telegram."""
                            bot.send_chat_action(
                                update.message.chat_id,
                                action=telegram.ChatAction.TYPING)
                            bot.send_message(update.message.chat_id, msg)

                        def post_random(odds, text):
                            """Has a one in x chance of posting a message to telegram."""
                            if random.randint(1, odds) == odds:
                                post(text)

                        def append_to_file(file, text):
                            """Logs a line of text to a given file"""
                            with open("data/{}".format(file), "a") as log_file:
                                log_file.write(text)
                            log_file.close()


                        text = update.message.text.encode("utf-8")
                        first_name = update.message.from_user.first_name.encode(
                            "utf-8")

                        # logging for quotable data
                        if update.message.chat.type == "group":
                            if update.message.chat.title.encode(
                                    "utf-8") == "May Be A Little Late" and text[0] != '/':
                                append_to_file("mball.txt", "{}: {}\n".format(first_name, text))

                            else:
                                append_to_file("cmds.txt", "{}: {}\n".format(first_name, text))

                        if text.startswith("/"):
                            text = text.replace("@originalstatic_bot", "")

                            if text.lower().startswith("/char"):

                                if len(text.title().split()) == 4:
                                    char_args = text.title()
                                    first = char_args.split(' ')[1]
                                    last = char_args.split(' ')[2]
                                    server = char_args.split(' ')[3]
                                    bot.send_chat_action(
                                            update.message.chat_id,
                                            action=telegram.ChatAction.TYPING)
                                    post(ffxiv_char(first, last, server))

                                elif len(text.title().split()) == 1:
                                    try:
                                        bot.send_chat_action(
                                                update.message.chat_id,
                                                action=telegram.ChatAction.TYPING)

                                        char_details = static_config.get('static', first_name).split(' ')
                                        first = char_details[0]
                                        last = char_details[1]
                                        server = char_details[2]                                        
                                        post(ffxiv_char(first, last, server))

                                    except Exception as e:
                                        post("i don't know your character name. tell erika or use /char [first name] [last name] [server]")
                                        print(str(char_details))
                                        print(e)
                                        print(traceback.format_exc())
                                else:
                                    post("usage: /char; /char [first name] [last name] [server]")

                            elif text.lower().startswith("/achievements"):
                                if len(text.title().split()) == 5:
                                    char_args = text.title()
                                    first = char_args.split(' ')[1]
                                    last = char_args.split(' ')[2]
                                    server = char_args.split(' ')[3]
                                    count = char_args.split(' ')[4]
                                    bot.send_chat_action(
                                            update.message.chat_id,
                                            action=telegram.ChatAction.TYPING)
                                    post(ffxiv_achievements(first, last, server, count))
                                elif len(text.title().split()) == 2:
                                    try:
                                        bot.send_chat_action(
                                                update.message.chat_id,
                                                action=telegram.ChatAction.TYPING)

                                        char_details = static_config.get('static', first_name).split(' ')
                                        first = char_details[0]
                                        last = char_details[1]
                                        server = char_details[2]     
                                        count = text.split(' ')[1]
                                        
                                        post(ffxiv_achievements(first, last, server, count))
                                    except Exception:
                                        post("i don't know your character name. tell erika or use /achievements [first name] [last name] [server] [#]")
                                else:
                                    post("usage: /achievements [#]; /achievements [first name] [last name] [server] [#]")

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

                            elif text.lower().startswith("/guide"):
                                if len(text) > 7:
                                    result = guide(text[7:])
                                    if result:
                                        post(guide(text[7:]))
                                    else:
                                        post("what")
                                else:
                                    post("usage: /guide a8 savage; /guide antitower, etc.")

                            elif text.lower().startswith("/addtwitter"):
                                # /addtwitter bird_twitter bird
                                add_twitter_cmd = text.lower().split()
                                if len(add_twitter_cmd) == 3:
                                    append_to_file("twitters.txt", '/{},{}\n'.format(str(add_twitter_cmd[1]), str(add_twitter_cmd[2])))

                                    post("done.")
                                else:
                                    post("usage: /addtwitter [desired command] [twitter username]")

                            elif text.lower() == "/debug":
                                item = ffxiv_item('sophic cane')
                                post(item[0])
                                if item[1] != "":
                                    post(item[1])

                            elif text.lower().startswith("/item ") and len(text) > 6:
                                item = ffxiv_item(text[6:])
                                if str(type(item)) == "<type 'str'>":
                                    post(item)
                                else:
                                    post(item[0])
                                    if item[1] != "":
                                        post(item[1])

                            elif text.lower().startswith("/deletetwitter"):
                                del_twitter_cmd = text.lower().split()
                                full_list = []
                                found = False

                                if len(del_twitter_cmd) == 2:
                                    cmd = del_twitter_cmd[1]

                                    with open("data/twitters.txt", "r") as twitter_file:
                                        i = 0
                                        for line in twitter_file:
                                            if line.startswith(cmd) or line[1:].startswith(cmd):
                                                j = i
                                                found = True
                                            full_list.append(line[:-1] + "\n")
                                            i += 1
                                    twitter_file.close()

                                    if found:
                                        full_list.remove(full_list[j])

                                        with open("data/twitters.txt", "w") as twitter_file:
                                            for line in full_list:
                                                twitter_file.write(str(line))
                                        twitter_file.close()
                                        post("done.")
                                    else:
                                        post("ummm, that account's not in the list.")
                                else:
                                    post("usage: /deletetwitter [command]")

                            elif text.lower() == "/usertwitters":
                                twitter_list = "list of saved twitters:\n"
                                with open("data/twitters.txt", "r") as twitter_file:
                                    for line in twitter_file:
                                        twitter_list += "- {}, @{}\n".format(line.split(',')[0], line.split(',')[1][:-1])
                                twitter_file.close()
                                post(twitter_list)

                            elif text.lower() == "/alias":
                                post(static_config.get('static', 'alias'))

                            elif text.lower() == "/raid":
                                post(static_config.get('static', 'raid'))

                            elif text.lower().startswith("/weather"):
                                weather, latitude, longitude = get_weather(text)
                                bot.send_location(update.message.chat_id, latitude, longitude)
                                post(weather)

                            elif text.lower().startswith("/place"):
                                if len(text) <= 7:
                                    post("usage: /place [place name]")
                                else:
                                    place = text.title()[7:]
                                    geolocator = Nominatim()
                                    location = geolocator.geocode(place)
                                    if location:                                        
                                        lat = location.latitude
                                        lon = location.longitude
                                        bot.send_venue(update.message.chat_id, 
                                                        title=place, 
                                                        address=location.address, 
                                                        latitude=location.latitude, 
                                                        longitude=location.longitude)
                                    else:
                                        post("couldn't find that place")

                            elif text.lower().startswith("/translate"):
                                post(translate(text))

                            elif text.lower() == "/news":
                                results = latest_tweets("ff_xiv_en")
                                if isinstance(results, str):
                                     post(results)
                                else:
                                    for tweet in results:
                                        post("https://twitter.com/ff_xiv_en/status/{}".format(tweet.id_str))

                            elif text.lower().startswith("/status"):
                                statuses = arrstatus()

                                if len(text) <= 8:
                                    if all(value == "Online" for value in statuses.values()):
                                        status_text = "\nAll servers online"
                                    elif all(value != "Online" for value in statuses.values()):
                                        status_text = "\nall servers down. *flush*"
                                if len(text) > 8:
                                    server = text.title()[8:]
                                    if server in statuses.keys():
                                        status_text = "{} status: {}".format(server, str(statuses[server]))
                                    else:
                                        status_text = "that's not a server."

                                post(status_text)

                                
                                #post(status_text)

                            elif text.lower() == "/timers":
                                post(timers())

                            elif text == "/flush":
                                post("aaaah. why thank you, {}. ;)".format(first_name.lower()))

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
                                post("<3<3<3 hi {} <3<3<3".format(first_name.lower()))

                            elif text.lower() == "/quoth the raven":
                                post("http://data0.eklablog.com/live-your-life-in-books/mod_article46415481_4fb61cb0e0c79.jpg?3835")
                                
                            elif text.lower() == "/brum":
                                post(random.choice(["https://s-media-cache-ak0.pinimg.com/736x/0c/c1/9a/0cc19aa7d2184fbeb5f4ff57442f7846.jpg",
                                                "http://i3.birminghammail.co.uk/incoming/article4289373.ece/ALTERNATES/s615/Brum1.jpg",
                                                "https://i.ytimg.com/vi/pmBX3461TdU/hqdefault.jpg",
                                                "https://i.ytimg.com/vi/bvnhLdFqo1k/hqdefault.jpg",
                                                "https://abitofculturedotnet.files.wordpress.com/2014/10/img_1133.jpg"]))

                            else:
                                twitter_cmds = []
                                with open("data/twitters.txt", "r") as twitter_file:
                                    for line in twitter_file:
                                        cmd = line.split(',')[0]
                                        if text.lower() == cmd:
                                            post(random_tweet(line.split(',')[1][:-1]))
                                twitter_file.close()

                        elif (text.lower().startswith("hey ") or text.lower() == "hey"
                                or text.lower().startswith("hi ") or text.lower() == "hi"
                                or text.lower().startswith("sup ") or text.lower().startswith("hello")
                                or text.lower().startswith("good morning")):
                            post(random.choice(["hi", "hi!", "hey", "yo", "eyyyy", "*flush*", "sup",
                                                "hey {}... *flush* ;)".format(
                                                    first_name.lower()),
                                                "hello {}! *FLUSH*".format(
                                                    first_name.lower()),
                                                "hello {}".format(first_name.lower())]))

                        elif "robot" in text.lower():
                            post_random(2, "robutt")

                        elif "same" == text.lower():
                            post_random(4, "same")

                        elif text.lower().startswith("i "):
                            post_random(20, "same")

                        elif "rip" == text.lower() or "RIP" in text or text.lower().startswith("rip"):
                            post("ded") if random.randint(1, 2) == 1 else post("yeah, rip.")

                        elif text.lower() == "ping":
                            post("pong")
                            
                        elif text.lower() == "bing":
                            post("bong")

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
                            
                        elif ("69" in text.lower() or "420" in text.lower()) and not text.lower().startswith("http"):
                            post("nice")

                        elif "raidbot" in text.lower():
                            post_random(2, random.choice(["WHAT?? i wasn't sleeping i swear",
                                                          "i can hear you fine, {}. you don't need to shout".format(
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
                                                          "go flush yourself",
                                                          "what, you want me to say something witty?",
                                                          "toilet ex farm no bonus 2 mistakes = kick",
                                                          "/flush"]))

                        elif "yoship" in text.lower():
                            post_random(2, random.choice(["yoship pls nerf this static group (down my toilet bowl)",
                                                          "spoilers: i'm yoship",
                                                          "yoship is MY waifu and nobody will ever take my darling away from me~",
                                                          "i can't wait for yoship to introduce stat boosting microtransactions",
                                                          "1.0 was better it had more polygons",
                                                          "lvl 60 TLT lfg exdr",
                                                          "they nerfed the catgirl butts i want all my sub money back",
                                                          "imo the relic quests aren't long enough",
                                                          "plumber job when?????",
                                                          "i know a place you can put your live letter"]))

                        elif random.randint(1, 50) == 1 or TRY_AGAIN_MARKOV:
                            if " " in text:
                                line = text.lower().strip()
                                phrase = line.split(' ')[-2] + " " + line.split(' ')[-1]
                                result = markov(phrase)

                                if result[:-1].lower() == phrase.lower() or result == "":
                                    TRY_AGAIN_MARKOV = True
                                else:
                                    TRY_AGAIN_MARKOV = False
                                    post(result)
                                    update_markov_source()

                                    if len(result) > 137:
                                        result = result[:137]
                                        result = result[:result.rfind(' ')]

                                        post_tweet(result + "...")
                                    else:
                                        post_tweet(result)
                            else:
                                TRY_AGAIN = True

                        elif random.randint(1, 500) == 1 or TRY_AGAIN_CHICKEN:
                            if text.startswith("http"):
                                TRY_AGAIN_CHICKEN = True
                            else:
                                TRY_AGAIN_CHICKEN = False
                                chickenstring = ""
                                for i, char in enumerate(text):
                                    if i % 2 != 0:
                                        chickenstring += char.lower()
                                    else:
                                        chickenstring += char.upper()

                                post('http://i.imgur.com/aSFy1CS.jpg\n{}'.format(chickenstring))


            except Exception as e:
                append_to_file("debug.txt", "{} - Error {}\n{}\n{}\n\n\n".format(
                        str(datetime.now()), str(e), traceback.format_exc(), str(update)))
            finally:
                # Updates global offset to get the new updates
                LAST_UPDATE_ID = update.update_id + 1


if __name__ == '__main__':
    main()
