"""
@author Hermann Krumrey<hermann@krumreyh.com>
"""

import os
import time

"""
Writes the log of an event, sent or received.
"""
def writeLogAndPrint(sentRec, sender, message):

    log = open(os.getenv("HOME") + "/.whatsapp-bot/logs/" + time.strftime("%Y-%m-%d"), "a")
    string = sentRec + ": " + sender + ": " + message
    print(string)
    log.write(string)
    log.close()