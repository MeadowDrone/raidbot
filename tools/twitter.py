# -*- coding: utf-8 -*-
#!/usr/bin/env python
"""Module for handling twitter input and output.

Available functions:
- random_tweet: Get a random recent tweet.
- latest: Get the five most recent tweets.
- get_tweet: Builds a list of tweet URLs.
- post_tweet: Posts a tweet to https://twitter.com/raidbot
- retweet: Retweets raidbot's most recently requested tweet.
"""
import json
import tweepy
import random
import io

from tools.config import config

client_key = config.get('twitter', 'client_key')
client_secret = config.get('twitter', 'client_secret')
access_token = config.get('twitter', 'access_token')
access_secret = config.get('twitter', 'access_secret')

auth = tweepy.OAuthHandler(client_key, client_secret)
auth.set_access_token(access_token, access_secret)
api = tweepy.API(auth)

error = "either the tweet or the account was deleted. or something just went horrendously wrong ¯\_(ツ)_/¯"


def random_tweet(username):
    """Get a random non-reply tweet from the latest 50 tweets of an account.
    
    This function checks to make sure it the latest tweets are not entirely 
    reply tweets, and if not, choose a random tweet and loop until a 
    non-reply tweet is found. Also writes the ID of the tweet to file, so
    it can be retweeted later.
    
    Args:
        username: The username of the twitter account.
        
    Returns:
        String containing the URL of the tweet. Information if only replies
        were found.
    """
    tweet_urls = get_tweets(username, 50)

    if all(tweet.text[0] == "@" for tweet in tweet_urls):
        return "just a buncha replies in here ¯\_(ツ)_/¯"

    tweet = random.choice(tweet_urls)

    while tweet.text[0] == "@":
        tweet = random.choice(tweet_urls)

    # Save tweet ID to file for retweeting later
    with open('data/tweet.txt', 'w+') as f:
        f.write(str(tweet.id))

    return "https://twitter.com/{}/status/{}".format(username, tweet.id_str)


def latest_tweets(username):
    """Get the latest five tweets from an account.
    
    Args:
        username: The username of the twitter account.
        size: The number of latest tweets to be returned.
        
    Returns:
        List containing five twitter URL strings.
    """
    tweet_urls = get_tweets(username, 5)
    return tweet_urls

    
def get_tweets(username, size):
    """Builds a list of a twitter account's most recent tweets.
    
    Args:
        username: The username of the twitter account.
        size: The number of latest tweets to be returned.
        
    Returns:
        List containing a number of twitter URLs depending
        on the value of the size variable.
    """
    tweet_urls = []
    try:
        for tweet in tweepy.Cursor(api.user_timeline, id=username).items(size):
            tweet_urls.append(tweet)
        return tweet_urls
    except tweepy.TweepError as e:
        return "{} ({})".format(error, username)

        
def post_tweet(text):
    """Posts a tweet to https://twitter.com/raidbot.
    
    Args:
        text: The text to be posted.
    """
    api.update_status(text)


def retweet():
    """Retweets raidbot's most recently requested tweet.
    
    Returns:
        String with a success or error message.
    """
    tweet = open("data/tweet.txt").read()
    try:
        api.retweet(tweet)
        return "done. (http://twitter.com/raidbot)"
    except tweepy.error.TweepError as e:
        return "i've already already retweeted that"
