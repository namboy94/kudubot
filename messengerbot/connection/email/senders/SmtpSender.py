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
import smtplib
from typing import Tuple
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

from messengerbot.connection.generic.Message import Message


class SmtpSender(object):
    """
    Class that handles the sending of emails via SMTP
    """

    credentials = ()
    """
    The credentials used to log on to the SMTP server
    """

    def __init__(self, credentials: Tuple[str, str, str, str, str]) -> None:
        """
        Constructor for the SmtpSender class that stores the credentials as a class variable

        :param credentials: The credentials to store
        :return: None
        """
        self.credentials = credentials

    def send_text_email(self, message: Message) -> None:
        """
        Sends an email message via SMTP
        :param message: The message to be send
        :return: None
        """
        email_address, password, server, imap_port, smtp_port = self.credentials

        # Set up message as email
        body = MIMEText(message.message_body, 'plain')
        email_message = MIMEMultipart()
        email_message['From'] = email_address
        email_message['To'] = message.address
        email_message['Subject'] = message.message_title
        email_message.attach(body)

        # Initialize SMTP Connection
        smtp = smtplib.SMTP_SSL("smtp." + server, int(smtp_port))
        smtp.set_debuglevel(0)
        smtp.login(email_address, password)

        # Send Email
        smtp.sendmail(email_address, message.address, email_message.as_string())
        smtp.quit()
