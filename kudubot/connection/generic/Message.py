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


class Message(object):
    """
    Class that combines multipleattributes to model a generic message entity
    """

    outgoing = False
    """
    If set to True, this is an outgoing message
    """

    incoming = False
    """
    If set to True, this is an incoming message
    """

    group = False
    """
    If set to True, this is a group message
    """

    address = ""
    """
    The address of the sender/receiver. Can also be the address of a group
    """

    single_address = ""
    """
    If the message sender/receiver is a group, this is the address of the individual sender/receiver
    """

    name = ""
    """
    A friendly, human-readable name for the sender/receiver. Can also be the name of a group
    """

    single_name = ""
    """
    A friendly, human-readable name for the individual sender/receiver if in a group
    """

    message_body = ""
    """
    The body of the message
    """

    message_title = ""
    """
    The title of the message
    """

    timestamp = ""
    """
    The timestamp of the message's creation
    """

    def __init__(self, message_body: str, address: str, message_title: str = "", incoming: bool = False, name: str = "",
                 group: bool = False, single_address: str = "", single_name: str = "", timestamp: float = -1.0) -> None:
        """
        Constructor for the Message class. The only required parameters are the address and message body parameters

        :param message_body: The actual message text
        :param address: the sender address
        :param message_title: The title of the message
        :param incoming: True is incoming message, False if outgoing
        :param name: the sender name
        :param group: True if this is a group. The following information must only be entered when the message comes
                        from/is addressed at a group
        :param single_address: the address of the individual group participant
        :param single_name: the name of the individual group participant
        :param timestamp: The time stamp of the message creation
        """
        self.message_body = message_body
        self.message_title = message_title

        self.address = address
        self.name = name
        self.group = group

        self.incoming = incoming
        self.outgoing = not incoming

        if self.group:
            self.single_address = single_address
            self.single_name = single_name

        self.timestamp = time.time() if timestamp < 0.0 else timestamp

    def to_string(self) -> str:
        """
        Creates a string from the message's attributes

        :return: the message as a string
        """
        if self.incoming:
            message_as_string = "RECV: From " + str(self.address) + ": " + str(self.message_body)
        else:
            message_as_string = "SENT: To " + str(self.address) + ": " + str(self.message_body)

        return message_as_string

    def get_individual_address(self) -> str:
        """
        Always returns the address of the uniques user, even when in a group

        :return: the unique address
        """
        return self.single_address if self.group else self.address

    def get_user_name(self) -> str:
        """
        Returns the name of the user (not of a group)

        :return: the user's name
        """
        return self.single_name if self.group else self.name
