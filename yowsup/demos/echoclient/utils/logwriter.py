import os
import time

def writeLogAndPrint(sentRecCmd, sender, message):

    log = open(os.getenv("HOME") + "/.whatsapp-bot/logs/" + time.strftime("%Y-%m-%d"), "a")
    string = sentRecCmd + ": " + sender + ": " + message
    print(string)
    log.write(string)
    log.close()