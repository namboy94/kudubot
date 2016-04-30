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

import os
import re
from threading import Thread
from subprocess import Popen, PIPE
from PIL import Image

try:
    from plugins.GenericPlugin import GenericPlugin
    from yowsupwrapper.entities.WrappedTextMessageProtocolEntity import WrappedTextMessageProtocolEntity
except ImportError:
    from whatsbot.plugins.GenericPlugin import GenericPlugin
    from whatsbot.yowsupwrapper.entities.WrappedTextMessageProtocolEntity import WrappedTextMessageProtocolEntity


class ImageSender(GenericPlugin):
    """
    The ImageSender Class
    """

    def __init__(self, layer, message_protocol_entity=None):
        """
        Constructor
        Defines parameters for the plugin.
        :param layer: the overlying yowsup layer
        :param message_protocol_entity: the received message information
        :return: void
        """
        super().__init__(layer, message_protocol_entity)

        self.images_dir = os.getenv("HOME") + "/.whatsbot/images/temp/"
        self.link = ""
        self.image_name = ""
        self.error = ""
        self.thread_is_done = False

    def regex_check(self):
        """
        Checks if the user input is valid for this plugin to continue
        :return: True if input is valid, False otherwise
        """
        if re.search(r"^/img (http(s)?://|www.)[^;>\| ]+(.png|.jpg)$", self.message):
            if "&&" in self.message:
                # self.send_message(WrappedTextMessageProtocolEntity("Nice try.", to=self.sender))
                return False
            else:
                return True
        else:
            return False

    def parse_user_input(self):
        """
        Parses the user's input
        :return: void
        """
        self.link = self.message.split("/img ")[1]
        self.image_name = self.link.rsplit("/", 1)[1]
        thread = Thread(target=self.__wget_image__)
        thread.start()
        thread.join(timeout=5)

    def get_response(self):
        """
        Returns the response calculated by the plugin
        :return: the response as a WrappedMessageProtocolEntity
        """
        if self.error:
            return WrappedTextMessageProtocolEntity(self.error, to=self.sender)
        try:
            image_file = self.images_dir + self.image_name
            if not os.path.isfile(image_file) or os.path.getsize(image_file) > 8000000:
                raise Exception("File too large or does not exist")
            elif not self.thread_is_done:
                raise Exception("Second thread didn't finish (Timeout)")
            else:
                im = Image.open(image_file)
                if im.size[0] > 8000 or im.size[1] > 4000:
                    raise Exception("Resolution too high")
                else:
                    self.send_image(self.entity.getFrom(), self.images_dir + self.image_name, self.link)
        except Exception as e:
            str(e)
            return WrappedTextMessageProtocolEntity("Sorry, image could not be sent", to=self.sender)

    @staticmethod
    def get_description(language):
        """
        Returns a helpful description of the plugin's syntax and functionality
        :param language: the language to be returned
        :return: the description as string
        """
        if language == "en":
            return
        else:
            return "Help not available in this language"

    @staticmethod
    def get_plugin_name():
        """
        Returns the plugin name
        :return: the plugin name
        """
        return "ImageSender Plugin"

    def __wget_image__(self):
        """
        Wgets the image from the link
        :return: void
        """
        try:
            spider_process_command = ['wget', '--spider', self.link]
            spider_process = Popen(spider_process_command, stdout=PIPE, stderr=PIPE)
            spider, spider_err = spider_process.communicate()
            spider_err = spider_err.decode()
            filesize = int(spider_err.split("Length: ")[1].split(" ")[0])
            if filesize > 8000000:
                raise Exception("File size too large")
            os.system("wget " + self.link + " -O " + self.images_dir + self.image_name)
        except Exception as e:
            if str(e) == "File size too large":
                self.error = str(e)
            else:
                self.error = "Error loading image from source."
        self.threadIsDone = True
