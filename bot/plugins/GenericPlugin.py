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

# imports
from utils.logging.LogWriter import LogWriter
from yowsupwrapper.entities.WrappedTextMessageProtocolEntity import WrappedTextMessageProtocolEntity


class GenericPlugin(object):
    """
    The GenericPlugin Class
    """

    def __init__(self, layer, message_protocol_entity=None):
        """
        Constructor
        Defines parameters for the plugin.
        :param layer: the overlying yowsup layer
        :param message_protocol_entity: the received message information
        :return: void
        """
        if message_protocol_entity is None:
            self.layer = layer
            self.entity = None
            return
        self.layer = layer
        self.entity = message_protocol_entity
        self.message = self.entity.get_body().lower()
        self.cap_message = self.entity.get_body()
        self.sender = self.entity.get_from()
        self.participant = self.entity.get_participant()
        if not self.participant:
            self.participant = self.sender

    def regex_check(self):
        """
        Checks if the user input is valid for this plugin to continue
        :return True if input is valid, False otherwise
        """
        raise NotImplementedError()

    def parse_user_input(self):
        """
        Parses the user's input
        :return: void
        """
        raise NotImplementedError()

    def get_response(self):
        """
        Returns the response calculated by the plugin
        :return the response as a MessageProtocolEntity
        """
        raise NotImplementedError()

    @staticmethod
    def get_description(language):
        """
        Returns a helpful description of the plugin's syntax and functionality
        :param language: the language to be returned
        :return the description as string
        """
        raise NotImplementedError()

    def parallel_run(self):
        """
        Starts a parallel background activity if this class has one.
        Defaults to False if not implemented
        @:return False, if no parallel activity defined, should be implemented to return True if one is implemented.
        """
        if self:
            return False

    def send_message(self, entity):
        """
        Sends a message outside of the normal yowsup loop
        :param entity: the entity to be sent
        :return: void
        """
        if self.layer.muted:
            LogWriter.write_event_log("s(m)", entity)
        else:
            LogWriter.write_event_log("sent", entity)
            self.layer.to_lower(entity)

    def send_image(self, recipient, image_path, caption):
        """
        Sends an image outside of the normal yowsup loop
        :param recipient: the receiver of the image
        :param image_path: the file path to the image
        :param caption: the caption to be sent
        :return: void
        """
        if self.layer.muted:
            LogWriter.write_event_log("i(m)", WrappedTextMessageProtocolEntity(image_path + " --- " + caption,
                                                                               to=recipient))
        else:
            LogWriter.write_event_log("imgs", WrappedTextMessageProtocolEntity(image_path + " --- " + caption,
                                                                               to=recipient))
            self.layer.send_image(recipient.split("@")[0], image_path, caption)

    def send_audio(self, recipient, audio_path, audio_text="Audio"):
        """
        Sends an audio file outside of the normal yowsup loop
        :param recipient: the receiver of the audio
        :param audio_path: the audio file to be send
        :param audio_text: text for logging purposes
        :return: void
        """
        if self.layer.muted:
            LogWriter.write_event_log("a(m)", WrappedTextMessageProtocolEntity(audio_text, to=recipient))
        else:
            LogWriter.write_event_log("audi", WrappedTextMessageProtocolEntity(audio_text, to=recipient))
            self.layer.send_audio(recipient.split("@")[0], audio_path)
