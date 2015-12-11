"""
Class that manages the plugins. Acts as facade to the Yowsup layer
@:author Hermann Krumrey
"""

from threading import Thread
from yowsup.layers.protocol_messages.protocolentities import TextMessageProtocolEntity
from plugins.internetServicePlugins import Weather, Mensa, FootballScores, TheTVDB, KVV
from plugins.localServicePlugins import Reminder
from plugins.simpleTextResponses import SimpleContainsResponse

"""
The PluginManager class
"""
class PluginManager(object):

    """
    Constructor
    @:param layer - the overlying yowsup layer
    @:param messageProtocolEntity - the incoming MessageProtocolEntity
    """
    def __init__(self, layer, messageProtocolEntity=None):
        self.layer = layer
        self.messageProtocolEntity = messageProtocolEntity

    """
    Runs all plugins
    """
    def runPlugins(self):

        if self.messageProtocolEntity is None: raise Exception("Wrong initialization")

        plugins = []
        plugins.append(Weather.Weather(self.layer, self.messageProtocolEntity))
        plugins.append(TheTVDB.TheTVDB(self.layer, self.messageProtocolEntity))
        plugins.append(Reminder.Reminder(self.layer, self.messageProtocolEntity))
        plugins.append(Mensa.Mensa(self.layer, self.messageProtocolEntity))
        plugins.append(FootballScores.FootballScores(self.layer, self.messageProtocolEntity))
        plugins.append(KVV.KVV(self.layer, self.messageProtocolEntity))
        plugins.append(SimpleContainsResponse.SimpleContainsResponse(self.layer, self.messageProtocolEntity))
        ### ADD NEW PLUGINS HERE ###

        if self.messageProtocolEntity.getBody().lower() in ["/help", "/hilfe"]:
            helpString = "/help\tDisplays this help message"
            for plugin in plugins:
                if not plugin.getDescription("en") == "":
                    helpString += "\n\n\n"
                if self.messageProtocolEntity.getBody().lower() == "/help":
                    helpString += plugin.getDescription("en")
                elif self.messageProtocolEntity.getBody().lower() == "/hilfe":
                    helpString += plugin.getDescription("de")
            return TextMessageProtocolEntity(helpString, to=self.messageProtocolEntity.getFrom())

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

        threads.append(Thread(target=Reminder.Reminder(self.layer).parallelRun))
        ### ADD NEW PLUGINS REQUIRING A PARALLEL THREAD HERE ###

        for thread in threads:
            thread.start()

        return threads