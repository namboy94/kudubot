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

from nose.tools import with_setup
from nose.tools import assert_false
from nose.tools import assert_true

try:
    from plugins.internetServicePlugins.ImageSender import ImageSender
    from yowsupwrapper.entities.WrappedTextMessageProtocolEntity import WrappedTextMessageProtocolEntity
except ImportError:
    from whatsbot.plugins.internetServicePlugins.ImageSender import ImageSender
    from whatsbot.yowsupwrapper.entities.WrappedTextMessageProtocolEntity import WrappedTextMessageProtocolEntity


class Test(object):
    """
    Unit Test Class that tests the Image Sender Plugin
    """

    def __init__(self):
        """
        Constructor
        """
        self.message = None
        self.layer = None
        self.sender = "test@test.com"

    @classmethod
    def setup_class(cls):
        """
        Sets up the test class
        """
        print()

    @classmethod
    def teardown_class(cls):
        """
        Tears down the test class
        """
        print()

    def setup(self):
        """
        Sets up a test
        """
        str(self)

    def teardown(self):
        """
        Tears down a test
        """
        str(self)

    @with_setup(setup, teardown)
    def test_regex(self):
        """
        Tests the regex cehck function
        """
        correct = ["/img http://image.com/image.jpg",
                   "/img https://image.com/image.jpg",
                   "/img www.image.com/image.jpg",
                   "/img http://image.com/image.png",
                   "/img https://image.com/image.png",
                   "/img www.image.com/image.png",
                   "/img http://www.image.com/image.jpg",
                   "/img https://www.image.com/image.jpg",
                   "/img http://www.image.com/image.png",
                   "/img https://www.image.com/image.png"]

        incorrect = ["/img http://image.com/image.jpg&&reboot",
                     "/img http://image&&reboot.com/image.jpg",
                     "/img randomsrinsadalkdsads;k;m;m;m;k;a",
                     "/img http://image.com/ image.jpg"]

        for correct_message in correct:
            plugin = ImageSender(self.layer, WrappedTextMessageProtocolEntity(body=correct_message,
                                                                              _from=self.sender))
            assert_true(plugin.regex_check())

        for incorrect_message in incorrect:
            plugin = ImageSender(self.layer, WrappedTextMessageProtocolEntity(body=incorrect_message,
                                                                              _from=self.sender))
            assert_false(plugin.regex_check())
