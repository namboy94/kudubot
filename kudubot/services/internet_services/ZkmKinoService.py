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

from kudubot.connection.generic.Message import Message
from kudubot.services.internet_services.CinemaService import CinemaService


class ZkmKinoService(CinemaService):
    """
    The ZkmKinoService Class that extends the generic Service class.
    The service fetches information for showtimes at the cinema:
    Filmpalast am ZKM in Karlsruhe
    """

    identifier = "zkm-kino"
    """
    The identifier for this service
    """

    help_description = {"en": "/zkm\tLists show time for the Filmpalast am ZKM\n"
                              "syntax:\n"
                              "/zkm <in how many days>",
                        "de": "/zkm\tListet Vorstelllungszeiten des Filmpalast am ZKM\n"
                              "syntax:\n"
                              "/zkm <in wievielen Tagen>"}
    """
    Help description for this service.
    """

    no_data_available = {"en": "No data available for this day (yet)",
                         "de": "(Noch) keine Daten für diesen Tag verfügbar"}

    def process_message(self, message: Message) -> None:
        """
        Process a message according to the service's functionality

        :param message: the message to process
        :return: None
        """
        try:
            in_days = int(message.message_body.split("/zkm ")[1])
        except IndexError:
            in_days = 0
        cinema_data = self.get_cinema_data("karlsruhe", in_days, "f090a3fbcdb43f69")

        try:
            reply = self.format_cinema_data(cinema_data)[0]
        except IndexError:
            reply = self.no_data_available[self.connection.last_used_language]
            
        reply_message = self.generate_reply_message(message, "ZKM Kino", reply)
        self.send_text_message(reply_message)

    @staticmethod
    def regex_check(message: Message) -> bool:
        """
        Checks if the user input is valid for this service to continue

        :return: True if input is valid, False otherwise
        """
        regex = "/zkm( [0-9]+)?"
        return re.search(re.compile(regex), message.message_body.lower())
