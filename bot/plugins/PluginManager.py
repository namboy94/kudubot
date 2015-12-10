from plugins import Weather
import re

"""
"""
class PluginManager(object):

    def __init__(self, layer, messageProtocolEntity):
        self.layer = layer
        self.messageProtocolEntity = messageProtocolEntity

    def runPlugins(self):

        message = self.messageProtocolEntity.getBody()
        minMessage = message.lower()
        response = False

        if re.search(Weather.Weather.getRegex(), minMessage):
            weather = Weather.Weather(self.layer, self.messageProtocolEntity)
            weather.parseUserInput()
            response = weather.getResponse()

        elif True:
            print("TODO")

    def startParallelRuns(self):

        print("TODO")