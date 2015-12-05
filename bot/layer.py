"""
@author Hermann Krumrey<hermann@krumreyh.com>

The layer component of the bot. Used to send and receive messages
"""
import re

from yowsup.layers.interface import YowInterfaceLayer, ProtocolEntityCallback
from yowsup.layers.protocol_messages.protocolentities import TextMessageProtocolEntity

from bot.deciders.GeneralDecider import GeneralDecider
from bot.utils.adressbook import *
from bot.utils.emojicode import *
from bot.utils.logwriter import writeLogAndPrint

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

        decision = GeneralDecider(message, sender, participant).decide()

        if decision:
            writeLogAndPrint("sent", getContact(decision.sender), decision.message)
            outgoingMessageProtocolEntity = TextMessageProtocolEntity(convertToBrokenUnicode(decision.message), to=decision.sender)
            self.toLower(outgoingMessageProtocolEntity)



        """
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


    """
    method run whenever a whatsapp receipt is issued
    """
    @ProtocolEntityCallback("receipt")
    def onReceipt(self, entity):
        self.toLower(entity.ack())
