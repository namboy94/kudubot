# coding=utf-8
"""
LICENSE:
Copyright 2015,2016 Hermann Krumrey

This file is part of kudubot.

    kudubot makes use of various third-party python modules to serve
    information via online chat services.

    kudubot is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    kudubot is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with kudubot.  If not, see <http://www.gnu.org/licenses/>.
LICENSE
"""

# imports
import re
import pywapi
from typing import Tuple, Dict

from kudubot.servicehandlers.Service import Service
from kudubot.connection.generic.Message import Message


class WeatherService(Service):
    """
    The KickTippService Class that extends the generic Service class.
    The service parses www.kicktipp.de to get a kicktipp group's current standings
    """

    identifier = "weather"
    """
    The identifier for this service
    """

    help_description = {"en": "/weather\tSends weather information\n"
                              "syntax:\t/weather[:][options;] <cityname>[, <region>][, <country>]\n"
                              "options: text, verbose",
                        "de": "/wetter\tSchickt Wetterinformationen\n"
                              "syntax:\t/wetter[optionen;] <stadtname>[, <region>][, <land>]\n"
                              "optionen: text, verbos"}
    """
   Help description for this service.
   """

    weather_keywords = {"weather": "en",
                        "wetter": "de"}
    """
    Keywords that map to the language to be used
    """

    options = {"text": False,
               "verbose": False}

    weather_identifiers = {"sunny": {"em":  "☀", "de": "sonnig"},
                           "clear": {"em":  "☀", "de": "klar"},
                           "sunny / windy": {"em":  "☀", "de": "sonnig / windig"},
                           "clear / windy": {"em":  "☀", "de": "klar / windig"},
                           "light rain": {"em":  "🌧", "de": "leichter Regen"},
                           "light rain shower": {"em":  "🌧", "de": "leichter Regenschauer"},
                           "haze": {"em":  "🌫", "de": "Dunst"},
                           "fog": {"em":  "🌫", "de": "Nebel"},
                           "mist": {"em":  "🌫", "de": "Nebel"},
                           "thunderstorms": {"em":  "⛈", "de": "Gewitter"},
                           "t-storm": {"em":  "⛈", "de": "Gewitter"},
                           "fair": {"em":  "🌤", "de": "recht sonnig"},
                           "partly cloudy": {"em":  "⛅", "de": "teils bewölkt"},
                           "mostly cloudy": {"em":  "🌥", "de": "stark bewölkt"},
                           "not defined": {"em":  "❔", "de": "nicht definiert"},
                           "cloudy": {"em":  "☁", "de": "bewölkt"},
                           "rain shower": {"em":  "☔", "de": "Regenschauer"},
                           "thunderclouds": {"em":  "🌩", "de": "Gewitterwolken"},
                           "snow": {"em":  "🌨", "de": "Schnee"},
                           "windy": {"em":  "🌬", "de": "windig"},
                           "tornado": {"em":  "🌪", "de": "Tornado"}}
    """
    A dictionary of weather identifiers for icons (and different languages)
    """

    weather_message_dictionary = {"en": ("It is ", " and ", " now in "),
                                  "de": ("Es ist ", " und ", " in ")}
    """
    Defines the weather message for multiple languages
    """

    city_not_found_message = {"en": "City not found",
                              "de": "Stadt nicht gefunden"}

    def process_message(self, message: Message) -> None:
        """
        Process a message according to the service's functionality

        :param message: the message to process
        :return: None
        """
        language, city, country, region = self.parse_user_input(message)
        self.connection.last_used_language = language

        location = self.get_location(city, country, region)
        if location is not None:
            weather = pywapi.get_weather_from_weather_com(location[0])
            reply = self.generate_weather_string(language, location, weather)
        else:
            reply = self.city_not_found_message[language]

        reply_message = self.generate_reply_message(message, "Weather", reply)
        self.send_text_message(reply_message)

    @staticmethod
    def regex_check(message: Message) -> bool:
        """
        Checks if the user input is valid for this service to continue

        :return: True if input is valid, False otherwise
        """
        regex = "^/" + Service.regex_string_from_dictionary_keys([WeatherService.weather_keywords])
        regex += "(:(text;|verbose;)+)?( (([^ ,]+| )+)(, ([^ ,]+| )+)?(, ([^ ,]+| )+)?)?$"

        return re.search(re.compile(regex), message.message_body)

    def parse_user_input(self, message: Message) -> Tuple[str, str, str, str]:
        """
        Parses the user input. It determines the used language, if text mode or verbose mode should
        be used and the city, country and region to check
        The options are stored in the options dictionary

        :return: a tuple of the parsed information in the order:
                    -language
                    -city
                    -country
                    -region
        """
        message = message.message_body.lower().split("/", 1)[1].split(" ")
        command = message[0]
        option_split = command.split(":")

        language = self.weather_keywords[option_split[0]]

        verbose = False
        text_mode = False

        if len(option_split) > 1:
            options = option_split[1].split(";")
            if "verbose" in options:
                verbose = True
            if "text" in options:
                text_mode = True

        self.options["text"] = text_mode
        self.options["verbose"] = verbose

        city = ""
        country = ""
        region = ""

        # This concats all space-delimited parts of the string for so long until a comma is found at the end,
        # then it jumps on to the next-less relevant regional identifier (city->country->region)
        for position in range(1, len(message)):
            if city.endswith(","):
                if country.endswith(","):
                    if region.endswith(","):
                        break
                    else:
                        region += " " + message[position]
                else:
                    country += " " + message[position]
            else:
                city += " " + message[position]

        # Remove commas and surrounding space characters
        city = city.replace(",", "").strip()
        country = country.replace(",", "").strip()
        region = region.replace(",", "").strip()

        return language, city, country, region

    @staticmethod
    def get_location(city: str, country: str, region: str) -> Tuple[str, str]:
        """
        Gets a pywapi location ID Tuple for a city, country and region

        :param city: The city to be searched
        :param country: The country to be searched
        :param region: The region to be searched
        :return: the pywapi location ID Tuple, or None if no location was found
        """
        search_term = city
        if country:
            search_term += (", " + country)
        if region:
            search_term += (", " + region)

        try:
            location = pywapi.get_loc_id_from_weather_com(search_term)[0]
        except KeyError:
            return None

        # Add 'USA' to US-american location strings
        if len(location[1].split(", ")) < 3:
            location_string = location[1]
            location_string += ", USA"
            location = (location[0], location_string)

        return location

    def generate_weather_string(self, language: str, location: Tuple[str, str], weather: Dict) -> str:
        """
        Generates a message string to send back for the selected location's weather using the
        specified options

        :param language: the language to use
        :param location: the loaction tuple of the location to check
        :param weather: the weather dictionary of that location
        :return: the message string
        """
        try:
            weather_type = weather['current_conditions']['text']
            temperature = weather['current_conditions']['temperature']
            location_string = location[1]

            if not self.options['verbose']:
                location_string = location_string.split(", ")[0] + ", " + location_string.split(", ")[2]

            if not self.options['text']:
                try:
                    weather_type = WeatherService.weather_identifiers[weather_type.lower()]["em"]
                except KeyError:
                    weather_type = WeatherService.weather_identifiers["not defined"]["em"]
            else:
                if language != "en":
                    try:
                        weather_type = WeatherService.weather_identifiers[weather_type.lower()]["de"]
                    except KeyError:
                        weather_type = WeatherService.weather_identifiers["not defined"]["de"]

            language_message = WeatherService.weather_message_dictionary[language]
            message_string = language_message[0] + weather_type + language_message[1]
            message_string += temperature + "°C" + language_message[2] + location_string

            return message_string
        except KeyError:
            return "Weather data currently unavailable"
