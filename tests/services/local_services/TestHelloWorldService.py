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
from kudubot.services.local_services.HelloWorldService import HelloWorldService


# noinspection PyMethodMayBeStatic
class TestHelloWorldService(object):
    """
    A Unit Test Class for the HelloWorldService class
    """

    correct_messages = ["/helloworld java", "/helloworld c++", "/helloworld c#", "/helloworld x86 assembly",
                        "/helloworld list"]
    incorrect_messages = ["/helloworld", "/helloworld  python", "/helloworld assembly x86", "helloworld python",
                          "/ helloworld haskell", " /helloworld erlang", "/helloworld bash "]

    service = HelloWorldService
    initialized_service = None
    response = ""

    def store_reply(self, reply_message: Message) -> None:
        """
        Stores the reply in a variable

        :param reply_message: the reply
        :return: None
        """
        self.response = reply_message.message_body

    @classmethod
    def setup_class(cls) -> None:
        """
        Sets up the test class

        :return: None
        """
        pass

    @classmethod
    def teardown_class(cls) -> None:
        """
        Tears down the test class

        :return: None
        """
        pass

    def setup(self) -> None:
        """
        Sets up a test

        :return: None
        """

        class Dummy(object):
            """
            Just a dummy connection class
            """
            pass

        dummy_connection = Dummy()
        dummy_connection.last_used_language = "en"
        dummy_connection.identifier = "dummy"
        self.initialized_service = self.service(dummy_connection)
        self.initialized_service.send_text_message = self.store_reply

    def teardown(self) -> None:
        """
        Tears down a test

        :return: None
        """
        pass

    @with_setup(setup, teardown)
    def test_regex(self) -> None:
        """
        Tests the service's regex check

        :return: None
        """
        for message in self.correct_messages:
            message_object = Message(message_body=message, address="")
            print(message)
            assert_true(self.service.regex_check(message_object))
        for message in self.incorrect_messages:
            message_object = Message(message_body=message, address="")
            assert_false(self.service.regex_check(message_object))

    def test_list_response(self) -> None:
        """
        Tests the service's list functionality

        :return: None
        """
        message = Message(message_body="/helloworld list", address="")
        self.initialized_service.process_message(message)
        for language in HelloWorldService.implementations:
            assert_true(language in self.response)
