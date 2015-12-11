"""
Class that handles randomness
@author Hermann Krumrey <hermann@krumreyh.com>
"""

import random

"""
The Randomizer Class
"""
class Randomizer(object):

    """
    Returns a random element of a list
    @:return the random element
    """
    @staticmethod
    def getRandomElement(set):
        randNumber = random.randint(0, len(set) - 1)
        return set[randNumber]