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
from typing import Tuple
from bs4 import BeautifulSoup
from urllib.parse import urlencode

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
                              "/cinema <city>[, <theater>][, <movie>]",
                        "de": "/kino\tListet die Spielzeiten für Filme im Kino\n"
                              "syntax:\n"
                              "/kino <stadt>[, <theater>][, <film>]"}
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
        city, theater, movie = self.parse_user_input(message.message_body.lower())

        reply = ""
        reply_message = self.generate_reply_message(message, "Cinema", reply)
        self.send_text_message(reply_message)

    @staticmethod
    def regex_check(message: Message) -> bool:
        """
        Checks if the user input is valid for this service to continue

        :return: True if input is valid, False otherwise
        """
        any_word = "(([^ ,]+| )?[^ ,]+)"

        regex = "^" + CinemaService.regex_string_from_dictionary_keys([CinemaService.cinema_keywords])
        regex += " " + any_word + "(, " + any_word + ")?(, " + any_word + ")?$"

        return re.search(re.compile(regex), message.message_body.lower())

    def parse_user_input(self, user_input: str) -> Tuple[str, str, str]:
        """
        Parses the user input for the city, theater and movie to search

        :param user_input: the user input to parse
        :return: the city, theater, movie parsed
        """
        language_key, options = user_input.split(" ", 1)
        self.connection.last_used_language = self.cinema_keywords[language_key]

        city = ""
        theater = ""
        movie = ""

        for part in options.split(" "):
            if not city.endswith(", "):
                city += part + " "
            elif not theater.endswith(", "):
                theater += part + " "
            else:
                movie += part + " "

        city = city.rsplit(",", 1)[0]
        theater = theater.rsplit(",", 1)[0]
        movie = movie.rsplit(",", 1)[0]

        return city, theater, movie

    def get_cinema_data(self, city: str, theater: str, movie: str) -> str:

        # tid == theater ID, mid == movie ID
        payload = {"near": city, "tid": theater, "mid": movie}
        params = {}
        for param in payload:
            if payload[param] != "":
                params[str(params)] = payload[param]
        params = urlencode(params)

        google_request = requests.get("http://google.com/movies?" + params).text
        google_soup = BeautifulSoup(google_request, 'html.parser')

        theater_selection = google_soup.find_all('div', attrs={'class': 'theater'})

        # print(movie_selection)
        for x in theater_selection:
            print(x.div.text)  # = Theater Name
            movies = x.find_all('div', {'class': 'movie'})
            for movie in movies:
                print(movie.div.text)
            print()
            print()

if __name__ == '__main__':
    service = CinemaService(None)
    service.get_cinema_data("karlsruhe", "", "")