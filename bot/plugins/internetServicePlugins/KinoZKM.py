# coding=utf-8
"""
Copyright 2015,2016 Hermann Krumrey

This file is part of whatsapp-bot.

    whatsapp-bot makes use of various third-party python modules to serve
    information via the online chat service Whatsapp.

    whatsapp-bot is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    whatsapp-bot is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with whatsapp-bot.  If not, see <http://www.gnu.org/licenses/>.
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
        if re.search(r"^/kinozkm summaries$", self.message):
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
            return "/kinozkm\tFetches current information regarding the cinema at the ZKM in Karlsruhe\n" \
                   "syntax: /kinozkm [summaries]"
        elif language == "de":
            return "/kinozkm\tZeigt Aktuelle Kinoinformationen für das Kino am ZKM in Karlsruhe an\n" \
                   "syntax: /kinozkm [summaries]"
        else:
            return "Help not available in this language"

    ### Local Methods ###

    """
    Returns all currently running movies and movie descriptions.
    @:return the movie titles and descriptions as formatted string.
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