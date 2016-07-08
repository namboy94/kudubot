# coding=utf-8
"""
LICENSE:
Copyright 2015,2016 Hermann Krumrey

This file is part of kudubot.

    kudubot makes use of various third-party python modules to serve
    information via online chat services.

    kudubot is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    kudubot is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with kudubot.  If not, see <http://www.gnu.org/licenses/>.
LICENSE
"""

# imports
import os
import re
import time
import datetime
from typing import Tuple, List, Dict

from kudubot.servicehandlers.Service import Service
from kudubot.connection.generic.Message import Message
from kudubot.config.LocalConfigChecker import LocalConfigChecker


class WeeklyReminderService(Service):
    """
    The WeeklyReminderService Class that extends the generic Service class.
    The service offers weekly reminder messages
    """

    identifier = "weekly_reminder"
    """
    The identifier for this service
    """

    help_description = {"en": "/w-remind\tStores a continuous (weekly) reminder\n"
                              "syntax:\n"
                              "/w-remind \"<message>\" <day> <hh-mm-ss>\n"
                              "/w-remind list\tLists all reminders currently stored"
                              "/w-remind delete <index>\tDeletes the reminder at the given index",
                        "de": "/w-remind\tSpeichert eine wöchentliche Errinnerung\n"
                              "syntax:\n"
                              "/w-erinner \"<nachricht>\" <tag> <hh-mm-ss>\n"
                              "/w-erinner liste\tListet alle Erinnerungen "
                              "/w-erinner löschen <index>\tLöscht die Erinnerung am gegebenen Index"}
    """
    Help description for this service.
    """

    has_background_process = True
    """
    Indicates that the serice has a background process
    """

    w_reminder_directory = "w_reminder"
    """
    The directory in which the reminders are stored
    """

    w_remind_keywords = {"w-remind": "en",
                         "w-erinner": "de"}
    """
    Keywords for the w-remind command
    """

    list_keywords = {"list": "en",
                     "liste": "de"}
    """
    Keywords for the list command
    """

    delete_keywords = {"delete": "en",
                       "löschen": "de"}
    """
    Keywords for the delete command
    """

    weekday_keywords = {"monday": ("en", "monday", 1),
                        "montag": ("de", "monday", 1),
                        "tuesday": ("en", "tuesday", 2),
                        "dienstag": ("de", "tuesday", 2),
                        "wednesday": ("en", "wednesday", 3),
                        "mittwoch": ("de", "wednesday", 3),
                        "thursday": ("en", "thursday", 4),
                        "donnerstag": ("de", "thursday", 4),
                        "friday": ("en", "friday", 5),
                        "freitag": ("de", "friday", 5),
                        "saturday": ("en", "saturday", 6),
                        "samstag": ("de", "saturday", 6),
                        "sunday": ("en", "sunday", 7),
                        "sonntag": ("de", "sunday", 7)}
    """
    Keywords to identify the individual weekdays
    """

    message_stored_message = {"en": "Reminder successfully stored",
                              "de": "Erinnerung erfolgreich abgespeichert"}
    """
    Message for the user letting him/her knoww that the reminder was stored
    """

    no_reminders_found_message = {"en": "No reminders stored",
                                  "de": "Keine Erinnerungen gespeichert"}
    """
    Message to be sent to the user when he/she requests the list of his/her reminders,
    but there are none saved
    """

    delete_index_out_of_bounds_message = {"en": "No reminder known for the selected index",
                                          "de": "Keine Erinnerung für den gegebenen Index bekannt"}
    """
    Message to be sent if the user's delete index is out of bounds
    """

    reminder_deleted_message = {"en": "Reminder successfully deleted",
                                "de": "Erinnerung erfolgreich gelöscht"}
    """
    Message to be sent if the user's delete request was successfull
    """

    def initialize(self) -> None:
        """
        Constructor extender for the WeeklyRenamer class that initializes a directory for the reminder files

        :return: None
        """
        self.w_reminder_directory = \
            os.path.join(LocalConfigChecker.services_directory, self.connection.identifier, self.w_reminder_directory)
        LocalConfigChecker.validate_directory(self.w_reminder_directory)

    def process_message(self, message: Message) -> None:
        """
        Process a message according to the service's functionality

        :param message: the message to process
        :return: None
        """
        options, language, list_mode, delete_mode = self.parse_user_input(message.message_body)

        if list_mode:
            reply = self.list_stored_reminders(message.identifier, language)
        elif delete_mode:
            reply = self.delete_stored_reminder(message.identifier, language, options)
        else:
            reply = self.store_reminder(message.identifier, language, options[0], options[1], options[2])

        reply_message = self.generate_reply_message(message, "Weekly Reminder", reply)
        self.send_text_message(reply_message)

    @staticmethod
    def regex_check(message: Message) -> bool:
        """
        Checks if the user input is valid for this service to continue

        :return: True if input is valid, False otherwise
        """
        weekdays = {}
        for weekday in WeeklyReminderService.weekday_keywords:
            weekdays[weekday] = WeeklyReminderService.weekday_keywords[weekday][0]

        base_regex = "^/" + Service.regex_string_from_dictionary_keys([WeeklyReminderService.w_remind_keywords]) + " "

        regex = base_regex + "\"[^\"]+\" " + Service.regex_string_from_dictionary_keys([weekdays])
        regex += " ([0-9]{2}-[0-9]{2}-[0-9]{2})$"

        list_regex = base_regex + Service.regex_string_from_dictionary_keys([WeeklyReminderService.list_keywords]) + "$"
        delete_regex = base_regex + Service.regex_string_from_dictionary_keys([WeeklyReminderService.delete_keywords])\
                                  + " [0-9]+$"

        return re.search(re.compile(regex), message.message_body.lower())\
            or re.search(re.compile(list_regex), message.message_body.lower())\
            or re.search(re.compile(delete_regex), message.message_body.lower())

    def parse_user_input(self, user_input: str) -> Tuple[(Tuple[str, str, str] or str), str, bool, bool]:
        """
        Parses the user input, figures out what the user wants, and the language used

        :param user_input: the user input to parse
        :return: the message to save as reminder together with the weekday and time (or the deletion index),
                    the language used, flag for list mode, flag for delete mode
        """
        list_mode = False
        delete_mode = False

        command_key = user_input.split(" ")[0].split("/")[1].lower()
        language = self.w_remind_keywords[command_key]

        options = user_input.lower().split(" ")
        options.pop(0)

        if len(options) == 1 and options[0] in self.list_keywords:
            list_mode = True
            return "", language, list_mode, delete_mode
        elif len(options) == 2 and options[0] in self.delete_keywords:
            delete_mode = True
            index = options[1]
            return index, language, list_mode, delete_mode
        else:
            message = user_input.split("\"", 1)[1].split("\"", 1)[0]
            options = user_input.lower().rsplit("\" ", 1)[1].split(" ")
            weekday = self.weekday_keywords[options[0]][1]
            time_of_day = options[1]
            return (message, weekday, time_of_day), language, list_mode, delete_mode

    def store_reminder(self, receiver: str, language: str, message: str, weekday: str, send_time: str) -> str:
        """
        Stores a continuous reminder as a local file

        :param receiver: the user requesting a new reminder
        :param language: The language for the reply message
        :param message: the message to be saved
        :param weekday: the weekday on which the reminder will be sent
        :param send_time: the time it will be sent
        :return: A message to be sent to the user
        """

        reminder_filename = ""
        index = 0

        # Emulate a do-while loop
        while True:
            reminder_filename = os.path.join(self.w_reminder_directory,
                                             weekday + "@" + send_time + "@" + receiver + "#####COUNT" + str(index))
            if not os.path.isfile(reminder_filename):
                break
            else:
                index += 1

        opened_file = open(reminder_filename, "w")
        opened_file.write(message)
        opened_file.close()

        return self.message_stored_message[language]

    def list_stored_reminders(self, sender: str, language: str) -> str:
        """
        Lists all stored reminders of a user

        :param sender: the user whoes reminders should be checked
        :param language: The language to be used when no entries were found
        :return: the list of reminders as a formatted string
        """
        list_of_reminders_string = ""
        list_of_reminders = self.get_user_reminders(sender)

        for index in range(0, len(list_of_reminders)):
            reminder = list_of_reminders[index]

            reminder_day = reminder["day"]
            for day in self.weekday_keywords:
                if self.weekday_keywords[day][1] == reminder_day and self.weekday_keywords[day][0] == language:
                    reminder_day = day

            list_of_reminders_string += str(index + 1) + ": " + reminder["send_time"] + " " + reminder_day + "\n"
            list_of_reminders_string += reminder["content"] + "\n\n"

        if list_of_reminders_string == "":
            list_of_reminders_string = self.no_reminders_found_message[language]

        return list_of_reminders_string.rsplit("\n\n", 1)[0]

    def delete_stored_reminder(self, sender: str, language: str, index: str) -> str:
        """
        Deletes a stored reminder

        :param sender:
        :param language:
        :param index:
        :return:
        """
        list_of_reminders = self.get_user_reminders(sender)
        index = int(index)

        if index < 1:
            return self.delete_index_out_of_bounds_message[language]

        try:
            reminder = list_of_reminders[index - 1]
            os.remove(reminder["file_path"])
            return self.reminder_deleted_message[language]

        except IndexError:
            return self.delete_index_out_of_bounds_message[language]

    def get_user_reminders(self, user: str) -> List[Dict[str, (str or int)]]:
        """
        Returns a list of reminders a user has currently stored

        :param user: the user whose reminders should be searched
        :return: A list of dictionaries with the information about the reminders
                    - day: number of day in week (e.g Monday=1) the message is usually sent
                    - send_time: at which time the reminder is usually sent
                    - content: The content of the reminder
                    - file_path: The path of the reminder file
        """
        list_of_reminders = []

        for file_name in os.listdir(self.w_reminder_directory):
            file_path = os.path.join(self.w_reminder_directory, file_name)

            if user in file_name:
                day = self.weekday_keywords[file_name.split("@", 1)[0]][1]
                send_time = file_name.split("@", 2)[1]

                opened_file = open(file_path, 'r')
                content = opened_file.read()
                opened_file.close()

                list_of_reminders.append({"day": day,
                                          "send_time": send_time,
                                          "content": content,
                                          "file_path": file_path})

        return sorted(list_of_reminders, key=lambda dictionary: (dictionary["day"], dictionary["send_time"]))

    def background_process(self) -> None:
        """
        Runs constantly in the background and checks if a message is due for sending

        :return: None
        """
        while True:

            # Calculate the current time
            current = datetime.datetime.utcnow()
            current_day = current.date().strftime("%A").lower()
            current_time = {"hour": current.hour,
                            "minute": current.minute,
                            "second": current.second}
            current_time_stamp = self.calculate_seconds_since_week_start(current_time, current_day)

            for file_name in os.listdir(self.w_reminder_directory):
                file_path = os.path.join(self.w_reminder_directory, file_name)

                # Calculate the due time for the reminder
                due_day = str(file_name.split("@", 1)[0])
                due_time = str(file_name.split("@", 2)[1])
                due_time = self.parse_time_string(due_time)
                reminder_timestamp = self.calculate_seconds_since_week_start(due_time, due_day)

                # Get the difference between the reminder time and the current time
                time_difference = abs(current_time_stamp - reminder_timestamp)

                # Send the reminder when in range of 3 seconds of the reminder time
                if time_difference < 3 and not file_name.endswith("+++WEEKDONE+++"):

                    # Read file content
                    opened_file = open(file_path, 'r')
                    content = opened_file.read()
                    opened_file.close()
                    os.rename(file_path, file_path + "+++WEEKDONE+++")  # Mark the file as done for the week

                    # Get the user's address
                    # noinspection PyTypeChecker
                    address = file_name.split("@", 2)[2].split("#####COUNT")[0]

                    message = Message(content, "Weekly Reminder", str(address), False)
                    self.send_text_message(message)

                if time_difference > 30 and file_name.endswith("+++WEEKDONE+++"):

                    os.rename(file_path, file_path.split("+++WEEKDONE+++")[0])  # Mark the file as not done

            time.sleep(1)

    @staticmethod
    def parse_time_string(time_string: str) -> Dict[str, int]:
        """
        Parses a time string to a dictionary

        :param time_string: the time string to parse
        :return: the time as a dictionary with the keys 'hour', 'minute' and 'second'
        """
        return {"hour": int(time_string.split("-")[0]),
                "minute": int(time_string.split("-")[1]),
                "second": int(time_string.split("-")[2])}

    def calculate_seconds_since_week_start(self, time_dictionary: Dict[str, int], weekday: str) -> int:
        """
        Calculates the amount of seconds that have passed for the specified time since the start of the week

        :param time_dictionary: the time as a dictionary
        :param weekday: the weekday to use in the calculation
        :return: the time in seconds since monday, 00:00:00
        """
        seconds = self.weekday_keywords[weekday][2] * 86400
        seconds += time_dictionary["second"]
        seconds += time_dictionary["minute"] * 60
        seconds += time_dictionary["hour"] * 3600
        return seconds
