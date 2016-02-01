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

import os
import re
from plugins.GenericPlugin import GenericPlugin

"""
The TextToSpeechConverter Class
"""
class TextToSpeechConverter(GenericPlugin):

    """
    Constructor
    Defines parameters for the plugin.
    @:param layer - the overlying yowsup layer
    @:param messageProtocolEntity - the received message information
    @:override
    """
    def __init__(self, layer, messageProtocolEntity=None):
        if messageProtocolEntity is None: self.layer = layer; return
        self.layer = layer
        self.entity = messageProtocolEntity
        self.capitalMessage = self.entity.getBody()
        self.message = self.capitalMessage.lower()
        self.sender = self.entity.getFrom()
        self.voiceMessage = ""
        self.language = "en-us"

    """
    Checks if the user input is valid for this plugin to continue
    @:return True if input is valid, False otherwise
    @:override
    """
    def regexCheck(self):
        return re.search(r"^/speak \"[^\"]+\"( german| english| french)?$", self.message)

    """
    Parses the user's input
    @:override
    """
    def parseUserInput(self):
        self.voiceMessage = self.capitalMessage.split("\"", 1)[1].rsplit("\"", 1)[0]
        if self.message.endswith("german"): self.language = "de-de"
        if self.message.endswith("french"): self.language = "fr-fr"

    """
    Returns the response calculated by the plugin
    @:return the response as a MessageProtocolEntity
    @:override
    """
    def getResponse(self):
        self.__generateAudio__()
        self.sendAudio(self.sender, "/tmp/tempAudio.wav", self.voiceMessage)
        return None

    """
    Returns a helpful description of the plugin's syntax and functionality
    @:param language - the language to be returned
    @:return the description as string
    @:override
    """
    @staticmethod
    def getDescription(language):
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

    """
    Generates an audio file
    """
    def __generateAudio__(self):
        file = open("/tmp/messageText", 'w')
        file.write(self.voiceMessage)
        file.close()
        #Popen(["pico2wave", "-l=" + self.language, "-w=/tmp/tempAudio.wav", "$(cat", "/tmp/messageText)"]).wait()
        #os.system("pico2wave -l=" + self.language + " -w=/tmp/tempAudio.wav \"$(cat /tmp/messageText)\"")
        os.system("espeak -v " + self.language + " -f /tmp/messageText -w /tmp/tempAudio.wav")