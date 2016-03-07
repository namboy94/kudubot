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


class PluginConfigParser(object):
    """
    The PluginConfigParser Class
    """

    def __init__(self):
        """
        Constructor
        :return void
        """
        self.configFile = os.getenv("HOME") + "/.whatsbot/config"

    def read_plugins(self):
        """
        Reads the plugins from the config file
        :return: a dictionary with the plugins as keys and True/False as parameters
        """
        plugin_dictionary = {}
        file = open(self.configFile, 'r')
        for line in file:
            plugin_name = line.rsplit("=", 1)[0]
            plugin_state = line.rsplit("=", 1)[1]
            if "1" in plugin_state:
                plugin_dictionary[plugin_name] = True
            else:
                plugin_dictionary[plugin_name] = False
        file.close()
        return plugin_dictionary

    def write_plugins(self, plugin_dictionary):
        """
        Writes the plugins to the config file
        :param plugin_dictionary: the plugin dictionary to write
        :return: void
        """
        file = open(self.configFile, "w")
        for name in plugin_dictionary:
            state = "0"
            if plugin_dictionary[name]:
                state = "1"
            file.write(name + "=" + state + "\n")
        file.close()
