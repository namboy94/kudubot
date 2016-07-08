# coding=utf-8
"""
LICENSE:
Copyright 2015,2016 Hermann Krumrey

This file is part of kudubot.

    kudubot makes use of various third-party python modules to serve
    information via online chat services.

    kudubot is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    kudubot is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with kudubot.  If not, see <http://www.gnu.org/licenses/>.
LICENSE
"""

# imports
import smtplib
import mimetypes
from typing import Tuple, List
from email.mime.base import MIMEBase
from email.mime.text import MIMEText
from email.mime.audio import MIMEAudio
from email.mime.image import MIMEImage
from email.mime.multipart import MIMEMultipart

from kudubot.connection.generic.Message import Message


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
        body = MIMEText(message.message_body, 'plain')
        self.send_mime_part_email([body], message.message_title, message.address)

    def send_image_email(self, image_path: str, title: str, recipient: str) -> None:
        """
        Sends an embedded image via email and a title for it as the email subject

        :param image_path: the path to the image
        :param title: the image title
        :param recipient: the receiver of the email message
        :return: None
        """
        sub_type = self.guess_file_type(image_path)

        image_file = open(image_path, 'rb')  # Open the file in read-bytes mode
        image_data = image_file.read()
        image_file.close()

        image = MIMEImage(image_data, _subtype=sub_type)
        self.send_mime_part_email([image], title, recipient)

    def send_audio_email(self, audio_path: str, title: str, recipient: str) -> None:
        """
        Sends an audio file via email and a title for it as the email subject

        :param audio_path: the path to the audio file
        :param title: the audio title
        :param recipient: the receiver of the email message
        :return: None
        """
        sub_type = self.guess_file_type(audio_path)

        audio_file = open(audio_path, 'rb')  # Open the file in read-bytes mode
        audio_data = audio_file.read()
        audio_file.close()

        audio = MIMEAudio(audio_data, _subtype=sub_type)
        self.send_mime_part_email([audio], title, recipient)

    # noinspection PyTypeChecker
    def send_mime_part_email(self, mime_objects: List[MIMEBase], title: str, recipient: str) -> None:
        """
        Sends an email containing MIME Parts (like MIMEText or MIMEImage) and a title to a receiving
        email address

        :param mime_objects: a list of MIME objects to be sent
        :param title: the title of the email
        :param recipient: the receiver of the email
        :return: None
        """
        email_address, password, server, imap_port, smtp_port = self.credentials

        email_message = MIMEMultipart()
        email_message['From'] = email_address
        email_message['To'] = recipient
        email_message['Subject'] = title

        for part in mime_objects:
            email_message.attach(part)

        # Initialize SMTP Connection
        smtp = smtplib.SMTP_SSL("smtp." + server, int(smtp_port))
        smtp.set_debuglevel(0)
        smtp.login(email_address, password)

        # Send Email
        smtp.sendmail(email_address, recipient, email_message.as_string())
        smtp.quit()

    @staticmethod
    def guess_file_type(file_path: str) -> str:
        """
        Guesses the file tpye of a media file according to its file type extension

        :param file_path: the file to be checked
        :return: the media (sub)type
        """
        content_type, encoding = mimetypes.guess_type(file_path)
        if content_type is None or encoding is not None:
            content_type = 'application/octet-stream'
        return content_type.split('/', 1)[1]
