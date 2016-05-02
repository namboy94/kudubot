# coding=utf-8
"""
Copyright 2015,2016 Hermann Krumrey

This file is part of messengerbot.

    messengerbot makes use of various third-party python modules to serve
    information via the online chat services.

    messengerbot is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    messengerbot is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with messengerbot.  If not, see <http://www.gnu.org/licenses/>.
"""

# imports
import os
import re
import time
import calendar
import datetime
from typing import Tuple, Dict

from messengerbot.servicehandlers.Service import Service
from messengerbot.connection.generic.Message import Message
from messengerbot.config.LocalConfigChecker import LocalConfigChecker


class ReminderService(Service):
    """
    The ReminderService Class that extends the generic Service class.
    The service parses www.kicktipp.de to get a kicktipp group's current standings
    """

    identifier = "reminder"
    """
    The identifier for this service
    """

    help_description = {"en": "/remind\tSaves a reminder and sends it back at the specified time\n"
                              "syntax: /remind \"<message>\" <time>\n"
                              "time syntax: <YYYY-MM-DD-hh-mm-ss>\n"
                              "or: <amount> [years|months|days|hours|minutes|seconds]",
                        "de": "/remind\tSpeichert eine Erinnerung und verschickt diese zum angegebenen Zeitpunkt\n"
                              "syntax: /remind \"<nachricht>\" <zeit>\n"
                              "zeit syntax: YYYY-MM-DD-hh-mm-ss\n"
                              "oder: <anzahl> [jahre|monate|tage|stunden|minuten|sekunden]"}
    """
    Help description for this service.
    """

    has_background_process = True
    """
    Indicates that the serice has a background process
    """

    message_stored_reply = {"en": "Message Stored",
                            "de": "Nachricht gespeichert"}

    reminder_directory = "reminder"
    """
    The directory in which the reminders are stored
    """

    remind_keywords = {"remind": "en",
                       "erinner": "en"}
    """
    Keywords for the remind command
    """

    time_adder_keywords = {"years": ["en", "years"],
                           "jahre": ["de", "years"],
                           "months": ["en", "months"],
                           "monate": ["de", "months"],
                           "days": ["en", "days"],
                           "tage": ["de", "days"],
                           "hours": ["en", "hours"],
                           "stunden": ["de", "hours"],
                           "minutes": ["en", "minutes"],
                           "minuten": ["de", "minutes"],
                           "seconds": ["en", "seconds"],
                           "sekunden": ["de", "seconds"]}
    """
    Keywords for specific time sizes
    """

    tomorrow_keywords = {"tomorrow": "en",
                         "morgen": "de"}
    """
    Keywords that define the tomorrow option
    """

    remider_time = {"years": 0,
                    "months": 0,
                    "days": 0,
                    "hours": 0,
                    "minutes": 0,
                    "seconds": 0}
    "The time when the reminder shoul be activated"

    def initialize(self) -> None:
        """
        Constructor extender for the Renamer class that initializes a directory for the reminder files

        :return: None
        """
        self.reminder_directory = \
            os.path.join(LocalConfigChecker.services_directory, self.connection.identifier, self.reminder_directory)
        LocalConfigChecker.validate_directory(self.reminder_directory)

    def process_message(self, message: Message) -> None:
        """
        Process a message according to the service's functionality

        :param message: the message to process
        :return: None
        """
        language, reminder_options, reminder_message = self.parse_user_input(message.message_body)
        reminder_time = self.determine_reminder_time(reminder_options)
        reminder_time = self.normalize_time(reminder_time)

        self.store_reminder(reminder_time, reminder_message, message.address)

        reply = self.message_stored_reply[language]
        reply_message = self.generate_reply_message(message, "Reminder", reply)
        self.send_text_message(reply_message)

    @staticmethod
    def regex_check(message: Message) -> bool:
        """
        Checks if the user input is valid for this service to continue

        :return: True if input is valid, False otherwise
        """
        regex = "^/" + Service.regex_string_from_dictionary_keys([ReminderService.remind_keywords])
        regex += " \"[^\"]+\" ([0-9]+ " + \
                 Service.regex_string_from_dictionary_keys([ReminderService.time_adder_keywords])
        regex += "|" + Service.regex_string_from_dictionary_keys([ReminderService.tomorrow_keywords])
        regex += "|[0-9]{4}-[0-9]{2}-[0-9]{2}(-[0-9]{2}-[0-9]{2}-[0-9]{2})?)$"

        return re.search(re.compile(regex), message.message_body.lower())

    def parse_user_input(self, user_input: str) -> Tuple[str, str, str]:
        """
        Parses the user input and determines the used language, the reminder to be stored,
        as well as th options defining when the reminder will be activated

        :param user_input: the user input to be parsed
        :return: language, options, reminder text
        """

        remind_keyword, options = user_input.split(" ", 1)  # Split message into /remind and the rest of the message
        language = self.remind_keywords[remind_keyword.split("/")[1]]  # Get the language using the /remind keyword

        # Split message into three parts:
        # junk: empty string, stuff that comes before the first quotation mark
        # reminder_message: The message nested between quotation marks
        # options: the options after the reminder string
        junk, reminder_message, options = options.split("\"", 2)

        options = options.lstrip()  # Remove leading whitespace

        return language, options, reminder_message

    def determine_reminder_time(self, options: str) -> Dict[str, int]:
        """
        Determines the reminder time from the given options

        :param options: the options to be parsed
        :return: the reminder time as a dictionary
        """

        reminder_time = self.get_current_time()

        if options in self.tomorrow_keywords:
            reminder_time["days"] += 1

        elif re.search(r"[0-9]{4}-[0-9]{2}-[0-9]{2}(-[0-9]{2}-[0-9]{2}-[0-9]{2})?", options):
            selected_time = options.split("-")
            reminder_time["years"] = int(selected_time[0])
            reminder_time["months"] = int(selected_time[1])
            reminder_time["days"] = int(selected_time[2])
            if len(selected_time) > 3:
                reminder_time["hours"] = int(selected_time[3])
                reminder_time["minutes"] = int(selected_time[4])
                reminder_time["seconds"] = int(selected_time[5])

        else:
            modifier, key = options.split(" ")
            reminder_time[key] += int(modifier)

        return reminder_time

    def store_reminder(self, reminder_time: Dict[str, int], reminder_message: str, reminder_address: str) -> None:
        """
        Stores a reminder in the reminder directory as a reminder file.

        :param reminder_time: the time the reminder activates
        :param reminder_message: the reminder text itself
        :param reminder_address: the address to where the reminder will be sent
        :return: None
        """
        timestamp = ReminderService.convert_time_to_utc_timestamp(reminder_time)

        # emulate a do-while loop
        # The loop makes sure that no existing file is overwritten
        counter = 0
        while True:
            reminder_filename = str(timestamp) + "#" + str(counter) + "@" + reminder_address
            reminder_file = os.path.join(self.reminder_directory, reminder_filename)
            if not os.path.isfile(reminder_file):
                break
            else:
                counter += 1

        # Disable inspection because the loop will run at least once
        # noinspection PyUnboundLocalVariable
        opened_file = open(reminder_file, 'w')
        opened_file.write(reminder_message)
        opened_file.close()

    @staticmethod
    def get_current_time() -> Dict[str, int]:
        """
        Returns the current time as a dicitonary

        :return: the time dictionary
        """
        current_time = datetime.datetime.utcnow()
        return {"years": current_time.year,
                "months": current_time.month,
                "days": current_time.day,
                "hours": current_time.hour,
                "minutes": current_time.minute,
                "seconds": current_time.second}

    @staticmethod
    def normalize_time(time_dictionary: Dict[str, int]) -> Dict[str, int]:
        """
        Normalizes a time dictionary (seconds to max 60, months to max 12 etc.)

        :param time_dictionary: the time dictionary to be normalized
        :return: the normalized time dictionary
        """

        def transfer_overdraft(smaller_unit: int, larger_unit: int, limit: int) -> Tuple[int, int]:
            """
            Transfers an overdraft to the next biggest unit

            :param smaller_unit: the value of the smaller unit
            :param larger_unit: the value of the larger unit
            :param limit: the limit of the smaller unit
            :return: the new smaller and largr unit values as a Tuple
            """

            extra_larger_unit = int((smaller_unit - smaller_unit % limit) / limit)
            smaller_unit %= limit
            larger_unit += extra_larger_unit

            return smaller_unit, larger_unit

        def get_month_length() -> int:
            """
            Calculates the length of a the currently selected month of the time dictionary

            :return: the amount of days in that month
            """
            if time_dictionary["months"] in [1, 3, 5, 7, 8, 10, 12]:
                return 31
            elif time_dictionary["months"] in [4, 6, 9, 11]:
                return 30
            elif time_dictionary["months"] == 2 and time_dictionary["years"] % 4 == 0:
                return 29
            else:
                return 28

        def increment_month() -> None:
            """
            Increments the month of the time dictionary by 1

            :return: the incremented dictionary
            """
            if time_dictionary["months"] == 12:
                time_dictionary["months"] = 1
                time_dictionary["years"] += 1
            else:
                time_dictionary["months"] += 1

        time_dictionary["seconds"], time_dictionary["minutes"] =\
            transfer_overdraft(time_dictionary["seconds"], time_dictionary["minutes"], 60)

        time_dictionary["minutes"], time_dictionary["hours"] = \
            transfer_overdraft(time_dictionary["minutes"], time_dictionary["hours"], 60)

        time_dictionary["hours"], time_dictionary["days"] = \
            transfer_overdraft(time_dictionary["hours"], time_dictionary["days"], 24)

        time_dictionary["months"], time_dictionary["years"] = \
            transfer_overdraft(time_dictionary["months"], time_dictionary["years"], 12)

        month_length = get_month_length()
        while time_dictionary["days"] > month_length:
            time_dictionary["days"] -= month_length
            increment_month()
            month_length = get_month_length()

        return time_dictionary

    @staticmethod
    def convert_time_to_utc_timestamp(time_dict: Dict[str, int]) -> int:
        """
        Converts a time dictionary to a UTC time stamp, rounded to seconds

        :param time_dict: the time dictionary to be converted
        :return: the timestamp
        """

        date = str(time_dict["years"]) + "-" + str(time_dict["months"]) + "-" + str(time_dict["days"]) + ":"
        date += str(time_dict["hours"]) + "-" + str(time_dict["minutes"]) + "-" + str(time_dict["seconds"])
        date = time.strptime(date, "%Y-%m-%d:%H-%M-%S")

        return int(calendar.timegm(date))

    def background_process(self) -> None:
        """
        Background process that checks for due reminders and sends them to the sender if they are.

        :return: None
        """
        while True:

            for reminder_file_name in os.listdir(self.reminder_directory):
                reminder_file = os.path.join(self.reminder_directory, reminder_file_name)

                reminder_due_time = int(reminder_file_name.split("#", 1)[0])
                current_time = int(time.time())

                if current_time >= reminder_due_time:
                    receiver = reminder_file_name.split("@", 1)[1]

                    opened_file = open(reminder_file, 'r')
                    message_text = opened_file.read()
                    opened_file.close()
                    os.remove(reminder_file)

                    # noinspection PyTypeChecker
                    message = Message(message_text, "Reminder", receiver, False)

                    self.connection.send_text_message(message)

            time.sleep(1)
