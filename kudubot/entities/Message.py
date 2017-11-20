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

import time
from typing import Dict
from kudubot.users.Contact import Contact
from kudubot.users.Contact import from_dict as contact_from_dict


class Message(object):
    """
    Class that models a message entity.
    """

    def __init__(self, message_title: str, message_body: str,
                 receiver: Contact, sender: Contact,
                 sender_group: Contact = None, timestamp: float = -1.0):
        """
        Initializes the Message object

        Since Messages may also come from chat groups,
        an optional group argument exists.
        A group is another contact, just like any other contact.
        Group messages must define a contact for the group as well as for the
        individual sender of the message.

        A Message object whose group is None is a private message.

        :param message_title: The title of the message. Not always applicable,
                              depending on the connection
        :param message_body: The body of the message
        :param receiver: The recipient of the message,
                         which is a Contact object
        :param sender: The sender of the message, which is a Contact object
        :param sender_group: Optionally the group Contact object if this is a
                             message originating from a group
        :param timestamp: The timestamp of the message.
                          If it is not specified,
                          the current UNIX timestamp is used
        """
        self.message_title = message_title
        self.message_body = message_body
        self.receiver = receiver
        self.sender = sender
        self.sender_group = sender_group
        self.timestamp = timestamp if timestamp != -1.0 else time.time()

    def get_direct_response_contact(self) -> Contact:
        """
        :return: The contact to which one can immediately respond to.
                 I.e. if the message came from a group,
                 this method will return the group contact,
                 private chats however will return the individual sender
        """
        return self.sender if self.sender_group is None else self.sender_group

    def to_dict(self) -> Dict[str, str or float or Dict[str, str or int]]:
        """
        :return: The message data as a dictionary which can be used
                 to store a message as a JSON file
        """

        sender_group = \
            None if self.sender_group is None else self.sender_group.to_dict()
        return {
            "message_title": self.message_title,
            "message_body": self.message_body,
            "sender": self.sender.to_dict(),
            "sender_group": sender_group,
            "receiver": self.receiver.to_dict(),
            "timestamp": self.timestamp,
        }


def from_dict(data: Dict[str, str or float or Dict[str, str or int]])\
        -> Message:
    """
    Generates a Message object from a dictionary

    :param data: The dictionary to turn into a Message
    :return: The generates Message object
    """

    if data["sender_group"] is None:
        sender_group = None
    else:
        sender_group = contact_from_dict(data["sender_group"])
    return Message(
        data["message_title"],
        data["message_body"],
        contact_from_dict(data["receiver"]),
        contact_from_dict(data["sender"]),
        sender_group,
        data["timestamp"]
    )
