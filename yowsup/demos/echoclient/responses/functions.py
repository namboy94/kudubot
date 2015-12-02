# coding=utf-8

import random
import pywapi

def getRandom(inputs):
    randomnumber = random.randint(0, len(inputs) - 1)
    return inputs[randomnumber]

def wetter(city):

    #weatherTypes = ["sunny", "sunny/cloudy", "cloudy", "thunderstorms", "rain", "snow", "fog"]
    weatherEmoji = ["☀", "⛅", "☁", "⚡", "☔", "❄", "🌁"]

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
    if weatherType in ["fair", "fair / windy", "clear"]: weatherIcon = weatherEmoji[0]
    elif weatherType == "partly cloudy" : weatherIcon = weatherEmoji[1]
    elif weatherType in ["mostly cloudy", "cloudy"]: weatherIcon = weatherEmoji[2]
    elif weatherType == "thunderstorms": weatherIcon = weatherEmoji[3]
    elif weatherType in ["light rain", "rain shower"]: weatherIcon = weatherEmoji[4]
    elif weatherType == "snow": weatherIcon = weatherEmoji[5]
    elif weatherType == "haze": weatherIcon = weatherEmoji[6]
    else: weatherIcon = "???"

    print(weatherType)

    return "It is " + weatherIcon + " and " + temp + "Â°C now in " + city.capitalize()
