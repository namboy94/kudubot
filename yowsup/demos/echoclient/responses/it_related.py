# coding=utf-8

import random

def getRandom(inputs):
    randomnumber = random.randint(0, len(inputs) - 1)
    return inputs[randomnumber]

def wuerfel():
    options = ["Würfel sind toll",
               "Du hast eine " + str(random.randint(1,6)) + " gewürfelt!",
               "https://play.google.com/store/apps/details?id=com.namibsun.android.dice"]
    return getRandom(options)

def umlaute():
    options = ["Ä", "ä", "Ü", "ü", "Ö", "ö", "ß"]
    return getRandom(options)
