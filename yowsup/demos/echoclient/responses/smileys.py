# coding=utf-8

import random

def getRandom(inputs):
    randomnumber = random.randint(0, len(inputs) - 1)
    return inputs[randomnumber]

def happyTears():
    options = ["ððð"]
    return getRandom(options)

def middleFinger():
    options = ["ð¡ðð»"]
    return getRandom(options)

def kisses():
    options = ["ð"]
    return getRandom(options)
