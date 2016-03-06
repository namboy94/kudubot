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
from yowsupwrapper.entities.WrappedTextMessageProtocolEntity import WrappedTextMessageProtocolEntity


class Reminder(GenericPlugin):
    """
    The Reminder Class
    """

    def __init__(self, layer, message_protocol_entity=None):
        """
        Constructor
        :param layer: the overlying yowsup layer
        :param message_protocol_entity: the received message information
        :return: void
        """
        super().__init__(layer, message_protocol_entity)

        self.leapyear = False
        if datetime.datetime.now().year % 4 == 0:
            self.leapyear = True

        self.year = 0
        self.month = 0
        self.day = 0
        self.hour = 0
        self.minute = 0
        self.second = 0
        self.reminder_message = ""

    def regex_check(self):
        """
        Checks if the user input matches the regex needed for the plugin to function correctly
        :return: True if input is valid, False otherwise
        """
        regex = r"^/remind \"[^\"]+\" (tomorrow|morgen|" \
                r"[0-9]+ (years|yahre|months|monate|days|tage|hours|stunden|minutes|minuten|seconds|sekunden)|" \
                r"[0-9]{4}-[0-9]{2}-[0-9]{2}(-[0-9]{2}-[0-9]{2}-[0-9]{2})?)$"
        if re.search(regex, self.message):
            return True
        else:
            return False

    def parse_user_input(self):
        """
        Parses the user input
        :return: void
        """
        self.reminder_message = self.cap_message.split("\"", 1)[1].rsplit("\"", 1)[0]

        current_time = datetime.datetime.now()
        current_year = int(current_time.year)
        current_month = int(current_time.month)
        current_day = int(current_time.day)
        current_hour = int(current_time.hour)
        current_minute = int(current_time.minute)
        current_second = int(current_time.second)
        params = self.message.split("\" ", 1)[1]
        if params in ["morgen", "tomorrow"]:
            self.__set_reminder_time__(current_year, current_month, current_day + 1,
                                       current_hour, current_minute, current_second)
        if re.search(r"^[0-9]+ (years|jahre)$", params):
            self.__set_reminder_time__(current_year + int(params.split(" ")[0]), current_month, current_day,
                                       current_hour, current_minute, current_second)
        if re.search(r"^[0-9]+ (months|monate)$", params):
            self.__set_reminder_time__(current_year, current_month + int(params.split(" ")[0]), current_day,
                                       current_hour, current_minute, current_second)
        if re.search(r"^[0-9]+ (days|tage)$", params):
            self.__set_reminder_time__(current_year, current_month, current_day + int(params.split(" ")[0]),
                                       current_hour, current_minute, current_second)
        if re.search(r"^[0-9]+ (hours|stunden)$", params):
            self.__set_reminder_time__(current_year, current_month, current_day,
                                       current_hour + int(params.split(" ")[0]), current_minute, current_second)
        if re.search(r"^[0-9]+ (minutes|minuten)$", params):
            self.__set_reminder_time__(current_year, current_month, current_day,
                                       current_hour, current_minute + int(params.split(" ")[0]), current_second)
        if re.search(r"^[0-9]+ (sekunden|seconds)$", params):
            self.__set_reminder_time__(current_year, current_month, current_day,
                                       current_hour, current_minute, current_second + int(params.split(" ")[0]))
        if re.search(r"^[0-9]{4}-[0-9]{2}-[0-9]{2}$", params):
            self.__set_reminder_time__(int(params.split("-")[0]), int(params.split("-")[1]),
                                       int(params.split("-")[2]), 0, 0, 0)
        if re.search(r"^[0-9]{4}-[0-9]{2}-[0-9]{2}-[0-9]{2}-[0-9]{2}-[0-9]{2}$", params):
            self.__set_reminder_time__(int(params.split("-")[0]), int(params.split("-")[1]),
                                       int(params.split("-")[2]), int(params.split("-")[3]),
                                       int(params.split("-")[4]), int(params.split("-")[5]))
        self.__calendarize_time__()

    def get_response(self):
        """
        Sends a confirmation back to the sender that the message was stored
        :return: the confirmation as a TextMessageProtocolEntity
        """
        file = open(os.getenv("HOME") + "/.whatsapp-bot/reminders/" + str(int(time.time())), 'w')
        file.write("sender=" + self.sender)
        file.write("\nmessage=" + self.reminder_message)
        file.write("\ntime=" + self.__create_reminder_time_string__())
        file.close()
        return WrappedTextMessageProtocolEntity("Reminder Stored", to=self.sender)

    def parallel_run(self):
        """
        Continuously checks if reminders are due and sends them to the intended recipient if needed.
        :return: void
        """
        while True:
            reminders = self.__find_reminders__()
            for reminder in reminders:
                self.send_message(reminder)
                time.sleep(1)
            time.sleep(1)

    @staticmethod
    def get_description(language):
        """
        Returns a description about this plugin
        :param language: the language in which to display the description
        :return the description in the specified language
        """
        if language == "en":
            return "/remind\tSaves a reminder and sends it back at the specified time\n" \
                   "syntax: /remind \"<message>\" <time>\n" \
                   "time syntax: <YYYY-MM-DD-hh-mm-ss>\n" \
                   "or: <amount> [years|months|days|hours|minutes|seconds]"
        elif language == "de":
            return "/remind\tSpeichert eine Erinnerung und verschickt diese zum angegebenen Zeitpunkt\n" \
                   "syntax: /remind \"<nachricht>\" <zeit>\n" \
                   "zeit syntax: YYYY-MM-DD-hh-mm-ss\n" \
                   "oder: <anzahl> [jahre|monate|tage|stunden|minuten|sekunden]"
        else:
            return "Help not available in this language"

    # Private Methods

    def __set_reminder_time__(self, year, month, day, hour, minute, second):
        """
        Sets the reminder time
        :return: void
        """
        self.year = year
        self.month = month
        self.day = day
        self.hour = hour
        self.minute = minute
        self.second = second

    def __calendarize_time__(self):
        """
        Makes sure that only values valid in the Gregorian Calendar and metric time measurement systems
        :return: void
        """
        seconds_left = self.second - self.second % 60
        self.second %= 60
        self.minute += int(seconds_left / 60)
        minutes_left = self.minute - self.minute % 60
        self.minute %= 60
        self.hour += int(minutes_left / 60)
        self.hour %= 24
        self.day += int(self.hour / 24)
        month_length = self.__get_month_length__()
        while self.day > month_length:
            self.day -= month_length
            self.__increment_month__()

    def __get_month_length__(self):
        """
        Calculates the lenth of the current month in days
        :return: the amount of days in the current month
        """
        if self.month in [1, 3, 5, 7, 8, 10, 12]:
            month_length = 31
        elif self.month in [4, 6, 9, 11]:
            month_length = 30
        elif self.month == 2 and self.leapyear:
            month_length = 29
        else:
            month_length = 28
        return month_length

    def __increment_month__(self):
        """
        Increments the month by one
        :return: void
        """
        if self.month < 12:
            self.month += 1
        elif self.month == 12:
            self.month = 1
            self.year += 1

    def __create_reminder_time_string__(self):
        """
        Turns the current reminder time into a string
        :return: the reminder time string
        """
        return str(self.year) + "-" + str(self.month) + "-" + str(self.day) + "-" + str(self.hour) + "-" + str(
            self.minute) + "-" + str(self.second)

    def __find_reminders__(self):
        """
        Searches all currently saved reminders and checks if they are due. If they are, they are returned
        :return: a list of due reminders as TextMessageProtocolEntities
        """
        reminders = os.listdir(os.getenv("HOME") + "/.whatsapp-bot/reminders")
        reminder_entities = []
        reminder_paths = []
        for reminder in reminders:
            path = os.getenv("HOME") + "/.whatsapp-bot/reminders/" + reminder
            if not os.path.isdir(path):
                reminder_paths.append(path)
        for reminder in reminder_paths:
            file = open(reminder, "r")
            file_content = file.read()
            file.close()
            sender = file_content.split("\n")[0].split("sender=")[1]
            message = file_content.split("\n")[1].split("message=")[1]
            time_string = file_content.split("\n")[2].split("time=")[1]
            if self.__remind_due__(time_string):
                os.system("rm " + reminder)
                outgoing_entity = WrappedTextMessageProtocolEntity(message, to=sender)
                reminder_entities.append(outgoing_entity)
        return reminder_entities

    @staticmethod
    def __remind_due__(time_string):
        """
        Checks if a timestring is due
        :param time_string: the time string to be checked
        :return: True if it is due, False if not.
        """
        current_time = datetime.datetime.now()
        current_year = int(current_time.year)
        current_month = int(current_time.month)
        current_day = int(current_time.day)
        current_hour = int(current_time.hour)
        current_minute = int(current_time.minute)
        current_second = int(current_time.second)
        remind_time = time_string.split("-")
        remind_year = int(remind_time[0])
        remind_month = int(remind_time[1])
        remind_day = int(remind_time[2])
        remind_hour = int(remind_time[3])
        remind_minute = int(remind_time[4])
        remind_second = int(remind_time[5])

        if current_year < remind_year:
            return False
        elif current_month < remind_month:
            return False
        elif current_day < remind_day:
            return False
        elif current_hour < remind_hour:
            return False
        elif current_minute < remind_minute:
            return False
        elif current_second < remind_second:
            return False
        else:
            return True
