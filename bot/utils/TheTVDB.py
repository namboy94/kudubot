import tvdb_api

class TheTVDB(object):

    def __init__(self, userInput):
        self.userInput = userInput
        self.parseUserInput()

    def parseUserInput(self):
        self.tvshow = self.userInput.split(" ", 1)[1].rsplit(" s", 1)[0]
        self.season = int(self.userInput.rsplit("s", 1)[1].rsplit(" e", 1)[0])
        self.episode = int(self.userInput.rsplit("e", 1)[1])

    def getEpisodeName(self):

        tvdb = tvdb_api.Tvdb()
        episodeInfo = tvdb[self.tvshow][self.season][self.episode]
        episodeName = episodeInfo['episodename']

        return episodeName