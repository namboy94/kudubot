# coding=utf-8
"""
Copyright 2015,2016 Hermann Krumrey

This file is part of messengerbot.

    messengerbot makes use of various third-party python modules to serve
    information via the online chat services.

    messengerbot is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    messengerbot is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with messengerbot.  If not, see <http://www.gnu.org/licenses/>.
"""

from nose.tools import with_setup
from nose.tools import assert_false
from nose.tools import assert_true

from messengerbot.connection.generic.Message import Message
from messengerbot.services.internet_services.EmailSenderService import EmailSenderService


# noinspection PyMethodMayBeStatic
class TestEmailSenderService(object):
    """
    A Unit Test Class for a Service class
    """
    # TODO MAKE ^ PART OF REGEX
    # TODO CHECK TLD ENDING

    correct_messages = ["/email \"Test\" user@domain.tld", "/email \"Test\" \"Title\" user@domain.tld",
                        "/email \"Test Message\" user@domain.tld", "/email \"Te st\" \"Title Test\" user@domain.tld"]
    incorrect_messages = ["---/email \"test\" user@domain.com", "/email \"test\" user@domain.com---", "/email",
                          "/email \"tes\"t message\" user@domain.tld", "/email \"tes\"t \"mes\"sage\" user@domain.tld"]
    service = EmailSenderService

    @classmethod
    def setup_class(cls):
        """
        Sets up the test class
        """
        pass

    @classmethod
    def teardown_class(cls):
        """
        Tears down the test class
        """
        pass

    def setup(self):
        """
        Sets up a test
        """
        pass

    def teardown(self):
        """
        Tears down a test
        """
        pass

    @with_setup(setup, teardown)
    def test_regex(self):
        """
        Tests the service's regex check
        """
        for message in self.correct_messages:
            message_object = Message(message_body=message, address="")
            print(message)
            assert_true(self.service.regex_check(message_object))
        for message in self.incorrect_messages:
            message_object = Message(message_body=message, address="")
            assert_false(self.service.regex_check(message_object))
