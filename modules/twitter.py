#!/usr/bin/env python
# -*- coding: utf-8 -*-
import requests
import json
import tweepy
import configparser
import random
import io

from modules.config import config

client_key = config.get('twitter', 'client_key')
client_secret = config.get('twitter', 'client_secret')
access_token = config.get('twitter', 'access_token')
access_secret = config.get('twitter', 'access_secret')

auth = tweepy.OAuthHandler(client_key, client_secret)
auth.set_access_token(access_token, access_secret)
api = tweepy.API(auth)


def twitter(screenName):
    tweet_urls = []
    try:
        for tweet in tweepy.Cursor(api.user_timeline, id=screenName).items(50):
            tweet_urls.append(tweet)
    except tweepy.TweepError as e:
        return "either the tweet or the account (%s) was deleted. or something just went horrendously wrong ¯\_(ツ)_/¯" % (screenName)
    
    # If every tweet is a reply then what are you even doing?
    if all(tweet.text[0] == "@" for tweet in tweet_urls):
        return "just a buncha replies in here ¯\_(ツ)_/¯"

    tweet = random.choice(tweet_urls)

    # Loop until it finds a non-reply tweet
    while tweet.text[0] == "@":
        print("Twitter reply found: %s\nTrying again...\n" % (tweet.text))
        tweet = random.choice(tweet_urls)
        
    # Save tweet ID to file for retweeting later
    with open('data/tweet.txt', 'w+') as f:
        f.write(str(tweet.id))
        
    return "https://twitter.com/%s/status/%s" % (screenName, tweet.id_str)
    

def latest(screenName):
    tweet_urls = []
    try:
        for tweet in tweepy.Cursor(api.user_timeline, id=screenName).items(5):
            tweet_urls.append("https://twitter.com/%s/status/%s" % (screenName, tweet.id_str))
    except tweepy.TweepError as e:
        return "either the tweet or the account (%s) was deleted. or something just went horrendously wrong ¯\_(ツ)_/¯" % (screenName)
    
    return tweet_urls

    
def post_tweet(text):
    api.update_status(text)

    
def retweet():
    tweet = open("data/tweet.txt").read()
    try:
        api.retweet(tweet)
        return "done. (http://twitter.com/raidbot)"
    except tweepy.error.TweepError as e:
        return "i've already already retweeted that"
        