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
from plugins.localServicePlugins.Reminder import Reminder
from plugins.simpleTextResponses.SimpleContainsResponse import SimpleContainsResponse
from plugins.simpleTextResponses.SimpleEqualsResponse import SimpleEqualsResponse
from plugins.restrictedAccessplugins.Muter import Muter

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
                        "Muter": True,
                        "KinoZKM": True}
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
        if self.plugins["Muter"]: plugins.append(Muter(self.layer, messageProtocolEntity))
        if self.plugins["KinoZKM"]: plugins.append(KinoZKM(self.layer, messageProtocolEntity))
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
        ### ADD NEW PLUGINS REQUIRING A PARALLEL THREAD HERE ###

        for thread in threads:
            thread.start()

        return threads