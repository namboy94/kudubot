"""
@author Hermann Krumrey<hermann@krumreyh.com>

The layer component of the bot. Used to send and receive messages
"""
from yowsup.layers.protocol_messages.protocolentities import TextMessageProtocolEntity
from yowsup.layers.interface import YowInterfaceLayer, ProtocolEntityCallback
from yowsup.demos.echoclient.deciders.GeneralDecider import GeneralDecider
from yowsup.demos.echoclient.utils.emojicode import *
from yowsup.demos.echoclient.utils.adressbook import *
import subprocess
import sys
import time
import re

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
        senderNumber = messageProtocolEntity.getFrom(False)
        message = fixBrokenUnicode(messageProtocolEntity.getBody())

        group = False
        if re.compile("[0-9]+-[0-9]+").match(senderNumber): group = True

        try:
            participant = messageProtocolEntity.getParticipant(False)
        except: participant = ""

        decision = GeneralDecider(message, sender, senderNumber, participant).decide()


        #TODO remove everything except the last toLower and a few lines to make this possible
        willBeKilled = False

        if decision[0] == "😨🔫":
            willBeKilled = True
        elif decision[2]:
            decision[0] = subprocess.check_output(args=decision[2], shell=True)
            decision[0] = sizeChecker(decision[0])
            print(decision[0])

        if decision[0]:
            decision[0] = sizeChecker(decision[0])
            if group: decision[0] = convertToBrokenUnicode(decision[0])
            outgoingMessageProtocolEntity = TextMessageProtocolEntity(decision[0], to=decision[1])
            self.toLower(outgoingMessageProtocolEntity)

        if willBeKilled:
            time.sleep(2)            
            sys.exit(0)


    """
    method run whenever a whatsapp receipt is issued
    """
    @ProtocolEntityCallback("receipt")
    def onReceipt(self, entity):
        self.toLower(entity.ack())
