"""
Collection of static methods that handle logging
@author Hermann Krumrey<hermann@krumreyh.com>
"""

import os
import time
from utils.contacts.AddressBook import AddressBook

"""
The LogWriter class
"""
class LogWriter(object):

    """
    writes an event (Sent, received, etc.) to the standard log file
    """
    @staticmethod
    def writeEventLog(event, entity):

        log = open(os.getenv("HOME") + "/.whatsapp-bot/logs/" + time.strftime("%Y-%m-%d"), "a")

        if event == "recv": contact = AddressBook.getContactName(entity.getTo(False))
        else: contact = AddressBook.getContactName(entity.getFrom(False))

        string = event + ": " + contact + ": " + entity.getBody()
        print(string)
        log.write(string)
        log.close()