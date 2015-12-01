# coding=utf-8

import random

def getRandom(inputs):
    randomnumber = random.randint(0, len(inputs) - 1)
    return inputs[randomnumber]

def wuerfel():
    options = ["WÃ¼rfel sind toll",
               "Du hast eine " + str(random.randint(1,6)) + " gewÃ¼rfelt!",
               "https://play.google.com/store/apps/details?id=com.namibsun.android.dice"]
    return getRandom(options)

def umlaute():
    options = ["Ã", "Ã¤", "Ã", "Ã¼", "Ã", "Ã¶", "Ã"]
    return getRandom(options)