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
import tvdb_api
from tvdb_exceptions import tvdb_episodenotfound, tvdb_seasonnotfound, tvdb_shownotfound
from requests.exceptions import ConnectionError

from kudubot.servicehandlers.Service import Service
from kudubot.connection.generic.Message import Message


class TvdbService(Service):
    """
    The TvdbService Class that extends the generic Service class.
    The service gets tv show nformation from thetvdb.com
    """

    identifier = "tvdb"
    """
    The identifier for this service
    """

    help_description = {"en": "/tvdb\tSends episode name of an episode from TVDB\n"
                              "syntax: /tvdb <show> s<season> e<episode>",
                        "de": "/tvdb\tSchickt den Episodennamen einer Episode auf TVDB\n"
                              "syntax: /tvdb <show> s<staffel> e<episode>"}
    """
    Help description for this service.
    """

    episode_not_found_error = {"en": "Episode not found on the TV database (thetvdb.com)",
                               "de": "Episode nicht auf der TV Database gefunden (thetvdb.com)"}

    def process_message(self, message: Message) -> None:
        """
        Process a message according to the service's functionality

        :param message: the message to process
        :return: None
        """
        tv_show = message.message_body.split(" ", 1)[1].rsplit(" s", 1)[0]
        season = int(message.message_body.rsplit("s", 1)[1].rsplit(" e", 1)[0])
        episode = int(message.message_body.rsplit("e", 1)[1])

        reply = self.get_tvdb_info(tv_show, season, episode)

        reply_message = self.generate_reply_message(message, "Tvdb", reply)
        self.send_text_message(reply_message)

    @staticmethod
    def regex_check(message: Message) -> bool:
        """
        Checks if the user input is valid for this service to continue

        :return: True if input is valid, False otherwise
        """
        return re.search(r"^/(tvdb) ([^ ]+| )+ s[0-9]{1,2} e[0-9]{1,4}$", message.message_body.lower())

    def get_tvdb_info(self, show: str, season: int, episode: int) -> str:
        """
        Gets information for the given tv show parameters

        :param show: the show to check
        :param season: the season to check
        :param episode: the episode to check
        :return: the received information from thetvdb.com
        """
        try:
            tvdb = tvdb_api.Tvdb()
            episode_info = tvdb[show][season][episode]
            return episode_info['episodename']
        except (tvdb_episodenotfound, tvdb_seasonnotfound, tvdb_shownotfound, ConnectionError):
            return TvdbService.episode_not_found_error[self.connection.last_used_language]
