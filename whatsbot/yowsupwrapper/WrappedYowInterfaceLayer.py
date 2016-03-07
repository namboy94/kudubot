# coding=utf-8
"""
Copyright 2015,2016 Hermann Krumrey

This file is part of whatsbot.

    whatsbot makes use of various third-party python modules to serve
    information via the online chat service Whatsapp.

    whatsbot is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    whatsbot is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with whatsbot.  If not, see <http://www.gnu.org/licenses/>.
"""

# imports
from yowsup.layers.interface import YowInterfaceLayer


class WrappedYowInterfaceLayer(YowInterfaceLayer):
    """
    A class that adapts the YowInterfaceLayer to offer normally styled python
    methods and variables
    """

    def to_lower(self, entity):
        """
        Processes a yowsup entity
        :param entity: the entity to be processed
        :return: void
        """
        try:
            self.toLower(entity.get_entity())
        except Exception as e:
            str(e)
            self.toLower(entity)

    def send_iq(self, entity, success_fn, error_fn):
        """

        :param entity:
        :param success_fn:
        :param error_fn:
        :return:
        """
        return self._sendIq(entity, success_fn, error_fn)

    def get_own_jid(self):
        """

        :return:
        """
        return self.getOwnJid()
