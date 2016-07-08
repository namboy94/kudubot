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

from nose.tools import with_setup
from nose.tools import assert_false
from nose.tools import assert_true

from kudubot.connection.generic.Message import Message
from kudubot.services.simple_services.SimpleEqualsResponseService import SimpleEqualsResponseService


# noinspection PyMethodMayBeStatic
class TestEqualsResponseService(object):
    """
    A Unit Test Class for a Service class
    """

    correct_messages = ["uptime"]
    incorrect_messages = [" uptime "]
    service = SimpleEqualsResponseService

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
            print("Testing correct Regex for: " + message)
            assert_true(self.service.regex_check(message_object))
        for message in self.incorrect_messages:
            message_object = Message(message_body=message, address="")
            assert_false(self.service.regex_check(message_object))
            print("Testing incorrect Regex for: " + message)
