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
from subprocess import Popen
import argparse
import sys
import os

# Sets the encoding to UTF-8 when running this program in python2
if sys.version_info[0] == 2:
    # noinspection PyUnresolvedReferences
    reload(sys)
    sys.setdefaultencoding('utf8')


def main():
    """
    Starts the main loop of the program
    :return: void
    """

    # Argument Parser
    parser = argparse.ArgumentParser()
    parser.add_argument("-g", "--gui", help="starts the whatsbot with a gui to disable certain plugins",
                        action="store_true")
    parser.add_argument("-r", "--register", help="Registers a new number")
    parser.add_argument("-a", "--activate", help="Activates a new number")
    args = parser.parse_args()

    # Check if installed
    installed = Installer.is_installed()

    if not installed:
        Installer.install()
        print("Program was installed. Now use --register to register your phone number")
        sys.exit(0)

    if args.register:
        number_file = open(os.getenv("HOME") + "/.whatsbot/creds", 'w')
        number_file.write("number=" + args.register + "\n")
        number_file.write("password=")
        os.system("yowsup-cli registration --requestcode sms --phone 49XXXXXXXX --cc 49 --mcc 123 --mnc 456")


    try:
        credentials = ConfigParser.config_parse()
    except EOFError:
        print("No valid login credentials provided in config file")
        print("Use --register to register a new number or --activate to activate a previously registered number")
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

    # Forgive the CamelCase, it's yowsup's fault!
    stack = YowStack(layers)
    stack.setProp(YowAuthenticationProtocolLayer.PROP_CREDENTIALS, credentials)  # setting credentials
    stack.setProp(YowNetworkLayer.PROP_ENDPOINT, YowConstants.ENDPOINTS[0])      # whatsapp server address
    stack.setProp(YowCoderLayer.PROP_DOMAIN, YowConstants.DOMAIN)
    stack.setProp(YowCoderLayer.PROP_RESOURCE, env.CURRENT_ENV.getResource())    # info about us as WhatsApp client
    stack.broadcastEvent(YowLayerEvent(YowNetworkLayer.EVENT_STATE_CONNECT))     # sending the connect signal
    # this is the program mainloop
    stack.loop()

if __name__ == '__main__':
    main()
