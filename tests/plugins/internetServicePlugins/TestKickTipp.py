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
from nose.tools import assert_true

try:
    from plugins.internetServicePlugins.KickTipp import KickTipp
    from yowsupwrapper.entities.WrappedTextMessageProtocolEntity import WrappedTextMessageProtocolEntity
except ImportError:
    from whatsbot.plugins.internetServicePlugins.KickTipp import KickTipp
    from whatsbot.yowsupwrapper.entities.WrappedTextMessageProtocolEntity import WrappedTextMessageProtocolEntity


class Test(object):
    """
    Unit Test Class that tests the Kicktipp plugin
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
    def test_stellies(self):
        """
        Tests the results for the Kicktipp community "Stellies"
        """
        plugin = KickTipp(self.layer, WrappedTextMessageProtocolEntity(body="/kicktipp stellies", _from=self.sender))
        assert_true(plugin.regex_check())
        plugin.parse_user_input()
        reply = plugin.get_response().get_body()

        users = ["MisterD", "SirSimon", "Frederick", "hermann", "E.I"]
        for user in users:
            assert_true(user in reply)
