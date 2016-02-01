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
A GUI for the Plugin Manager
@author Hermann Krumrey<hermann@krumreyh.com>
"""
import sys
if sys.version_info[0] == 2:
    from Tkinter import *
else:
    from tkinter import *
from startup.config.PluginConfigParser import PluginConfigParser

"""
The PluginManagerGUI class
"""
class PluginManagerGUI(object):

    """
    Constructor that starts the GUI
    """
    def __init__(self, pluginManager):

        self.pluginManager = pluginManager
        self.pluginDictionary = pluginManager.getPlugins()
        self.gui = Tk()

        self.buttons = {}

        for key in self.pluginDictionary:
            color = "red"
            if self.pluginDictionary[key]: color = "green"
            button = Button(self.gui, text=key, background=color, command=lambda key=key:self.__toggleValue__(key))
            self.buttons[key] = button
            button.pack(fill=X)

        Button(self.gui, text="Confirm", command=self.gui.destroy).pack()

        self.gui.mainloop()
        PluginConfigParser().writePlugins(self.pluginDictionary)
        self.pluginManager.setPlugins(self.pluginDictionary)

    """
    Toggles the value of a button
    """
    def __toggleValue__(self, key):

        if self.pluginDictionary[key]:
            self.pluginDictionary[key] = False
            self.buttons[key].config(background='red')
        else:
            self.pluginDictionary[key] = True
            self.buttons[key].config(background='green')