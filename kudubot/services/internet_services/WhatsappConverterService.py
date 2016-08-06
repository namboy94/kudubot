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
import sqlite3

from puffotter.fileops import ensure_directory_exists, ensure_sqlite3_db_exists
from kudubot.servicehandlers.Service import Service
from kudubot.connection.generic.Message import Message
from kudubot.config.LocalConfigChecker import LocalConfigChecker


class WhatsappConverterService(Service):
    """
    Class that converts incoming Whatsapp messages. It also allows the user to reply.
    """

    identifier = "whatsapp_convert"
    """
    The identifier for this service
    """

    help_description = {"en": "/wc\tThe Whatsapp Converter\n"
                              "syntax:\n"
                              "/wc start (starts the whatsapp converter)\n"
                              "/wc register \"whatsapp-number\" \"telegram-api-key\"\n"
                              "/wc send <\"recipient\"> \"message\" (sends a message to the recipient)",
                        "de": "/wc\tDer Whatsapp Konvertierer\n"
                              "Syntax:\n"
                              "/wc start (startet den Whatsapp Konvertierer)\n"
                              "/wc register \"whatsapp-number\" \"telegram-api-key\"\n"
                              "/wc send <\"recipient\"> \"message\" (sendet eine Nachricht zum Empfänger)"}
    """
    Help description for this service.
    """

    whatsapp_connection = None
    """
    The internal Whatsapp connection
    """

    owner = None
    """
    The 'owner' of the telegram bot, i.e. the person that activated the converter
    """

    last_sender = None
    """
    The last sender, useful for simplifying the syntax
    """

    addressbook = os.path.join(LocalConfigChecker.contacts_directory, "whatsapp", "addressbook.db")
    """
    The addressbook database file path
    """

    telegram_bot_db = ""
    """
    Path to the telegram bot directory
    """

    telegram_bots = {}
    """
    List of telegram listeners
    """

    def process_message(self, message: Message) -> None:
        """
        Processes the message, either starting the whatsapp connection or sending a new message

        :param message: the message to process
        :return: None
        """
        WhatsappConverterService.telegram_bot_db = os.path.join(LocalConfigChecker.services_directory,
                                                                self.connection.identifier,
                                                                "whatsapp_convert",
                                                                "telegrambots.db")

        sql_init = "CREATE TABLE Bots (whatsapp_address TEXT, telegram_api_key TEXT)"

        ensure_directory_exists(os.path.dirname(WhatsappConverterService.telegram_bot_db))
        ensure_sqlite3_db_exists(WhatsappConverterService.telegram_bot_db, sql_init, True)

        # Import here to avoid import errors
        from kudubot.connection.whatsapp.wrappers.ForwardedWhatsappConnection import ForwardedWhatsappConnection

        if not self.connection.authenticator.is_from_admin(message):
            self.connection.send_text_message(Message("Sorry, only admins are allowed to do that", message.address))
        elif self.connection.identifier != "telegram":
            self.connection.send_text_message(Message("The service is already running", message.address))

        elif message.message_body.lower().startswith("/wc start"):

            if WhatsappConverterService.whatsapp_connection is not None:
                return

            ForwardedWhatsappConnection.establish_connection()
            WhatsappConverterService.whatsapp_connection = ForwardedWhatsappConnection.singleton_variable
            WhatsappConverterService.whatsapp_connection.set_callback(self.forward_message)
            WhatsappConverterService.owner = message.address
            self.connection.send_text_message(Message("Whatsapp Converter Started", message.address))
            self.initialize_telegram_listeners()

        elif message.message_body.lower().startswith("/wc register"):

            whatsapp_address = message.message_body.split("\"", 1)[1].split("\"", 1)[0]
            telegram_key = message.message_body.rsplit("\"", 2)[1]

            database = sqlite3.connect(WhatsappConverterService.telegram_bot_db)

            insertion = "INSERT INTO Bots (whatsapp_address, telegram_api_key) VALUES(?, ?)"
            database.execute(insertion, (whatsapp_address, telegram_key))
            database.commit()
            database.close()

            self.connection.send_text_message(Message("New Telegram API key stored", message.address))

            if WhatsappConverterService.whatsapp_connection is not None:
                self.initialize_single_telegram_listener(telegram_key, whatsapp_address)

        elif message.message_body.lower().startswith("/wc msg"):

            receiver = message.message_body.split("\"", 1)[1].split("\"", 1)[0]
            message_text = message.message_body.rsplit("\"", 2)[1]

            if receiver == message_text:
                receiver = WhatsappConverterService.last_sender

            if receiver is None:
                return

            database = sqlite3.connect(self.addressbook)
            query = database.execute("SELECT address FROM Contacts WHERE name = ?", (receiver,)).fetchall()
            database.close()

            if len(query) > 0:
                receiver = query[0][0]

            whatsapp_message = Message(message_text, receiver)
            WhatsappConverterService.whatsapp_connection.send_text_message(whatsapp_message)

    def forward_message(self, message: Message) -> None:
        """
        Forwards a Whatsapp message to the connected service
        WHATSAPP->TELEGRAM

        :return: None
        """
        database = sqlite3.connect(self.telegram_bot_db)
        query = database.execute("SELECT telegram_api_key FROM Bots WHERE whatsapp_address = ?", (message.address,))\
            .fetchall()
        database.close()

        if len(query) != 0:

            message_text = message.message_body
            if message.group:
                message_text = message.single_name + ":\n" + message_text

            telegram_bot = WhatsappConverterService.telegram_bots[query[0][0]]
            telegram_bot.send_text_message(Message(message_text, WhatsappConverterService.owner))

        else:
            message_text = "Sender\n" + message.address + "\n" + message.name + "\n\n" + message.message_body
            forward_message = Message(message_text, WhatsappConverterService.owner)
            WhatsappConverterService.last_sender = message.address
            self.connection.send_text_message(forward_message)

    # noinspection PyUnresolvedReferences
    def initialize_telegram_listeners(self) -> None:
        """
        Initializes existing Telegram bots for contacts with API keys

        :return: None
        """
        database = sqlite3.connect(self.telegram_bot_db)
        query = database.execute("SELECT whatsapp_address, telegram_api_key FROM Bots").fetchall()
        database.close()

        for contact in query:

            whatsapp_address = contact[0]
            key = contact[1]
            self.initialize_single_telegram_listener(key, whatsapp_address)

    # noinspection PyUnresolvedReferences,PyMethodMayBeStatic
    def initialize_single_telegram_listener(self, api_key: str, whatsapp_address: str) -> 'SimpleTelegramConnection':
        """
        Initializes a single Telegram listener bot

        :param api_key: the bot's API key
        :param whatsapp_address: the whatsapp address linked to this bot
        :return: None
        """
        # import here to avoid import errors:
        from kudubot.connection.telegram.wrappers.SimpleTelegramConnection import SimpleTelegramConnection

        def forward_message_to_whatsapp(message: Message) -> None:
            """
            Forwards a message to the Whatsapp service

            :param message: the message to forward
            :return: None
            """
            WhatsappConverterService.whatsapp_connection.send_text_message(
                Message(message.message_body, whatsapp_address))

        bot = SimpleTelegramConnection.establish_async_connection(api_key, forward_message_to_whatsapp)
        WhatsappConverterService.telegram_bots[api_key] = bot

    @staticmethod
    def regex_check(message: Message) -> bool:
        """
        Checks if the user input is valid for this service to continue

        :return: True if input is valid, False otherwise
        """
        regex = "^/wc (start|register \"[^\"]+\" \"[^\"]+\"|msg \"[^\"]+\"( \"[^\"]+\")?)$"
        return re.search(re.compile(regex), message.message_body.lower())
