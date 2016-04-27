# coding=utf-8
"""
Copyright 2015,2016 Hermann Krumrey

This file is part of messengerbot.

    messengerbot makes use of various third-party python modules to serve
    information via online chat services.

    messengerbot is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    messengerbot is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with whatsbot.  If not, see <http://www.gnu.org/licenses/>.
"""

# imports
import os
import sys

from yowsup.layers.interface import ProtocolEntityCallback
from yowsup.layers.protocol_media.mediauploader import MediaUploader
from yowsup.layers.protocol_messages.protocolentities import MessageProtocolEntity
from yowsup.layers.protocol_presence.protocolentities import PresenceProtocolEntity
from yowsup.layers.protocol_profiles.protocolentities import SetStatusIqProtocolEntity
from yowsup.layers.protocol_media.protocolentities import RequestUploadIqProtocolEntity

from messengerbot.connection.whatsapp.yowsupwrapper.entities.EntityAdapter import EntityAdapter
from messengerbot.connection.whatsapp.yowsupwrapper.WrappedYowInterfaceLayer import WrappedYowInterfaceLayer
from messengerbot.connection.whatsapp.yowsupwrapper.entities.WrappedTextMessageProtocolEntity import \
    WrappedTextMessageProtocolEntity
from messengerbot.connection.whatsapp.yowsupwrapper.entities.WrappedImageDownloadableMediaMessageProtocolEntity import \
    WrappedImageDownloadableMediaMessageProtocolEntity
from messengerbot.connection.whatsapp.yowsupwrapper.entities.WrappedAudioDownloadableMediaMessageProtocolEntity import \
    WrappedAudioDownloadableMediaMessageProtocolEntity


class YowsupEchoLayer(WrappedYowInterfaceLayer):
    """
    The Yowsup Echo layer class
    The layer component of the whatsapp connection. Used to receive messages.
    """

    @ProtocolEntityCallback("receipt")
    def on_receipt(self, entity: EntityAdapter) -> None:
        """
        method run whenever a whatsapp receipt is issued

        :param entity: The receipt entity
        :return: void
        """
        self.to_lower(entity.ack())

    def send_image(self, number: str, path: str, caption: str = None) -> None:
        """
        Sends an image

        :param number: the receiver of the image
        :param path: the path to the image file
        :param caption: the caption to be shown
        :return: void
        """
        jid = self.alias_to_jid(number)
        entity = RequestUploadIqProtocolEntity(RequestUploadIqProtocolEntity.MEDIA_TYPE_IMAGE, filePath=path)

        def success_fn(success_entity: WrappedTextMessageProtocolEntity, original_entity: MessageProtocolEntity) \
                -> None:
            """
            Function called on successful media upload

            :param success_entity: the success entity
            :param original_entity: the original entity
            :return: None
            """
            # noinspection PyTypeChecker
            self.on_request_upload_result(jid, path, success_entity, original_entity, caption)

        def error_fn(error_entity: MessageProtocolEntity, original_entity: RequestUploadIqProtocolEntity) -> None:
            """
            Function called on failed media upload

            :param error_entity: the error entity
            :param original_entity: the original entity
            :return: None
            """
            YowsupEchoLayer.on_request_upload_error(jid, path, error_entity, original_entity)

        self.send_iq(entity, success_fn, error_fn)

    def send_audio(self, number: str, path: str) -> None:
        """
        Sends an audio file

        :param number: the number of the receiver of the file
        :param path: the path to the audio file
        :return: None
        """
        jid = self.alias_to_jid(number)
        entity = RequestUploadIqProtocolEntity(RequestUploadIqProtocolEntity.MEDIA_TYPE_AUDIO, filePath=path)

        def success_fn(success_entity: WrappedTextMessageProtocolEntity, original_entity: MessageProtocolEntity) \
                -> None:
            """
            Function called on successful media upload

            :param success_entity: the success entity
            :param original_entity: the original entity
            :return: None
            """
            # noinspection PyTypeChecker
            self.on_request_upload_result(jid, path, success_entity, original_entity)

        def error_fn(error_entity: MessageProtocolEntity, original_entity: RequestUploadIqProtocolEntity) -> None:
            """
            Function called on failed media upload

            :param error_entity: the error entity
            :param original_entity: the original entity
            :return: None
            """
            YowsupEchoLayer.on_request_upload_error(jid, path, error_entity, original_entity)

        self.send_iq(entity, success_fn, error_fn)

    def on_request_upload_result(self, jid: str, file_path: str,
                                 result_request_upload_iq_protocol_entity: MessageProtocolEntity,
                                 request_upload_iq_protocol_entity: RequestUploadIqProtocolEntity,
                                 caption: str = None) -> None:
        """
        Method run when a media upload result is positive

        :param jid: the jid to receive the media
        :param file_path: the path to the media file
        :param result_request_upload_iq_protocol_entity: the result entity
        :param request_upload_iq_protocol_entity: the request entity
        :param caption: the media caption, if applicable
        :return: None
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

            def success_fn(inner_file_path: str, inner_jid: str, url: str) -> None:
                """
                Function called when upload was successful

                :param inner_file_path: path to the media file
                :param inner_jid: the receiver's jid
                :param url: the whatsapp media url
                :return: None
                """
                do_send_fn(inner_file_path, url, inner_jid, result_request_upload_iq_protocol_entity.get_ip(), caption)

            media_uploader = MediaUploader(jid, self.get_own_jid(), file_path,
                                           result_request_upload_iq_protocol_entity.get_url(),
                                           result_request_upload_iq_protocol_entity.get_resume_offset(), success_fn,
                                           YowsupEchoLayer.on_upload_error, YowsupEchoLayer.on_upload_progress,
                                           async=False)
            media_uploader.start()

    @staticmethod
    def on_request_upload_error(jid: str, path: str, error_request_upload_iq_protocol_entity: MessageProtocolEntity,
                                request_upload_iq_protocol_entity: RequestUploadIqProtocolEntity) -> None:
        """
        Method run when a media upload result is negative

        :param jid: the jid to receive the media
        :param path: the file path to the media
        :param error_request_upload_iq_protocol_entity: the error result entity
        :param request_upload_iq_protocol_entity: the request entity
        :return: None
        """
        if error_request_upload_iq_protocol_entity and request_upload_iq_protocol_entity:
            print("Request upload for file %s for %s failed" % (path, jid))

    @staticmethod
    def on_upload_error(file_path: str, jid: str, url: str) -> None:
        """
        Method run when an upload error occurs

        :param file_path: the file path of the file to upload
        :param jid: the jid of the receiver of the file
        :param url: the upload url
        :return: None
        """
        print("Upload file %s to %s for %s failed!" % (file_path, url, jid))

    @staticmethod
    def on_upload_progress(file_path: str, jid: str, url: str, progress: float) -> None:
        """
        Method that keeps track of the upload process

        :param file_path: the file path of the media file
        :param jid: the jid of the receiver
        :param url: the whatsapp upload url
        :param progress: the current progress
        :return:None
        """
        if url:
            sys.stdout.write("%s => %s, %d%% \r" % (os.path.basename(file_path), jid, progress))
            sys.stdout.flush()

    def alias_to_jid(self, c_alias: str) -> str:
        """
        Turns an alias into a jid

        :param c_alias: the current alias
        :return: the jid
        """
        for alias, a_jid in self.jid_aliases.items():
            if c_alias.lower() == alias.lower():
                return YowsupEchoLayer.normalize_jid(a_jid)

        return YowsupEchoLayer.normalize_jid(c_alias)

    @staticmethod
    def normalize_jid(number: str) -> str:
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

    def send_receipt(self, message_protocol_entity: MessageProtocolEntity) -> None:
        """
        Sends the whatsapp servers that the message was received

        :param message_protocol_entity: the message protocol entity that was received
        :return: None
        """
        self.to_lower(message_protocol_entity.ack())
        self.to_lower(message_protocol_entity.ack(True))

    def do_send_image(self, file_path: str, url: str, to: str, ip: str = None, caption: str = None) -> None:
        """
        Sends an image file

        :param file_path: the path to the file
        :param url: the whatsapp upload url
        :param to: the receiver
        :param ip: the ip of the receiver
        :param caption: the caption to be displayed together with the image
        :return: None
        """
        entity = WrappedImageDownloadableMediaMessageProtocolEntity.from_file_path(file_path, url, ip, to,
                                                                                   caption=caption)
        self.to_lower(entity)

    def do_send_audio(self, file_path: str, url: str, to: str, ip: str = None) -> None:
        """
        Sends an audio file

        :param file_path: the path to the audio file
        :param url: the whatsapp upload url
        :param to: the receiver of the file
        :param ip: the ip of the receiver
        :return: None
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

    def profile_set_status(self, text: str) -> None:
        """
        Sets the profile status of the whatsbot
        :param text:
        :return: None
        """
        def on_success(result_iq_entity: MessageProtocolEntity, original_iq_entity: MessageProtocolEntity) -> None:
            """
            Run when successful
            :param result_iq_entity: the result entity
            :param original_iq_entity: the original entity

            :return: None
            """
            if result_iq_entity and original_iq_entity:
                print()

        def on_error(error_iq_entity: MessageProtocolEntity, original_iq_entity: MessageProtocolEntity) -> None:
            """
            Run when the profile status change failed

            :param error_iq_entity: the error entity
            :param original_iq_entity: the original entity
            :return: None
            """
            if error_iq_entity and original_iq_entity:
                print("Error updating status")

        entity = SetStatusIqProtocolEntity(text)
        self.send_iq(entity, on_success, on_error)
