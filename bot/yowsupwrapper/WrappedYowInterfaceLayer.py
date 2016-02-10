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
        self.toLower(entity.get_entity())
