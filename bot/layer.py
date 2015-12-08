"""
@author Hermann Krumrey<hermann@krumreyh.com>

The layer component of the bot. Used to send and receive messages
"""
import re
import time
import random

from yowsup.layers.interface import YowInterfaceLayer, ProtocolEntityCallback
from yowsup.layers.protocol_media.protocolentities import ImageDownloadableMediaMessageProtocolEntity
from yowsup.layers.protocol_messages.protocolentities import TextMessageProtocolEntity
from bot.deciders.GeneralDecider import GeneralDecider
from bot.utils.adressbook import *
from bot.utils.emojicode import *
from bot.utils.logwriter import writeLogAndPrint
from bot.deciders.Decision import Decision

class EchoLayer(YowInterfaceLayer):

    """
    Method run when a message is received
    @param: messageProtocolEntity - the message received
    """
    @ProtocolEntityCallback("message")
    def onMessage(self, messageProtocolEntity):

        if not messageProtocolEntity.getType() == 'text': return

        #Notify whatsapp that message was read
        self.toLower(messageProtocolEntity.ack())
        self.toLower(messageProtocolEntity.ack(True))

        sender = messageProtocolEntity.getFrom()
        message = messageProtocolEntity.getBody()

        group = False
        if re.compile("[0-9]+-[0-9]+").match(sender.split("@")[0]): group = True

        if group: message = fixBrokenUnicode(message)

        try:
            participant = messageProtocolEntity.getParticipant(False)
        except: participant = ""

        writeLogAndPrint("recv", getContact(sender), message)

        try:
            decision = GeneralDecider(message, sender, participant, self).decide()
            if decision:
                if len(decision.message) > 2500: decision.message = "Message too long to send"
        except Exception as e:
            print(str(e))
            decision = Decision("An exception occured", sender)

        if decision:
            if decision.message:
                time.sleep(random.randint(0, 3))
                writeLogAndPrint("sent", getContact(decision.sender), decision.message)
                if group: decision.message = convertToBrokenUnicode(decision.message)
                self.toLower(TextMessageProtocolEntity(decision.message, to=decision.sender))

    """
    method run whenever a whatsapp receipt is issued
    """
    @ProtocolEntityCallback("receipt")
    def onReceipt(self, entity):
        self.toLower(entity.ack())