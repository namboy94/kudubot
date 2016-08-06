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
import time
from threading import Thread
from telegram.error import NetworkError, Unauthorized
from kudubot.connection.telegram.TelegramConnection import TelegramConnection


class SimpleTelegramConnection(TelegramConnection):
    """
    A simple Telegram Connection without a lot of the generic Connection's functionality
    """

    def __init__(self, api_key: str, on_message_callback: callable) -> None:
        super().__init__(api_key)
        self.on_incoming_message = on_message_callback

    def initialize(self) -> None:
        """
        Overrides the initialize method to do nothing

        :return: None
        """
        pass

    @staticmethod
    def establish_async_connection(api_key: str, callback: callable) -> 'SimpleTelegramConnection':
        """
        Establishes the connection to the telegram service

        :param api_key: the API key of the bot
        :param callback: the callback method for handling messages
        :return: the simple telegram connection
        """
        telegram_connection = SimpleTelegramConnection(api_key, callback)

        def poll():
            """
            Polls the bot continuously

            :return: None
            """

            while True:

                try:
                    messages = telegram_connection.get_messages()
                    for message in messages:
                        telegram_connection.on_incoming_message(message)
                except (Unauthorized, NetworkError):
                    # The user has removed or blocked the bot.
                    telegram_connection.update_id += 1

                time.sleep(1)

        thread = Thread(target=poll)
        thread.daemon = True
        thread.start()

        return telegram_connection
