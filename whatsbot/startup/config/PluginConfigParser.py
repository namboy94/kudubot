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
        self.global_config = os.getenv("HOME") + "/.whatsbot/config"
        self.plugin_config_dir = os.getenv("HOME") + "/.whatsbot/plugins"

    def read_plugins(self, group=None):
        """
        Reads the plugins from the config file
        :param group: the group for which to check the active plugins
        :return: a dictionary with the plugins as keys and True/False as parameters
        """
        if group is None:
            file = open(self.global_config, 'r')
        else:
            groupfile = self.plugin_config_dir + "/" + group
            if not os.path.isfile(groupfile):
                self.write_plugins(self.read_plugins(), group)
            file = open(groupfile, 'r')
        plugin_dictionary = {}
        for line in file:
            plugin_name = line.rsplit("=", 1)[0]
            plugin_state = line.rsplit("=", 1)[1]
            if "1" in plugin_state:
                plugin_dictionary[plugin_name] = True
            else:
                plugin_dictionary[plugin_name] = False
        file.close()
        return plugin_dictionary

    def write_plugins(self, plugin_dictionary, group=None):
        """
        Writes the plugins to the config file
        :param plugin_dictionary: the plugin dictionary to write
        :param group: the group for which the plugins should be set
        :return: void
        """
        if group is None:
            file = open(self.global_config, "w")
        else:
            file = open(self.plugin_config_dir + "/" + group, 'w')
        for name in plugin_dictionary:
            state = "0"
            if plugin_dictionary[name]:
                state = "1"
            file.write(name + "=" + state + "\n")
        file.close()

    def read_all_plugin_configs(self, expected_plugins):
        """
        Reads all plugin config files and returns it as a dictionary of dictionaries
        :param expected_plugins: A list of plugins that absolutely need to be in the config files
        :return: all plugin information
        """
        # Read
        plugin_dict = {}
        for file in os.listdir(self.plugin_config_dir):
            plugin_dict[file] = self.read_plugins(file)
        plugin_dict["global"] = self.read_plugins()

        # Check if all excpected plugins are there
        for config in plugin_dict:
            needs_to_write = False
            for plugin in expected_plugins:
                try:
                    plugin_dict[config][plugin]
                except KeyError:
                    needs_to_write = True
                    plugin_dict[config][plugin] = True
            if needs_to_write:
                if config != "global":
                    self.write_plugins(plugin_dict[config], config)
                else:
                    self.write_plugins(plugin_dict["global"])

        return plugin_dict
