from threading import Thread

from yowsup.layers.protocol_messages.protocolentities import TextMessageProtocolEntity
from plugins.internetServicePlugins import Weather, Mensa, FootballScores, TheTVDB
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
        ### ADD NEW PLUGINS HERE ###

        if self.messageProtocolEntity.getBody().lower() in ["/help", "/hilfe"]:
            helpString = ""
            for plugin in plugins:
                if self.messageProtocolEntity.getBody().lower() == "/help":
                    helpString += plugin.getDescription("en")
                elif self.messageProtocolEntity.getBody().lower() == "/hilfe":
                    helpString += plugin.getDescription("de")
                helpString += "\n\n\n"
            return TextMessageProtocolEntity(helpString, to=self.messageProtocolEntity.getFrom())

        for plugin in plugins:
            if plugin.regexCheck():
                plugin.parseUserInput()
                return plugin.getResponse()

        """
        weather = Weather.Weather(self.layer, self.messageProtocolEntity)
        if weather.regexCheck():
            weather.parseUserInput()
            return weather.getResponse()

        theTVDB = TheTVDB.TheTVDB(self.layer, self.messageProtocolEntity)
        if theTVDB.regexCheck():
            theTVDB.parseUserInput()
            return theTVDB.getResponse()

        reminder = Reminder.Reminder(self.layer, self.messageProtocolEntity)
        if reminder.regexCheck():
            reminder.parseUserInput()
            return reminder.getResponse()

        mensa = Mensa.Mensa(self.layer, self.messageProtocolEntity)
        if mensa.regexCheck():
            mensa.parseUserInput()
            return mensa.getResponse()

        football = FootballScores.FootballScores(self.layer, self.messageProtocolEntity)
        if football.regexCheck():
            football.parseUserInput()
            return football.getResponse()
        """



        return False

    def startParallelRuns(self):

        threads = []

        threads.append(Thread(target=Weather.Weather(self.layer).parallelRun))
        threads.append(Thread(target=TheTVDB.TheTVDB(self.layer).parallelRun))
        threads.append(Thread(target=Reminder.Reminder(self.layer).parallelRun))
        threads.append(Thread(target=Mensa.Mensa(self.layer).parallelRun))

        ### ADD NEW PLUGINS HERE ###

        for thread in threads:
            thread.start()

        return threads