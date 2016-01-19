# coding=utf-8

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