# coding=utf-8
"""
Copyright 2015,2016 Hermann Krumrey

This file is part of messengerbot.

    messengerbot makes use of various third-party python modules to serve
    information via online chat services.

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

    identifier = ""
    """
    A unique identifier for the sender/receiver. Can also be the identifier for a group
    """

    single_identifier = ""
    """
    A unique identifier for a unique user in a group
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

    def __init__(self, message_body: str, message_title: str, address: str, incoming: bool,
                 identifier: str = "", name: str = "",
                 group: bool = False, single_address: str = "", single_identifier: str = "", single_name: str = "")\
            -> None:
        """
        Constructor for the Message class

        :param message_body: The actual message text
        :param message_title: The title of the message
        :param address: the sender address
        :param incoming: True is incoming message, False if outgoing
        :param identifier: the sender identifier
        :param name: the sender name
        :param group: True if this is a group. The following information must onl be entered when the message comes
                        from/is addressed at a group
        :param single_address: the address of the individual group participant
        :param single_identifier: the identifier of the individual group participant
        :param single_name: the name of the individual group participant
        """
        self.message_body = message_body
        self.message_title = message_title

        self.address = address
        self.identifier = identifier
        self.name = name
        self.group = group

        if incoming:
            self.incoming = True
        else:
            self.outgoing = True

        if self.group:
            self.single_address = single_address
            self.single_identifier = single_identifier
            self.single_name = single_name

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
