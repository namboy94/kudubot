# coding=utf-8
"""
Copyright 2015,2016 Hermann Krumrey

This file is part of messengerbot.

    messengerbot makes use of various third-party python modules to serve
    information via the online chat services.

    messengerbot is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    messengerbot is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with messengerbot.  If not, see <http://www.gnu.org/licenses/>.
"""

# imports
import re
import requests
from bs4 import BeautifulSoup
from urllib.parse import urlencode
from typing import Tuple, List, Dict

from messengerbot.servicehandlers.Service import Service
from messengerbot.connection.generic.Message import Message


class CinemaService(Service):
    """
    The CinemaService Class that extends the generic Service class.
    The service parses http://www.google.com/movies for current cinema show times
    and listings
    """

    identifier = "cinema"
    """
    The identifier for this service
    """

    help_description = {"en": "/cinema\tLists show times for movies in cinema\n"
                              "syntax:\n"
                              "/cinema <city> [in how many days]",
                        "de": "/kino\tListet die Spielzeiten für Filme im Kino\n"
                              "syntax:\n"
                              "/kino <stadt> [in wievielen Tage]"}
    """
    Help description for this service.
    """

    cinema_keywords = {"/cinema": "en",
                       "/kino": "de"}
    """
    Keywords for the cinema command
    """

    def process_message(self, message: Message) -> None:
        """
        Process a message according to the service's functionality

        :param message: the message to process
        :return: None
        """
        city, in_days = self.parse_user_input(message.message_body.lower())
        cinema_data = self.get_cinema_data(city, in_days)

        reply = self.format_cinema_data(cinema_data)
        reply_message = self.generate_reply_message(message, "Cinema", reply)
        self.send_text_message(reply_message)

    @staticmethod
    def regex_check(message: Message) -> bool:
        """
        Checks if the user input is valid for this service to continue

        :return: True if input is valid, False otherwise
        """
        regex = "^" + CinemaService.regex_string_from_dictionary_keys([CinemaService.cinema_keywords])
        regex += " (([^ ,]+| )?[^ ,]+)( [0-9]+)?$"

        return re.search(re.compile(regex), message.message_body.lower())

    def parse_user_input(self, user_input: str) -> Tuple[str, int]:
        """
        Parses the user input for the city and the date for which information
        should be fetched

        :param user_input: the user input to parse
        :return: the city and how many days into the future the request is made
        """
        language_key, options = user_input.split(" ", 1)
        self.connection.last_used_language = self.cinema_keywords[language_key]

        if re.search(r"^(([^ ,]+| )?[^ ,]+) [0-9]+$", options):
            city, in_days = options.rsplit(" ", 1)
            return city, int(in_days)

        else:
            return options, 0

    # noinspection PyTypeChecker
    @staticmethod
    def format_cinema_data(cinema_data: Dict[str, Dict[str, (str or List[str])]]) -> str:
        """
        Formats cinema data to be human-readable

        :param cinema_data: the cinema data
        :return: A readable, formatted text of the information contained within the cinema data
        """
        cinema_data_string = ""
        for theater in cinema_data:
            cinema_data_string += theater + "\n\n\n"
            for movie in cinema_data[theater]:
                cinema_data_string += movie + "\n"
                cinema_data_string += cinema_data[theater][movie]["runtime"] + "\n"
                for show_time in cinema_data[theater][movie]["times"]:
                    cinema_data_string += show_time + " "
                cinema_data_string = cinema_data_string.rstrip()
                cinema_data_string += "\n\n"
            cinema_data_string += "\n\n"
        return cinema_data_string.rstrip()

    # noinspection PyTypeChecker
    @staticmethod
    def get_cinema_data(city: str, in_days: int = 0) -> Dict[str, Dict[str, (str or List[str])]]:
        """
        Retrieves the data for the given parameters from google.com/movies

        :param city: the city whose cinemas should be listed
        :param in_days: the data from how many days into the future is requested
        :return: a dictionary containing all theaters and the movies playing in them, as well
                    as some basic information on those movies as well as the show times
        """

        # tid == theater ID, mid == movie ID
        payload = urlencode({"near": city, "date": str(in_days)})

        google_request = requests.get("http://google.com/movies?" + payload).text
        google_soup = BeautifulSoup(google_request, 'html.parser')

        theaters = {}
        theater_selection = google_soup.find_all('div', attrs={'class': 'theater'})

        # print(movie_selection)
        for theater in theater_selection:
            theater_name = theater.div.h2.text

            theaters[theater_name] = {}
            movies = theater.find_all('div', {'class': 'movie'})

            for movie in movies:
                movie_name = movie.div.text

                theaters[theater_name][movie_name] = {"runtime": "",
                                                      "age_info": "",
                                                      "times": []}
                if movie.span.text:
                    theaters[theater_name][movie_name]["runtime"] = movie.span.text.split(" - Rated ")[0]
                    theaters[theater_name][movie_name]["age_info"] = movie.span.text.split(" - Rated ")[1]

                times = movie.find_all('div', {'class': 'times'})
                for show_time in times:
                    theaters[theater_name][movie_name]["times"].append(show_time.text)

        return theaters
