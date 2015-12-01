# coding=utf-8

import random

def getRandom(inputs):
    randomnumber = random.randint(0, len(inputs) - 1)
    return inputs[randomnumber]

def ls():
    options = ["something\nsomething else\n...\nsome more stuff"]
    return getRandom(options)

def cat():
    options = ["You're a kitty!",
               "https://xkcd.com/231/",
               "https://xkcd.com/729/",
               "https://xkcd.com/26/"]
    return getRandom(options)

def man():
    options = ["Oh, I'm sure you can figure it out."]
    return getRandom(options)

def echo(input):
    if len(input) < 5: options = ["echo what?"]
    else: options = [input.split(" ")[1]]
    return getRandom(options)