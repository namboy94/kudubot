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

import datetime
import os
import re
import time

from plugins.GenericPlugin import GenericPlugin
from  yowsupwrapper.entities.WrappedTextMessageProtocolEntity import WrappedTextMessageProtocolEntity


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

        file = open(os.getenv("HOME") + "/.whatsapp-bot/reminders/continuous/" + self.sender, 'a')
        file.write("message=" + self.reminder_message)
        file.write("---endofmessage---time=" + time_string + "@" + weekday)
        file.write("\n")

        file.close()

    def __find_continuous_reminders__(self):
        """
        Searches all continuous reminders
        :return: the due TextMessageProtocolEntitiies found
        """

        weekday = datetime.date.today().strftime("%A").lower()
        current_time = datetime.datetime.now()
        current_hour = int(current_time.hour)
        current_minute = int(current_time.minute)
        current_second = int(current_time.second)

        recipients = os.listdir(os.getenv("HOME") + "/.whatsapp-bot/reminders/continuous")
        reminder_entities = []
        receiver_paths = []
        for receiver in recipients:
            if os.path.isdir(os.getenv("HOME") + "/.whatsapp-bot/reminders/continuous/" + receiver): continue
            receiver_paths.append(os.getenv("HOME") + "/.whatsapp-bot/reminders/continuous/" + receiver)
        for receiver in receiver_paths:
            receiver_name = receiver.rsplit("/", 1)[1]
            file = open(receiver, "r")
            file_content = file.read()
            file.close()

            reminders = file_content.split("\n")
            if not reminders[len(reminders) - 1]: reminders.pop()
            refreshed_reminders = []
            for reminder in reminders:
                reminderDay = reminder.split("---endofmessage---")[1].split("@")[1]

                if not "@@@DONE@@@" in reminder:
                    message = reminder.split("---endofmessage---")[0].split("message=")[1]
                    reminderTime = reminder.split("---endofmessage---")[1].split("@")[0].split("time=")[1]
                    hour = int(reminderTime.split("-")[0])
                    min = int(reminderTime.split("-")[1])
                    sec = int(reminderTime.split("-")[2])

                    outgoingEntity = TextMessageProtocolEntity(message, to=receiver_name)

                    if not reminderDay == weekday: refreshed_reminders.append(reminder)
                    else:
                        if current_hour < hour: refreshed_reminders.append(reminder);
                        elif current_minute < min: refreshed_reminders.append(reminder);
                        elif current_second < sec: refreshed_reminders.append(reminder);
                        else:
                            refreshed_reminders.append(reminder + "@@@DONE@@@")
                            reminder_entities.append(outgoingEntity)

                else:
                    if not weekday == reminderDay:
                        reminder = reminder.replace("@@@DONE@@@", "")
                        refreshed_reminders.append(reminder)
                    else:
                        refreshed_reminders.append(reminder)

            file = open(receiver, 'w')
            for reminder in refreshed_reminders:
                file.write(reminder + "\n")
            file.close()

        return reminder_entities

    def __getStored__(self):
        path = os.getenv("HOME") + "/.whatsapp-bot/reminders/continuous/" + self.sender
        if not os.path.isfile(path): return "None"
        file = open(path, 'r')
        file_content = file.read()
        file.close()
        file_content = file_content.split("\n")
        if not file_content[len(file_content) - 1]: file_content.pop()

        storedString = ""

        i = 0
        for reminder in file_content:
            message = reminder.split("---endofmessage---")[0].split("message=")[1]
            reminderTime = reminder.split("---endofmessage---")[1].split("@")[0].split("time=")[1]
            reminderDay = reminder.split("---endofmessage---")[1].split("@")[1]

            storedString += str(i) + " \"" + message + "\" on " + reminderDay + "@" + reminderTime + "\n"

            i += 1

        return storedString

    def __deleteReminder__(self, index):
        path = os.getenv("HOME") + "/.whatsapp-bot/reminders/continuous/" + self.sender
        if not os.path.isfile(path): return "Nothing to delete"
        file = open(path, 'r')
        file_content = file.read()
        file.close()
        file_content = file_content.split("\n")
        if not file_content[len(file_content) - 1]: file_content.pop()
        deleted = file_content.pop(index)
        file = open(path, 'w')
        for line in file_content: file.write(line + "\n")
        file.close()
        return "Deleted:\n" + deleted