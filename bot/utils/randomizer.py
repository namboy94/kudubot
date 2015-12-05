import random

def getRandom(inputs):
    randomnumber = random.randint(0, len(inputs) - 1)
    return inputs[randomnumber]