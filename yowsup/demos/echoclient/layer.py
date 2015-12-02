# coding=utf-8
from yowsup.layers.protocol_messages.protocolentities import TextMessageProtocolEntity
from yowsup.layers.interface import YowInterfaceLayer, ProtocolEntityCallback
from yowsup.demos.echoclient.decider import decide, sizeChecker
import subprocess
import sys
import time

class EchoLayer(YowInterfaceLayer):

    @ProtocolEntityCallback("message")
    def onMessage(self, messageProtocolEntity):

        willBeKilled = False

        if not messageProtocolEntity.getType() == 'text': return

        decision = decide(messageProtocolEntity)

        if decision[0] == "😨🔫":
            willBeKilled = True
        elif decision[2]:
            decision[0] = subprocess.check_output(args=decision[2], shell=True)
            decision[0] = sizeChecker(decision[0])
            print(decision[0])

        if decision[0]:
            decision[0] = sizeChecker(decision[0])
            outgoingMessageProtocolEntity = TextMessageProtocolEntity(decision[0], to=decision[1])
            self.toLower(outgoingMessageProtocolEntity)

        self.toLower(messageProtocolEntity.ack())
        self.toLower(messageProtocolEntity.ack(True))

        if willBeKilled:
            time.sleep(2)            
            sys.exit(0)


    @ProtocolEntityCallback("receipt")
    def onReceipt(self, entity):
        self.toLower(entity.ack())
