# coding=utf-8
"""
Copyright 2015,2016 Hermann Krumrey

This file is part of whatsbot.

    whatsbot makes use of various third-party python modules to serve
    information via the online chat service Whatsapp.

    whatsbot is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    whatsbot is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with whatsbot.  If not, see <http://www.gnu.org/licenses/>.
"""

import re
import pywapi
from plugins.GenericPlugin import GenericPlugin
from yowsupwrapper.entities.WrappedTextMessageProtocolEntity import WrappedTextMessageProtocolEntity


class Weather(GenericPlugin):
    """
    Class that stores relevant information, parses user input and gets weather data
    """

    def __init__(self, layer, message_protocol_entity=None):
        """
        Constructor
        :param layer: the overlying yowsup layer
        :param message_protocol_entity: the received message information
        :return: void
        """
        super().__init__(layer, message_protocol_entity)
        
        self.emojis = True
        self.verbose = False
        self.lang = "en"

        self.city = ""
        self.province = ""
        self.country = ""

        self.location = ""
        self.location_code = ""
        self.weather = ""

    def regex_check(self):
        """
        Checks if the user input matches the regex needed for the plugin to function correctly
        :return: True if input is valid, False otherwise
        """
        regex = r"^/(weather|wetter)(:(text;|verbose;)+)?( ([^ ]+| )+(, ([^ ]+| )+)?(, ([^ ]+| )+)?)?$"
        if re.search(regex, self.message):
            return True
        else:
            return False

    def parse_user_input(self):
        """
        Parses the user input
        :return: void
        """
        trimmed_input = self.message.split(":")
        args = []
        if len(trimmed_input) > 1:
            args = trimmed_input[1].split(";")
            if not args[len(args) - 1] in ["verbose", args]:
                args.pop()
            if trimmed_input[0] == "wetter":
                self.lang = "de"
        else:
            if self.message.split(" ")[0] == "wetter": 
                self.lang = "de"
        for arg in args:
            if arg == "verbose": 
                self.verbose = True
            if arg == "text":
                self.emojis = False

        try:
            city_string = self.message.split(" ", 1)[1]
        except NameError:
            city_string = "karlsruhe"

        split_city = city_string.split(", ")

        self.city = split_city[0]
        if len(split_city) == 2:
            self.province = False
            self.country = split_city[1]
        elif len(split_city) == 3:
            self.province = split_city[1]
            self.country = split_city[2]
        else:
            self.province = False
            self.country = False

    def get_response(self):
        """
        Gets the weather data for the location specified by the user input
        :return: the weather data as a WrappedTextMessageProtocolEntity
        """
        try:
            self.location = self.__special_places__(self.city)
            if not self.location:
                self.location = self.__get_location__()
            self.location_code = self.location[0]
            self.location = self.__repair_american_location__()
            self.weather = pywapi.get_weather_from_weather_com(self.location_code)
        except Exception as e:
            str(e)
            return WrappedTextMessageProtocolEntity("City not Found", to=self.sender)

        return WrappedTextMessageProtocolEntity(self.__messageGenerator__(), to=self.sender)

    @staticmethod
    def get_description(language):
        """
        Returns a description about this plugin
        :param language: the language in which to display the description
        :return: the description in the specified language
        """
        if language == "en":
            return "/weather\tSends weather information\n" \
                   "syntax:\t/weather[:][options;] <cityname>[, <region>][, <country>]\n" \
                   "options: text,verbose"
        elif language == "de":
            return "/wetter\tSchickt Wetterinformationen\n" \
                   "syntax:\t/wetter[optionen;] <stadtname>[, <region>][, <land>]\n" \
                   "options: text,verbose"
        else:
            return "Help not available in this language"
        
    # private methods
    @staticmethod
    def __special_places__(city):
        """
        Helper method for getWeather(), which catches special, predefined cities.
        For example, the default search result for Windhoek is Windhoek in South Africa, but with the help of
        this method, the search is overriden and Windhoek in Namibia is displayed
        :return: the city info
        """

        if city == "windhoek":
            return 'WAXX0004', 'Windhoek, KH, Namibia'
        if city == "???":
            raise NameError("Invalid City")
        if city == "johannesburg":
            return "SFXX0023", 'Johannesburg, GT, South Africa'

    def __get_location__(self):
        """
        Gets the location code of a city
        :return: the location code for the user's input
        """
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
                if result == "count":
                    break
                if search[result][1].split(", ")[1].lower() == self.province and \
                        (search[result][1].split(", ")[2].lower() == self.country or self.country == "usa"):
                    return search[result]
            raise NameError("City not Found")

    def __repair_american_location__(self):
        """
        Repairs American Locations (since they only store the state, not the country)
        :return: the repaired location data
        """
        if len(self.location[1].split(", ")) == 2:
            return [self.location[0], self.location[1] + ', USA']
        else:
            return self.location

    @staticmethod
    def __get_weather_emoji__(weather_type):
        """
        Determines the weather emoji for all weather types
        :return: the weatherEmoji to the corresponding weather_type
        """
        if weather_type in ["sunny", "clear", "sunny / windy", "clear / windy"]:
            return "☀"
        elif weather_type in ["fair"]:
            return "🌤"
        elif weather_type in ["partly cloudy"]:
            return "⛅"
        elif weather_type in ["mostly cloudy"]:
            return "🌥"
        elif weather_type in ["not definded"]:
            return "🌦"
        elif weather_type in ["light rain", "light rain shower"]:
            return "🌧"
        elif weather_type in ["cloudy"]:
            return"☁"
        elif weather_type in ["thunderstorms", "t-storm"]:
            return "⛈"
        elif weather_type in ["rain shower"]:
            return "☔"
        elif weather_type in ["thunderclouds"]:
            return "🌩"
        elif weather_type in ["snow"]:
            return "🌨"
        elif weather_type in ["windy"]:
            return "🌬"
        elif weather_type in ["tornado"]:
            return "🌪"
        elif weather_type in ["haze", "fog", "mist"]:
            return "🌫"
        else:
            return "???"

    # noinspection PyTypeChecker
    def __messageGenerator__(self):
        """
        Generates a message string to send back
        :return: the message string
        """
        try:
            weather_type = self.weather['current_conditions']['text'].lower()
            temp = self.weather['current_conditions']['temperature'].lower()
        except Exception as e:
            str(e)
            return "Weather data currently unavailable"

        city_string = self.location[1].split(", ")[0] + ", " + self.location[1].split(", ")[2]
        weather_message = weather_type

        if self.emojis:
            weather_message = self.__get_weather_emoji__(weather_type)
        if self.verbose:
            city_string = self.location[1].split(", ")[0] + ", " + self.location[1].split(", ")[1] + ", " +\
                          self.location[1].split(", ")[2]

        if self.lang == "en":
            return "It is " + weather_message + " and " + temp + "°C now in " + city_string
        elif self.lang == "de":
            return "Es ist " + weather_message + " und " + temp + "°C in " + city_string
        else:
            return "Unknown language error"
