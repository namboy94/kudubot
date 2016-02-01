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

import re
from yowsup.layers.protocol_messages.protocolentities import TextMessageProtocolEntity
from utils.encoding.DummyTextMessageProtocolEntity import DummyTextMessageProtocolEntity

"""
The Unicoder class
"""
class Unicoder(object):

    """
    Checks an incoming TextMessageProtocolEntity for valid Unicode encoding and repairs it if necessary.
    @:return the fixed TextMessageProtocolEntity as a DummyTextMessageProtocolEntity
    """
    @staticmethod
    def fixIncominEntity(entity):
        fixedEntity = entity
        if re.compile("[0-9]+-[0-9]+").match(entity.getFrom(True).split("@")[0]):
            fixedMessage = Unicoder.__fixIncomingUnicode__(entity.getBody())
            fixedEntity = DummyTextMessageProtocolEntity(fixedMessage, entity.getFrom(),
                                                         entity.getFrom(False), entity.getParticipant(),
                                                         entity.getNotify())
        return fixedEntity

    """
    Checks an outgoing TextMessageProtocolEntity for valid Unicode encoding and repairs it if necessary
    @:return the fixed TextMessageProtocolEntity as TextMessageProtocolEntity, ready to send
    """
    @staticmethod
    def fixOutgoingEntity(entity):
        brokenEntity = entity
        if re.compile("[0-9]+-[0-9]+").match(entity.getTo(True).split("@")[0]):
            fixedMessage = Unicoder.__fixOutgoingUnicode__(entity.getBody())
            brokenEntity = TextMessageProtocolEntity(fixedMessage, to=entity.getTo())
        return brokenEntity

    """
    Fixes a broken incoming Unicode string
    @:return the fixed string
    """
    @staticmethod
    def __fixIncomingUnicode__(brokenEmoji):

        byteEmoji = bytes(brokenEmoji, 'utf-8')
        goodByteEmoji = []
        i = 0

        while i < len(byteEmoji):
            if not byteEmoji[i] == 194:
                if byteEmoji[i] == 195:
                    i += 1
                    goodByteEmoji.append(byteEmoji[i] + 64)
                else:
                    goodByteEmoji.append(byteEmoji[i])
            i += 1

        goodByteEmoji = bytes(goodByteEmoji)
        return goodByteEmoji.decode()

    """
    Fixes a broken outgoing Unicode string
    @:return the fixed string
    """
    @staticmethod
    def __fixOutgoingUnicode__(goodUnicode):

        newWord = ""

        for char in goodUnicode:

            byteUnicode = list(bytes(char, 'utf-8'))
            if len(byteUnicode) == 1: newWord += char; continue

            brokenByteUnicode = []
            i = 0
            has195 = False
            lastIs194 = False
            lastIs195 = False


            while i < len(byteUnicode):

                if not has195:
                    brokenByteUnicode.append(195)
                    has195 = True
                    lastIs195 = True

                else:
                    if lastIs195:
                        brokenByteUnicode.append(byteUnicode[i] - 64)
                        lastIs195 = False
                        i += 1
                    elif lastIs194:
                        brokenByteUnicode.append(byteUnicode[i])
                        lastIs194 = False
                        i += 1
                    else:
                        brokenByteUnicode.append(194)
                        lastIs194 = True

            newWord += bytes(brokenByteUnicode).decode()

        return newWord
