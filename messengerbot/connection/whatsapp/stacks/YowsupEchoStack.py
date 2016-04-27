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
from yowsup.stacks import YowStack
from yowsup.layers import YowLayerEvent
from yowsup.layers import YowParallelLayer
from yowsup.layers.auth import YowCryptLayer
from yowsup.layers.coder import YowCoderLayer
from yowsup.layers.logger import YowLoggerLayer
from yowsup.layers.network import YowNetworkLayer
from yowsup.layers.interface import YowInterfaceLayer
from yowsup.layers.protocol_iq import YowIqProtocolLayer
from yowsup.layers.protocol_acks import YowAckProtocolLayer
from yowsup.layers.stanzaregulator import YowStanzaRegulator
from yowsup.layers.auth import YowAuthenticationProtocolLayer
from yowsup.layers.protocol_calls import YowCallsProtocolLayer
from yowsup.layers.protocol_media import YowMediaProtocolLayer
from yowsup.layers.protocol_messages import YowMessagesProtocolLayer
from yowsup.layers.protocol_receipts import YowReceiptProtocolLayer


class YowsupEchoStack(object):
    """
    The Yowsup Stack that handles the communication to the whatsapp servers
    """

    def __init__(self, bot_layer: YowInterfaceLayer, credentials, encryption_enabled=False) -> None:
        """
        :param bot_layer: The Yowsup layer to include in the stack
        :param credentials: The credentials used to log in on the whatsapp servers
        :param encryption_enabled: Flag to enable or disable encryption

        :return: None
        """
        if encryption_enabled:
            from yowsup.layers.axolotl import YowAxolotlLayer
            layers = (
                bot_layer,
                YowParallelLayer([YowAuthenticationProtocolLayer,
                                  YowMessagesProtocolLayer,
                                  YowReceiptProtocolLayer,
                                  YowAckProtocolLayer,
                                  YowMediaProtocolLayer,
                                  YowIqProtocolLayer,
                                  YowCallsProtocolLayer]),
                YowAxolotlLayer,
                YowLoggerLayer,
                YowCoderLayer,
                YowCryptLayer,
                YowStanzaRegulator,
                YowNetworkLayer
            )
        else:
            layers = (
                bot_layer,
                YowParallelLayer([YowAuthenticationProtocolLayer,
                                  YowMessagesProtocolLayer,
                                  YowReceiptProtocolLayer,
                                  YowAckProtocolLayer,
                                  YowMediaProtocolLayer,
                                  YowIqProtocolLayer,
                                  YowCallsProtocolLayer]),
                YowLoggerLayer,
                YowCoderLayer,
                YowCryptLayer,
                YowStanzaRegulator,
                YowNetworkLayer
            )

        self.stack = YowStack(layers)
        self.stack.setCredentials(credentials)

    def start(self) -> None:
        """
        Starts the Yowsup Loop

        :return: None
        """
        self.stack.broadcastEvent(YowLayerEvent(YowNetworkLayer.EVENT_STATE_CONNECT))
        try:
            self.stack.loop()
        except Exception as e:
            print("Authentication Error: %s" % str(e))
