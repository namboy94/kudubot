# coding=utf-8
import re
import os
import time
from yowsup.demos.echoclient.responses.food import *
from yowsup.demos.echoclient.responses.it_related import *
from yowsup.demos.echoclient.responses.smileys import *
from yowsup.demos.echoclient.responses.pseudocommands import *
from yowsup.demos.echoclient.responses.phrases import *
from yowsup.demos.echoclient.responses.weather import *
from yowsup.demos.echoclient.responses.publicterm import *
from yowsup.demos.echoclient.utils.emojicode import *
from yowsup.demos.echoclient.utils.logwriter import *

def decide(sender, senderNumber, senderName, message, minMessage, participant, participantName):

    decision = ["", sender, ""]

    # Instant text replies
    #weather
    if re.compile("(weather|wetter)((:){1}(;text|;verbose)*)?( [^ :;]*)?").match(minMessage):
        decision[0] = weather(minMessage).getWeather()

    #food
    if "keks" in minMessage or "cookie" in minMessage: decision[0] = kekse()
    elif "kuchen" in minMessage: decision[0] = kuchen()
    elif "uups" in minMessage or "ups" in minMessage or "oops" in minMessage: decision[0] = oops()

    #it_related
    elif "würfel" in minMessage or "wuerfel" in minMessage: decision[0] = wuerfel()
    elif "umlaut" in minMessage: decision[0] = umlaute()

    #smileys
    elif "😂" in minMessage: decision[0] = happyTears()
    elif "🖕🏻" in minMessage: decision[0] = middleFinger()
    elif "liebe" in minMessage and "bot" in minMessage: decision[0] = kisses()
    elif "beste bot" in minMessage or "bester bot" in minMessage: decision[0] = kisses()

    #pseudocommands
    elif minMessage.startswith("ls"): decision[0] = ls()
    elif minMessage.startswith("man"): decision[0] = man()
    elif minMessage.startswith("cat"): decision[0] = cat()
    elif minMessage.startswith("echo"): decision[0] = echo(minMessage)
    elif minMessage == "uptime": decision[0] = uptime()

    #public terminal
    elif minMessage.startswith("term:ls "): decision[2] = publicLs(sentmessage)
    elif minMessage == "term:uptime": decision[2] = "uptime"


    #Restricted Terminal
    elif senderName == "Hermann" or participantName == "Hermann":
        #Special Text commands
        if minMessage in ["die", "stirb", "killbot"]: decision[0] = "😨🔫"


    #Print to console and log
    writeLogAndPrint("recv", senderName, message)
    if decision[0]:
        writeLogAndPrint("sent", senderName, decision[0])
    elif decision[2]:
        writeLogAndPrint("cmnd", senderName, decision[2])

    return decision

def sizeChecker(string):
    if len(string) > 500: return "Message too long to send"
    else: return string
