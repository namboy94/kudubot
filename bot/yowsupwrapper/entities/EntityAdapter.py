# coding=utf-8
"""
Copyright 2015,2016 Hermann Krumrey

This file is part of whatsapp-bot.

    whatsapp-bot makes use of various third-party python modules to serve
    information via the online chat service Whatsapp.

    whatsapp-bot is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    whatsapp-bot is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with whatsapp-bot.  If not, see <http://www.gnu.org/licenses/>.
"""

# imports
from utils.encoding.Unicoder import Unicoder


class EntityAdapter(object):
    """
    A class that wraps around an entity to ensure non-camelcase style in the rest of the project
    It also takes care of encoding and decoding unicode
    """

    def __init__(self, original_entity):
        """
        Constructor
        :param original_entity: the original entity to be wrapped around
        :return: void
        """
        self.entity = original_entity

    def get_entity(self):
        """

        :return:
        """
        return self.entity

    def get_type(self):
        """
        Returns the entities' type
        :return: the type of the entity
        """
        return self.entity.getType()

    def ack(self, send=False):
        """

        :return:
        """
        return self.entity.ack(send)

    def get_time_stamp(self):
        """

        :return:
        """
        return self.entity.getTimestamp()

    def get_from(self, full=True):
        """

        :param full:
        :return:
        """
        return self.entity.getFrom(full)

    def get_participant(self, full=True):
        """

        :param full:
        :return:
        """
        return self.entity.getParticipant(full)

    def get_to(self, full=True):
        """

        :param full:
        :return:
        """
        return self.entity.getTo(full)

    def get_notify(self):
        """

        :return:
        """
        return self.entity.getNotify()

    def get_body(self):
        """

        :return:
        """
        return self.entity.getBody()

    def is_duplicate(self):
        """

        :return:
        """
        return self.entity.isDuplicate()

    def get_url(self):
        """

        :return:
        """
        return self.entity.getUrl()

    def get_ip(self):
        """

        :return:
        """
        return self.entity.getIp()

    def get_resume_offset(self):
        """

        :return:
        """
        return self.entity.getResumeOffset()