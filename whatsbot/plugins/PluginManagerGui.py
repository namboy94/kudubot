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
from startup.config.PluginConfigParser import PluginConfigParser
import sys
if sys.version_info[0] == 2:
    from Tkinter import *
else:
    from tkinter import *


class PluginManagerGUI(object):
    """
    The PluginManagerGUI class
    A GUI for the Plugin Manager
    """

    def __init__(self, plugin_manager):
        """
        Constructor that starts the GUI
        :param plugin_manager: The plugin manager linked to this GUI
        :return: void
        """
        self.plugin_manager = plugin_manager
        self.plugin_dictionary = plugin_manager.getPlugins()
        self.gui = Tk()

        self.buttons = {}

        for key in self.plugin_dictionary:
            color = "red"
            if self.plugin_dictionary[key]:
                color = "green"
            button = Button(self.gui, text=key, background=color,
                            command=lambda lambda_key=key: self.__toggleValue__(lambda_key))
            self.buttons[key] = button
            button.pack(fill=X)

        Button(self.gui, text="Confirm", command=self.gui.destroy).pack()

        self.gui.mainloop()
        PluginConfigParser().write_plugins(self.plugin_dictionary)
        self.plugin_manager.setPlugins(self.plugin_dictionary)

    def __toggleValue__(self, key):
        """
        Toggles the value of a button
        :param key: the key name of the plugin to toggle
        :return: void
        """

        if self.plugin_dictionary[key]:
            self.plugin_dictionary[key] = False
            self.buttons[key].config(background='red')
        else:
            self.plugin_dictionary[key] = True
            self.buttons[key].config(background='green')
