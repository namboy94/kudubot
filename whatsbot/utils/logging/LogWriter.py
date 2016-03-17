# coding=utf-8
"""
Copyright 2015,2016 Hermann Krumrey

This file is part of whatsbot.

    whatsbot makes use of various third-party python modules to serve
    information via the online chat service Whatsapp.

    whatsbot is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    whatsbot is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with whatsbot.  If not, see <http://www.gnu.org/licenses/>.
"""

import os
import time
import re

try:
    from utils.contacts.AddressBook import AddressBook
except ImportError:
    from whatsbot.utils.contacts.AddressBook import AddressBook


class LogWriter(object):
    """
    The LogWriter class
    """

    @staticmethod
    def write_event_log(event, entity):
        """
        writes an event (Sent, received, etc.) to the standard log file
        :param entity: the entity to log
        :param event: the event type to be logged
        """

        log_file = os.getenv("HOME") + "/.whatsbot/logs/"
        if event in ["recv", "sent", "s(m)", "i(m)", "imgs", "a(m)", "audi"]:
            if event == "recv":
                user_name = entity.get_from(False)
            else:
                user_name = entity.get_to(False)

            if re.search(r"^[0-9]+-[0-9]+$", user_name):
                log_file += "groups/"
            else:
                log_file += "users/"
            log_file += user_name + "---" + time.strftime("%Y-%m-%d")
        elif event == "exep" or event == "e(m)":
            log_file += "exceptions/" + time.strftime("%Y-%m-%d")
        elif event == "bugs" or event == "b(m)":
            log_file += "bugs/" + time.strftime("%Y-%m-%d")

        log = open(log_file, "a")

        contact = ""
        if event == "recv":
            contact = AddressBook().get_contact_name(entity, True)
        elif event == "sent" or event == "s(m)":
            contact = AddressBook().get_contact_name(entity, False)
        elif event == "imgs" or event == "i(m)":
            contact = AddressBook().get_contact_name(entity, False)
        elif event == "audi" or event == "a(m)":
            contact = AddressBook().get_contact_name(entity, False)
        elif event == "exep" or event == "e(m)":
            contact = "Exception"
        elif event == "bugs" or event == "b(m)":
            contact = "Bug"

        string = event + ": " + contact + ": " + entity.get_body()

        try:
            print(string)
        except IOError:  # Prevents Exceptions being thrown in case the Terminal is gone.
            str(string)

        log.write((string + "\n"))
        log.close()
