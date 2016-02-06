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
from yowsup import env
from yowsup.common import YowConstants
from yowsup.layers import YowLayerEvent
from yowsup.layers.axolotl import YowAxolotlLayer
from yowsup.layers.auth import YowCryptLayer, YowAuthenticationProtocolLayer
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
from layers.BotLayer import BotLayer
from layers.BotLayerWithGUI import BotLayerWithGUI
from startup.config.ConfigParser import ConfigParser
from startup.installation.Installer import Installer
import argparse
import sys

# Sets the encoding to UTF-8 when running this program in python2
if sys.version_info[0] == 2:
    reload(sys)
    sys.setdefaultencoding('utf8')


def main():
    """
    Starts the main loop of the program
    :return: void
    """

    # Argument Parser
    parser = argparse.ArgumentParser()
    parser.add_argument("-i", "--install", help="installs the program", action="store_true")
    parser.add_argument("-u", "--update", help="updates the program", action="store_true")
    parser.add_argument("-g", "--gui", help="starts the bot with a gui to disable certain plugins", action="store_true")
    args = parser.parse_args()

    # Check if installed
    installed = Installer.isInstalled()

    if args.install:
        if installed:
            print("Program already installed. Use --update to update to the newest version")
            sys.exit(1)
        Installer.install()
        sys.exit(0)

    if not installed:
        print("Program not installed correctly, please use the --install option")
        sys.exit(1)

    if args.update:
        Installer.update()
        sys.exit(0)

    try:
        credentials = ConfigParser.configParse()
    except EOFError:
        print("No valid login credentials provided in config file")
        sys.exit(1)

    if args.gui:
        selected_layer = BotLayerWithGUI
    else:
        selected_layer = BotLayer

    # This may have to be implemented some day if passing layers as tuples will be
    # deprecated, as being warned by yowsup currently. Sadly, this will also change
    # how the layer classes are built up, and I honestly would rather not do that now.
    """
    stack_builder = YowStackBuilder()
    stack = stack_builder.pushDefaultLayers(True).push(selected_layer).build()
    stack.setCredentials(credentials)
    stack.broadcastEvent(YowLayerEvent(selected_layer.EVENT_START))

    try:
        stack.loop(timeout=0.5, discrete=0.5)
    except AuthError as e:
        print("Auth Error, reason %s" % e)
    except KeyboardInterrupt:
        print("\nBot Dead")
        sys.exit(0)
    """

    layers = (
        selected_layer,
        (YowAuthenticationProtocolLayer,
         YowMessagesProtocolLayer,
         YowReceiptProtocolLayer,
         YowAckProtocolLayer,
         YowMediaProtocolLayer,
         YowIqProtocolLayer,
         YowCallsProtocolLayer),
        YowAxolotlLayer,
        YowLoggerLayer,
        YowCoderLayer,
        YowCryptLayer,
        YowStanzaRegulator,
        YowNetworkLayer
        )

    stack = YowStack(layers)
    stack.setProp(YowAuthenticationProtocolLayer.PROP_CREDENTIALS, credentials)  # setting credentials
    stack.setProp(YowNetworkLayer.PROP_ENDPOINT, YowConstants.ENDPOINTS[0])      # whatsapp server address
    stack.setProp(YowCoderLayer.PROP_DOMAIN, YowConstants.DOMAIN)
    stack.setProp(YowCoderLayer.PROP_RESOURCE, env.CURRENT_ENV.getResource())    # info about us as WhatsApp client
    stack.broadcastEvent(YowLayerEvent(YowNetworkLayer.EVENT_STATE_CONNECT))     # sending the connect signal
    # this is the program mainloop
    stack.loop()
    print("Bot Dead")

if __name__ == '__main__':
    main()
