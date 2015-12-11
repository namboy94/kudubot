"""
Weather plugin for a whatsapp bot

@:author Hermann Krumrey<hermann@krumreyh.com>
"""

import re
import pywapi
from yowsup.layers.protocol_messages.protocolentities import TextMessageProtocolEntity
from plugins.GenericPlugin import GenericPlugin

"""
Class that stores relevant information, parses user input and gets weather data
"""
class Weather(GenericPlugin):

    """
    Constructor
    @:param layer - the overlying yowsup layer
    @:param messageProtocolEntity - the received message information
    @:override
    """
    def __init__(self, layer, messageProtocolEntity=None):
        if messageProtocolEntity is None: self.layer = layer; return
        self.emojis = True
        self.verbose = False
        self.lang = "en"

        self.layer = layer
        self.entity = messageProtocolEntity
        self.message = messageProtocolEntity.getBody().lower()
        self.sender = messageProtocolEntity.getFrom()

        self.city = ""
        self.province = ""
        self.country = ""

    """
    Checks if the user input matches the regex needed for the plugin to function correctly
    @:override
    """
    def regexCheck(self):
        regex = r"^/(weather|wetter)(:)?(text;|verbose;)*( )?(([^ ]+| ){0,5})?$"
        if re.search(regex, self.message): return True
        else: return False


    """
    Parses the user input
    @:param userInput - the user input
    @:override
    """
    def parseUserInput(self):

        trimmedInput = self.message.split(":")
        args = []
        if len(trimmedInput) > 1:
            args = trimmedInput[1].split(";")
            if not args[len(args) - 1] in ["verbose", args]:
                args.pop()
            if trimmedInput[0] == "wetter": self.lang = "de"
        else:
            if self.message.split(" ")[0] == "wetter": self.lang = "de"
        for arg in args:
            if arg == "verbose": self.verbose = True
            if arg == "text": self.emojis = False

        cityString = ""
        try: cityString = self.message.split(" ", 1)[1]
        except: cityString = "karlsruhe"

        splitCity = cityString.split(", ")

        self.city = splitCity[0]
        if len(splitCity) == 2:
            self.province = False
            self.country = splitCity[1]
        elif len(splitCity) == 3:
            self.province = splitCity[1]
            self.province = splitCity[2]
        else:
            self.province = False
            self.country = False

    """
    Gets the weather data for the location specified by the user input
    @returns the weather data as a TextMessageProtocolEntity
    @:override
    """
    def getResponse(self):

        try:
            self.location = self.__specialPlaces__(self.city)
            if not self.location:
                self.location = self.__getLocation__()
            self.locationCode = self.location[0]
            self.location = self.__repairAmericanLocation__()
            self.weather = pywapi.get_weather_from_weather_com(self.locationCode)
        except:
            return TextMessageProtocolEntity("City not Found", self.sender)

        return TextMessageProtocolEntity(self.__messageGenerator__(), to=self.sender)

    """
    Returns a description about this plugin
    @:override
    """
    @staticmethod
    def getDescription(language):
        if language == "en":
            return "/weather\tSends weather information\n" \
                   "syntax:\t/weather[:][options;] <cityname>[, <region>][, <country>]\n" \
                   "options: text,verbose\n\n"
        elif language == "de":
            return "/wetter\tSchickt Wetterinformationen\n" \
                   "syntax:\t/wetter[optionen;] <stadtname>[, <region>][, <land>]\n" \
                   "options: text,verbose\n\n"
        else:
            return "Help not available in this language"



### private methods ###


    """
    Helper method for getWeather(), which catches special, predefined cities.
    For example, the default search result for Windhoek is Windhoek in South Africa, but with the help of
    this method, the search is overriden and Windhoek in Namibia is displayed
    """
    def __specialPlaces__(self, city):

        if city == "windhoek": return ('WAXX0004', 'Windhoek, KH, Namibia')
        if city == "???": raise NameError("Invalid City")
        if city =="johannesburg": return ("SFXX0023", 'Johannesburg, GT, South Africa')

    """
    Gets the location code of a city
    """
    def __getLocation__(self):
        if not self.country and not self.province:
            return pywapi.get_loc_id_from_weather_com(self.city)[0]
        elif self.country and not self.province:
            search = pywapi.get_loc_id_from_weather_com(self.city)
            for result in search:
                if search[result][1].split(", ")[2].lower() == self.country:
                    return search[result]
            raise NameError("City not Found")
        elif self.country and self.province:
            search = pywapi.get_loc_id_from_weather_com(self.city)
            for result in search:
                if result == "count": break
                if search[result][1].split(", ")[1].lower() == self.province \
                        and (search[result][1].split(", ")[2].lower() == self.country
                        or self.country == "usa"):
                    return search[result]
            raise NameError("City not Found")

    """
    Repairs American Locations (since they only store the state, not the country)
    @returns the repaired location data
    """
    def __repairAmericanLocation__(self):
        if len(self.location[1].split(", ")) == 2:
            return [self.location[0], self.location[1] + ', USA']
        else: return self.location

    """
    Determines the weather emoji for all weather types
    @returns the weatherEmoji to the corresponding weatherType
    """
    def __getWeatherEmoji__(self, weatherType):

        if weatherType in ["sunny", "clear", "sunny / windy", "clear / windy"]: return "☀"
        elif weatherType in ["fair"]: return "🌤"
        elif weatherType in ["partly cloudy"]: return "⛅"
        elif weatherType in ["mostly cloudy"]: return "🌥"
        elif weatherType in ["not definded"]: return "🌦"
        elif weatherType in ["light rain", "light rain shower"]: return "🌧"
        elif weatherType in ["cloudy"]: return"☁"
        elif weatherType in ["thunderstorms", "t-storm"]: return "⛈"
        elif weatherType in ["rain shower"]: return "☔"
        elif weatherType in ["thunderclouds"]: return "🌩"
        elif weatherType in ["snow"]: return "🌨"
        elif weatherType in ["windy"]: return "🌬"
        elif weatherType in ["tornado"]: return "🌪"
        elif weatherType in ["haze", "fog", "mist"]: return "🌫"
        else: return "???"

    """
    Generates a message string to send back
    """
    def __messageGenerator__(self):

        try:
            weatherType = self.weather['current_conditions']['text'].lower()
            temp = self.weather['current_conditions']['temperature'].lower()
        except: return "Weather data currently unavailable"

        cityString = self.location[1].split(", ")[0] + ", " + self.location[1].split(", ")[2]
        weatherMessage = weatherType

        if self.emojis: weatherMessage = self.__getWeatherEmoji__(weatherType)
        if self.verbose: cityString = self.location[1].split(", ")[0] + ", " + self.location[1].split(", ")[1] + ", " + self.location[1].split(", ")[2]

        if self.lang == "en":
            return "It is " + weatherMessage + " and " + temp + "°C now in " + cityString
        elif self.lang == "de":
            return "Es ist " + weatherMessage + " und " + temp + "°C in " + cityString
        else: return "Unknown language error"