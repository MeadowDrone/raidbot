# -*- coding: utf-8 -*-
import os
import random
from apiclient.discovery import build
from apiclient.errors import HttpError
from oauth2client.tools import argparser

from config import config

DEVELOPER_KEY = config.get('youtube', 'api_server_key')
YOUTUBE_API_SERVICE_NAME = "youtube"
YOUTUBE_API_VERSION = "v3"


def youtube(text):
    replacer = {'/youtube': '', '/yt': ''}
    search_term = replace_all(text, replacer)
    
    if len(search_term) < 1:
        return "Usage: /yt keywords or /youtube keywords"

    youtube = build(YOUTUBE_API_SERVICE_NAME, YOUTUBE_API_VERSION,
                    developerKey=DEVELOPER_KEY)

    # Call the search.list method to retrieve results matching the specified
    # query term.
    search_response = youtube.search().list(
        q=search_term,
        part="id,snippet",
        maxResults=2
    ).execute()

    videos = []
    # Add each result to the appropriate list, and then display the lists of
    # matching videos, channels, and playlists.
    for search_result in search_response.get("items", []):
        if search_result["id"]["kind"] == "youtube#video":
            videos.append(
                "%s (%s)" %
                (search_result["snippet"]["title"],
                 "https://www.youtube.com/watch?v=" +
                 search_result["id"]["videoId"]))

            return "\n".join(videos)
        else:
            return "¯\_(ツ)_/¯"

def vgm():
    rng = random.randint(1, 1947)
    search_term = 'SupraDarky %s' % (str(rng))
    vgm_title_filters = {'Best VGM ' + str(rng) + ' - ': ''}
    
    youtube = build(
        YOUTUBE_API_SERVICE_NAME,
        YOUTUBE_API_VERSION,
        developerKey=DEVELOPER_KEY)

    # Call the search.list method to retrieve results matching the specified
    # query term.
    search_response = youtube.search().list(
        q=search_term,
        part="id,snippet",
        maxResults=2
    ).execute()

    videos = []
    # Add each result to the appropriate list, and then display the lists of
    # matching videos, channels, and playlists.
    for search_result in search_response.get("items", []):
        if search_result["id"]["kind"] == "youtube#video":
            videos.append(
                "%s (%s)" %
                (search_result["snippet"]["title"],
                 "https://www.youtube.com/watch?v=" +
                 search_result["id"]["videoId"]))

            #message = "\n".join(videos)
            return replace_all("\n".join(videos), vgm_title_filters)


def error():
    return "Either the service is unavailable or Youtube data API quota limit has been reached :("

    if __name__ == "__main__":
        try:
            youtube(search_term)
        except HttpError, e:
            print "An HTTP error %d occurred:\n%s" % (e.resp.status, e.content)
            error()

def replace_all(text, dic):
    for i, j in dic.iteritems():
        text = text.replace(i, j)
    return text