# coding=utf-8
"""
Copyright 2015,2016 Hermann Krumrey

This file is part of whatsbot.

    whatsbot makes use of various third-party python modules to serve
    information via the online chat service Whatsapp.

    whatsbot is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    whatsbot is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with whatsbot.  If not, see <http://www.gnu.org/licenses/>.
"""

import os
import re

try:
    from plugins.GenericPlugin import GenericPlugin
except ImportError:
    from whatsbot.plugins.GenericPlugin import GenericPlugin


class TextToSpeechConverter(GenericPlugin):
    """
    The TextToSpeechConverter Class
    """
    
    def __init__(self, layer, message_protocol_entity=None):
        """
        Constructor
        Defines parameters for the plugin.
        :param layer: the overlying yowsup layer
        :param message_protocol_entity: the received message information
        :return: void
        """
        super().__init__(layer, message_protocol_entity)
        self.voice_message = ""
        self.language = "en-us"

    def regex_check(self):
        """
        Checks if the user input is valid for this plugin to continue
        :return: True if input is valid, False otherwise
        """
        return re.search(r"^/speak \"[^\"]+\"( german| english| french)?$", self.message)

    def parse_user_input(self):
        """
        Parses the user's input
        :return: void
        """
        self.voice_message = self.cap_message.split("\"", 1)[1].rsplit("\"", 1)[0]
        if self.message.endswith("german"):
            self.language = "de-de"
        if self.message.endswith("french"):
            self.language = "fr-fr"

    def get_response(self):
        """
        Returns the response calculated by the plugin
        :return: the response as a MessageProtocolEntity
        """
        self.__generate_audio__()
        self.send_audio(self.sender, "/tmp/tempAudio.wav", self.voice_message)
        return None

    @staticmethod
    def get_description(language):
        """
        Returns a helpful description of the plugin's syntax and functionality
        :param language: the language to be returned
        :return: the description as string
        """
        if language == "en":
            return "/speak\tA text-to-speech engine\n" \
                   "syntax:\n" \
                   "/speak \"<text>\" <language>"
        elif language == "de":
            return "/speak\tEine text-to-speech Funktion\n" \
                   "syntax:\n" \
                   "/speak \"<text>\" <sprache>"
        else:
            return "Help not available in this language"

    @staticmethod
    def get_plugin_name():
        """
        Returns the plugin name
        :return: the plugin name
        """
        return "Text To Speech Plugin"

    def __generate_audio__(self):
        """
        Generates an audio file
        :return: void
        """
        file = open("/tmp/messageText", 'w')
        file.write(self.voice_message)
        file.close()
        os.system("espeak -v " + self.language + " -f /tmp/messageText -w /tmp/tempAudio.wav")
        # Popen(["pico2wave", "-l=" + self.language, "-w=/tmp/tempAudio.wav", "$(cat", "/tmp/messageText)"]).wait()
        # os.system("pico2wave -l=" + self.language + " -w=/tmp/tempAudio.wav \"$(cat /tmp/messageText)\"")
