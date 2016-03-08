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

import datetime
import os
import re
import time

try:
    from plugins.GenericPlugin import GenericPlugin
    from yowsupwrapper.entities.WrappedTextMessageProtocolEntity import WrappedTextMessageProtocolEntity
except ImportError:
    from whatsbot.plugins.GenericPlugin import GenericPlugin
    from whatsbot.yowsupwrapper.entities.WrappedTextMessageProtocolEntity import WrappedTextMessageProtocolEntity


class ContinuousReminder(GenericPlugin):
    """
    The ContinuousReminder Class
    """

    def __init__(self, layer, message_protocol_entity=None):
        """
        Constructor
        :param layer: the overlying yowsup layer
        :param message_protocol_entity: the received message information
        :return: void
        """
        super().__init__(layer, message_protocol_entity)

        self.reminder_message = ""
        self.params = ""

        self.continuous = False
        self.mode = "store"

    def regex_check(self):
        """
        Checks if the user input matches the regex needed for the plugin to function correctly
        :return: True if input is valid, False otherwise
        """
        if "---endofmessage---" in self.message: 
            return False
        if "@@@DONE@@@" in self.cap_message: 
            return False
        regex = r"^/cremind \"[^\"]+\" (monday|tuesday|wednesday|thursday|friday|saturday|sunday|" \
                r"montag|dienstag|mittwoch|donnerstag|freitag|samstag|sonntag) ([0-9]{2}-[0-9]{2}-[0-9]{2})$"
        if re.search(regex, self.message): 
            return True
        regex = r"^/cremind (list|delete [0-9]+)$"
        if re.search(regex, self.message): 
            return True
        else: 
            return False

    def parse_user_input(self):
        """
        Parses the user input
        :return: void
        """
        self.params = self.message.split(" ", 1)[1]
        if self.params == "list":
            self.mode = "list"
        elif self.params.startswith("delete"):
            self.mode = "delete"
        else:
            self.params = self.message.split("\" ", 1)[1]
            self.reminder_message = self.cap_message.split("\"", 1)[1].rsplit("\"", 1)[0]

    def get_response(self):
        """
        Sends a confirmation back to the sender that the message was stored
        :return: the confirmation as a TextMessageProtocolEntity
        """
        if self.mode == "store":
            self.__set_continuous_reminder__(self.params)
            return WrappedTextMessageProtocolEntity("Reminder Stored", to=self.sender)
        elif self.mode == "list":
            return WrappedTextMessageProtocolEntity(self.__get_stored__(), to=self.sender)
        elif self.mode == "delete":
            index = int(self.params.split(" ")[1])
            return WrappedTextMessageProtocolEntity(self.__delete_reminder__(index), to=self.sender)

    def parallel_run(self):
        """
        Continuously checks if reminders are due and sends them to the intended recipient if needed.
        :return: void
        """
        while True:
            reminders = self.__find_continuous_reminders__()
            for reminder in reminders:
                self.send_message(reminder)
                time.sleep(1)
            time.sleep(1)

    @staticmethod
    def get_description(language):
        """
        Returns a description about this plugin
        :param language: the language in which to display the description
        :return: the description in the specified language
        """
        if language == "en":
            return "/cremind\tStores a continuous (weekly) reminder\n" \
                   "syntax:\n" \
                   "/cremind \"<message>\" <day> <hh-mm-ss>\n" \
                   "/cremind list\tLists all reminders currently stored" \
                   "/cremind delete <index>\tDeletes the reminder at the given index"
        elif language == "de":
            return "/cremind\tSpeichert eine wöchentliche Errinnerung\n" \
                   "syntax:\n" \
                   "/cremind \"<nachricht>\" <tag> <hh-mm-ss>\n" \
                   "/cremind list\tListet alle Erinnerungen " \
                   "/cremind delete <index>\tDeletes the reminder at the given index"
        else:
            return "Help not available in this language"

    @staticmethod
    def get_plugin_name():
        """
        Returns the plugin name
        :return: the plugin name
        """
        return "Continuous Reminder Plugin"

    # Private Methods
    def __set_continuous_reminder__(self, params):
        """
        Stores a continuous (weekly) reminder
        :param params: the user input split as parameters
        """
        weekday = params.split(" ")[0]

        if weekday == "montag": 
            weekday = "monday"
        if weekday == "dienstag": 
            weekday = "tuesday"
        if weekday == "mittwoch": 
            weekday = "wednesday"
        if weekday == "donnerstag": 
            weekday = "thursday"
        if weekday == "freitag": 
            weekday = "friday"
        if weekday == "samstag":
            weekday = "saturday"
        if weekday == "sonntag": 
            weekday = "sunday"

        time_string = params.split(" ")[1]

        file = open(os.getenv("HOME") + "/.whatsbot/reminders/continuous/" + self.sender, 'a')
        file.write("message=" + self.reminder_message)
        file.write("---endofmessage---time=" + time_string + "@" + weekday)
        file.write("\n")

        file.close()

    @staticmethod
    def __find_continuous_reminders__():
        """
        Searches all continuous reminders
        :return: the due TextMessageProtocolEntitiies found
        """
        weekday = datetime.date.today().strftime("%A").lower()
        current_time = datetime.datetime.now()
        current_hour = int(current_time.hour)
        current_minute = int(current_time.minute)
        current_second = int(current_time.second)

        recipients = os.listdir(os.getenv("HOME") + "/.whatsbot/reminders/continuous")
        reminder_entities = []
        receiver_paths = []
        for receiver in recipients:
            if os.path.isdir(os.getenv("HOME") + "/.whatsbot/reminders/continuous/" + receiver):
                continue
            receiver_paths.append(os.getenv("HOME") + "/.whatsbot/reminders/continuous/" + receiver)
        for receiver in receiver_paths:
            receiver_name = receiver.rsplit("/", 1)[1]
            file = open(receiver, "r")
            file_content = file.read()
            file.close()

            reminders = file_content.split("\n")
            if not reminders[len(reminders) - 1]: 
                reminders.pop()
            refreshed_reminders = []
            for reminder in reminders:
                reminder_day = reminder.split("---endofmessage---")[1].split("@")[1]

                if "@@@DONE@@@" not in reminder:
                    message = reminder.split("---endofmessage---")[0].split("message=")[1]
                    reminder_time = reminder.split("---endofmessage---")[1].split("@")[0].split("time=")[1]
                    hour = int(reminder_time.split("-")[0])
                    minute = int(reminder_time.split("-")[1])
                    second = int(reminder_time.split("-")[2])

                    outgoing_entity = WrappedTextMessageProtocolEntity(message, to=receiver_name)

                    if not reminder_day == weekday:
                        refreshed_reminders.append(reminder)
                    else:
                        if current_hour < hour:
                            refreshed_reminders.append(reminder)
                        elif current_minute < minute:
                            refreshed_reminders.append(reminder)
                        elif current_second < second:
                            refreshed_reminders.append(reminder)
                        else:
                            refreshed_reminders.append(reminder + "@@@DONE@@@")
                            reminder_entities.append(outgoing_entity)

                else:
                    if not weekday == reminder_day:
                        reminder = reminder.replace("@@@DONE@@@", "")
                        refreshed_reminders.append(reminder)
                    else:
                        refreshed_reminders.append(reminder)

            file = open(receiver, 'w')
            for reminder in refreshed_reminders:
                file.write(reminder + "\n")
            file.close()

        return reminder_entities

    def __get_stored__(self):
        """
        Reads the stored reminders from file and turns them into a string
        :return: the stored reminders
        """
        path = os.getenv("HOME") + "/.whatsbot/reminders/continuous/" + self.sender
        if not os.path.isfile(path):
            return "None"
        file = open(path, 'r')
        file_content = file.read()
        file.close()
        file_content = file_content.split("\n")
        if not file_content[len(file_content) - 1]:
            file_content.pop()

        stored_string = ""

        i = 0
        for reminder in file_content:
            message = reminder.split("---endofmessage---")[0].split("message=")[1]
            reminder_time = reminder.split("---endofmessage---")[1].split("@")[0].split("time=")[1]
            reminder_day = reminder.split("---endofmessage---")[1].split("@")[1]

            stored_string += str(i) + " \"" + message + "\" on " + reminder_day + "@" + reminder_time + "\n"

            i += 1

        return stored_string

    def __delete_reminder__(self, index):
        """
        Deletes a reminder
        :param index: the index of the reminder to be deleted
        :return: A string that states which reminder was deleted
        """
        path = os.getenv("HOME") + "/.whatsbot/reminders/continuous/" + self.sender
        if not os.path.isfile(path):
            return "Nothing to delete"
        file = open(path, 'r')
        file_content = file.read()
        file.close()
        file_content = file_content.split("\n")
        if not file_content[len(file_content) - 1]:
            file_content.pop()
        deleted = file_content.pop(index)
        file = open(path, 'w')
        for line in file_content:
            file.write(line + "\n")
        file.close()
        return "Deleted:\n" + deleted
