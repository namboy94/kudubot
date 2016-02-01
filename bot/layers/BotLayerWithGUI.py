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

"""
Class that implements a BotLayer with a GUI that can disable certain plugins on startup
@author Hermann Krumrey<hermann@krumreyh.com>
"""

from layers.BotLayer import BotLayer
from plugins.PluginManager import PluginManager
from plugins.PluginManagerGui import PluginManagerGUI
from startup.config.PluginConfigParser import PluginConfigParser

"""
The BotLayerWithGUI class
"""
class BotLayerWithGUI(BotLayer):

    def pluginManagerSetup(self):
        if self.pluginManager is None:
            self.pluginManager = PluginManager(self)
            self.pluginManager.setPlugins(PluginConfigParser().readPlugins())
            PluginManagerGUI(self.pluginManager)
            if not self.parallelRunning:
                print("Starting Parallel Threads")
                PluginManager(self).startParallelRuns()
                self.parallelRunning = True