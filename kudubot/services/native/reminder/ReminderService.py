"""
Copyright 2015-2017 Hermann Krumrey

This file is part of kudubot.

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
"""

import datetime
import re
import time
from typing import Dict

from kudubot.entities.Message import Message
from kudubot.services.HelperService import HelperService
from kudubot.services.native.reminder.database import initialize_database, \
    store_reminder, get_unsent_reminders, \
    mark_reminder_sent, convert_datetime_to_string


class ReminderService(HelperService):
    """
    Class that implements a Service for the Kudubot framework that allows
    users to store reminder message that are then sent at a later time
    """

    def init(self):
        """
        Initializes the database table and starts a background thread that
        perpetually searches for expired reminders
        """
        self.initialize_database_table(initializer=initialize_database)
        self.start_daemon_thread(self.background_loop)

    @staticmethod
    def define_identifier() -> str:
        """
        Defines the identifier for this service

        :return: The Service's identifier
        """
        return "reminder"

    def define_command_name(self, language: str):
        """
        Defines the command name for this service
        :param language: the language in which to get the command name
        :return: The command name in the specified language
        """
        return {"en": "/remind", "de": "/erinner"}[language]

    def define_language_text(self) -> Dict[str, Dict[str, str]]:
        """
        :return: A dictionary used to translate any user-facing messages
        """
        return {
            "@remind_command": {"en": "/remind", "de": "/erinner"},
            "@list_argument": {"en": "list", "de": "auflisten"},
            "@second_singular": {"en": "second", "de": "sekunde"},
            "@second_plural": {"en": "seconds", "de": "sekunden"},
            "@minute_singular": {"en": "minute", "de": "minute"},
            "@minute_plural": {"en": "minutes", "de": "minuten"},
            "@hour_singular": {"en": "hour", "de": "stunde"},
            "@hour_plural": {"en": "hours", "de": "stunden"},
            "@day_singular": {"en": "day", "de": "tag"},
            "@day_plural": {"en": "days", "de": "tage"},
            "@week_singular": {"en": "week", "de": "woche"},
            "@week_plural": {"en": "weeks", "de": "wochen"},
            "@year_singular": {"en": "year", "de": "jahr"},
            "@year_plural": {"en": "years", "de": "jahre"},
            "@stored_reply_title": {
                "en": "Message Stored", "de": "Nachricht gespeichert"
            },
            "@stored_confirmation_message": {
                "en": "The reminder message has successfully been stored.",
                "de": "Die Erinnerungsnachricht wurde erfolgreich gespeichert"
            },
            "@list_stored_message_start": {
                "en": "The following reminders are pending",
                "de": "Die folgenden Erinnerungen stehen noch aus"
            },
            "@list_response_title": {
                "en": "List of Reminders", "de": "Liste der Erinnerungen"
            },
            "@invalid_title": {
                "en": "Invalid Reminder", "de": "Ungültige Erinnerung"
            },
            "@invalid_message": {
                "en": "The reminder is invalid. "
                      "Please consult /remind syntax for more information.",
                "de": "Die Erinnerung ist fehlerhaft."
                      "Sehe dir die /erinner syntax an, "
                      "und versuch es dann noch einmal."
            }
        }

    def handle_message(self, message: Message):
        """
        Handles a message received by the Service

        :param message: The message to handle
        :return: None
        """
        target = message.get_direct_response_contact()
        command = self.parse_message(message.message_body.strip(),
                                     self.determine_language(message))

        if command["mode"] == "store":
            store_reminder(self.connection.db,
                           command["data"]["message"],
                           command["data"]["due_time"],
                           target.database_id)
            self.reply_translated("@stored_reply_title",
                                  "@stored_confirmation_message", message)

        elif command["mode"] == "list":
            reminders = list(filter(
                lambda x: x["receiver"].database_id == target.database_id,
                get_unsent_reminders(self.connection.db)
            ))
            text = "@list_stored_message_start:\n\n"
            for reminder in reminders:
                text += convert_datetime_to_string(reminder["due_time"])
                text += ":" + reminder["message"] + "\n"
            self.reply_translated("@list_response_title", text, message)

        elif command["mode"] == "invalid":
            self.reply_translated(
                "@invalid_title", "@invalid_message", message)

    def is_applicable_to(self, message: Message) -> bool:
        """
        Checks if the Service is applicable to a message

        :param message: The message to check
        :return: True if the Service is applicable, otherwise False
        """
        language = self.determine_language(message)
        body = message.message_body.lower().strip()

        regex = "^@remind_command ([0-9]+ (" \
                "@second_singular|@second_plural|@minute_singular|" \
                "@minute_plural|@hour_singular|@hour_plural|" \
                "@day_singular|@day_plural|@week_singular|@week_plural" \
                "|@year_singular|@year_plural) )+" \
                "\"[^\"]+\"$"
        lang_regex = re.compile(self.translate(regex, language))

        return re.match(lang_regex, body) \
            or body == self.translate(
                "@remind_command @list_argument", language)

    def background_loop(self):
        """
        Perpetually checks for expiring reminders.

        :return: None
        """
        db = self.connection.get_database_connection_copy()
        while True:
            unsent = get_unsent_reminders(db)

            for reminder in unsent:

                due_time = reminder["due_time"].timestamp()
                now = datetime.datetime.utcnow().timestamp()
                if due_time < now:

                    self.connection.send_message(Message(
                        "Reminder",
                        reminder["message"],
                        reminder["receiver"],
                        self.connection.user_contact)
                    )
                    mark_reminder_sent(db, reminder["id"])

            time.sleep(1)

    def define_syntax_description(self, language: str) -> str:
        """
        Defines the syntax with which the user can interact with this service

        :param language: The language to use
        :return: The syntax description in the specified language
        """
        return {
            "en": "Set a reminder:\n"
                  "/remind X second(s) \"Message\"\n"
                  "/remind X minute(s) \"Message\"\n"
                  "/remind X hour(s) \"Message\"\n"
                  "/remind X day(s) \"Message\"\n"
                  "/remind X week(s) \"Message\"\n"
                  "/remind X year(s) \"Message\"\n"
                  "/remind tomorrow \"Message\"\n"
                  "/remind next week \"Message\"\n"
                  "/remind next year \"Message\"\n\n"
                  "Combinations:\n"
                  "/remind X hours Y minutes Z seconds \"Message\"\n\n"
                  "List pending reminders:\n"
                  "/remind list",
            "de": "Erinnerung setzen:\n"
                  "/erinner X sekunde(n) \"Message\"\n"
                  "/erinner X minute(n) \"Message\"\n"
                  "/erinner X stunde(n) \"Message\"\n"
                  "/erinner X tag(e) \"Message\"\n"
                  "/erinner X woche(n) \"Message\"\n"
                  "/erinner X jahr(e) \"Message\"\n"
                  "/erinner morgen \"Message\"\n"
                  "/erinner nächste woche \"Message\"\n"
                  "/erinner nächstes jahr \"Message\"\n\n"
                  "Kombinationen:\n"
                  "/erinner X stunden Y minuten Z sekunden \"Message\"\n\n"
                  "Gespeicherte Erinnerungen auflisten:\n"
                  "/erinner auflisten"
        }[language]

    def determine_language(self, message: Message) -> str:
        """
        Determines the language used in a message

        :param message: The message to analyse
        :return: The language that was found
        """

        if message.message_body.startswith("/erinner"):
            return "de"
        else:
            return "en"

    def define_help_message(self, language: str) -> str:
        """
        Defines the help message for this service in various languages

        :param language: The language to be used
        :return: The help description in the specified language
        """
        return {
            "en": "The reminder service allows you to store a reminder "
                  "on the server to be sent back to you at a specified time. "
                  "See /remind syntax for possible ways "
                  "to use the reminder service.",
            "de": "Der Erinnerungsdienst erlaubt es einem Nutzer eine "
                  "Erinnerung auf dem Server zu speichern, welcher dann zu"
                  "einem spezifizierten Zeitpunkt zurückgesendet wird. "
                  "Sehe dir /erinner syntax an, um dir ein Bild davon zu "
                  "machen wie man den Erinnerungsdienst verwendet."
        }[language]

    def parse_message(self, text: str, language: str) \
            -> Dict[str, str or Dict[str, str or datetime]]:
        """
        Parses the message and determines the mode of operation

        :param text: The text to parse
        :param language: The language in which to parse the text
        :return: A dictionary with at least the key 'status' with three
                 different possible states:
                 - no-match: The message does not match the command syntax
                 - help:     A query for the help message.
                             Will result in the help message being
                             sent to the sender
                 - store:    Command to store a new reminder
        """
        self.logger.debug("Parsing message")

        if self.translate("@remind_command @list_argument", language) \
                == text.lower():
            return {"mode": "list"}
        else:

            time_string = text.lower().split(" \"")[0].split(
                self.translate("@remind_command ", language))[1]
            reminder_message = text.split("\"")[1]

            usertime = self.parse_time_string(time_string.strip(), language)

            if usertime is None:
                self.logger.debug("Invalid reminder message")
                return {"mode": "invalid"}
            else:
                self.logger.debug("Will store reminder")
                return {
                    "mode": "store",
                    "data": {
                        "message": reminder_message,
                        "due_time": usertime
                    }
                }

    def parse_time_string(self, time_string: str, language: str) \
            -> datetime or None:
        """
        Parses a time string like '1 week' or '2 weeks 1 day' etc. and returns
        a datetime object with the specified time difference to the current
        time.

        :param time_string: The time string to parse
        :param language: In which language the string should be parsed
        :return: The parsed datetime object or None in case the parsing failed
        """

        # turn all units into english singular units
        for unit in ["second", "minute", "hour", "day", "week", "year"]:

            # The order is very important here!
            for mode in ["plural", "singular"]:

                key = "@" + unit + "_" + mode
                text = self.translate(key, language)
                time_string = time_string.replace(text, unit)

        now = datetime.datetime.utcnow()
        parsed = time_string.split(" ")

        try:
            for i in range(0, len(parsed), 2):

                value = int(parsed[i])
                key = parsed[i + 1]

                if key == "year":
                    now += datetime.timedelta(days=value * 365)
                elif key == "week":
                    now += datetime.timedelta(weeks=value)
                elif key == "day":
                    now += datetime.timedelta(days=value)
                elif key == "hour":
                    now += datetime.timedelta(hours=value)
                elif key == "minute":
                    now += datetime.timedelta(minutes=value)
                elif key == "second":
                    now += datetime.timedelta(seconds=value)
                else:
                    self.logger.debug("Invalid time keyword " + key + " used")
                    return None

            return now

        # Datetime exception, too high date values
        except (ValueError, OverflowError):
            return None
