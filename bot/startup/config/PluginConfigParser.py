"""
Configparse that determines which plugins to run
@author Hermann Krumrey <hermann@krumreyh.com>
"""
import os

"""
The PluginConfigParser Class
"""
class PluginConfigParser(object):

    """
    Constructor
    """
    def __init__(self):
        self.configFile = os.getenv("HOME") + "/.whatsapp-bot/plugins"

    def readPlugins(self):
        pluginDictionary = {}
        file = open(self.configFile, 'r')
        for line in file:
            pluginName = line.rsplit("=", 1)[0]
            pluginState = line.rsplit("=", 1)[1]
            if "1" in pluginState:
                pluginDictionary[pluginName] = True
            else:
                pluginDictionary[pluginName] = False
        file.close()
        return pluginDictionary

    def writePlugins(self, pluginDictionary):
        file = open(self.configFile, "w")
        for name in pluginDictionary:
            state = "0"
            if pluginDictionary[name]: state = "1"
            file.write(name + "=" + state + "\n")
        file.close()