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
from kudubot.logger.PrintLogger import PrintLogger

from yowsup.layers import YowLayerEvent
from yowsup.layers.auth import AuthError
from yowsup.stacks import YowStackBuilder
from yowsup.layers.network import YowNetworkLayer
from yowsup.layers.interface import YowInterfaceLayer


class YowsupEchoStack(object):
    """
    The Yowsup Stack that handles the communication to the whatsapp servers
    """

    def __init__(self, bot_layer: YowInterfaceLayer, credentials, encryption_enabled=True) -> None:
        """
        :param bot_layer: The Yowsup layer to include in the stack
        :param credentials: The credentials used to log in on the whatsapp servers
        :param encryption_enabled: Flag to enable or disable encryption

        :return: None
        """
        stack_builder = YowStackBuilder()
        self.stack = stack_builder \
            .pushDefaultLayers(encryption_enabled) \
            .push(bot_layer) \
            .build()

        self.stack.setCredentials(credentials)

    def start(self) -> None:
        """
        Starts the Yowsup Loop

        :return: None
        """
        self.stack.broadcastEvent(YowLayerEvent(YowNetworkLayer.EVENT_STATE_CONNECT))
        try:
            self.stack.loop()
        except AuthError as e:
            PrintLogger.print("Authentication Error: %s" % str(e))
