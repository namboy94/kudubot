"""
LICENSE:
Copyright 2015-2017 Hermann Krumrey

This file is part of kudubot.

    kudubot is a chat bot framework. It allows developers to write
    services for arbitrary chat services.

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

import time
from kudubot.users.Contact import Contact


class Message(object):
    """
    Class that models a message entity.
    """

    def __init__(self, message_title: str, message_body: str, receiver: Contact, sender: Contact,
                 sender_group: Contact = None, timestamp: float = None):
        """
        Initializes the Message object

        Since Messages may also come from chat groups, an optional group argument exists.
        A group is another contact, just like any other contact. Group messages must define
        a contact for the group as well as for the individual sender of the message.

        A Message object whose group is None is a private message.

        :param message_title: The title of the message. Not always applicable, depending on the connection
        :param message_body: The body of the message
        :param receiver: The recipient of the message, which is a Contact object
        :param sender: The sender of the message, which is a Contact object
        :param sender_group: Optionally the group Contact object if this is a message originating from a group
        :param timestamp: The timestamp of the message. If it is not specified, the current UNIX timestamp is used
        """
        self.message_title = message_title
        self.message_body = message_body
        self.receiver = receiver
        self.sender = sender
        self.sender_group = sender_group
        self.timestamp = timestamp if timestamp != -1.0 else time.time()
