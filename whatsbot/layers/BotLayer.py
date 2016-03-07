# coding=utf-8
"""
Copyright 2015,2016 Hermann Krumrey

This file is part of whatsbot.

    whatsbot makes use of various third-party python modules to serve
    information via the online chat service Whatsapp.

    whatsbot is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    whatsbot is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with whatsbot.  If not, see <http://www.gnu.org/licenses/>.
"""

# imports
import os
import sys
import time
import traceback

from yowsup.layers.interface import YowInterfaceLayer, ProtocolEntityCallback
from yowsup.layers.protocol_media.mediauploader import MediaUploader
from yowsup.layers.protocol_media.protocolentities import RequestUploadIqProtocolEntity
from yowsup.layers.protocol_presence.protocolentities import PresenceProtocolEntity
from yowsup.layers.protocol_profiles.protocolentities import SetStatusIqProtocolEntity

try:
    from plugins.PluginManager import PluginManager
    from startup.config.PluginConfigParser import PluginConfigParser
    from utils.contacts.AddressBook import AddressBook
    from utils.logging.LogWriter import LogWriter
    from yowsupwrapper.WrappedYowInterfaceLayer import WrappedYowInterfaceLayer
    from yowsupwrapper.entities.WrappedImageDownloadableMediaMessageProtocolEntity import \
        WrappedImageDownloadableMediaMessageProtocolEntity
    from yowsupwrapper.entities.EntityAdapter import EntityAdapter
    from yowsupwrapper.entities.WrappedAudioDownloadableMediaMessageProtocolEntity import \
        WrappedAudioDownloadableMediaMessageProtocolEntity
    from yowsupwrapper.entities.WrappedTextMessageProtocolEntity import WrappedTextMessageProtocolEntity
except ImportError:
    from whatsbot.plugins.PluginManager import PluginManager
    from whatsbot.startup.config.PluginConfigParser import PluginConfigParser
    from whatsbot.utils.contacts.AddressBook import AddressBook
    from whatsbot.utils.logging.LogWriter import LogWriter
    from whatsbot.yowsupwrapper.WrappedYowInterfaceLayer import WrappedYowInterfaceLayer
    from whatsbot.yowsupwrapper.entities.WrappedImageDownloadableMediaMessageProtocolEntity import \
        WrappedImageDownloadableMediaMessageProtocolEntity
    from whatsbot.yowsupwrapper.entities.EntityAdapter import EntityAdapter
    from whatsbot.yowsupwrapper.entities.WrappedAudioDownloadableMediaMessageProtocolEntity import \
        WrappedAudioDownloadableMediaMessageProtocolEntity
    from whatsbot.yowsupwrapper.entities.WrappedTextMessageProtocolEntity import WrappedTextMessageProtocolEntity


class BotLayer(WrappedYowInterfaceLayer):
    """
    The BotLayer class
    The layer component of the whatsbot. Used to send and receive messages
    """

    # class variables
    disconnect_action_prompt = 0
    parallel_running = False
    plugin_manager = None
    muted = False

    @ProtocolEntityCallback("message")
    def on_message(self, message_protocol_entity):
        """
        Method run when a message is received
        :param message_protocol_entity: the message received
        :return: void
        """
        try:
            message_protocol_entity = WrappedTextMessageProtocolEntity("", entity=message_protocol_entity)
        except AttributeError:
            message_protocol_entity = EntityAdapter(message_protocol_entity)
        self.send_receipt(message_protocol_entity)

        # Cases in which responses won't trigger
        if not message_protocol_entity.get_type() == 'text':
            return
        if message_protocol_entity.get_time_stamp() < int(time.time()) - 200:
            return
        if AddressBook().is_black_listed(message_protocol_entity.get_from(False)):
            return
        if AddressBook().is_black_listed(message_protocol_entity.get_participant()):
            return

        try:
            LogWriter.write_event_log("recv", message_protocol_entity)
            response = self.plugin_manager.run_plugins(message_protocol_entity)

            if response:
                if not self.muted:
                    LogWriter.write_event_log("sent", response)
                    self.to_lower(response)
                else:
                    LogWriter.write_event_log("s(m)", response)

        except Exception as e:
            trace = traceback.format_exc()
            exception = WrappedTextMessageProtocolEntity("Exception: " + str(e) + "\n" + trace + "\n",
                                                         to=message_protocol_entity.get_from())
            exception_image = os.getenv("HOME") + "/.whatsbot/images/exception.jpg"
            if not self.muted:
                LogWriter.write_event_log("exep", exception)
                LogWriter.write_event_log("imgs", WrappedTextMessageProtocolEntity(
                    exception_image + " --- " + exception.get_body(), to=message_protocol_entity.get_from(False)))
                self.send_image(message_protocol_entity.get_from(False), exception_image, exception.get_body())
            else:
                LogWriter.write_event_log("e(m)", exception)
                LogWriter.write_event_log("i(m)",
                                          WrappedTextMessageProtocolEntity(exception_image + " --- " +
                                                                           exception.get_body(),
                                                                           to=message_protocol_entity.get_from()))

    def plugin_manager_setup(self):
        """
        Sets up the plugin manager
        :return: void
        """
        if self.plugin_manager is None:
            self.plugin_manager = PluginManager(self)
            self.plugin_manager.set_plugins(PluginConfigParser().read_plugins())
            if not self.parallel_running:
                print("Starting Parallel Threads")
                PluginManager(self).start_parallel_runs()
                self.parallel_running = True

    # YOWSUP SPECIFIC METHODS

    def __init__(self):
        """
        Constructor, can be expanded for more functionality
        :return: void
        """
        # Required by Yowsup
        # Some CamelCase formatting, please ignore
        super(BotLayer, self).__init__()
        YowInterfaceLayer.__init__(self)
        self.accountDelWarnings = 0
        self.connected = False
        self.username = None
        self.sendReceipts = True
        self.disconnectAction = self.__class__.disconnect_action_prompt
        self.credentials = None
        self.jid_aliases = {}

        # Methods to run on start
        self.plugin_manager_setup()
        self.set_presence_name("Whatsapp-Bot")
        self.profile_set_status("I am a whatsbot.")

    @ProtocolEntityCallback("receipt")
    def on_receipt(self, entity):
        """
        method run whenever a whatsapp receipt is issued
        :param entity: The receipt entity
        :return: void
        """
        self.to_lower(entity.ack())

    def send_image(self, number, path, caption=None):
        """
        Sends an image
        :param number: the receiver of the image
        :param path: the path to the image file
        :param caption: the caption to be shown
        :return: void
        """
        jid = self.alias_to_jid(number)
        entity = RequestUploadIqProtocolEntity(RequestUploadIqProtocolEntity.MEDIA_TYPE_IMAGE, filePath=path)

        def success_fn(success_entity, original_entity):
            """
            Function called on successful media upload
            :param success_entity: the success entity
            :param original_entity: the original entity
            :return: void
            """
            self.on_request_upload_result(jid, path, success_entity, original_entity, caption)

        def error_fn(error_entity, original_entity):
            """
            Function called on failed media upload
            :param error_entity: the error entity
            :param original_entity: the original entity
            :return: void
            """
            BotLayer.on_request_upload_error(jid, path, error_entity, original_entity)

        self.send_iq(entity, success_fn, error_fn)

    # Todo get rid of the lambdas
    def send_audio(self, number, path):
        """
        Sends an audio file
        :param number: the number of the receiver of the file
        :param path: the path to the audio file
        :return: void
        """
        jid = self.alias_to_jid(number)
        entity = RequestUploadIqProtocolEntity(RequestUploadIqProtocolEntity.MEDIA_TYPE_AUDIO, filePath=path)

        def success_fn(success_entity, original_entity):
            """
            Function called on successful media upload
            :param success_entity: the success entity
            :param original_entity: the original entity
            :return: void
            """
            self.on_request_upload_result(jid, path, success_entity, original_entity)

        def error_fn(error_entity, original_entity):
            """
            Function called on failed media upload
            :param error_entity: the error entity
            :param original_entity: the original entity
            :return: void
            """
            BotLayer.on_request_upload_error(jid, path, error_entity, original_entity)

        self.send_iq(entity, success_fn, error_fn)

    # TODO get rid of the lambdas
    def on_request_upload_result(self, jid, file_path, result_request_upload_iq_protocol_entity,
                                 request_upload_iq_protocol_entity, caption=None):
        """
        Method run when a media upload result is positive
        :param jid: the jid to receive the media
        :param file_path: the path to the media file
        :param result_request_upload_iq_protocol_entity: the result entity
        :param request_upload_iq_protocol_entity: the request entity
        :param caption: the media caption, if applicable
        :return: void
        """
        result_request_upload_iq_protocol_entity = EntityAdapter(result_request_upload_iq_protocol_entity)

        if request_upload_iq_protocol_entity.mediaType == RequestUploadIqProtocolEntity.MEDIA_TYPE_AUDIO:
            do_send_fn = self.do_send_audio
        else:
            do_send_fn = self.do_send_image

        if result_request_upload_iq_protocol_entity.is_duplicate():
            do_send_fn(file_path, result_request_upload_iq_protocol_entity.get_url(), jid,
                       result_request_upload_iq_protocol_entity.get_ip(), caption)
        else:
            def success_fn(inner_file_path, inner_jid, url):
                """
                Function called when upload was successful
                :param inner_file_path: path to the media file
                :param inner_jid: the receiver's jid
                :param url: the whatsapp media url
                :return: void
                """
                do_send_fn(inner_file_path, url, inner_jid, result_request_upload_iq_protocol_entity.get_ip(), caption)

            media_uploader = MediaUploader(jid, self.get_own_jid(), file_path,
                                           result_request_upload_iq_protocol_entity.get_url(),
                                           result_request_upload_iq_protocol_entity.get_resume_offset(), success_fn,
                                           BotLayer.on_upload_error, BotLayer.on_upload_progress, async=False)
            media_uploader.start()

    @staticmethod
    def on_request_upload_error(jid, path, error_request_upload_iq_protocol_entity,
                                request_upload_iq_protocol_entity):
        """
        Method run when a media upload result is negative
        :param jid: the jid to receive the media
        :param path: the file path to the media
        :param error_request_upload_iq_protocol_entity: the error result entity
        :param request_upload_iq_protocol_entity: the request entity
        :return: void
        """
        if error_request_upload_iq_protocol_entity and request_upload_iq_protocol_entity:
            print("Request upload for file %s for %s failed" % (path, jid))

    @staticmethod
    def on_upload_error(file_path, jid, url):
        """
        Method run when an upload error occurs
        :param file_path: the file path of the file to upload
        :param jid: the jid of the receiver of the file
        :param url: the upload url
        :return: void
        """
        print("Upload file %s to %s for %s failed!" % (file_path, url, jid))

    @staticmethod
    def on_upload_progress(file_path, jid, url, progress):
        """
        Method that keeps track of the upload process
        :param file_path: the file path of the media file
        :param jid: the jid of the receiver
        :param url: the whatsapp upload url
        :param progress: the current progress
        :return:void
        """
        if url:
            sys.stdout.write("%s => %s, %d%% \r" % (os.path.basename(file_path), jid, progress))
            sys.stdout.flush()

    def alias_to_jid(self, c_alias):
        """
        Turns an alias into a jid
        :param c_alias: the current alias
        :return: the jid
        """
        for alias, a_jid in self.jid_aliases.items():
            if c_alias.lower() == alias.lower():
                return BotLayer.normalize_jid(a_jid)

        return BotLayer.normalize_jid(c_alias)

    @staticmethod
    def normalize_jid(number):
        """
        Normalizes a jid
        :param number: the number to be receive a normalized jid
        :return: the normalized jid
        """
        if '@' in number:
            return number
        elif "-" in number:
            return number + "@g.us"

        return number + "@s.whatsapp.net"

    def send_receipt(self, message_protocol_entity):
        """
        Sends the whatsapp servers that the message was received
        :param message_protocol_entity: the message protocol entity that was received
        :return: void
        """
        self.to_lower(message_protocol_entity.ack())
        self.to_lower(message_protocol_entity.ack(True))

    def do_send_image(self, file_path, url, to, ip=None, caption=None):
        """
        Sends an image file
        :param file_path: the path to the file
        :param url: the whatsapp upload url
        :param to: the receiver
        :param ip: the ip of the receiver
        :param caption: the caption to be displayed together with the image
        :return: void
        """
        entity = WrappedImageDownloadableMediaMessageProtocolEntity.from_file_path(file_path, url, ip, to,
                                                                                   caption=caption)
        self.to_lower(entity)

    def do_send_audio(self, file_path, url, to, ip=None):
        """
        Sends an audio file
        :param file_path: the path to the audio file
        :param url: the whatsapp upload url
        :param to: the receiver of the file
        :param ip: the ip of the receiver
        :return: void
        """
        entity = WrappedAudioDownloadableMediaMessageProtocolEntity.from_file_path(file_path, url, ip, to)
        self.to_lower(entity)

    def set_presence_name(self, name):
        """
        Sets the presence name of the whatsbot
        :param name: the presence name to set
        :return: void
        """
        entity = PresenceProtocolEntity(name=name)
        self.to_lower(entity)

    def profile_set_status(self, text):
        """
        Sets the profile status of the whatsbot
        :param text:
        :return: void
        """
        def on_success(result_iq_entity, original_iq_entity):
            """
            Run when successful
            :param result_iq_entity: the result entity
            :param original_iq_entity: the original entity
            :return: void
            """
            if result_iq_entity and original_iq_entity:
                print()

        def on_error(error_iq_entity, original_iq_entity):
            """
            Run when the profile status change failed
            :param error_iq_entity: the error entity
            :param original_iq_entity: the original entity
            :return: void
            """
            if error_iq_entity and original_iq_entity:
                print("Error updating status")

        entity = SetStatusIqProtocolEntity(text)
        self.send_iq(entity, on_success, on_error)
