# coding=utf-8
"""
Copyright 2015,2016 Hermann Krumrey

This file is part of whatsapp-bot.

    whatsapp-bot makes use of various third-party python modules to serve
    information via the online chat service Whatsapp.

    whatsapp-bot is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    whatsapp-bot is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with whatsapp-bot.  If not, see <http://www.gnu.org/licenses/>.
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