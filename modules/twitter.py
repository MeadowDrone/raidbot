#!/usr/bin/env python
# -*- coding: utf-8 -*-
import requests
import json
import tweepy
import configparser
import random
import io

from modules.config import config

ckey = config.get('twitter', 'client_key')
csecret = config.get('twitter', 'client_secret')
atoken = config.get('twitter', 'access_token')
asecret = config.get('twitter', 'access_secret')

auth = tweepy.OAuthHandler(ckey, csecret)
auth.set_access_token(atoken, asecret)
api = tweepy.API(auth)


def twitter(screenName):
    statuses = []
    try:
        for status in tweepy.Cursor(api.user_timeline, id=screenName).items(50):
            statuses.append(status)
    except tweepy.TweepError as e:
        return "Either the username does not exist or the service is unavailable."

    status = random.choice(statuses)

    if status.text[0] == "@":
        print("Twitter reply found: %s\nTrying again...", status.text)
        return twitter(screenName)
    else:
        with open('data/tweet.txt', 'w+') as f:
            f.write(str(status.id))
        return "https://twitter.com/%s/status/%s" % (screenName, status.id_str)

    return "if you can read this something probably went horrendously wrong ¯\_(ツ)_/¯"

def post_tweet(first_name, text):
    api.update_status(first_name + ": " + text)

def retweet():
    tweet = open("data/tweet.txt").read()
    try:
        api.retweet(tweet)
        return "done."
        #return "done. (http://twitter.com/raidbot)"
    except tweepy.error.TweepError as e:
        return "didn't work m8. you probably already retweeted it"


def latest(screenName, tweet_count):

    if ' ' in screenName:
        screenName = screenName.replace(' ', '')

    returnval = ""
    item_count = 1

    try:
        for status in tweepy.Cursor(api.user_timeline, id=screenName).items(7):
            if item_count == tweet_count:
                returnval += '\"' + status.text + '\"\n' + 'https://twitter.com/' + \
                    screenName + '/status/' + status.id_str + ''
            item_count += 1

        return returnval

    except tweepy.TweepError as e:
        error = "Either the username does not exist or the service is unavailable."
        return error


def twittersearch(keyword):

    returnval = ""
    item_count = 0

    try:
        for status in tweepy.Cursor(
                api.search,
                q=keyword,
                show_user=True).items(4):
            u = api.get_user(status.user.id)
            item_count += 1
            returnval += '\"' + str(item_count) + ':' + status.text + ' ' + \
                'https://twitter.com/' + u.screen_name + '/status/' + status.id_str + '\n'
        return returnval

    except tweepy.TweepError as e:
        error = "The service is unavailable."
        return error


def twittertrends(place):

    trends = ""
    item_count = 0
    woeid = getWoeid(place)
    if not woeid:
        return 'Invalid country name provided. Try /tt country'
    else:
        try:
            trends1 = api.trends_place(id=woeid)
            for trend in trends1[0]['trends']:
                trends += trend['name'] + '\n'
            return 'Trending on twitter:\n' + trends
        except tweepy.TweepError as e:
            error = 'Invalid country name provided or the service is not available right now.'
            return error


def getWoeid(placename):
    CONSUMER_KEY = config.get('yahoo', 'CONSUMER_KEY')
    location = placename

    if not location:
        print 'no location provided'

    url = 'http://where.yahooapis.com/v1/places.q(\'%s\')?appid=%s&format=json' % (
        location, CONSUMER_KEY)
    r = requests.get(url)
    json = r.json()
    places = json['places']
    # print places
    if not places['count']:
        print 'found nothing'
    place = places['place'][0]

    return place['woeid']
