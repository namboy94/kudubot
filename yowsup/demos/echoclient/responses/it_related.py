import random

def getRandom(inputs):
    randomnumber = random.randint(0, len(inputs) - 1)
    return inputs[randomnumber]

def wuerfel():
    options = ["Wuerfel sind toll",
               "Du hast eine " + str(random.randint(1,6)) + " gewuerfelt!",
               "https://play.google.com/store/apps/details?id=com.namibsun.android.dice"]
    return getRandom(options)