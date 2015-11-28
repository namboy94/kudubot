from yowsup.layers.protocol_messages.protocolentities import TextMessageProtocolEntity
from yowsup.layers.interface import YowInterfaceLayer, ProtocolEntityCallback
from yowsup.demos.echoclient.decider import decide
import os

class EchoLayer(YowInterfaceLayer):

    @ProtocolEntityCallback("message")
    def onMessage(self, messageProtocolEntity):

        decision = decide(messageProtocolEntity)

        if decision[2]:
            os.system(decision[2])
        elif decision[0]:
            outgoingMessageProtocolEntity = TextMessageProtocolEntity(decision[0], to=messageProtocolEntity.getFrom())
            self.toLower(outgoingMessageProtocolEntity)

        self.toLower(messageProtocolEntity.ack())
        self.toLower(messageProtocolEntity.ack(True))


    @ProtocolEntityCallback("receipt")
    def onReceipt(self, entity):
        self.toLower(entity.ack())