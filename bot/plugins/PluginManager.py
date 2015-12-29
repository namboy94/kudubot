"""
Class that manages the plugins. Acts as facade to the Yowsup layer
@:author Hermann Krumrey
"""

from threading import Thread
from yowsup.layers.protocol_messages.protocolentities import TextMessageProtocolEntity
from plugins.internetServicePlugins.Weather import Weather
from plugins.internetServicePlugins.Mensa import Mensa
from plugins.internetServicePlugins.FootballScores import FootballScores
from plugins.internetServicePlugins.TheTVDB import TheTVDB
from plugins.internetServicePlugins.KVV import KVV
from plugins.internetServicePlugins.KinoZKM import KinoZKM
from plugins.internetServicePlugins.KickTipp import KickTipp
from plugins.internetServicePlugins.XKCD import XKCD
from plugins.internetServicePlugins.ImageSender import ImageSender
from plugins.localServicePlugins.Reminder import Reminder
from plugins.localServicePlugins.Terminal import Terminal
from plugins.simpleTextResponses.SimpleContainsResponse import SimpleContainsResponse
from plugins.simpleTextResponses.SimpleEqualsResponse import SimpleEqualsResponse
from plugins.restrictedAccessplugins.Muter import Muter
from plugins.localServicePlugins.Roulette import Roulette

"""
The PluginManager class
"""
class PluginManager(object):

    """
    Constructor
    @:param layer - the overlying yowsup layer
    @:param messageProtocolEntity - the incoming MessageProtocolEntity
    """
    def __init__(self, layer):
        self.layer = layer
        self.plugins = {"Weather Plugin": True,
                        "TVDB Plugin": True,
                        "Reminder Plugin": True,
                        "Mensa Plugin": True,
                        "Football Scores Plugin": True,
                        "KVV Plugin": True,
                        "Simple Contains Plugin": True,
                        "Simple Equals Plugin": True,
                        "Muter Plugin": True,
                        "KinoZKM Plugin": True,
                        "Terminal Plugin": True,
                        "Kicktipp Plugin": True,
                        "XKCD Plugin": True,
                        "ImageSender Plugin": True,
                        "Roulette Plugin": True}
        ### ADD NEW PLUGINS HERE ###

    """
    Runs all plugins
    """
    def runPlugins(self, messageProtocolEntity):

        if messageProtocolEntity is None: raise Exception("Wrong initialization")

        plugins = []
        if self.plugins["Weather Plugin"]: plugins.append(Weather(self.layer, messageProtocolEntity))
        if self.plugins["TVDB Plugin"]: plugins.append(TheTVDB(self.layer, messageProtocolEntity))
        if self.plugins["Reminder Plugin"]: plugins.append(Reminder(self.layer, messageProtocolEntity))
        if self.plugins["Mensa Plugin"]: plugins.append(Mensa(self.layer, messageProtocolEntity))
        if self.plugins["Football Scores Plugin"]: plugins.append(FootballScores(self.layer, messageProtocolEntity))
        if self.plugins["KVV Plugin"]: plugins.append(KVV(self.layer, messageProtocolEntity))
        if self.plugins["Simple Contains Plugin"]: plugins.append(SimpleContainsResponse(self.layer, messageProtocolEntity))
        if self.plugins["Simple Equals Plugin"]: plugins.append(SimpleEqualsResponse(self.layer, messageProtocolEntity))
        if self.plugins["Muter Plugin"]: plugins.append(Muter(self.layer, messageProtocolEntity))
        if self.plugins["KinoZKM Plugin"]: plugins.append(KinoZKM(self.layer, messageProtocolEntity))
        if self.plugins["Terminal Plugin"]: plugins.append(Terminal(self.layer, messageProtocolEntity))
        if self.plugins["Kicktipp Plugin"]: plugins.append(KickTipp(self.layer, messageProtocolEntity))
        if self.plugins["XKCD Plugin"]: plugins.append(XKCD(self.layer, messageProtocolEntity))
        if self.plugins["ImageSender Plugin"]: plugins.append(ImageSender(self.layer, messageProtocolEntity))
        if self.plugins["Roulette Plugin"]: plugins.append(Roulette(self.layer, messageProtocolEntity))

        ### ADD NEW PLUGINS HERE ###

        if messageProtocolEntity.getBody().lower() in ["/help", "/hilfe"]:
            helpString = "/help\tDisplays this help message"
            for plugin in plugins:
                if not plugin.getDescription("en") == "":
                    helpString += "\n\n\n"
                if messageProtocolEntity.getBody().lower() == "/help":
                    helpString += plugin.getDescription("en")
                elif messageProtocolEntity.getBody().lower() == "/hilfe":
                    helpString += plugin.getDescription("de")
            return TextMessageProtocolEntity(helpString, to=messageProtocolEntity.getFrom())

        for plugin in plugins:
            if plugin.regexCheck():
                plugin.parseUserInput()
                return plugin.getResponse()

        return False

    """
    Starts all parallel threads needed by the plugins.
    Intended to only be used once.
    """
    def startParallelRuns(self):

        threads = []

        threads.append(Thread(target=Reminder(self.layer).parallelRun))
        threads.append(Thread(target=Roulette(self.layer).parallelRun))
        ### ADD NEW PLUGINS REQUIRING A PARALLEL THREAD HERE ###

        for thread in threads:
            thread.setDaemon(True)
            thread.start()

        return threads

    """
    @:return a dictionary of the current plugin configuration
    """
    def getPlugins(self):
        return self.plugins

    """
    Sets a new status of the plugins
    @:param the new plugin states as a dictionary
    """
    def setPlugins(self, pluginDictionary):
        self.plugins = pluginDictionary