"""
@author Hermann Krumrey<hermann@krumreyh.com>
The layer component of the bot. Used to send and receive messages
"""
import time

from yowsup.layers.interface import YowInterfaceLayer, ProtocolEntityCallback
from yowsup.layers.protocol_media.protocolentities import ImageDownloadableMediaMessageProtocolEntity, \
    RequestUploadIqProtocolEntity
from yowsup.layers.protocol_messages.protocolentities import TextMessageProtocolEntity

from utils.encoding.Unicoder import Unicoder
from utils.logging.LogWriter import LogWriter
from utils.contacts.AddressBook import AddressBook
from plugins.PluginManager import PluginManager
from plugins.PluginManagerGui import PluginManagerGUI


class BotLayer(YowInterfaceLayer):

    parallelRunning = False
    pluginManager = None
    muted = False


    """
    Method run when a message is received
    @param: messageProtocolEntity - the message received
    """
    @ProtocolEntityCallback("message")
    def onMessage(self, messageProtocolEntity):

        if self.pluginManager is None:
            self.pluginManager = PluginManager(self)
            PluginManagerGUI(self.pluginManager)
            if not self.parallelRunning:
                print("Starting Parallel Threads")
                PluginManager(self).startParallelRuns()
                self.parallelRunning = True

        #Notify whatsapp that message was read
        self.toLower(messageProtocolEntity.ack())
        self.toLower(messageProtocolEntity.ack(True))

        #Cases in which responses won't trigger
        if not messageProtocolEntity.getType() == 'text': return
        if messageProtocolEntity.getTimestamp() < int(time.time()) - 200: return
        if AddressBook().isBlackListed(messageProtocolEntity.getFrom(False)): return
        try:
            if AddressBook().isBlackListed(messageProtocolEntity.getParticipant(False)): return
        except: print()

        try:

            messageProtocolEntity = Unicoder.fixIncominEntity(messageProtocolEntity)

            LogWriter.writeEventLog("recv", messageProtocolEntity)

            response = self.pluginManager.runPlugins(messageProtocolEntity)

            if response:
                if not self.muted:
                    LogWriter.writeEventLog("sent", response)
                    response = Unicoder.fixOutgoingEntity(response)
                    self.toLower(response)
                else:
                    LogWriter.writeEventLog("s(m)", response)

        except Exception as e:
            exception = TextMessageProtocolEntity("Exception: " + str(e), to=messageProtocolEntity.getFrom())
            if not self.muted:
                LogWriter.writeEventLog("exep", exception)
                self.toLower(exception)
            else:
                LogWriter.writeEventLog("e(m)", exception)

    #YOWSUP SPECIFIC METHODS

    """
    method run whenever a whatsapp receipt is issued
    """
    @ProtocolEntityCallback("receipt")
    def onReceipt(self, entity):
        self.toLower(entity.ack())