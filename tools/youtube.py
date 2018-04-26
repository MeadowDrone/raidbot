# -*- coding: utf-8 -*-
import os
import random
from apiclient.discovery import build

from config import config

DEVELOPER_KEY = config.get('youtube', 'api_server_key')


def youtube(text):
    replacer = {'/youtube': '', '/yt': ''}
    search_term = replace_all(text, replacer)

    if len(search_term) < 1:
        return "Usage: /yt keywords or /youtube keywords"

    result = get_video(search_term)
    return "¯\_(ツ)_/¯" if not result else result


def vgm():
    rng = random.randint(1, 2063)
    search_term = 'SupraDarky {}'.format(str(rng))
    vgm_title_filters = {'Best VGM ' + str(rng) + ' - ': ''}
    
    return replace_all(get_video(search_term), vgm_title_filters)


def guide(duty):
    search_term = 'mizzteq {}'.format(duty)
    
    return get_video(search_term)


def get_video(search_term):
    youtube_vid = build("youtube", "v3", developerKey=DEVELOPER_KEY)
    videos = []

    # Call the search.list method to retrieve results matching the specified
    # query term.
    search_response = youtube_vid.search().list(
        q=search_term,
        part="id,snippet",
        maxResults=2
    ).execute()
    
    # Add each result to the appropriate list, and then display the lists of
    # matching videos, channels, and playlists.
    for search_result in search_response.get("items", []):
        if search_result["id"]["kind"] == "youtube#video":
            videos.append("{} ({})".format(
                search_result["snippet"]["title"],
                "https://www.youtube.com/watch?v=" + search_result["id"]["videoId"]))

            return "\n".join(videos)


def replace_all(text, dic):
    for i, j in dic.iteritems():
        text = text.replace(i, j)
    return text
