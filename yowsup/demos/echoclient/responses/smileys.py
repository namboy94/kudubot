# coding=utf-8

import random
from yowsup.demos.echoclient.utils.emojicode import *

def getRandom(inputs):
    randomnumber = random.randint(0, len(inputs) - 1)
    return inputs[randomnumber]

def happyTears(group):
    if group: options=[convertToBrokenUnicode("😂😂😂", 3)]
    else: options = ["😂😂😂"]
    print(options)
    return getRandom(options)

def middleFinger(group):
    if group: options = [convertToBrokenUnicode("😡", 1) + convertToBrokenUnicode("🖕🏻", 2)]
    else: options = ["😡🖕🏻"]
    return getRandom(options)

def kisses(group):
    if group: options = [convertToBrokenUnicode("😘", 1)]
    else: options = ["😘"]

    return getRandom(options)
