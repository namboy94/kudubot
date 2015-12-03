# coding=utf-8
import pywapi
from yowsup.demos.echoclient.utils.emojicode import *

class weather(object):

    city = ""
    emojis = True
    verbose = False
    group = False

    def __init__(self, userInput, group):
        self.parseUserInput(userInput)
        self.group = group

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
        weather = self.getWeatherData(locationCode)

        try:
            weatherType = weather['current_conditions']['text'].lower()
            temp = weather['current_conditions']['temperature'].lower()
        except: return "Error reading weather data"

        location = self.repairAmericanLocation(location)
        cityName = location[1].split(", ")[0]
        provinceName = location[1].split(", ")[1]
        countryName = location[1].split(", ")[2]
        locationstring = cityName + ", " + countryName
        verboseLocationString = location[1] + " (" + locationCode + ")"

        if self.group: deg = convertToBrokenUnicode("°")
        else: deg = "°"

        if self.emojis: return "It is " + self.getWeatherEmoji(weatherType) + " and " + temp + deg + "C now in " + locationstring
        else: return "It is " +weatherType + " and " + temp + deg + "C in " + locationstring

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

        if self.group:
            weatherEmoji = [convertToBrokenUnicode("☀"),   #sunny / clear
                            convertToBrokenUnicode("🌤"), #fair
                            convertToBrokenUnicode("⛅"),  #partly cloudy
                            convertToBrokenUnicode("🌥"), #mostly cloudy
                            convertToBrokenUnicode("🌦"), #clouds sun and rain?
                            convertToBrokenUnicode("🌧"), #light rain
                            convertToBrokenUnicode("☁"), #cloudy
                            convertToBrokenUnicode("⛈"), #thunderstorms
                            convertToBrokenUnicode("🌩"), #thunderclouds
                            convertToBrokenUnicode("☔"), #rain
                            convertToBrokenUnicode("🌨"), #snow
                            convertToBrokenUnicode("🌬"), #windy
                            convertToBrokenUnicode("🌪"), #tornado
                            convertToBrokenUnicode("🌫")] #fog
        else:
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


        trimmedInput = userInput.split(";")
        args = []
        print(trimmedInput)

        if not len(trimmedInput) == 1:
            i = 1
            while i < len(trimmedInput):
                args.append(trimmedInput[i])
                i += 1

        print(args)

        for arg in args:
            if arg == "verbose": self.verbose = True
            if arg == "text": self.emojis = False

        try:
            cityString = userInput.split(" ")[1]
        except: cityString = "karlsruhe"

        self.city = cityString