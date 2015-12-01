# coding=utf-8
from yowsup.layers.protocol_messages.protocolentities import TextMessageProtocolEntity
from yowsup.layers.interface import YowInterfaceLayer, ProtocolEntityCallback
from yowsup.demos.echoclient.decider import decide, sizeChecker
import subprocess
import sys

class EchoLayer(YowInterfaceLayer):

    @ProtocolEntityCallback("message")
    def onMessage(self, messageProtocolEntity):

        willBeKilled = False

        if messageProtocolEntity.getType() == 'media': outgoingMessageProtocolEntity = Proto
        elif not messageProtocolEntity.getType() == 'text': return

        decision = decide(messageProtocolEntity)

        if decision[0] == "ð¨ð«":
            willBeKilled = True
        elif decision[2] and not sizeChecker(decision[2]) == "Message too long to send":
            decision[0] = subprocess.check_output(args=decision[2], shell=True)
            decision[0] = sizeChecker(decision[0])
            print(decision[0])

        if not sizeChecker(decision[0]) == "Message too long to send" and decision[0]:
            outgoingMessageProtocolEntity = TextMessageProtocolEntity(decision[0], to=decision[1])
            self.toLower(outgoingMessageProtocolEntity)

        self.toLower(messageProtocolEntity.ack())
        self.toLower(messageProtocolEntity.ack(True))

        if willBeKilled: sys.exit(0)


    @ProtocolEntityCallback("receipt")
    def onReceipt(self, entity):
        self.toLower(entity.ack())
