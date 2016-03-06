# coding=utf-8
"""
Copyright 2015,2016 Hermann Krumrey

This file is part of whatsapp-bot.

    whatsapp-bot makes use of various third-party python modules to serve
    information via the online chat service Whatsapp.

    whatsapp-bot is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    whatsapp-bot is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with whatsapp-bot.  If not, see <http://www.gnu.org/licenses/>.
"""

import re
import requests
from bs4 import BeautifulSoup
from plugins.GenericPlugin import GenericPlugin
from yowsupwrapper.entities.WrappedTextMessageProtocolEntity import WrappedTextMessageProtocolEntity


class FootballScores(GenericPlugin):
    """
    The FootballScores class
    """

    def __init__(self, layer, message_protocol_entity=None):
        """
        Constructor
        :param layer: the overlying yowsup layer
        :param message_protocol_entity: the received message information
        :return: void
        """
        super().__init__(layer, message_protocol_entity)
        self.bundesliga = False
        self.lang = "en"
        self.country = ""
        self.league = ""
        self.mode = None

    def regex_check(self):
        """
        Checks if the user input matches the regex needed for the plugin to function correctly
        :return: True if the regex matches, False otherwise
        """
        regex = r"^/(table|tabelle|spieltag|matchday)( [^ ]+, [^ ]+)?$"
        if re.search(regex, self.message):
            return True
        else:
            return False

    def parse_user_input(self):
        """
        Parses the user input
        :return: void
        """
        if not len(self.message.split(" ")) == 1 and "bundesliga" not in self.message:
            country_league = self.message.split(" ", 1)[1]
            self.country = country_league.split(", ")[0]
            self.league = country_league.split(", ")[1]
        else:
            self.bundesliga = True
            self.country = "germany"
            self.league = "bundesliga"

        self.mode = self.message.split(" ")[0].split("/")[1].lower()
        if self.mode in ["tabelle", "spieltag"]:
            self.lang = "de"

    def get_response(self):
        """
        Returns the result of the plugin calculation
        :return: the result of the pluin calculation
        """
        response = ""
        if self.bundesliga:
            if self.mode in ["tabelle", "table"]:
                response = self.__get_bundesliga_table__()
            if self.mode in ["spieltag", "matchday"]:
                response = self.__get_bundesliga_match_day__()
        else:
            if self.mode in ["table", "tabelle"]:
                response = self.__get_generic_table__()
            if self.mode in ["matchday", "spieltag"]:
                response = self.__get_generic_match_day__()
        return WrappedTextMessageProtocolEntity(response, to=self.sender)

    @staticmethod
    def get_description(language):
        """
        Returns a description about this plugin
        :param language: the language in which to display the description
        :return: the description in the specified language
        """
        if language == "en":
            return "/table\tSends football table information\n" \
                   "syntax: /table [<country>][, <league>]\n\n" \
                   "/matchday\tSends football matchday information\n" \
                   "syntax: /matchday [<country>][, <league>]"
        elif language == "de":
            return "/tabelle\tSchickt Fußball Tabelleninformationen\n" \
                   "syntax: /tabelle [<land>][, <league>]\n\n" \
                   "/spieltag\tSchickt Fußball Spieltaginformationen\n" \
                   "syntax: /spieltag [<country>][, <league>]"
        else:
            return "Help not available in this language"

    # Private Methods
    def __get_bundesliga_table__(self):
        """
        Fetches the current bundesliga table
        :return: a formatted string containing the bundesliga table
        """
        return_string = ""
        teamres = self.__get_web_resource__('.team')
        ptsres = self.__get_web_resource__('.pts')

        team_name_index = 1
        point_index = 15
        goals_for_index = 12  # goals for
        goals_against_index = 13  # goals against
        while team_name_index < 19:
            place = str(team_name_index) + ".\t"
            team = self.__make_bundesliga_readable__(teamres[team_name_index].text)
            points = ptsres[point_index].text
            goals_for = ptsres[goals_for_index].text
            goals_against = ptsres[goals_against_index].text
            spacer = "\t"
            if len(goals_against + goals_for) < 4:
                spacer += "\t"
            return_string += place + goals_for + ":" + goals_against + spacer + points + "\t" + team + "\n"
            team_name_index += 1
            point_index += 8
            goals_for_index += 8
            goals_against_index += 8

        return return_string

    def __get_bundesliga_match_day__(self):
        """
        Fetches data for the current Bundesliga match day and returns it
        :return: the bundesliga matchday scores
        """
        return_string = ""
        res = self.__get_web_resource__('.row-gray')

        i = 0
        for r in res:
            if i < 9:
                return_string += r.text + "\n"
                i += 1

        return self.__make_bundesliga_readable__(return_string)

    @staticmethod
    def __make_bundesliga_readable__(string):
        """
        Replaces Names of clubs that are simply too long, or English
        :return: the replaced name
        """
        return_string = string
        return_string = return_string.replace("Borussia Moenchengladbach", "Gladbach")
        return_string = return_string.replace("Bayern Munich", "FC Bayern München")
        return_string = return_string.replace("FC Cologne", "1.FC Köln")
        return return_string

    def __get_generic_match_day__(self):
        """
        Fetches information about a generic country/league matchday
        :return: the matchday as string
        """
        return_string = ""
        res = self.__get_web_resource__('.row-gray')

        for r in res:
            return_string += r.text + "\n"

        return return_string

    def __get_generic_table__(self):
        """
        Fetches the information about a generic country/league table
        :return: the league table as string
        """
        return_string = ""
        teamres = self.__get_web_resource__('.team')

        i = 1
        while i < len(teamres):
            return_string += str(i) + ".\t" + teamres[i].text + "\n"
            i += 1

        return return_string

    def __get_web_resource__(self, html_element):
        """
        Gets the web resource for a specific HTML element from livescore.com
        This will be applied to whatever the currently selected country and league are.
        :param html_element: the html element to look for
        :return: the resource found
        """
        url = "http://www.livescore.com/soccer/" + self.country + "/" + self.league + "/"
        html = requests.get(url).text
        soup = BeautifulSoup(html, "html.parser")
        return soup.select(html_element)
