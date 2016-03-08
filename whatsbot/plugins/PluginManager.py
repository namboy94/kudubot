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

# imports
from threading import Thread

try:
    from plugins.internetServicePlugins.FootballScores import FootballScores
    from plugins.internetServicePlugins.ImageSender import ImageSender
    from plugins.internetServicePlugins.KVV import KVV
    from plugins.internetServicePlugins.KickTipp import KickTipp
    from plugins.internetServicePlugins.KinoZKM import KinoZKM
    from plugins.internetServicePlugins.Mensa import Mensa
    from plugins.internetServicePlugins.TheTVDB import TheTVDB
    from plugins.internetServicePlugins.Weather import Weather
    from plugins.internetServicePlugins.XKCD import XKCD
    from plugins.internetServicePlugins.EmailSender import EmailSender
    from plugins.localServicePlugins.Casino import Casino
    from plugins.localServicePlugins.ContinuousReminder import ContinuousReminder
    from plugins.localServicePlugins.Reminder import Reminder
    from plugins.localServicePlugins.TextToSpeechConverter import TextToSpeechConverter
    from plugins.localServicePlugins.Terminal import Terminal
    from plugins.localServicePlugins.casino.Roulette import Roulette
    from plugins.restrictedAccessPlugins.Muter import Muter
    from plugins.restrictedAccessPlugins.PluginSelector import PluginSelector
    from plugins.simpleTextResponses.SimpleContainsResponse import SimpleContainsResponse
    from plugins.simpleTextResponses.SimpleEqualsResponse import SimpleEqualsResponse
    from plugins.localServicePlugins.Help import Help
    from yowsupwrapper.entities.WrappedTextMessageProtocolEntity import WrappedTextMessageProtocolEntity
    from startup.config.PluginConfigParser import PluginConfigParser
except ImportError:
    from whatsbot.plugins.internetServicePlugins.FootballScores import FootballScores
    from whatsbot.plugins.internetServicePlugins.ImageSender import ImageSender
    from whatsbot.plugins.internetServicePlugins.KVV import KVV
    from whatsbot.plugins.internetServicePlugins.KickTipp import KickTipp
    from whatsbot.plugins.internetServicePlugins.KinoZKM import KinoZKM
    from whatsbot.plugins.internetServicePlugins.Mensa import Mensa
    from whatsbot.plugins.internetServicePlugins.TheTVDB import TheTVDB
    from whatsbot.plugins.internetServicePlugins.Weather import Weather
    from whatsbot.plugins.internetServicePlugins.XKCD import XKCD
    from whatsbot.plugins.internetServicePlugins.EmailSender import EmailSender
    from whatsbot.plugins.localServicePlugins.Casino import Casino
    from whatsbot.plugins.localServicePlugins.ContinuousReminder import ContinuousReminder
    from whatsbot.plugins.localServicePlugins.Reminder import Reminder
    from whatsbot.plugins.localServicePlugins.TextToSpeechConverter import TextToSpeechConverter
    from whatsbot.plugins.localServicePlugins.Terminal import Terminal
    from whatsbot.plugins.localServicePlugins.casino.Roulette import Roulette
    from whatsbot.plugins.restrictedAccessPlugins.Muter import Muter
    from whatsbot.plugins.restrictedAccessPlugins.PluginSelector import PluginSelector
    from whatsbot.plugins.simpleTextResponses.SimpleContainsResponse import SimpleContainsResponse
    from whatsbot.plugins.simpleTextResponses.SimpleEqualsResponse import SimpleEqualsResponse
    from whatsbot.plugins.localServicePlugins.Help import Help
    from whatsbot.yowsupwrapper.entities.WrappedTextMessageProtocolEntity import WrappedTextMessageProtocolEntity
    from whatsbot.startup.config.PluginConfigParser import PluginConfigParser


class PluginManager(object):
    """
    The PluginManager class
    Handles plugin activity
    """

    def __init__(self, layer):
        """
        Constructor
        :param: layer - the overlying yowsup layer
        :return: void
        """
        self.layer = layer
        expected_plugins = [Weather.get_plugin_name(),
                            TheTVDB.get_plugin_name(),
                            Reminder.get_plugin_name(),
                            Mensa.get_plugin_name(),
                            FootballScores.get_plugin_name(),
                            KVV.get_plugin_name(),
                            SimpleContainsResponse.get_plugin_name(),
                            SimpleEqualsResponse.get_plugin_name(),
                            Muter.get_plugin_name(),
                            KinoZKM.get_plugin_name(),
                            Terminal.get_plugin_name(),
                            KickTipp.get_plugin_name(),
                            XKCD.get_plugin_name(),
                            ImageSender.get_plugin_name(),
                            Casino.get_plugin_name(),
                            ContinuousReminder.get_plugin_name(),
                            TextToSpeechConverter.get_plugin_name(),
                            Roulette.get_plugin_name(),
                            PluginSelector.get_plugin_name(),
                            EmailSender.get_plugin_name()]
        # ADD NEW PLUGINS HERE
        self.plugins = PluginConfigParser().read_all_plugin_configs(expected_plugins)

    def run_plugins(self, message_protocol_entity):
        """
        Checks all plugins for a specified input
        :param message_protocol_entity: the incoming message protocol entity
        :return: void
        """
        if message_protocol_entity is None:
            raise Exception("Wrong initialization")

        sender = message_protocol_entity.get_from(False)
        try:
            plugin_dict = self.plugins[sender]
        except KeyError:
            plugin_dict = self.plugins["global"]

        plugins = []
        if plugin_dict["Weather Plugin"]:
            plugins.append(Weather(self.layer, message_protocol_entity))
        if plugin_dict["TVDB Plugin"]:
            plugins.append(TheTVDB(self.layer, message_protocol_entity))
        if plugin_dict["Reminder Plugin"]:
            plugins.append(Reminder(self.layer, message_protocol_entity))
        if plugin_dict["Mensa Plugin"]:
            plugins.append(Mensa(self.layer, message_protocol_entity))
        if plugin_dict["Football Scores Plugin"]:
            plugins.append(FootballScores(self.layer, message_protocol_entity))
        if plugin_dict["KVV Plugin"]:
            plugins.append(KVV(self.layer, message_protocol_entity))
        if plugin_dict["Simple Contains Plugin"]:
            plugins.append(SimpleContainsResponse(self.layer, message_protocol_entity))
        if plugin_dict["Simple Equals Plugin"]:
            plugins.append(SimpleEqualsResponse(self.layer, message_protocol_entity))
        if plugin_dict["Muter Plugin"]:
            plugins.append(Muter(self.layer, message_protocol_entity))
        if plugin_dict["Plugin Selector Plugin"]:
            plugins.append(PluginSelector(self.layer, message_protocol_entity))
        if plugin_dict["KinoZKM Plugin"]:
            plugins.append(KinoZKM(self.layer, message_protocol_entity))
        if plugin_dict["Terminal Plugin"]:
            plugins.append(Terminal(self.layer, message_protocol_entity))
        if plugin_dict["Kicktipp Plugin"]:
            plugins.append(KickTipp(self.layer, message_protocol_entity))
        if plugin_dict["XKCD Plugin"]:
            plugins.append(XKCD(self.layer, message_protocol_entity))
        if plugin_dict["ImageSender Plugin"]:
            plugins.append(ImageSender(self.layer, message_protocol_entity))
        if plugin_dict["Casino Plugin"]:
            plugins.append(Casino(self.layer, message_protocol_entity))
        if plugin_dict["Roulette Plugin"]:
            plugins.append(Roulette(self.layer, message_protocol_entity))
        if plugin_dict["Continuous Reminder Plugin"]:
            plugins.append(ContinuousReminder(self.layer, message_protocol_entity))
        if plugin_dict["Text To Speech Plugin"]:
            plugins.append(TextToSpeechConverter(self.layer, message_protocol_entity))
        if plugin_dict["Email Sender Plugin"]:
            plugins.append(EmailSender(self.layer, message_protocol_entity))
        # ADD NEW PLUGINS HERE

        help_plugin = Help(self.layer, plugins, message_protocol_entity)
        if help_plugin.regex_check():
            help_plugin.parse_user_input()
            return help_plugin.get_response()

        for plugin in plugins:
            if plugin.regex_check():
                plugin.parse_user_input()
                return plugin.get_response()

        return False

    def start_parallel_runs(self):
        """
        Starts all parallel threads needed by the plugins.
        Intended to only be used once.
        :return: void
        """

        threads = [Thread(target=Reminder(self.layer).parallel_run), Thread(target=Casino(self.layer).parallel_run),
                   Thread(target=Roulette(self.layer).parallel_run),
                   Thread(target=ContinuousReminder(self.layer).parallel_run)]
        # ADD NEW PLUGINS REQUIRING A PARALLEL THREAD HERE

        for thread in threads:
            thread.setDaemon(True)
            thread.start()

        return threads

    def get_plugins(self):
        """
        Getter method to get the active plugins as a dictionary
        :return: a dictionary of the current plugin configuration
        """
        return self.plugins

    def set_plugins(self, plugin_dictionary):
        """
        Sets a new status of the plugins
        :param plugin_dictionary: the new plugin states as a dictionary
        :return: void
        """
        self.plugins = plugin_dictionary

    def set_plugin_state(self, sender, plugin, state):
        """
        Activates a plugin
        :param sender: the group/user for which to activate the plugin
        :param plugin: the plugin to be activated
        :param state: The state in which the plugin should be put
        :return: True, if all went well, False if plugin could not be found
        """
        try:
            plugin_dict = self.plugins[sender]
        except KeyError:
            self.plugins[sender] = self.plugins["global"]
            plugin_dict = self.plugins[sender]

        try:
            str(plugin_dict[plugin])
            plugin_dict[plugin] = state
            PluginConfigParser().write_plugins(plugin_dict, sender)
            return True
        except KeyError:
            return False
