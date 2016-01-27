# coding=utf-8

"""
Collection of static methods that handle logging
@author Hermann Krumrey<hermann@krumreyh.com>
"""

import os
import time
import re
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

        logFile = os.getenv("HOME") + "/.whatsapp-bot/logs/"
        if event in ["recv", "sent", "s(m)", "i(m)", "imgs", "a(m)", "audi"]:
            if event == "recv":
                userName = entity.getFrom(False)
            else:
                userName = entity.getTo(False)

            if re.search(r"^[0-9]+-[0-9]+$", userName):
                logFile += "groups/"
            else:
                logFile += "users/"
            logFile += userName + "---" + time.strftime("%Y-%m-%d")
        elif event == "exep" or event == "e(m)":
            logFile += "exceptions/" + time.strftime("%Y-%m-%d")
        elif event == "bugs" or event == "b(m)":
            logFile += "bugs/" + time.strftime("%Y-%m-%d")

        log = open(logFile, "a")

        contact = ""
        if event == "recv": contact = AddressBook().getContactName(entity, True)
        elif event == "sent" or event == "s(m)": contact = AddressBook().getContactName(entity, False)
        elif event == "imgs" or event == "i(m)": contact = AddressBook().getContactName(entity, False)
        elif event == "audi" or event == "a(m)": contact = AddressBook().getContactName(entity, False)
        elif event == "exep" or event == "e(m)": contact = "Exception"
        elif event == "bugs" or event == "b(m)": contact = "Bug"

        string = event + ": " + contact + ": " + entity.getBody()
        print(string)
        log.write((string + "\n"))
        log.close()