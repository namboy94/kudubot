"""
@author Hermann Krumrey<hermann@krumreyh.com>
The layer component of the bot. Used to send and receive messages
"""
import time
import logging
import sys
import os
from yowsup.layers.interface import YowInterfaceLayer, ProtocolEntityCallback
from yowsup.layers.protocol_media.protocolentities import ImageDownloadableMediaMessageProtocolEntity, \
    RequestUploadIqProtocolEntity, AudioDownloadableMediaMessageProtocolEntity
from yowsup.layers.protocol_messages.protocolentities import TextMessageProtocolEntity
from yowsup.layers.protocol_media.mediauploader import MediaUploader

from utils.encoding.Unicoder import Unicoder
from utils.logging.LogWriter import LogWriter
from utils.contacts.AddressBook import AddressBook
from plugins.PluginManager import PluginManager
from plugins.PluginManagerGui import PluginManagerGUI

logger = logging.getLogger(__name__)

class BotLayer(YowInterfaceLayer):

    DISCONNECT_ACTION_PROMPT = 0

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
                exceptionImage = os.getenv("HOME") + "/.whatsapp-bot/images/exception.jpg"
                self.sendImage(messageProtocolEntity.getFrom(False), exceptionImage,  exception.getBody())
            else:
                LogWriter.writeEventLog("e(m)", exception)

    #YOWSUP SPECIFIC METHODS

    def __init__(self):
        super(BotLayer, self).__init__()
        YowInterfaceLayer.__init__(self)
        self.accountDelWarnings = 0
        self.connected = False
        self.username = None
        self.sendReceipts = True
        self.disconnectAction = self.__class__.DISCONNECT_ACTION_PROMPT
        self.credentials = None

        #add aliases to make it user to use commands. for example you can then do:
        # /message send foobar "HI"
        # and then it will get automaticlaly mapped to foobar's jid
        self.jidAliases = {
            # "NAME": "PHONE@s.whatsapp.net"
        }

    """
    method run whenever a whatsapp receipt is issued
    """
    @ProtocolEntityCallback("receipt")
    def onReceipt(self, entity):
        self.toLower(entity.ack())

    def sendImage(self, number, path, caption = None):
        jid = self.aliasToJid(number)
        entity = RequestUploadIqProtocolEntity(RequestUploadIqProtocolEntity.MEDIA_TYPE_IMAGE, filePath=path)
        successFn = lambda successEntity, originalEntity: self.onRequestUploadResult(jid, path, successEntity, originalEntity, caption)
        errorFn = lambda errorEntity, originalEntity: self.onRequestUploadError(jid, path, errorEntity, originalEntity)

        self._sendIq(entity, successFn, errorFn)

    def onRequestUploadResult(self, jid, filePath, resultRequestUploadIqProtocolEntity, requestUploadIqProtocolEntity, caption = None):

        if requestUploadIqProtocolEntity.mediaType == RequestUploadIqProtocolEntity.MEDIA_TYPE_AUDIO:
            doSendFn = self.doSendAudio
        else:
            doSendFn = self.doSendImage

        if resultRequestUploadIqProtocolEntity.isDuplicate():
            doSendFn(filePath, resultRequestUploadIqProtocolEntity.getUrl(), jid,
                             resultRequestUploadIqProtocolEntity.getIp(), caption)
        else:
            successFn = lambda filePath, jid, url: doSendFn(filePath, url, jid, resultRequestUploadIqProtocolEntity.getIp(), caption)
            mediaUploader = MediaUploader(jid, self.getOwnJid(), filePath,
                                      resultRequestUploadIqProtocolEntity.getUrl(),
                                      resultRequestUploadIqProtocolEntity.getResumeOffset(),
                                      successFn, self.onUploadError, self.onUploadProgress, async=False)
            mediaUploader.start()

    def onRequestUploadError(self, jid, path, errorRequestUploadIqProtocolEntity, requestUploadIqProtocolEntity):
        logger.error("Request upload for file %s for %s failed" % (path, jid))

    def onUploadError(self, filePath, jid, url):
        logger.error("Upload file %s to %s for %s failed!" % (filePath, url, jid))

    def onUploadProgress(self, filePath, jid, url, progress):
        sys.stdout.write("%s => %s, %d%% \r" % (os.path.basename(filePath), jid, progress))
        sys.stdout.flush()

    def aliasToJid(self, calias):
        for alias, ajid in self.jidAliases.items():
            if calias.lower() == alias.lower():
                return self.normalizeJid(ajid)

        return self.normalizeJid(calias)

    def normalizeJid(self, number):
        if '@' in number:
            return number
        elif "-" in number:
            return "%s@g.us" % number

        return "%s@s.whatsapp.net" % number


    def doSendImage(self, filePath, url, to, ip = None, caption = None):
        entity = ImageDownloadableMediaMessageProtocolEntity.fromFilePath(filePath, url, ip, to, caption = caption)
        self.toLower(entity)

    def doSendAudio(self, filePath, url, to, ip = None, caption = None):
        entity = AudioDownloadableMediaMessageProtocolEntity.fromFilePath(filePath, url, ip, to)
        self.toLower(entity)