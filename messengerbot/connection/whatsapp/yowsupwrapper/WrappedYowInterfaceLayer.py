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
    along with whatsbot.  If not, see <http://www.gnu.org/licenses/>.
"""

# imports
from yowsup.layers.interface import YowInterfaceLayer
from yowsup.layers.protocol_messages.protocolentities import MessageProtocolEntity

from messengerbot.connection.whatsapp.yowsupwrapper.entities.EntityAdapter import EntityAdapter


class WrappedYowInterfaceLayer(YowInterfaceLayer):
    """
    A class that adapts the YowInterfaceLayer to offer PEP compatible
    methods and variables instead of CamelCased ones.
    """

    # Required local variables
    accountDelWarnings = 0
    connected = False
    username = None
    sendReceipts = True
    disconnectAction = 0
    credentials = None
    jid_aliases = {}

    def to_lower(self, entity: MessageProtocolEntity or EntityAdapter) -> None:
        """
        Processes a yowsup entity, i.e. sends it to via the Whatsapp Network

        :param entity: the entity to be processed. Can be either a WrappedEntity or a normal yowsup entity
        :return: None
        """
        try:
            self.toLower(entity.get_entity())
        except AttributeError:
            self.toLower(entity)

    def send_iq(self, entity: MessageProtocolEntity, success_fn: callable, error_fn: callable) -> None:
        """
        Used whenerver media files are sent

        :param entity: the entity to send
        :param success_fn: function to be called when successful
        :param error_fn: function to be called when unsuccessful
        :return: None
        """
        return self._sendIq(entity, success_fn, error_fn)

    def get_own_jid(self) -> str:
        """
        Calculates the own JID and returns it

        :return: the own JID
        """
        return self.getOwnJid()
