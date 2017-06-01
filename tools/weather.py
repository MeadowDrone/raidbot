#!/usr/bin/env python
# -*- coding: utf-8 -*-
import requests
import urllib
import json
import StringIO
import random

from config import config

# openweathermap weather codes and corresponding emojis
thunderstorm = u'\U0001F4A8'    # Code: 200s, 900, 901, 902, 905
drizzle = u'\U0001F4A7'         # Code: 300s
rain = u'\U00002614'            # Code: 500s
snowflake = u'\U00002744'       # Code: 600s
snowman = u'\U000026C4'         # Code: 600s 903, 906
atmosphere = u'\U0001F301'      # Code: 700s
clearSky = u'\U00002600'        # Code: 800
fewClouds = u'\U000026C5'       # Code: 801
clouds = u'\U00002601'          # Code: 802-803-804
hot = u'\U0001F525'             # Code: 904
defaultEmoji = u'\U0001F300'    # default
degree_sign = u'\N{DEGREE SIGN}'.encode('utf-8')


def get_weather(city_name):
    if len(city_name) < 10:
        return "usage: /weather (town name)"
        
    try:
        url_encode_pairs = {'q': city_name[9:],
                            'APPID': config.get('weather', 'api_key'),
                            'units': config.get('weather', 'weather_unit'),
                            'cnt': config.get('weather', 'weather_day_count')}

        encoded_url = urllib.urlencode(url_encode_pairs)
        weather_url_text = config.get('weather', 'weather_url') + encoded_url
        response = json.load(urllib.urlopen(weather_url_text))
        resultCode = response['cod']
        if resultCode == 200:  # Place found
            cityName = response.get('name')
            countryName = response.get('sys').get('country')
            temp_current = response.get('main').get('temp')
            temp_max = response.get('main').get('temp_max')
            temp_min = response.get('main').get('temp_min')
            description = response.get('weather')[0].get('description')
            description_brief = response.get('weather')[0].get('main')

            # gets ID of weather description, used for emoji
            weatherID = response.get('weather')[0].get('id')
            emoji = ""
            for i in range(0,9):
                emoji += getEmoji(weatherID).encode('utf-8')
            
            message = "{}\n{}, {}: {}{}C\nWeather: {}\n{}".format(
                emoji, cityName, countryName,
                str(temp_current), degree_sign,
                description_brief, emoji)

            if (emoji is thunderstorm or emoji is rain) and random.randint(
                    1, 15) == 3:
                message += "\nit's raining dongs, hallelujah it's raining dongs"

        else:
            message = random.choice(
                [
                    "didn't find a city with that name.",
                    "couldn't find wherever that is.",
                    "don't know that town name. do you live on a different planet maybe?"])
        return message

    except Exception as e:
        return('Error: - responseController.textInputRequest: ' + str(e))

# Return related emojis according to weather


def getEmoji(weatherID):
    if weatherID:
        if str(weatherID)[
                0] == '2' or weatherID == 900 or weatherID == 901 or weatherID == 902 or weatherID == 905:
            return thunderstorm
        elif str(weatherID)[0] == '3':
            return drizzle
        elif str(weatherID)[0] == '5':
            return rain
        elif str(weatherID)[0] == '6' or weatherID == 903 or weatherID == 906:
            return snowflake + snowman
        elif str(weatherID)[0] == '7':
            return atmosphere
        elif weatherID == 800:
            return clearSky
        elif weatherID == 801:
            return fewClouds
        elif weatherID == 802 or weatherID == 803 or weatherID == 803:
            return clouds
        elif weatherID == 904:
            return hot
        else:
            return defaultEmoji    # Default emoji

    else:
        return defaultEmoji  # Default emoji
