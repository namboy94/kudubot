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
from yowsup.layers.protocol_messages.protocolentities import TextMessageProtocolEntity
from utils.encoding.Unicoder import Unicoder
from yowsupwrapper.entities.EntityAdapter import EntityAdapter

import re


class WrappedTextMessageProtocolEntity(EntityAdapter):
    """

    """

    def __init__(self, body, to=None, _from=None):
        """

        :param body:
        :param to:
        :return:
        """
        if _from is not None:
            if re.compile("[0-9]+-[0-9]+").match(_from.split("@")[0]):
                body = Unicoder.fix_incoming_unicode(body)
        super().__init__(TextMessageProtocolEntity(body, to=to, _from=_from))

    def get_entity(self):
        """

        :return:
        """
        body = self.entity.getBody()
        if re.compile("[0-9]+-[0-9]+").match(self.entity.getTo(True).split("@")[0]):
            body = Unicoder.fix_outgoing_unicode(body)
            return TextMessageProtocolEntity(body, to=self.entity.getTo(True))
        else:
            return self.entity
