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
from typing import Dict, List

from kudubot.servicehandlers.Service import Service
from kudubot.connection.generic.Message import Message


class FootballInfoService(Service):
    """
    The FootballInfoService Class that extends the generic Service class.
    The service parses www.livescore.com to get current league table and match results
    for football matches.
    """

    identifier = "football_info"
    """
    The identifier for this service
    """

    help_description = {"en": "/table\tSends football table information\n"
                              "syntax: /table [<country>][, <league>]\n\n"
                              "/matchday\tSends football matchday information\n"
                              "syntax: /matchday [<country>][, <league>]",
                        "de": "/tabelle\tSchickt Fußball Tabelleninformationen\n"
                              "syntax: /tabelle [<land>][, <liga>]\n\n"
                              "/spieltag\tSchickt Fußball Spieltaginformationen\n"
                              "syntax: /spieltag [<country>][, <liga>]"}
    """
    Help description for this service.
    """

    league_mode = False
    """
    If the command parser check the command, it can set this flag to tell the program that the league table is
    requested
    """

    matchday_mode = False
    """
    If the command parser check the command, it can set this flag to tell the program that the match day results
    are requested
    """

    league_descriptors = {"league": "en", "liga": "de"}
    """
    Descriptors in different languages for the league mode (used for the command syntax)
    """

    matchday_descriptors = {"matchday": "en", "spieltag": "de"}
    """
    Descriptors in different languages for the matchday mode (used for the command syntax)
    """

    country = ""
    """
    The country to parse
    """

    league = ""
    """
    The league to parse
    """

    def process_message(self, message: Message) -> None:
        """
        Process a message according to the service's functionality

        :param message: the message to process
        :return: None
        """
        self.parse_command(message.message_body.lower())

        reply = ""

        if self.league_mode:
            reply = self.get_league_info()
        elif self.matchday_mode:
            reply = self.get_matchday_info()

        reply_message = self.generate_reply_message(message, "Football Info", reply)

        if self.connection.identifier in ["whatsapp", "telegram"]:
            self.send_text_as_image_message(reply_message)
        else:
            self.send_text_message(reply_message)

    @staticmethod
    def regex_check(message: Message) -> bool:
        """
        Checks if the user input is valid for this service to continue

        :return: True if input is valid, False otherwise
        """

        # Generate the Regex
        regex_term = "^/" + Service.regex_string_from_dictionary_keys([FootballInfoService.league_descriptors,
                                                                       FootballInfoService.matchday_descriptors]) \
                     + "( [a-zA-Z]+, [a-zA-Z]+( |[a-zA-Z]+|-)*)[a-zA-Z]+$"

        return re.search(re.compile(regex_term), message.message_body.lower())

    def parse_command(self, message_text: str) -> None:
        """
        Parses the command. It determines which country and league to parse and if a league table or
        a match day. The language is also checked

        :return: None
        """
        # Check which mode to use
        mode = message_text.split(" ")[0].split("/")[1].lower()
        if mode in self.league_descriptors:
            self.connection.last_used_language = self.league_descriptors[mode]
            self.league_mode = True
        elif mode in self.matchday_descriptors:
            self.connection.last_used_language = self.matchday_descriptors[mode]
            self.matchday_mode = True

        # Determine league and country
        country_league = message_text.split(" ", 1)[1]
        self.country = country_league.split(", ")[0]
        self.league = country_league.split(", ")[1].replace(" ", "-")

    def get_league_info(self) -> str:
        """
        Retrieves the info for a league table, pretifies it, and returns it as a string

        :return: the league table info
        """
        teams = self.get_web_resource('.team')
        stats = self.get_web_resource('.pts')

        league_table = {}

        team_position_index = 1
        stats_index = 8

        while team_position_index < len(teams) and stats_index < len(stats):

            team = {"team_name": teams[team_position_index].text,
                    "matches": stats[stats_index].text,
                    "wins": stats[stats_index + 1].text,
                    "draws": stats[stats_index + 2].text,
                    "losses": stats[stats_index + 3].text,
                    "goals_for": stats[stats_index + 4].text,
                    "goals_against": stats[stats_index + 5].text,
                    "goal_difference": stats[stats_index + 6].text,
                    "points": stats[stats_index + 7].text,
                    "position": str(team_position_index)}

            league_table[team_position_index] = team

            team_position_index += 1
            stats_index += 8

        return self.format_league_table(league_table)

    def get_matchday_info(self) -> str:
        """
        Retrieves the info for a matchday, pretifies it, and returns it as a string

        :return: the matchday results info
        """
        teams = self.get_web_resource('.ply')
        times = self.get_web_resource('.min')
        score = self.get_web_resource('.sco')

        matches = []

        for index in range(0, len(teams), 2):
            match = {"left_team": teams[index].text,
                     "right_team": teams[index + 1].text,
                     "time": times[int(index / 2)].text,
                     "score": score[int(index / 2)].text}

            matches.append(match)

        return self.format_matchday(matches)

    def get_web_resource(self, html_element: str) -> List:
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

    @staticmethod
    def format_league_table(league_table_dictionary: Dict[int, Dict[str, str]]) -> str:
        """
        Formats a league table dictionary

        :param league_table_dictionary: The league table dictionary to format
        :return: the league table as string
        """
        # Determine how long the longest team name is
        longest_team_name = 0
        for position in range(1, len(league_table_dictionary) + 1):
            team_name_length = len(league_table_dictionary[position]["team_name"])
            if team_name_length > longest_team_name:
                longest_team_name = team_name_length

        formatted_string = "#    " + "Team Name".ljust(longest_team_name) + \
                           "  P     W     D     L     GF    GA    GD    Pts\n"
        divider = "  "

        for position in range(1, len(league_table_dictionary) + 1):
            line = "\n" + str(position).ljust(3) + divider
            line += league_table_dictionary[position]["team_name"].ljust(longest_team_name) + divider
            line += league_table_dictionary[position]["matches"].ljust(4) + divider
            line += league_table_dictionary[position]["wins"].ljust(4) + divider
            line += league_table_dictionary[position]["draws"].ljust(4) + divider
            line += league_table_dictionary[position]["losses"].ljust(4) + divider
            line += league_table_dictionary[position]["goals_for"].ljust(4) + divider
            line += league_table_dictionary[position]["goals_against"].ljust(4) + divider
            line += league_table_dictionary[position]["goal_difference"].rjust(4) + divider
            line += league_table_dictionary[position]["points"].ljust(4)

            formatted_string += line

        return formatted_string

    @staticmethod
    def format_matchday(matchday_list: List[Dict[str, str]]) -> str:
        """
        Formats a matchday List into a sendable string

        :param matchday_list: The matchday list to be formatted
        :return: The formatted string
        """

        # Establish lengths of the team names
        longest_left = 0
        longest_right = 0

        for match in matchday_list:
            if len(match["left_team"]) > longest_left:
                longest_left = len(match["left_team"])
            if len(match["right_team"]) > longest_right:
                longest_right = len(match["left_team"])

        formatted_string = ""
        first = True

        for match in matchday_list:
            if first:
                first = False
            else:
                formatted_string += "\n"

            formatted_string += match["time"].ljust(6)
            formatted_string += match["left_team"].rjust(longest_left + 1)
            formatted_string += match["score"].ljust(5)
            formatted_string += match["right_team"].ljust(longest_right + 1)

        return formatted_string
