from yowsup.layers.protocol_messages.protocolentities import TextMessageProtocolEntity
from yowsup.layers.interface import YowInterfaceLayer, ProtocolEntityCallback
from yowsup.demos.echoclient.decider import decide
import os
import subprocess

class EchoLayer(YowInterfaceLayer):

    @ProtocolEntityCallback("message")
    def onMessage(self, messageProtocolEntity):

        if not messageProtocolEntity.getType() == 'text': return

        decision = decide(messageProtocolEntity)

        if decision[2]:
            decision[0] = subprocess.check_output(args=decision[2], shell=True)
            outgoingMessageProtocolEntity = TextMessageProtocolEntity(decision[0], to=messageProtocolEntity.getFrom())
            self.toLower(outgoingMessageProtocolEntity)
            os.system(decision[2])
        elif decision[0]:
            outgoingMessageProtocolEntity = TextMessageProtocolEntity(decision[0], to=messageProtocolEntity.getFrom())
            self.toLower(outgoingMessageProtocolEntity)

        self.toLower(messageProtocolEntity.ack())
        self.toLower(messageProtocolEntity.ack(True))


    @ProtocolEntityCallback("receipt")
    def onReceipt(self, entity):
        self.toLower(entity.ack())