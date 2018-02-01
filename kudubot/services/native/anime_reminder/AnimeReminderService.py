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


import re
import time
import requests
from typing import Dict
from kudubot.entities.Message import Message
from kudubot.services.HelperService import HelperService
from kudubot.services.native.anime_reminder.scraper import \
    scrape_reddit_discussion_threads
from kudubot.services.native.anime_reminder.database import \
    initialize_database, store_subscription, delete_subscription, \
    get_subscriptions, thread_exists, store_thread


class AnimeReminderService(HelperService):
    """
    The Kudubot Service that provides the anime reminder functionality
    """

    def init(self):
        """
        In addition to the normal initialization of a Service,
        this service initializes
        its database and starts the background thread
        """
        self.initialize_database_table(initializer=initialize_database)
        self.start_daemon_thread(self.background_loop)

    @staticmethod
    def define_identifier() -> str:
        """
        :return: The service's identifier
        """
        return "anime_reminder"

    def handle_message(self, message: Message):
        """
        Handles a message from the user

        :param message: The message to handle
        :return: None
        """
        mode = message.message_body.split(" ")[1].lower()
        user = message.get_direct_response_contact()
        user_id = user.database_id

        params = message.message_body.split("\"")
        show = "" if len(params) < 2 else params[1]

        if mode in [self.translate("@subscribe_command", x)
                    for x in self.supported_languages()]:

            result = "@successful_add_message" \
                if store_subscription(user_id, show, self.connection.db) \
                else "@exists_message"
            self.reply_translated("@reply_title", "@subscribe_message_start " +
                                  show + " " + result + ".", message)

        elif mode in [self.translate("@unsubscribe_command", x)
                      for x in self.supported_languages()]:

            result = "@successful_remove_message" \
                if delete_subscription(user_id, show, self.connection.db) \
                else "@does_not_exist_message"
            self.reply_translated("@reply_title",
                                  "@unsubscribe_message_start " + show +
                                  " " + result + ".", message)

        elif mode in [self.translate("@list_command", x)
                      for x in self.supported_languages()]:

            message_text = "@subscription_list_message:\n\n"
            for subscription in get_subscriptions(self.connection.db, user_id):
                message_text += subscription["show_name"] + "\n"
            self.reply_translated("@reply_title", message_text, message)

    def is_applicable_to(self, message: Message) -> bool:
        """
        Checks if a message is applicable to this Service

        :param message: The message to check
        :return: None
        """
        applicable = False
        for language in self.supported_languages():

            regex = "^@command_name " \
                    "(@list_command|@sub_unsub_command \"[^\"]+\")$"
            regex = re.compile(self.translate(regex, language))
            applicable = bool(re.search(regex, message.message_body)) \
                or applicable

        return applicable

    def define_syntax_description(self, language: str) -> str:
        """
        Defines the syntax description for the Service

        :param language: The language in which to display the syntax
                         description
        :return: The syntax description in the specified language
        """
        skeleton = "@command_name @list_command\n"
        skeleton += "@command_name @subscribe_command " \
                    "\"@show_name_parameter\"\n"
        skeleton += "@command_name @unsubscribe_command " \
                    "\"@show_name_parameter\""
        return self.translate(skeleton, language)

    def define_language_text(self) -> Dict[str, Dict[str, str]]:
        """
        Defines the Language strings for the service for the implemented
        languages

        :return: The dictionary used to translate strings
        """
        return {
            "@list_command": {"en": "list",
                              "de": "auflisten"},
            "@subscribe_command": {"en": "subscribe",
                                   "de": "abonnieren"},
            "@unsubscribe_command": {"en": "unsubscribe",
                                     "de": "abbestellen"},
            "@sub_unsub_command": {"en": "(un)?subscribe",
                                   "de": "(abonnieren|abbestellen)"},
            "@show_name_parameter": {"en": "Show Name",
                                     "de": "Serienname"},
            "@command_name": {"en": "/anime-remind",
                              "de": "/anime-erinner"},
            "@exists_message": {"en": "already exists",
                                "de": "existiert bereits"},
            '@does_not_exist_message': {"en": "does not exist",
                                        "de": "existiert nicht"},
            '@successful_add_message': {"en": "successful",
                                        "de": "wurde erfolgreich abonniert"},
            '@successful_remove_message': {"en": "successfully removed",
                                           "de": "wurde erfolgreich "
                                                 "abbestellt"},
            "@subscribe_message_start": {"en": "Subscription for",
                                         "de": "Abonnement für"},
            "@unsubscribe_message_start": {"en": "Subscription for",
                                           "de": "Abonnement für"},
            "@reply_title": {"en": "Anime Reminder",
                             "de": "Anime Erinnerung"},
            "@remind_title": {"en": "Anime Reminder",
                              "de": "Anime Erinnerung"},
            "@subscription_list_message": {"en": "You are subscribed to the"
                                                 "following shows",
                                           "de": "Du hast folgende Serien"
                                                 "abonniert"},
            "@episode": {"en": "episode",
                         "de": "Episode"},
            "@has_been_released": {"en": "has been released! Discuss it"
                                         "on reddit",
                                   "de": "wurde veröffentlicht! Diskuttier"
                                         "sie auf reddit"},
            "@help_message": {
                "en": "The Anime Reminder Service periodically checks for new "
                      "anime discussion threads on reddit's "
                      "r/anime board. A user can subscribe to specific shows "
                      "and will then be notified whenever a "
                      "new thread appears, which usually coincides with the "
                      "point in time that the episode is "
                      "available on streaming services like Crunchyroll, "
                      "Amazon or Funimation.\n"
                      "Users can also unsubscribe from shows and list all "
                      "their subscriptions. Subscription names "
                      "are case-insensitive.",
                "de": "Der Anime Erinnerungs-Service schaut in periodischen "
                      "Abständen nach, ob neue Anime Diskussionen "
                      "auf reddit.com/r/anime entstanden sind, welche neue "
                      "Anime Episode diskuttieren. Ein Nutzer kann "
                      "einzelne Serien abonnieren und wieder abbestellen. "
                      "Für abonnierte Serien erhält der Nutzer "
                      "eine Nachricht sobal eine neue Episode verfügbar ist."
                      "Die Namen für die Abonnements achten nicht auf Groß- "
                      "und Kleinschreibung. Man kann auch alle"
                      "Abonnements die derzeit aktiv sind auflisten lassen."
            }
        }

    def define_help_message(self, language: str) -> str:
        """
        Defines the help message for the service

        :param language: The target language to translate the message to
        :return: The help message in the specified language
        """
        return self.translate("@help_message", language)

    def determine_language(self, message: Message) -> str:
        """
        Determines the language used based on the incoming message

        :param message: The message to analyze
        :return: The language key to use
        """
        if message.message_body.startswith(self.define_command_name("de")):
            return "de"
        else:
            return "en"

    def define_command_name(self, language: str) -> str:
        """
        Defines the command name for the anime-remind functionality

        :param language: The language for which the command is valid
        :return: The command name in the specified language
        """
        return self.translate("@command_name", language)

    def background_loop(self):
        """
        Starts a new thread which will continuously check for new anime
        discussion threads on reddit.com/r/anime
        and notify users if they are subscribed to those shows

        :return: None
        """
        db = self.connection.get_database_connection_copy()
        while True:

            try:
                new_threads = scrape_reddit_discussion_threads()
            except requests.exceptions.ConnectionError:
                self.logger.error("Failed to connect")
                time.sleep(60)
                continue

            self.logger.debug("Checking for due subscriptions")

            for thread in new_threads:

                if not thread_exists(thread, db):
                    store_thread(thread, db)

                    for subscription in get_subscriptions(db):
                        if subscription["show_name"].lower() \
                                == thread["show_name"].lower():

                            receiver = self.connection.address_book\
                                .get_contact_for_id(
                                    subscription["user_id"], db
                                )

                            message_text = thread["show_name"] + " @episode "
                            message_text += str(thread["episode"])
                            message_text += " @has_been_released: "
                            message_text += thread["url"]

                            language = self.connection.language_selector.\
                                get_language_preference(
                                    receiver.database_id, db=db
                                )

                            message_text = \
                                self.translate(message_text, language)
                            title = self.translate("@remind_title", language)

                            self.connection.send_message(Message(
                                title, message_text, receiver,
                                self.connection.user_contact)
                            )

            time.sleep(60)
