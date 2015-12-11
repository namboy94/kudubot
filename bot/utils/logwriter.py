"""
@author Hermann Krumrey<hermann@krumreyh.com>
"""

import os
import time
from utils.adressbook import getContact

"""
Writes the log of an event, sent or received.
"""
def writeLogAndPrint(sentRec, entity):

    log = open(os.getenv("HOME") + "/.whatsapp-bot/logs/" + time.strftime("%Y-%m-%d"), "a")
    if sentRec == "sent": contact = getContact(entity.getTo(False))
    elif sentRec == "recv": contact = getContact(entity.getFrom(False))
    string = sentRec + ": " + contact + ": " + entity.getBody()
    print(string)
    log.write(string)
    log.close()