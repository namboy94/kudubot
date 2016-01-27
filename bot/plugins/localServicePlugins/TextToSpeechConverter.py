# coding=utf-8

"""
Plugin that can turn a string into a speech file
@author Hermann Krumrey <hermann@krumreyh.com>
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