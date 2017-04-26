"""
LICENSE:
Copyright 2015-2017 Hermann Krumrey

This file is part of kudubot.

    kudubot is a chat bot framework. It allows developers to write
    services for arbitrary chat services.

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

import os
import json
import time
import requests
from subprocess import Popen
from bs4 import BeautifulSoup
from typing import List, Tuple, Dict
from kudubot.services.Service import Service
from kudubot.entities.Message import Message, from_dict as message_from_dict


class ExternalService(Service):
    """
    A Service which allows the use of executable files written in other programming languages to be used
    in conjunction with the kudubot framework
    """

    # noinspection PyAttributeOutsideInit
    def init(self):
        """
        Initializes the message directory for the external service and makes sure the executable file
        exists. If it doesn't, it will download the file from the executable file url specified in
        define_executable_file_url()
        :return: None
        """
        self.message_dir = os.path.join(self.connection.external_services_directory, self.identifier)
        if not os.path.isdir(self.message_dir):
            os.makedirs(self.message_dir)

        self.executable_file = os.path.join(self.connection.config_handler.external_services_executables_directory,
                                            self.identifier)

        if not os.path.isfile(self.executable_file):
            self.download_executable()

    @staticmethod
    def define_identifier() -> str:
        """
        :return: The identifier for this service
        """
        raise NotImplementedError()

    @staticmethod
    def define_requirements() -> List[str]:
        """
        External Services can not have any dependencies
        :return: []
        """
        return []

    def define_executable_file_url(self):
        """
        :return: An URL to the executable file
        """
        raise NotImplementedError()

    def define_executable_command(self) -> List[str]:
        """
        Defines the commands preceding the exectuable file name to run the program.
        For example, [python] for a python script, or [java, -jar] for a .jar file

        :return: The preceding commands as a list of arguments
        """
        raise NotImplementedError()

    def download_executable(self):
        """
        Downloads the executable file

        :return: None
        """
        # noinspection PyBroadException
        try:
            with open(self.executable_file, 'wb') as destination:
                data = requests.get(self.define_executable_file_url()).content
                destination.write(data)
        except:
            self.logger.info("Could not download executable. Disabling Service.")
            if os.path.isfile(self.executable_file):
                os.remove(self.executable_file)

    def handle_message(self, message: Message):
        """
        Stores the Message in a json file and runs the executable file, then analyzes the result.

        :param message: The message to handle
        :return: None
        """
        if not os.path.isfile(self.executable_file):
            return

        message_file, response_file = self.store_message_in_file(message)

        Popen(self.define_executable_command() +
              [self.executable_file,
               "handle_message", message_file, response_file,
               self.connection.database_file_location]).wait()

        response = self.load_json(response_file)

        if response["mode"] == "reply":
            self.connection.send_message(self.retrieve_message_from_file(message_file))

        self.cleanup(message_file, response_file)

    def is_applicable_to(self, message: Message) -> bool:
        """
        Writes the message to a JSON file, then communicates with the executable to check if the
        message is applicable to the file

        :param message: The message to analyze
        :return: None
        """
        if not os.path.isfile(self.executable_file):
            return False

        message_file, response_file = self.store_message_in_file(message)

        Popen(self.define_executable_command() +
              [self.executable_file,
               "is_applicable_to", message_file, response_file,
               self.connection.database_file_location]).wait()

        response = self.load_json(response_file)

        return response["mode"] == "is_applicable" and response["applicable"]

    def store_message_in_file(self, message: Message) -> Tuple[str, str]:
        """
        Stores a message in a json file. The filename of the file will be the current time.
        Also generates a response file location in which the executable may write a response into

        :param message: The message to save
        :return: The location of the stored message json file, the location of the response file
        """

        json_data = message.to_dict()

        while True:  # Make sure that file does not exist
            message_file = os.path.join(self.message_dir, str(time.time()))
            if not os.path.isfile(message_file):
                with open(message_file + ".json", 'w') as json_file:
                    json.dump(json_data, json_file)
                return message_file + ".json", message_file + "-response.json"

    # noinspection PyMethodMayBeStatic
    def load_json(self, response_file: str) -> Dict[str, type]:
        """
        Loads a json file into a dictionary

        :param response_file: The file to parse
        :return: The generated dictionary
        """

        with open(response_file, 'r') as f:
            content = json.load(f)

        return content

    def retrieve_message_from_file(self, message_file: str) -> Message:
        """
        Loads a message from a message json file

        :param message_file: The json file location
        :return: The generates Message object
        """
        return message_from_dict(self.load_json(message_file))

    # noinspection PyMethodMayBeStatic
    def cleanup(self, message_file: str, response_file: str):
        """
        Deletes the message and response files

        :param message_file: The message file to delete
        :param response_file: The response file to delete
        :return: None
        """

        if os.path.isfile(message_file):
            os.remove(message_file)
        if os.path.isfile(response_file):
            os.remove(response_file)

    # noinspection PyMethodMayBeStatic
    def resolve_github_release_asset_url(self, owner: str, repository: str, filename: str) -> str:
        """
        Generates a download URL for a Github release artifact/asset

        :param owner: The owner of the Github repository
        :param repository: The name of the repository
        :param filename: The file to search for
        :return: The URL to the file, if it was found. If not, an empty string is returned
        """

        release_page = "https://github.com/" + owner + "/" + repository + "/releases/latest"
        soup = BeautifulSoup(requests.get(release_page).text, "html.parser")
        downloads = soup.select(".release-downloads")[0]

        for download in downloads.select("a"):
            name = download.select("strong")[0]

            if name == filename:
                return "https://github.com" + download["href"]

        return ""
