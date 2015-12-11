from threading import Thread

from yowsup.layers.protocol_messages.protocolentities import TextMessageProtocolEntity
from plugins.internetServicePlugins import Weather, Mensa, FootballScores, TheTVDB, KVV
from plugins.localServicePlugins import Reminder

"""
"""
class PluginManager(object):

    def __init__(self, layer, messageProtocolEntity=None):
        self.layer = layer
        self.messageProtocolEntity = messageProtocolEntity

    def runPlugins(self):

        if self.messageProtocolEntity is None: raise Exception("Wrong initialization")

        plugins = []
        plugins.append(Weather.Weather(self.layer, self.messageProtocolEntity))
        plugins.append(TheTVDB.TheTVDB(self.layer, self.messageProtocolEntity))
        plugins.append(Reminder.Reminder(self.layer, self.messageProtocolEntity))
        plugins.append(Mensa.Mensa(self.layer, self.messageProtocolEntity))
        plugins.append(FootballScores.FootballScores(self.layer, self.messageProtocolEntity))
        plugins.append(KVV.KVV(self.layer, self.messageProtocolEntity))
        ### ADD NEW PLUGINS HERE ###

        if self.messageProtocolEntity.getBody().lower() in ["/help", "/hilfe"]:
            helpString = "/help\tDisplays this help message"
            for plugin in plugins:
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

    def startParallelRuns(self):

        threads = []

        threads.append(Thread(target=Reminder.Reminder(self.layer).parallelRun))
        ### ADD NEW PLUGINS REQUIRING A PARALLEL THREAD HERE ###

        for thread in threads:
            thread.start()

        return threads