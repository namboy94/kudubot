from bs4 import BeautifulSoup
import requests

class KinoZKM(object):

    def __init__(self, userInput):
        self.userInput = userInput
        self.currentMovies = []

    def __parseUserInput(self):
        splitInput = self.userInput.split("/kinozkm ")[1]

    def getAllCurrent(self):
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
            if i > len(movieTitles): break

            movieDetails = []
            title = allMovieTitles[i * 2].text
            times = allMovies[i].text.split("Spielzeiten")[1]

            print(title)
            print(times)

            i += 1

