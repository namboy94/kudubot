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

# imports
from yowsup.layers.protocol_messages.protocolentities import MessageProtocolEntity


# noinspection PyUnresolvedReferences
class EntityAdapter(object):
    """
    A class that wraps around an entity to ensure non-camelcase style in the rest of the project
    It also takes care of encoding and decoding unicode
    """

    def __init__(self, original_entity: MessageProtocolEntity) -> None:
        """
        Constructor of the EntityAdapter

        :param original_entity: the original entity to be wrapped around
        :return: None
        """
        self.entity = original_entity

    def get_entity(self) -> MessageProtocolEntity:
        """
        Returns the original entitiy

        :return: the original entity
        """
        return self.entity

    def get_type(self) -> str:
        """
        Returns the entities' type

        :return: the type of the entity
        """
        return self.entity.getType()

    def ack(self, send: bool = False) -> object:
        """
        Wraps the ack() method

        :param send: The send variable
        :return: Don't know
        """
        return self.entity.ack(send)

    def get_time_stamp(self) -> str:
        """
        Gets the time stamp of the wrapped entity

        :return: the time stamp of the entity
        """
        return self.entity.getTimestamp()

    def get_from(self, full: bool = True) -> str:
        """
        Returns the sender of the message

        :param full: flag to get the full number of the message's sender
        :return: the sender of the message
        """
        return self.entity.getFrom(full)

    def get_participant(self, full=True) -> str:
        """
        Returns the specific user that sent the message when in a group

        :param full: flag to get the full number of the message's sender
        :return: the specific user that sent the message when in a group
        """
        return self.entity.getParticipant(full)

    def get_to(self, full: bool = True) -> str:
        """
        Returns the receiver of the message

        :param full: flag to get the full number of the message's receiver
        :return: the receiver of the message
        """
        return self.entity.getTo(full)

    def get_notify(self) -> str:
        """
        Gets the user name of the entity's sender/receiver
        :return: the user name
        """
        return self.entity.getNotify()

    def get_body(self) -> str:
        """
        Gets the message body of the entity
        :return: the message body
        """
        return self.entity.getBody()

    def is_duplicate(self) -> bool:
        """
        Check if the entity is a duplicate?
        :return: True or False
        """
        return self.entity.isDuplicate()

    def get_url(self) -> str:
        """
        Wrapps around the getUrl() method
        :return: the url
        """
        return self.entity.getUrl()

    def get_ip(self) -> str:
        """
        Wrapps around the getIp() method
        :return: the ip
        """
        return self.entity.getIp()

    def get_resume_offset(self) -> str:
        """
        Wrapps around the getResumeOffset() method
        :return: the resume offset
        """
        return self.entity.getResumeOffset()
