# coding=utf-8
from yowsup.layers.protocol_messages.protocolentities import TextMessageProtocolEntity
from yowsup.layers.interface import YowInterfaceLayer, ProtocolEntityCallback
from yowsup.demos.echoclient.decider import decide, sizeChecker
from yowsup.demos.echoclient.utils.emojicode import *
from yowsup.demos.echoclient.utils.adressbook import *
import subprocess
import sys
import time
import re

class EchoLayer(YowInterfaceLayer):

    @ProtocolEntityCallback("message")
    def onMessage(self, messageProtocolEntity):

        if not messageProtocolEntity.getType() == 'text': return

        #Notify whatsapp that message was read
        self.toLower(messageProtocolEntity.ack())
        self.toLower(messageProtocolEntity.ack(True))

        sender = messageProtocolEntity.getFrom()
        senderNumber = messageProtocolEntity.getFrom(False)
        senderName = getContact(senderNumber)
        message = fixBrokenUnicode(messageProtocolEntity.getBody())
        minMessage = message.lower()

        group = False
        if re.compile("[0-9]+-[0-9]+").match(senderNumber): group = True

        try:
            participant = messageProtocolEntity.getParticipant(False)
        except: participant = ""
        participantName = getContact(participant)

        decision = decide(sender, senderNumber, senderName, message, minMessage, participant, participantName)


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


    @ProtocolEntityCallback("receipt")
    def onReceipt(self, entity):
        self.toLower(entity.ack())
