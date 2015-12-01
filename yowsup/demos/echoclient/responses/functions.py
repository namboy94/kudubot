# coding=utf-8

import random
import pywapi

def getRandom(inputs):
    randomnumber = random.randint(0, len(inputs) - 1)
    return inputs[randomnumber]

def wetter(city):
    location = pywapi.get_loc_id_from_weather_com(city)[0][0]
    weather = pywapi.get_weather_from_weather_com(location)
    return "It is " + weather['current_conditions']['text'].lower() + " and " + weather['current_conditions']['temperature'] + "Â°C now in " + city