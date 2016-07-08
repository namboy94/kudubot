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
import time
import email
import imaplib
from typing import Tuple

from kudubot.logger.PrintLogger import PrintLogger
from kudubot.connection.generic.Message import Message


class ImapListener(object):
    """
    Class that implements a listener for IMAP messages
    """

    imap = None
    """
    The imap connection to the email server receiving messages
    """

    callback = None
    """
    The method that gets called whenever a new message arrives
    """

    def __init__(self, credentials: Tuple[str, str, str, str, str], callback_function: callable)\
            -> None:
        """
        Constructor for the ImapListener class that gets the necessary credentials for authenticating with the
        IMAP server via parameters, as well as a callback function that gets called whenever a new email
        is received.

        :param credentials: Credentials to log on to the IMAP server:
                                email-address, password, server, imap port, smtp port
        :param callback_function: The on_incoming_message method of the EmailConnection
        :return: None
        """
        # unpack the credentials
        username, password, server, imap_port, smtp_port = credentials

        # store the callback
        self.callback = callback_function

        PrintLogger.print("Connecting to the IMAP server", 1)

        # Connect to the server
        self.imap = imaplib.IMAP4_SSL("imap." + server, int(imap_port))
        self.imap.login(username, password)

    def listen(self) -> None:
        """
        Continuously checks for new unread messages and packs them as a Message object.
        Every time a message is received, the callback function is called with the Message object

        :return: None
        """
        PrintLogger.print("Starting listening for new Email messages", 1)

        while True:
            PrintLogger.print("Looping Email Listener", 3)

            # select the Inbox folder
            self.imap.select('INBOX')

            # Get the unseen email ids
            email_ids = self.imap.search(None, '(UNSEEN)')[1]

            # Now read all unseen emails
            for num in email_ids[0].split():
                message = self.imap.fetch(num, '(RFC822)')[1]  # Fetch the email
                self.imap.store(num, '+FLAGS', '\\Seen')  # Mark the email as read

                email_message = email.message_from_bytes(message[0][1])  # generate an email obect from the message

                try:
                    sender_name = email_message['From'].split(" <")[0]
                    sender_address = email_message['From'].split("<", 1)[1].rsplit(">", 1)[0]
                except IndexError:
                    sender_name = email_message["From"]
                    sender_address = sender_name

                title = email_message["Subject"]
                timestamp = time.mktime(email.utils.parsedate(email_message['Date']))
                body = ""

                for part in email_message.walk():
                    if part.get_content_type() == 'text/plain':
                        body += (part.get_payload()) + "\n"
                body = body.rstrip()

                message_object = Message(message_body=body, message_title=title, address=sender_address, incoming=True,
                                         name=sender_name, group=False, single_name="", single_address="",
                                         timestamp=timestamp)

                self.callback(message_object)

            # Sleep 2 seconds after every check
            time.sleep(2)
