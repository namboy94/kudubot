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

from threading import Thread
from yowsup.layers.protocol_messages.protocolentities import TextMessageProtocolEntity
from plugins.internetServicePlugins.FootballScores import FootballScores
from plugins.internetServicePlugins.ImageSender import ImageSender
from plugins.internetServicePlugins.KVV import KVV
from plugins.internetServicePlugins.KickTipp import KickTipp
from plugins.internetServicePlugins.KinoZKM import KinoZKM
from plugins.internetServicePlugins.Mensa import Mensa
from plugins.internetServicePlugins.TheTVDB import TheTVDB
from plugins.internetServicePlugins.Weather import Weather
from plugins.internetServicePlugins.XKCD import XKCD
from plugins.localServicePlugins.Casino import Casino
from plugins.localServicePlugins.ContinuousReminder import ContinuousReminder
from plugins.localServicePlugins.Reminder import Reminder
from plugins.localServicePlugins.TextToSpeechConverter import TextToSpeechConverter
from plugins.localServicePlugins.Terminal import Terminal
from plugins.localServicePlugins.casino.Roulette import Roulette
from plugins.restrictedAccessplugins.Muter import Muter
from plugins.simpleTextResponses.SimpleContainsResponse import SimpleContainsResponse
from plugins.simpleTextResponses.SimpleEqualsResponse import SimpleEqualsResponse


class PluginManager(object):
    """
    The PluginManager class
    Handles plugin activity
    """

    """
    Constructor
    @:param layer - the overlying yowsup layer
    @:param messageProtocolEntity - the incoming MessageProtocolEntity
    """

    def __init__(self, layer):
        self.layer = layer
        self.plugins = {"Weather Plugin": True,
                        "TVDB Plugin": True,
                        "Reminder Plugin": True,
                        "Mensa Plugin": True,
                        "Football Scores Plugin": True,
                        "KVV Plugin": True,
                        "Simple Contains Plugin": True,
                        "Simple Equals Plugin": True,
                        "Muter Plugin": True,
                        "KinoZKM Plugin": True,
                        "Terminal Plugin": True,
                        "Kicktipp Plugin": True,
                        "XKCD Plugin": True,
                        "ImageSender Plugin": True,
                        "Casino Plugin": True,
                        "Continuous Reminder Plugin": True,
                        "Text To Speech Plugin": True,
                        "Roulette Plugin": True}
        # ADD NEW PLUGINS HERE

    """
    Runs all plugins
    """

    def run_plugins(self, message_protocol_entity):

        if message_protocol_entity is None:
            raise Exception("Wrong initialization")

        plugins = []
        if self.plugins["Weather Plugin"]:
            plugins.append(Weather(self.layer, message_protocol_entity))
        if self.plugins["TVDB Plugin"]:
            plugins.append(TheTVDB(self.layer, message_protocol_entity))
        if self.plugins["Reminder Plugin"]:
            plugins.append(Reminder(self.layer, message_protocol_entity))
        if self.plugins["Mensa Plugin"]:
            plugins.append(Mensa(self.layer, message_protocol_entity))
        if self.plugins["Football Scores Plugin"]:
            plugins.append(FootballScores(self.layer, message_protocol_entity))
        if self.plugins["KVV Plugin"]:
            plugins.append(KVV(self.layer, message_protocol_entity))
        if self.plugins["Simple Contains Plugin"]:
            plugins.append(SimpleContainsResponse(self.layer, message_protocol_entity))
        if self.plugins["Simple Equals Plugin"]:
            plugins.append(SimpleEqualsResponse(self.layer, message_protocol_entity))
        if self.plugins["Muter Plugin"]:
            plugins.append(Muter(self.layer, message_protocol_entity))
        if self.plugins["KinoZKM Plugin"]:
            plugins.append(KinoZKM(self.layer, message_protocol_entity))
        if self.plugins["Terminal Plugin"]:
            plugins.append(Terminal(self.layer, message_protocol_entity))
        if self.plugins["Kicktipp Plugin"]:
            plugins.append(KickTipp(self.layer, message_protocol_entity))
        if self.plugins["XKCD Plugin"]:
            plugins.append(XKCD(self.layer, message_protocol_entity))
        if self.plugins["ImageSender Plugin"]:
            plugins.append(ImageSender(self.layer, message_protocol_entity))
        if self.plugins["Casino Plugin"]:
            plugins.append(Casino(self.layer, message_protocol_entity))
        if self.plugins["Roulette Plugin"]:
            plugins.append(Roulette(self.layer, message_protocol_entity))
        if self.plugins["Continuous Reminder Plugin"]:
            plugins.append(ContinuousReminder(self.layer, message_protocol_entity))
        if self.plugins["Text To Speech Plugin"]:
            plugins.append(TextToSpeechConverter(self.layer, message_protocol_entity))
        # ADD NEW PLUGINS HERE

        if message_protocol_entity.getBody().lower() in ["/help", "/hilfe"]:
            help_string = "/help\tDisplays this help message"
            for plugin in plugins:
                if not plugin.getDescription("en") == "":
                    help_string += "\n\n\n"
                if message_protocol_entity.getBody().lower() == "/help":
                    help_string += plugin.getDescription("en")
                elif message_protocol_entity.getBody().lower() == "/hilfe":
                    help_string += plugin.getDescription("de")
            return TextMessageProtocolEntity(help_string, to=message_protocol_entity.getFrom())

        for plugin in plugins:
            if plugin.regexCheck():
                plugin.parseUserInput()
                return plugin.getResponse()

        return False

    """
    Starts all parallel threads needed by the plugins.
    Intended to only be used once.
    """

    def start_parallel_runs(self):

        threads = [Thread(target=Reminder(self.layer).parallelRun), Thread(target=Casino(self.layer).parallelRun),
                   Thread(target=Roulette(self.layer).parallelRun),
                   Thread(target=ContinuousReminder(self.layer).parallelRun)]
        # ADD NEW PLUGINS REQUIRING A PARALLEL THREAD HERE

        for thread in threads:
            thread.setDaemon(True)
            thread.start()

        return threads

    """
    @:return a dictionary of the current plugin configuration
    """

    def get_plugins(self):
        return self.plugins

    """
    Sets a new status of the plugins
    @:param the new plugin states as a dictionary
    """

    def set_plugins(self, plugin_dictionary):
        self.plugins = plugin_dictionary
