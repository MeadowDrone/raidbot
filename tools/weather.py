#!/usr/bin/env python
# -*- coding: utf-8 -*-
import requests
import urllib
import json
import StringIO
import random
from geopy.geocoders import Nominatim

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
        return "usage: /weather (town name)", "", ""
        
    try:
        url_encode_pairs = {'q': city_name[9:],
                            'APPID': config.get('weather', 'api_key'),
                            'units': config.get('weather', 'weather_unit'),
                            'cnt': config.get('weather', 'weather_day_count')}

        encoded_url = urllib.urlencode(url_encode_pairs)
        weather_url_text = config.get('weather', 'weather_url') + encoded_url
        response = json.load(urllib.urlopen(weather_url_text))

        result_code = response['cod']
        if result_code == 200:  # Place found
            city_name = response.get('name')
            geolocator = Nominatim()
            location = geolocator.geocode(city_name)
            latitude = str(location.latitude)
            longitude = str(location.longitude)
            temp_current = response.get('main').get('temp')
            temp_max = response.get('main').get('temp_max')
            description = response.get('weather')[0].get('description')

            # gets ID of weather description, used for emoji
            weather_id = response.get('weather')[0].get('id')
            emoji = ""
            for i in range(0,9):
                emoji += get_emoji(weather_id).encode('utf-8')
            
            message = "{}\n".format(city_name)
            message += emoji
            message += "\nTemp: {}{}C\n".format(temp_current, degree_sign)
            message += "Max: {}{}C\n".format(temp_max, degree_sign)
            message += "Weather: {}{}\n".format(description[0].upper(), description[1:])
            message += emoji

            rainy = ["rain", "storm", "drizzle", "thunder"]
            if "rain" in description.lower() and random.randint(0,3) == 1:
                message += "\n\nit's raining dongs, hallelujah it's raining dongs"

        else:
            message = random.choice(
                [
                    "didn't find a city with that name.",
                    "couldn't find wherever that is.",
                    "don't know that town name. do you live on a different planet maybe?"])
            latitude = longitude = ""

        return message, latitude, longitude

    except Exception as e:
        return 'Error: - responseController.textInputRequest: ' + str(e), "", ""

# Return related emojis according to weather


def get_emoji(weather_id):
    if weather_id:
        if str(weather_id)[
                0] == '2' or weather_id == 900 or weather_id == 901 or weather_id == 902 or weather_id == 905:
            return thunderstorm
        elif str(weather_id)[0] == '3':
            return drizzle
        elif str(weather_id)[0] == '5':
            return rain
        elif str(weather_id)[0] == '6' or weather_id == 903 or weather_id == 906:
            return snowflake + snowman
        elif str(weather_id)[0] == '7':
            return atmosphere
        elif weather_id == 800:
            return clearSky
        elif weather_id == 801:
            return fewClouds
        elif weather_id == 802 or weather_id == 803 or weather_id == 803:
            return clouds
        elif weather_id == 904:
            return hot
        else:
            return defaultEmoji    # Default emoji

    else:
        return defaultEmoji  # Default emoji
