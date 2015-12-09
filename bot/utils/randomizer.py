"""
Hermann Krumrey <hermann@krumreyh.com>
"""

import random

"""
Returns a random element of a list
@:return the random element
"""
def getRandom(inputs):
    randomnumber = random.randint(0, len(inputs) - 1)
    return inputs[randomnumber]