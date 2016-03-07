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
try:
    from layers.BotLayer import BotLayer
    from plugins.PluginManager import PluginManager
    from plugins.PluginManagerGui import PluginManagerGUI
    from startup.config.PluginConfigParser import PluginConfigParser
except ImportError:
    from whatsbot.layers.BotLayer import BotLayer
    from whatsbot.plugins.PluginManager import PluginManager
    from whatsbot.plugins.PluginManagerGui import PluginManagerGUI
    from whatsbot.startup.config.PluginConfigParser import PluginConfigParser


class BotLayerWithGUI(BotLayer):
    """
    The BotLayerWithGUI class
    Class that implements a BotLayer with a GUI that can disable or enable certain plugins on startup
    """

    def plugin_manager_setup(self):
        """
        Sets up the plugin Manager via a GUI
        :return: void
        """
        if self.plugin_manager is None:
            self.plugin_manager = PluginManager(self)
            self.plugin_manager.set_plugins(PluginConfigParser().read_plugins())
            PluginManagerGUI(self.plugin_manager)
            if not self.parallel_running:
                print("Starting Parallel Threads")
                PluginManager(self).start_parallel_runs()
                self.parallel_running = True
