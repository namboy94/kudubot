import random

def getRandom(inputs):
    randomnumber = random.randint(0, len(inputs) - 1)
    return inputs[randomnumber]

def oops():
    options = ["Was hast du jetzt schon wieder kaputt gemacht?"]
    return getRandom(options)