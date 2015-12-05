"""
Class that provides Football (mostly Bundesliga) Information

@author Hermann Krumrey <hermann@krumreyh.com>
"""

from bs4 import BeautifulSoup
import requests

"""
FootballScores class
"""
class FootballScores(object):

    """
    Constructor (Does nothing)
    """
    def __init__(self):
        print()

    """
    Fetches data for the current Bundesliga match day and returns it
    """
    def getBundesligaScores(self):

        returnString = ""

        url = "http://www.livescore.com/soccer/germany/"
        html = requests.get(url).text
        soup = BeautifulSoup(html, "html.parser")
        res = soup.select('.row-gray')

        i = 0
        for r in res:
            if i < 9:
                returnString += r.text + "\n"
                i += 1

        return returnString

