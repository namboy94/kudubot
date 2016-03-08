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

import re
import os
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

try:
    from plugins.GenericPlugin import GenericPlugin
    from yowsupwrapper.entities.WrappedTextMessageProtocolEntity import WrappedTextMessageProtocolEntity
except ImportError:
    from whatsbot.plugins.GenericPlugin import GenericPlugin
    from whatsbot.yowsupwrapper.entities.WrappedTextMessageProtocolEntity import WrappedTextMessageProtocolEntity


class EmailSender(GenericPlugin):
    """
    The EmailSender Class
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
        self.email_creds = {}
        self.email_recipient = ""
        self.email_message = ""
        self.email_title = ""

    def regex_check(self):
        """
        Checks if the user input is valid for this plugin to continue
        :return: True if input is valid, False otherwise
        """
        return re.search(r"^/email (\"[^\"]+\") (\"[^\"]+\" )?[^ ]+@[^ ]+$", self.cap_message)

    def parse_user_input(self):
        """
        Parses the user's input
        :return: void
        """
        self.email_creds = self.parse_email_credentials()
        if not self.email_creds:
            return

        split_string = self.cap_message.split("/email \"")[1]
        first_string = split_string.split("\"")[0]
        split_string = split_string.split("\" ", 1)[1]
        title = split_string.startswith("\"")

        if title:
            self.email_title = first_string
            self.email_message = split_string.split("\"", 2)[1]
            split_string = split_string.split("\"", 2)[2]
            self.email_recipient = split_string.split(" ", 1)[1]
        else:
            self.email_title = ""
            self.email_message = first_string
            self.email_recipient = split_string

    def get_response(self):
        """
        Returns the response calculated by the plugin
        :return: the response as a MessageProtocolEntity
        """
        # Set up message
        msg = MIMEMultipart()
        msg['From'] = self.email_creds["adress"]
        msg['To'] = self.email_recipient
        msg['Subject'] = self.email_title
        body = MIMEText(self.email_message, 'plain')
        msg.attach(body)

        # Initialize Connection
        print(self.email_creds)
        smtp = smtplib.SMTP_SSL(self.email_creds["server"], int(self.email_creds["port"]))
        smtp.set_debuglevel(1)
        smtp.login(self.email_creds["adress"], self.email_creds["password"])

        # Send Email
        smtp.sendmail(self.email_creds["adress"], self.email_recipient, msg.as_string())
        smtp.quit()

        if not self.email_creds:
            return WrappedTextMessageProtocolEntity("No valid email credentials stored", to=self.sender)
        else:
            return WrappedTextMessageProtocolEntity("Email sent", to=self.sender)

    @staticmethod
    def get_description(language):
        """
        Returns a helpful description of the plugin's syntax and functionality
        :param language: the language to be returned
        :return: the description as string
        """
        if language == "en":
            return "/email\tSends an email\n" \
                   "syntax: /email <message> <recipient>"
        elif language == "de":
            return "/email\tSchickt eine email\n" \
                   "syntax: /email <Nachricht> <Empfänger>"
        else:
            return "Help not available in this language"

    @staticmethod
    def get_plugin_name():
        """
        Returns the plugin name
        :return: the plugin name
        """
        return "Email Sender Plugin"

    @staticmethod
    def parse_email_credentials():
        """
        Parses an email credential file
        :return: A dictionary of the server, port, adress and password, or False if an error occured
        """
        file = open(os.getenv("HOME") + "/.whatsbot/emailcreds", 'r')
        file_content = file.read().split("\n")
        file.close()
        info = {}

        count = 0

        for line in file_content:
            if line.startswith("server="):
                info["server"] = line.split("server=")[1]
                count += 1
            elif line.startswith("port="):
                info["port"] = line.split("port=")[1]
                count += 1
            elif line.startswith("adress="):
                info["adress"] = line.split("adress=")[1]
                count += 1
            elif line.startswith("password="):
                info["password"] = line.split("password=")[1]
                count += 1

        if count == 4:
            return info
        else:
            return False
