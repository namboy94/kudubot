"""
Class that retrieves information from the KIT Mensa webpage
"""

from bs4 import BeautifulSoup
import requests

class Mensa(object):

    def __init__(self):
        print()

    def getTodaysPlan(self):

        """
        url = "http://www.studentenwerk-karlsruhe.de/de/essen/"
        html = requests.get(url).text
        soup = BeautifulSoup(html, "html.parser")
        res = soup.select('.mensatype')

        for r in res:
            print(r.text)
            print("END")

        """

        return "Curry Queen\nSchnitzel-Bar"