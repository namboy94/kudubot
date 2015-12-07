"""
@author Hermann Krumrey<hermann@krumreyh.com>

weather module for a whatsapp bot
"""

import pywapi

"""
class that stores relevant information, parses user input and gets weather data
"""
class weather(object):

    #local variables

    """
    Constructor
    @param userInput - the complete string send via whatsapp
    """
    def __init__(self, userInput):
        self.emojis = True
        self.verbose = False
        self.lang = "en"
        self.parseUserInput(userInput)

    """
    Gets the weather data for the location specified by the user input
    @returns the weather data
    """
    def getWeather(self):

        try:
            self.location = self.specialPlaces(self.city)
            if not self.location:
                self.location = self.getLocation()
            self.locationCode = self.location[0]
            self.location = self.repairAmericanLocation()
            self.weather = pywapi.get_weather_from_weather_com(self.locationCode)
        except: return "City not Found"

        return self.messageGenerator()

    """
    Helper method for getWeather(), which catches special, predefined cities.
    For example, the default search result for Windhoek is Windhoek in South Africa, but with the help of
    this method, the search is overriden and Windhoek in Namibia is displayed
    """
    def specialPlaces(self, city):

        if city == "windhoek": return ('WAXX0004', 'Windhoek, KH, Namibia')
        if city == "???": raise NameError("Invalid City")
        if city =="johannesburg": return ("SFXX0023", 'Johannesburg, GT, South Africa')

    """
    Gets the location code of a city
    """
    def getLocation(self):
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
    def repairAmericanLocation(self):
        if len(self.location[1].split(", ")) == 2:
            return [self.location[0], self.location[1] + ', USA']
        else: return self.location

    """
    Determines the weather emoji for all weather types
    @returns the weatherEmoji to the corresponding weatherType
    """
    def getWeatherEmoji(self, weatherType):

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
    Parses the user input
    @param userInput - the user input
    """
    def parseUserInput(self, userInput):

        trimmedInput = userInput.split(":")
        args = []
        if len(trimmedInput) > 1:
            args = trimmedInput[1].split(";")
            if not args[len(args) - 1] in ["verbose", args]:
                args.pop()
            if trimmedInput[0] == "wetter": self.lang = "de"
        else:
            if userInput.split(" ")[0] == "wetter": self.lang = "de"
        for arg in args:
            if arg == "verbose": self.verbose = True
            if arg == "text": self.emojis = False

        cityString = ""
        try: cityString = userInput.split(" ", 1)[1]
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
    Generates a message string to send back
    """
    def messageGenerator(self):

        try:
            weatherType = self.weather['current_conditions']['text'].lower()
            temp = self.weather['current_conditions']['temperature'].lower()
        except: return "Weather data currently unavailable"

        cityString = self.location[1].split(", ")[0] + ", " + self.location[1].split(", ")[2]
        weatherMessage = weatherType

        if self.emojis: weatherMessage = self.getWeatherEmoji(weatherType)
        if self.verbose: cityString = self.location[1].split(", ")[0] + ", " + self.location[1].split(", ")[1] + ", " + self.location[1].split(", ")[2]

        if self.lang == "en":
            return "It is " + weatherMessage + " and " + temp + "°C now in " + cityString
        elif self.lang == "de":
            return "Es ist " + weatherMessage + " und " + temp + "°C in " + cityString
        else: return "Unknown language error"