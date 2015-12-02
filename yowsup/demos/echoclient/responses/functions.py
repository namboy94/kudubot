# coding=utf-8

import random
import pywapi

def getRandom(inputs):
    randomnumber = random.randint(0, len(inputs) - 1)
    return inputs[randomnumber]

def wetter(city):

    weatherEmoji = ["☀",   #sunny / clear
                    "🌤", #fair
                    "⛅",  #partly cloudy
                    "🌥", #mostly cloudy
                    "🌦", #clouds sun and rain?
                    "🌧", #light rain
                    "☁", #cloudy
                    "⛈", #thunderstorms
                    "🌩", #thunderclouds
                    "☔", #rain
                    "🌨", #snow
                    "🌬", #windy
                    "🌪", #tornado 
                    "🌫"] #fog

    search = pywapi.get_loc_id_from_weather_com(city)
    try:
        location = search[0][0]
    except: return "City not found"
    weather = pywapi.get_weather_from_weather_com(location)

    try:
        weatherType = weather['current_conditions']['text'].lower()
        temp = weather['current_conditions']['temperature']
    except: return "Error reading weather data"

    weatherIcon = ""
    if weatherType in ["sunny", "clear"]: weatherIcon = weatherEmoji[0]
    elif weatherType in ["fair"]: weatherIcon = weatherEmoji[1]
    elif weatherType in ["partly cloudy"]: weatherIcon = weatherEmoji[2]
    elif weatherType in ["mostly cloudy"]: weatherIcon = weatherEmoji[3]
    elif weatherType in ["not definded"]: weatherIcon = weatherEmoji[4]
    elif weatherType in ["light rain"]: weatherIcon = weatherEmoji[5]
    elif weatherType in ["cloudy"]: weatherIcon = weatherEmoji[6]
    elif weatherType in ["thunderstorms"]: weatherIcon = weatherEmoji[7]
    elif weatherType in ["rain shower"]: weatherIcon = weatherEmoji[8]
    elif weatherType in ["snow"]: weatherIcon = weatherEmoji[9]
    elif weatherType in ["windy"]: weatherIcon = weatherEmoji[10]
    elif weatherType in ["tornado"]: weatherIcon = weatherEmoji[11]
    elif weatherType in ["haze", "fog"]: weatherIcon = weatherEmoji[12]
    else: weatherIcon = "???"

    return "It is " + weatherIcon + " and " + temp + "°C now in " + city.capitalize()
