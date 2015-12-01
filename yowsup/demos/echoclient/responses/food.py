# coding=utf-8

import random

def getRandom(inputs):
    randomnumber = random.randint(0, len(inputs) - 1)
    return inputs[randomnumber]

def kekse():
    options = ["Ich will auch Kekse!",
               "Wo gibt's Kekse?",
               "Kekse sind klasse!",
               "Ich hab einen Gutschein fÃ¼r McDonald's Kekse!"]
    return getRandom(options)

def kuchen():
    options = ["Ich mag Kuchen",
               "Marmorkuchen!",
               "Kuchen gibt's bei Starbucks"]
    return getRandom(options)