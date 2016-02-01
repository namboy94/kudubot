# coding=utf-8
"""
Copyright 2015,2016 Hermann Krumrey

This file is part of whatsapp-bot.

    whatsapp-bot makes use of various third-party python modules to serve
    information via the online chat service Whatsapp.

    whatsapp-bot is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    whatsapp-bot is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with whatsapp-bot.  If not, see <http://www.gnu.org/licenses/>.
"""

"""
@author Hermann Krumrey<hermann@krumreyh.com>
The layer component of the bot. Used to send and receive messages
"""
import time
import logging
import sys
import os
import traceback
from yowsup.layers.interface import YowInterfaceLayer, ProtocolEntityCallback
from yowsup.layers.protocol_media.protocolentities import ImageDownloadableMediaMessageProtocolEntity, \
    RequestUploadIqProtocolEntity, AudioDownloadableMediaMessageProtocolEntity
from yowsup.layers.protocol_messages.protocolentities import TextMessageProtocolEntity
from yowsup.layers.protocol_media.mediauploader import MediaUploader
from yowsup.layers.protocol_presence.protocolentities import PresenceProtocolEntity
from yowsup.layers.protocol_profiles.protocolentities import SetStatusIqProtocolEntity

from startup.config.PluginConfigParser import PluginConfigParser
from utils.encoding.Unicoder import Unicoder
from utils.logging.LogWriter import LogWriter
from utils.contacts.AddressBook import AddressBook
from plugins.PluginManager import PluginManager

logger = logging.getLogger(__name__)

"""
The BotLayer class
"""
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
            trace = traceback.format_exc()
            exception = TextMessageProtocolEntity("Exception: " + str(e) + "\n" + trace + "\n", to=messageProtocolEntity.getFrom())
            exceptionImage = os.getenv("HOME") + "/.whatsapp-bot/images/exception.jpg"
            if not self.muted:
                LogWriter.writeEventLog("exep", exception)
                LogWriter.writeEventLog("imgs", TextMessageProtocolEntity(exceptionImage + " --- " + exception.getBody(), to=messageProtocolEntity.getFrom(False)))
                self.sendImage(messageProtocolEntity.getFrom(False), exceptionImage,  exception.getBody())
            else:
                LogWriter.writeEventLog("e(m)", exception)
                LogWriter.writeEventLog("i(m)", TextMessageProtocolEntity(exceptionImage + " --- " + exception.getBody(), to=messageProtocolEntity.getFrom()))

    """
    Sets up the plugin manager
    """
    def pluginManagerSetup(self):
        if self.pluginManager is None:
            self.pluginManager = PluginManager(self)
            self.pluginManager.setPlugins(PluginConfigParser().readPlugins())
            if not self.parallelRunning:
                print("Starting Parallel Threads")
                PluginManager(self).startParallelRuns()
                self.parallelRunning = True

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
        self.jidAliases = {}

        self.pluginManagerSetup()
        self.setPresenceName("Whatsapp-Bot")
        self.profile_setStatus("I am a bot.")


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

    def sendAudio(self, number, path):
        jid = self.aliasToJid(number)
        entity = RequestUploadIqProtocolEntity(RequestUploadIqProtocolEntity.MEDIA_TYPE_AUDIO, filePath=path)
        successFn = lambda successEntity, originalEntity: self.onRequestUploadResult(jid, path, successEntity, originalEntity)
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

    def setPresenceName(self, name):
        entity = PresenceProtocolEntity(name=name)
        self.toLower(entity)

    def profile_setStatus(self, text):
        def onSuccess(resultIqEntity, originalIqEntity):
            print()

        def onError(errorIqEntity, originalIqEntity):
            logger.error("Error updating status")

        entity = SetStatusIqProtocolEntity(text)
        self._sendIq(entity, onSuccess, onError)