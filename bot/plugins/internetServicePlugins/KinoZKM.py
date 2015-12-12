"""
Plugin that fetches Information about current movies at the Cinema by the ZKM in Karlsruhe
@author Hermann Krumrey <hermann@krumreyh.com>
"""

import re
import requests
from bs4 import BeautifulSoup
from yowsup.layers.protocol_messages.protocolentities import TextMessageProtocolEntity
from plugins.GenericPlugin import GenericPlugin
from utils.encoding.Unicoder import Unicoder

"""
The KinoZKM Class
"""
class KinoZKM(GenericPlugin):

    """
    Constructor
    Defines parameters for the plugin.
    @:param layer - the overlying yowsup layer
    @:param messageProtocolEntity - the received message information
    @:override
    """
    def __init__(self, layer, messageProtocolEntity=None):
        if messageProtocolEntity is None: self.layer = layer; return
        self.layer = layer
        self.entity = messageProtocolEntity
        self.message = self.entity.getBody().lower()
        self.sender = self.entity.getFrom()

        self.mode = ""

    """
    Checks if the user input is valid for this plugin to continue
    @:return True if input is valid, False otherwise
    @:override
    """
    def regexCheck(self):
        if re.search(r"/kinozkm summaries", self.message):
            return True
        else: return False

    """
    Parses the user's input
    @:override
    """
    def parseUserInput(self):
        if self.message == "/kinozkm summaries": self.mode="summary"

    """
    Returns the response calculated by the plugin
    @:return the response as a MessageProtocolEntity
    @:override
    """
    def getResponse(self):
        if self.mode == "summary":
            return TextMessageProtocolEntity(self.__getAllSummaries__(), to=self.sender)
        raise NotImplementedError()

    """
    Returns a helpful description of the plugin's syntax and functionality
    @:param language - the language to be returned
    @:return the description as string
    @:override
    """
    @staticmethod
    def getDescription(language):
        if language == "en":
            return ""
        elif language == "de":
            return ""
        else:
            return "Help not available in this language"

    ### Local Methods ###

    """
    def __getTimes__(self):
        html = requests.get("http://www.filmpalast.net/programm.html").text
        soup = BeautifulSoup(html, "html.parser")
        allMovies = soup.select('.row')
        allMovieTitles = soup.select('.gwfilmdb-film-title')
        movieTitles = []

        for title in allMovieTitles:
            movieTitles.append(title.text)

        i = 0
        for movies in allMovies:
            if i == 0: i += 1; continue
            if i >= len(movieTitles): break

            movieDetails = []
            title = allMovieTitles[i * 2 - 1].text
            times = allMovies[i].text.split("Spielzeiten")[1]

            print(title)
            print(times)

            i += 1
        return ""
    """
    """

    def __getSummaries__(self):
        html = requests.get("http://www.filmpalast.net/programm.html").text
        soup = BeautifulSoup(html, "html.parser")
        allMovies = soup.select('.row')
        allMovieTitles = soup.select('.gwfilmdb-film-title')
        movieTitles = []

        for title in allMovieTitles:
            movieTitles.append(title.text)

        i = 0
        for movies in allMovies:
            if i == 0: i += 1; continue
            if (i * 2 - 1) >= len(movieTitles): break

            movieDetails = []
            title = allMovieTitles[i * 2 - 1].text
            times = allMovies[i].text.split("Spielzeiten       ")[1]
            #print(title)
            print(times)

            i += 1
        return ""

    """

    def __getAllSummaries__(self):

        html = requests.get("http://www.filmpalast.net/programm.html").text
        soup = BeautifulSoup(html, "html.parser")
        allMovieDescriptions = soup.select('.gwfilmdb-film-description')
        allMovieTitles = soup.select('.gwfilmdb-film-title')

        movieTitles = []

        skip = False
        for title in allMovieTitles:
            if not skip:
                movieTitles.append(title)
                skip = True
            else:
                skip = False

        allDescriptions = "Zusammenfassungen Aktuelle Filme:\n\n"

        i = 0
        while i < len(movieTitles):
            allDescriptions += movieTitles[i].text + "\n"
            allDescriptions += allMovieDescriptions[i].text + "\n\n"
            i += 1

        return allDescriptions