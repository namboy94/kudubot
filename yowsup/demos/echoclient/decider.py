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

def decide(messageProtocolEntity):

    group = False
    sentmessage = fixBrokenUnicode(messageProtocolEntity.getBody())
    sentmessageMin = sentmessage.lower()
    sender = messageProtocolEntity.getFrom()
    pureSender = messageProtocolEntity.getFrom(False)
    if re.compile("[0-9]+-[0-9]+").match(pureSender): group = True;
    sendername = adressbook(pureSender)

    try:
        participant = messageProtocolEntity.getParticipant(False)
    except: participant = ""
    participantname = adressbook(participant)

    decision = ["", sender, ""]

    # Instant text replies
    #weather
    if re.compile("(weather|wetter)(:(;text|;verbose)*)? [^ ]*").match(sentmessageMin) \
            or re.compile("(weather|wetter)(;text|;verbose;)*").match(sentmessageMin):
        decision[0] = weather(sentmessageMin, group).getWeather()

    #food
    if "keks" in sentmessageMin or "cookie" in sentmessageMin: decision[0] = kekse()
    elif "kuchen" in sentmessageMin: decision[0] = kuchen()
    elif "uups" in sentmessageMin or "ups" in sentmessageMin or "oops" in sentmessageMin: decision[0] = oops()

    #it_related
    elif "würfel" in sentmessageMin or "wuerfel" in sentmessageMin: decision[0] = wuerfel()
    elif "umlaut" in sentmessageMin: decision[0] = umlaute()

    #smileys
    elif "😂" in sentmessageMin: decision[0] = happyTears(group)
    elif "🖕🏻" in sentmessageMin: decision[0] = middleFinger(group)
    elif "liebe" in sentmessageMin and "bot" in sentmessageMin: decision[0] = kisses(group)
    elif "beste bot" in sentmessage or "bester bot" in sentmessageMin: decision[0] = kisses(group)

    #pseudocommands
    elif sentmessageMin.startswith("ls"): decision[0] = ls()
    elif sentmessageMin.startswith("man"): decision[0] = man()
    elif sentmessageMin.startswith("cat"): decision[0] = cat()
    elif sentmessageMin.startswith("echo"): decision[0] = echo(sentmessageMin)
    elif sentmessageMin == "uptime": decision[0] = uptime()

    #public terminal
    elif sentmessageMin.startswith("term:ls "): decision[2] = publicLs(sentmessage)
    elif sentmessageMin == "term:uptime": decision[2] = "uptime"


    #Restricted Terminal
    elif sendername == "Hermann" or participantname == "Hermann":
        if sentmessageMin == "rsync-backup" and sendername.split([0]) == "Hermann:":
            decision[2] = sentmessageMin

        #Special Text commands
        elif sentmessageMin in ["die", "stirb", "killbot"]: decision[0] = "😨🔫"


    #Print to console and log
    log = open(os.getenv("HOME") + "/.whatsapp-bot/logs/" + time.strftime("%Y-%m-%d"), "a")
    print("recv: " + sendername + ": " + sentmessage)
    log.write("recv: " + sendername + ": " + sentmessage + "\n")
    if decision[0]:
        print("sent: " + sendername + ": " + decision[0])
        log.write("sent: " + sendername + ": " + decision[0] + "\n")
    elif decision[2]:
        print("cmnd: " + decision[2])
        log.write("cmnd: " + decision[2] + "\n")

    log.close()

    return decision


def adressbook(adress):
    if adress == "4915779781557-1418747022":    return "Land of the very Brave"
    elif adress == "4917628727937-1448730289":  return "Bottesting"
    elif adress == "4917628727937":             return "Hermann"
    else: return adress

def sizeChecker(string):
    if len(string) > 500: return "Message too long to send"
    else: return string
