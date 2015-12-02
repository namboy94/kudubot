# coding=utf-8

import random
import pywapi

def getRandom(inputs):
    randomnumber = random.randint(0, len(inputs) - 1)
    return inputs[randomnumber]

def wetter(city, emojis):

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

    try:
        weather_com_location = specialPlaces(city)
    except: return "City not found"

    if not weather_com_location:
        #location search
        weather_com_search = pywapi.get_loc_id_from_weather_com(city)
        #Getting location data
        try:
            weather_com_location = [weather_com_search[0]]
        except: return "City not found"
        print(weather_com_search)
    print(weather_com_location)

    #Getting weather data
    weather_com_weather = pywapi.get_weather_from_weather_com(weather_com_location[0][0])
    locationstring = weather_com_location[0][1]
    locationstring = locationstring.split(", ")[0] + ", " + locationstring.split(", ")[2]

    #Get Weather as strings
    try:
        weather_com_weatherType = weather_com_weather['current_conditions']['text'].lower()
        weather_com_temp = weather_com_weather['current_conditions']['temperature'].lower()
    except: return "Error reading weather data"

    weatherIcon = ""
    if weather_com_weatherType in ["sunny", "clear"]: weatherIcon = weatherEmoji[0]
    elif weather_com_weatherType in ["fair"]: weatherIcon = weatherEmoji[1]
    elif weather_com_weatherType in ["partly cloudy"]: weatherIcon = weatherEmoji[2]
    elif weather_com_weatherType in ["mostly cloudy"]: weatherIcon = weatherEmoji[3]
    elif weather_com_weatherType in ["not definded"]: weatherIcon = weatherEmoji[4]
    elif weather_com_weatherType in ["light rain"]: weatherIcon = weatherEmoji[5]
    elif weather_com_weatherType in ["cloudy"]: weatherIcon = weatherEmoji[6]
    elif weather_com_weatherType in ["thunderstorms"]: weatherIcon = weatherEmoji[7]
    elif weather_com_weatherType in ["rain shower"]: weatherIcon = weatherEmoji[8]
    elif weather_com_weatherType in ["snow"]: weatherIcon = weatherEmoji[9]
    elif weather_com_weatherType in ["windy"]: weatherIcon = weatherEmoji[10]
    elif weather_com_weatherType in ["tornado"]: weatherIcon = weatherEmoji[11]
    elif weather_com_weatherType in ["haze", "fog", "mist"]: weatherIcon = weatherEmoji[12]
    else: weatherIcon = "???"

    if emojis: return "It is " + weatherIcon + " and " + weather_com_temp + "°C now in " + locationstring
    else: return "It is " +weather_com_weatherType + " and " + weather_com_temp + "°C now in " + locationstring

def specialPlaces(city):

    if city == "windhoek": return [('WAXX0004', 'Windhoek, KH, Namibia')]
    if city == "???": raise NameError("Invalid City")
    if city =="johannesburg": return [("SFXX0023", 'Johannesburg, GT, South Africa')]