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
from typing import List, Dict

from kudubot.servicehandlers.Service import Service
from kudubot.connection.generic.Message import Message


class KickTippService(Service):
    """
    The KickTippService Class that extends the generic Service class.
    The service parses www.kicktipp.de to get a kicktipp group's current standings
    """

    identifier = "kicktipp"
    """
    The identifier for this service
    """

    help_description = {"en": "/kicktipp\tFetches Kicktipp Community Tables\n"
                              "syntax: /kicktipp <kicktipp-community>",
                        "de": "/kicktipp\tZeigt Kicktipp Community Tabellen\n"
                              "syntax: /kicktipp <kicktipp-community>"}
    """
    Help description for this service.
    """

    def process_message(self, message: Message) -> None:
        """
        Process a message according to the service's functionality

        :param message: the message to process
        :return: None
        """
        kicktipp_community = message.message_body.split("/kicktipp ", 1)[1]
        reply = self.get_kicktipp_info(kicktipp_community)

        reply_message = self.generate_reply_message(message, "Kicktipp", reply)
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
        return re.search(r"^/kicktipp [a-z]+(\-|[a-z]+)*[a-z]+$", message.message_body.lower())

    def get_kicktipp_info(self, kicktipp_community: str) -> str:
        """
        Gets the current kicktipp table standings from www.kicktipp.de for a specified kicktipp
        community.

        :param kicktipp_community: the kicktipp community to be checked
        :return: the kicktipp table standings
        """
        # Get the data from kicktipp.de
        html = requests.get("http://www.kicktipp.de/" + kicktipp_community + "/tippuebersicht").text
        soup = BeautifulSoup(html, "html.parser")
        names = soup.select(".mg_class")
        normal_scores = soup.select(".pkt")
        winner_scores = soup.select(".pkts")

        users = []

        normal_score_counter = 0
        winner_score_counter = 0

        for user in range(0, len(names)):
            user_dictionary = {'position': str(user + 1),
                               'name': names[user].text}
            if re.search(r"[0-9]+,[0-9]+", normal_scores[normal_score_counter].text):
                # If the first .pkt element for the user is already a float, it means that the user is a matchday
                # winner. Since winner's matchday points are stored in .pkts elements, we need to get the matchday
                # points of the winner from the .pkts elements and the rest from the .pkt elements
                user_dictionary['day_points'] = winner_scores[winner_score_counter].text
                user_dictionary['wins'] = normal_scores[normal_score_counter].text
                user_dictionary['total_points'] = normal_scores[normal_score_counter + 1].text
                winner_score_counter += 1
                normal_score_counter += 2
            else:
                # Otherwise, if the user is not a winner, just use the .pkt elements for everything
                user_dictionary['day_points'] = normal_scores[normal_score_counter].text
                user_dictionary['wins'] = normal_scores[normal_score_counter + 1].text
                user_dictionary['total_points'] = normal_scores[normal_score_counter + 2].text
                normal_score_counter += 3
            users.append(user_dictionary)

        return self.format_table(users)

    def format_table(self, users: List[Dict[str, str]]) -> str:
        """
        Formats the table for the current connection type

        :param users: A list of dictionaries containing the information for all users.
        :return: the table, formatted
        """
        longest_name = 0
        for user in users:
            if len(user["name"]) > longest_name:
                longest_name = len(user["name"])

        if self.connection.identifier in ["whatsapp", "telegram"]:
            formatted_table = "Pos Name         Pts Wins Tot\n"

            for user in users:
                formatted_table += user["position"].ljust(4)
                formatted_table += user["name"].ljust(12)
                formatted_table += user["day_points"].ljust(4)
                formatted_table += user["wins"].ljust(6)
                formatted_table += user["total_points"] + "\n"

        else:
            formatted_table = "Pos " + "Name".ljust(longest_name + 1) + " Pts  Wins  Tot\n"

            for user in users:
                formatted_table += user["position"].ljust(4)
                formatted_table += user["name"].ljust(longest_name + 1)
                formatted_table += user["day_points"].ljust(5)
                formatted_table += user["wins"].ljust(7)
                formatted_table += user["total_points"] + "\n"

        return formatted_table
