# coding=utf-8
import re
from yowsup.demos.echoclient.responses.food import *
from yowsup.demos.echoclient.responses.it_related import *
from yowsup.demos.echoclient.responses.smileys import *
from yowsup.demos.echoclient.responses.pseudocommands import *
from yowsup.demos.echoclient.responses.phrases import *
from yowsup.demos.echoclient.responses.functions import *

def decide(messageProtocolEntity):
    sentmessage = messageProtocolEntity.getBody()
    sentmessageMin = sentmessage.lower()
    sender = messageProtocolEntity.getFrom()

    sendername = adressbook(messageProtocolEntity.getFrom(False))

    try:
        participant = messageProtocolEntity.getParticipant(False)
    except: participant = ""
    decision = ["", sender, ""]

    print("recv: " + sendername + ": " + sentmessage)

    # Instant text replies
    #weather
    if re.compile("(weather|wetter) [^ ]+").match(sentmessageMin): decision[0] = wetter(sentmessageMin.split(" ", 1)[1], True)
    elif re.compile("(weather|wetter):text [^ ]+").match(sentmessageMin): decision[0] = wetter(sentmessageMin.split(" ", 1)[1], False)
    elif sentmessageMin in ["wetter", "weather"]: decision[0] = wetter("karlsruhe", True)
    elif sentmessageMin in ["wetter:text", "weather:text"]: decision[0] = wetter("karlsruhe", False)

    #food
    elif "keks" in sentmessageMin or "cookie" in sentmessageMin: decision[0] = kekse()
    elif "kuchen" in sentmessageMin: decision[0] = kuchen()
    elif "uups" in sentmessageMin or "ups" in sentmessageMin or "oops" in sentmessageMin: decision[0] = oops()

    #it_related
    elif "würfel" in sentmessageMin or "wuerfel" in sentmessageMin: decision[0] = wuerfel()
    elif "umlaut" in sentmessageMin: decision[0] = umlaute()

    #smileys
    elif "😂" in sentmessageMin: decision[0] = happyTears()
    elif "🖕🏻" in sentmessageMin: decision[0] = middleFinger()
    elif "liebe" in sentmessageMin and "bot" in sentmessageMin: decision[0] = kisses()
    elif "beste bot" in sentmessage or "bester bot" in sentmessageMin: decision[0] = kisses()

    #pseudocommands
    elif sentmessageMin.startswith("ls"): decision[0] = ls()
    elif sentmessageMin.startswith("man"): decision[0] = man()
    elif sentmessageMin.startswith("cat"): decision[0] = cat()
    elif sentmessageMin.startswith("echo"): decision[0] = echo(sentmessageMin)



    #terminal commands
    elif "term: " in sentmessageMin and sendername.split(" ")[0] == "Hermann":
        decision[2] = sentmessageMin.split("term: ")[1]
    elif sentmessageMin == "rsync-backup" and sendername.split([0]) == "Hermann:":
        decision[2] = sentmessageMin



    #Special Text commands
    elif sentmessageMin in ["die", "stirb", "killbot"]: decision[0] = "😨🔫"


    #Print to console
    if decision[0]: print("sent: " + sendername + ": " + decision[0])
    elif decision[2]: print("cmnd: " + decision[2])

    return decision


def adressbook(adress):
    if adress == "4915779781557-1418747022":    return "Land of the very Brave      "
    elif adress == "4917628727937-1448730289":  return "Bottesting                  "
    elif adress == "4917628727937":             return "Hermann                     "
    else: return adress

def sizeChecker(string):
    if len(string) > 500: return "Message too long to send"
    else: return string
