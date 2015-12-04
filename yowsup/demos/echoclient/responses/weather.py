# coding=utf-8
import pywapi
from yowsup.demos.echoclient.utils.emojicode import *

class weather(object):

    city = ""
    emojis = True
    verbose = False

    def __init__(self, userInput):
        self.parseUserInput(userInput)

    def getWeather(self):

        #local variables:
        location = ""
        locationCode = ""
        weather = ""
        weatherType = ""
        temp = ""
        splitCity = self.city.split(", ")

        #Search for city
        try:
            location = self.specialPlaces(self.city)
            if not location:
                if len(splitCity) == 1:
                    location = self.getLocationCity(splitCity[0])
                elif len(splitCity) == 2:
                    location = self.getLocationCityCountry(splitCity[0], splitCity[1])
                elif len(splitCity) == 3:
                    location = self.getLocationCityProvCountry(splitCity[0], splitCity[1], splitCity[2])
                else:
                    raise NameError("City not found")
        except: return "City not found"

        #Get weather data
        locationCode = location[0]
        location = self.repairAmericanLocation(location)
        weather = self.getWeatherData(locationCode)

        return self.messageGenerator(weather, location)

    def specialPlaces(self, city):

        if city == "windhoek": return ('WAXX0004', 'Windhoek, KH, Namibia')
        if city == "???": raise NameError("Invalid City")
        if city =="johannesburg": return ("SFXX0023", 'Johannesburg, GT, South Africa')

    def getLocationCity(self, city):
        return pywapi.get_loc_id_from_weather_com(city)[0]


    def getLocationCityCountry(self, city, country):
        search = pywapi.get_loc_id_from_weather_com(city)
        for result in search:
            if search[result][1].split(", ")[2].lower() == country:
                return search[result]
        raise NameError("City not Found")

    def getLocationCityProvCountry(self, city, province, country):
        search = pywapi.get_loc_id_from_weather_com(city)
        for result in search:
            if result == "count": break
            if search[result][1].split(", ")[1].lower() == province \
                    and (search[result][1].split(", ")[2].lower() == country
                    or country == "usa"):
                return search[result]
        raise NameError("City not Found")

    def repairAmericanLocation(self, location):
        if len(location[1].split(", ")) == 2:
            return [location[0], location[1] + ', USA']
        else: return location

    def getWeatherData(self, locationcode):
        return pywapi.get_weather_from_weather_com(locationcode)

    def getWeatherEmoji(self, weatherType):

#TODO halve the code
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
        elif weatherType in ["haze", "fog", "mist"]: weatherIcon = weatherEmoji[12]
        else: weatherIcon = "???"

        return weatherIcon

    def parseUserInput(self, userInput):

        trimmedInput = userInput.split(":")
        args = []
        if len(trimmedInput) > 1:
            args = trimmedInput[1].split(";")
            if not args[len(args) - 1] in ["verbose", args]:
                args.pop()

        for arg in args:
            if arg == "verbose": self.verbose = True
            if arg == "text": self.emojis = False

        cityString = ""
        try: cityString = userInput.split(" ", 1)[1]
        except: cityString = "karlsruhe"

        self.city = cityString

    def messageGenerator(self, weather, location):

        print (weather)
        print(location)
        try:
            weatherType = weather['current_conditions']['text'].lower()
            temp = weather['current_conditions']['temperature'].lower()
        except: return "Weather data currently unavailable"

        cityString = location[1].split(", ")[0] + ", " + location[1].split(", ")[2]
        weatherMessage = weatherType
        if self.emojis: weatherMessage = self.getWeatherEmoji(weatherType)
        if self.verbose: cityString = location[1].split(", ")[0] + ", " + location[1].split(", ")[1] + ", " + location[1].split(", ")[2]

        return "It is " + weatherMessage + " and " + temp + "°C now in " + cityString