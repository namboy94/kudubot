# coding=utf-8

import random
from yowsup.demos.echoclient.utils.emojicode import *

def getRandom(inputs):
    randomnumber = random.randint(0, len(inputs) - 1)
    return inputs[randomnumber]

def happyTears():
    options = ["😂😂😂"]
    return getRandom(options)

def middleFinger():
    options = ["😡🖕🏻"]
    return getRandom(options)

def kisses():
    options = ["😘"]
    return getRandom(options)
