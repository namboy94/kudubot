"""
Methods used to handle broken Unicode strings.
@author Hermann Krumrey<hermann@krumreyh.com>
"""

import re
from yowsup.layers.protocol_messages.protocolentities import TextMessageProtocolEntity

"""
Fixes a broken Unicode string
@:return the fixed string
"""
def fixBrokenUnicode(brokenEmoji):

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

    #testing
    #print(list(byteEmoji))
    #print(goodByteEmoji)

    goodByteEmoji = bytes(goodByteEmoji)
    return goodByteEmoji.decode()

"""
Converts a good Unicode string to a broken Unicode string
"""
def convertToBrokenUnicode(goodUnicode):

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

def fixEntity(entity):
    fixedEntity = entity
    if re.compile("[0-9]+-[0-9]+").match(entity.getFrom(True).split("@")[0]):
        fixedEntity = dummyEntity(fixBrokenUnicode(entity.getBody()), entity.getFrom(), entity.getFrom(False), entity.getParticipant())
    return fixedEntity

def convertEntityToBrokenUnicode(entity):
    brokenEntity = entity
    if re.compile("[0-9]+-[0-9]+").match(entity.getTo(True).split("@")[0]):
        brokenEntity = TextMessageProtocolEntity(convertToBrokenUnicode(entity.getBody()), to=entity.getTo())
    return brokenEntity

class dummyEntity(object):
    def __init__(self, message, sender, senderNumber, participant):
        self.message = message
        self.sender = sender
        self.senderNumber = senderNumber
        self.participant = participant

    def getFrom(self, full=True):
        if full:
            return self.sender
        else:
            return self.senderNumber

    def getBody(self):
        return self.message

    def getTo(self, full=True):
        return self.getFrom(full)

    def getParticipant(self):
        return self.participant