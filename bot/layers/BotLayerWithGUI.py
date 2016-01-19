# coding=utf-8

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