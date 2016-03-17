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
from yowsup.layers import YowParallelLayer, YowLayerEvent
from yowsup.layers.auth import YowAuthenticationProtocolLayer, YowCryptLayer
from yowsup.layers.coder import YowCoderLayer
from yowsup.layers.logger import YowLoggerLayer
from yowsup.layers.network import YowNetworkLayer
from yowsup.layers.protocol_acks import YowAckProtocolLayer
from yowsup.layers.protocol_calls import YowCallsProtocolLayer
from yowsup.layers.protocol_iq import YowIqProtocolLayer
from yowsup.layers.protocol_media import YowMediaProtocolLayer
from yowsup.layers.protocol_messages import YowMessagesProtocolLayer
from yowsup.layers.protocol_receipts import YowReceiptProtocolLayer
from yowsup.layers.stanzaregulator import YowStanzaRegulator
from yowsup.stacks import YowStack


class YowsupEchoStack(object):
    """
    The Yowsup Stack that handles the communication to the whatsapp servers
    """

    def __init__(self, bot_layer, credentials, encryption_enabled=False):
        """
        :param bot_layer: The Yowsup layer to include in the stack
        :param credentials: The credentials used to log in on the whatsapp servers
        :param encryption_enabled: Flag to enable or disable encryption
        :return: void
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

    def start(self):
        """
        Starts the Yowsup Loop
        :return: void
        """
        self.stack.broadcastEvent(YowLayerEvent(YowNetworkLayer.EVENT_STATE_CONNECT))
        try:
            self.stack.loop()
        except Exception as e:
            print("Authentication Error: %s" % str(e))
