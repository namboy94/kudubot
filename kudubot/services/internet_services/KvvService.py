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
import json
import urllib.error
import urllib.request
from typing import List, Dict, Tuple
from urllib.parse import quote_plus, urlencode

from kudubot.servicehandlers.Service import Service
from kudubot.connection.generic.Message import Message


class KvvService(Service):
    """
    The KvvService Class that extends the generic Service class.
    The service checks the curent timetables from the KVV Straßenbahn Network
    and displays the most relevant times
    """

    identifier = "kvv"
    """
    The identifier for this service
    """

    help_description = {"en": "/kvv\tShows KVV timetable information\n"
                              "syntax:\n"
                              "/kvv <station>",
                        "de": "/kvv\tZeigt KVV Zeiten an\n"
                              "syntax:\n"
                              "/kvv <station>"}
    """
    Help description for this service.
    """

    kvv_api_key = "377d840e54b59adbe53608ba1aad70e8"
    """
    The KVV API key
    """

    kvv_url = "http://live.kvv.de/webapp/"
    """
    The KVV URL
    """

    corrections = {"hauptbahnhof": "karlsruhe hauptbahnhof",
                   "vorplatz": "karlsruhe hbf vorplatz",
                   "karlruhe hauptbahnhof vorplatz": "karlsruhe hbf vorplatz",
                   "hauptbahnhof vorplatz": "karlsruhe hbf vorplatz"}
    """
    Corrections for the station parameter given by the user to attempt to deliver more relevant
    search results
    """

    def process_message(self, message: Message) -> None:
        """
        Process a message according to the service's functionality

        :param message: the message to process
        :return: None
        """
        station = message.message_body.split(" ", 1)[1]
        reply = self.get_kvv_info(station)
        reply_message = self.generate_reply_message(message, "KVV", reply)
        self.send_text_message(reply_message)

    @staticmethod
    def regex_check(message: Message) -> bool:
        """
        Checks if the user input is valid for this service to continue

        :return: True if input is valid, False otherwise
        """
        regex = "^/kvv "
        return re.search(re.compile(regex), message.message_body.lower())

    def get_kvv_info(self, station: str) -> str:
        """
        Gets the KVV information for a selected station

        :param station: the station for which information should be looked up
        :return: the information for that station
        """
        station_ids = self.get_location_ids(station)

        for station_id in station_ids:
            try:
                times, official_station_name = self.get_times_from_stop_id(station_id['id'])
                return self.format_timetable(times, official_station_name)
            except urllib.error.HTTPError:
                pass

    # noinspection PyDefaultArgument
    def query_kvv_webapp(self, path: str, options: Dict[str, str]={}) -> Dict[str, str]:
        """
        Queries the KVV Webapp for a specified URL and returns a JSON parsed dictionary

        :param path: the URL path to be queried
        :param options: Options to be sent with the query
        :return: the JSON parsed dictionary
        """
        options["key"] = self.kvv_api_key
        query_url = self.kvv_url + path + "?" + urlencode(options)

        query_request = urllib.request.Request(query_url)
        opened_query_url = urllib.request.urlopen(query_request)
        result = opened_query_url.read().decode("utf-8")

        return json.loads(result)

    def get_location_ids(self, station_name) -> List[Dict[str, str]]:
        """
        Searches for the location id of a station

        :param station_name: the name of the station
        :return: the station ID
        """
        if station_name.lower() in self.corrections:
            station_name = self.corrections[station_name.lower()]

        station_name = station_name.replace(" ", "_")

        location_search_path = "stops/byname/" + quote_plus(station_name)
        json_parsed_dictionary = self.query_kvv_webapp(location_search_path)

        # noinspection PyTypeChecker
        return json_parsed_dictionary["stops"]

    def get_times_from_stop_id(self, station_id: str) -> Tuple[List[Dict[str, str]], str]:
        """
        Searches for departure times at a KVV station

        :param station_id: The station ID of the station to be queried
        :return: a list of departure dictionaries as well as the official station name
        """
        timetable_path = "departures/bystop/" + station_id
        json_parsed_dictionary = self.query_kvv_webapp(timetable_path)

        return json_parsed_dictionary["departures"], json_parsed_dictionary["stopName"]

    @staticmethod
    def format_timetable(station_times: List[Dict[str, str]], station_name: str) -> str:
        """
        Formats the timetable with the queried information

        :param station_times: the list of departure times of the station
        :param station_name: the station name
        :return: A formated string of the timetable information
        """
        direction_1_departures = []
        direction_2_departures = []
        for departure in station_times:
            if departure['direction'] == '1':
                direction_1_departures.append(departure)
            elif departure['direction'] == '2':
                direction_2_departures.append(departure)
        all_directions = [direction_1_departures, direction_2_departures]

        formatted_string = "Abfahrten an der Haltestelle " + station_name + ":\n\n"

        for direction in all_directions:
            for departure in direction:
                formatted_string += departure["time"] + " "
                formatted_string += departure["route"] + " "
                formatted_string += departure["destination"] + "\n"
            formatted_string += "\n"

        return formatted_string.rsplit("\n\n", 1)[0]
