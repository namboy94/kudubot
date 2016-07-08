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
import requests
from bs4 import BeautifulSoup
from typing import Tuple

from kudubot.servicehandlers.Service import Service
from kudubot.connection.generic.Message import Message


class KitMensaService(Service):
    """
    The KitMensaService Class that extends the generic Service class.
    The service fetches the current Mensa plan for the Mensa at the Karlsruhe
    Institute of Technology (KIT)
    """

    identifier = "kit_mensa"
    """
    The identifier for this service
    """

    help_description = {"en": "/mensa\tSends the Mensa Plan\n"
                              "syntax: /mensa [<line>] [tomorrow]",
                        "de": "/mensa\tSchickt den Mensa Plan\n"
                              "syntax: /mensa [<linie>] [morgen]"}
    """
    Help description for this service.
    """

    mensa_line = {"1": "",
                  "2": "",
                  "3": "",
                  "4": "",
                  "5": "",
                  "6": "",
                  "schnitzelbar": "",
                  "curry queen": "",
                  "abend": "",
                  "cafeteria vormittag": "",
                  "cafeteria nachmittag": ""}

    line_order = {0: "1",
                  1: "2",
                  2: "3",
                  3: "4",
                  4: "5",
                  5: "6",
                  6: "schnitzelbar",
                  7: "curry queen",
                  8: "abend",
                  9: "cafeteria vormittag",
                  10: "cafeteria nachmittag"}

    """
    Dictionary that keeps track of the offering at every line
    """

    line_key = {"line": "en",
                "linie": "de"}
    """
    The phrase for line in different languages
    """

    tomorrow_key = {"tomorrow": "en",
                    "morgen": "de"}
    """
    The phrase for tomorrow in different languages
    """

    closed = False
    """
    Set to True if the mensa is closed for the day
    """

    closed_message = {"en": "The mensa is closed today",
                      "de": "Die Mensa ist heute geschlossen"}
    """
    Message to be sent if the Mensa is closed
    """

    def process_message(self, message: Message) -> None:
        """
        Process a message according to the service's functionality

        :param message: the message to process
        :return: None
        """
        language, line, tomorrow = self.parse_user_input(message.message_body.lower())
        self.get_current_info(tomorrow)

        if self.closed:
            reply = self.closed_message[language]

        elif line == "all":
            reply = ""
            first = False
            for line_no in range(0, len(self.mensa_line)):
                if first:
                    reply += self.mensa_line[self.line_order[line_no]]
                    first = False
                else:
                    reply += "\n" + self.mensa_line[self.line_order[line_no]]

        else:
            reply = self.mensa_line[line]

        reply_message = self.generate_reply_message(message, "KIT Mensa", reply)
        self.send_text_message(reply_message)

    @staticmethod
    def regex_check(message: Message) -> bool:
        """
        Checks if the user input is valid for this service to continue

        :return: True if input is valid, False otherwise
        """
        regex = "^/(mensa)( )?(" + Service.regex_string_from_dictionary_keys([KitMensaService.line_key])
        regex += " (1|2|3|4|5|6)|schnitzelbar|curry queen|abend|cafeteria vormittag|cafeteria nachmittag)?( "
        regex += Service.regex_string_from_dictionary_keys([KitMensaService.tomorrow_key])
        regex += ")?$"

        return re.search(re.compile(regex), message.message_body.lower())

    def get_current_info(self, tomorrow: bool = False) -> None:
        """
        Fetches the current info either for today or tomorrow and stores them in a local dictionary

        :param tomorrow: can be set to True to get the information for tomorrow
        :return: None
        """
        try:

            if tomorrow:
                url = "http://mensa.akk.uni-karlsruhe.de/?DATUM=morgen&uni=1"
            else:
                url = "http://mensa.akk.uni-karlsruhe.de/?DATUM=heute&uni=1"

            html = requests.get(url).text
            soup = BeautifulSoup(html, "html.parser")
            resource = soup.select('body')
            body = resource[0].text

            self.mensa_line["1"] = "Linie 1\n" + body.split("Linie 1:\n", 1)[1].split("Linie 2:", 1)[0]
            self.mensa_line["2"] = "Linie 2\n" + body.split("Linie 2:\n", 1)[1].split("Linie 3:", 1)[0]
            self.mensa_line["3"] = "Linie 3\n" + body.split("Linie 3:\n", 1)[1].split("Linie 4/5:", 1)[0]
            self.mensa_line["4"] = "Linie 4/5\n" + body.split("Linie 4/5:\n", 1)[1].split("Schnitzelbar:", 1)[0]
            self.mensa_line["5"] = self.mensa_line["4"]
            self.mensa_line["6"] = "L6 Update\n" + body.split("L6 Update:\n", 1)[1].split("Abend:", 1)[0]
            self.mensa_line["abend"] = "Abend\n" + body.split("Abend:\n", 1)[1].split("Curry Queen:", 1)[0]
            self.mensa_line["schnitzelbar"] = \
                "Schnitzelbar\n" + body.split("Schnitzelbar:\n", 1)[1].split("L6 Update:", 1)[0]
            self.mensa_line["curry queen"] = \
                "Curry Queen\n" + body.split("Curry Queen:\n", 1)[1].split("Cafeteria Heiße Theke:", 1)[0]
            self.mensa_line["cafeteria vormittag"] = \
                "Cafeteria Heiße Theke\n" + \
                body.split("Cafeteria Heiße Theke:\n", 1)[1].split("Cafeteria ab 14:30:", 1)[0]
            self.mensa_line["cafeteria nachmittag"] = \
                "Cafeteria ab 14:30\n" + body.split("Cafeteria ab 14:30:\n", 1)[1].split("Stand:", 1)[0]

        except IndexError:
            self.closed = True

    def parse_user_input(self, user_input: str) -> Tuple[str, str, bool]:
        """
        Parses the user's input

        :param user_input: the input to be parsed
        :return: the language, the selected line, if today's or tomorrow's plan should be fetched
        """
        language = self.connection.last_used_language

        # Check if only /mensa is entered, if not, strip away /mensa_
        try:
            user_input = user_input.split("/mensa ")[1]
        except IndexError:
            return language, "all", False

        options = user_input.split(" ")  # Split up all words into seperate strings

        # Check if the plan for tomorrow should be fetched
        tomorrow = False
        for key in self.tomorrow_key:
            if key in options:
                tomorrow = True

        # If tomorrow is the only option, select all lines
        if options[0] in self.tomorrow_key:
            language = self.tomorrow_key[options[0]]
            return language, "all", True

        # Otherwise check which line
        else:
            if tomorrow:
                options.pop()  # Remove the tomorrow keyword
            line = ""
            for option in options:
                line += option + " "

            line = line.rstrip()

            for key in self.line_key:
                if key in line:
                    language = self.line_key[key]
                    line = line.replace(key + " ", "")

            return language, line, tomorrow
