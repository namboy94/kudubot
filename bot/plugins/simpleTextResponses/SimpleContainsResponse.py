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

import random
from yowsup.layers.protocol_messages.protocolentities import TextMessageProtocolEntity
from utils.math.Randomizer import Randomizer
from plugins.GenericPlugin import GenericPlugin


class SimpleContainsResponse(GenericPlugin):
    """
    The SimpleContainsResponse Class
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

        self.response = ""
        self.case_insensitive_options = \
            [[["keks", "cookie"], ["Ich will auch Kekse!",
                                   "Wo gibt's Kekse?",
                                   "Kekse sind klasse!",
                                   "Ich hab einen Gutschein für McDonald's Kekse!",
                                   "🍪"]],
             [["kuchen", "cake"], ["Ich mag Kuchen",
                                   "Marmorkuchen!",
                                   "Kuchen gibt's bei Starbucks"]],
             [["ups", "oops", "uups"], ["Was hast du jetzt schon wieder kaputt gemacht?"]],
             [["wuerfel", "würfel"], ["Würfel sind toll",
                                      "Du hast eine " + str(random.randint(1, 6)) + " gewürfelt!",
                                      "https://play.google.com/store/apps/details?id=com.namibsun.android.dice"]],
             [["😂"], ["😂😂😂"]],
             [["🖕🏻"], ["😡🖕🏻"]],
             [["beste bot", "bester bot"], ["😘"]],
             [["chicken", "nuggets", "huhn", "hühnchen"], ["🐤", "Die armen Kücken!\n🐤🐤🐤"]],
             [["scheiße", "kacke"], ["💩"]]]
        self.case_sensitive_options = [[[], []]]

    def regex_check(self):
        """
        Checks if the user input is valid for this plugin to continue
        :return: True if input is valid, False otherwise
        """
        matches = 0
        for option in self.case_sensitive_options:
            match = False
            for opt in option[0]:
                if opt in self.cap_message:
                    match = True
            if match:
                matches += 1
        for option in self.case_insensitive_options:
            match = False
            for opt in option[0]:
                if opt in self.message:
                    match = True
            if match:
                matches += 1
        if matches == 1:
            return True
        else:
            return False

    def parse_user_input(self):
        """
        Parses the user's input
        :return void
        """
        for option in self.case_sensitive_options:
            for opt in option[0]:
                if opt in self.cap_message:
                    self.response = Randomizer.get_random_element(option[1])
                    return
        for option in self.case_insensitive_options:
            for opt in option[0]:
                if opt in self.message:
                    self.response = Randomizer.get_random_element(option[1])
                    return

    def get_response(self):
        """
        Returns the response calculated by the plugin
        :return: the response as a MessageProtocolEntity
        """
        return TextMessageProtocolEntity(self.response, to=self.sender)

    @staticmethod
    def get_description(language):
        """
        Empty Description
        :param language: the language to be returned
        :return: the description as string
        """
        return ""
