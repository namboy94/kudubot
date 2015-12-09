"""
Class that handles requests to the TV Database
@author Hermann Krumrey <hermann@krumreyh.com>
"""

import tvdb_api

"""
the TheTVDB class
"""
class TheTVDB(object):

    """
    Constructor
    @:param userInput - the user's input to establish the exact mode in which this module runs in.
    """
    def __init__(self, userInput):
        self.userInput = userInput
        self.parseUserInput()

    """
    Parses the user input
    """
    def parseUserInput(self):
        self.tvshow = self.userInput.split(" ", 1)[1].rsplit(" s", 1)[0]
        self.season = int(self.userInput.rsplit("s", 1)[1].rsplit(" e", 1)[0])
        self.episode = int(self.userInput.rsplit("e", 1)[1])

    """
    Fetches the episode name of a specific episode
    @:return the episode name
    """
    def getEpisodeName(self):

        try:
            tvdb = tvdb_api.Tvdb()
            episodeInfo = tvdb[self.tvshow][self.season][self.episode]
            episodeName = episodeInfo['episodename']
            return episodeName
        except Exception as e:
            if "cannot find show on TVDB" in str(e):
                return "Show not found"
            else:
                raise Exception("Unspecified Exception")