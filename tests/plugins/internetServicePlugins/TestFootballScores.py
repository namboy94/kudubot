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
from nose.tools import assert_equal
from nose.tools import assert_true

try:
    from plugins.internetServicePlugins.FootballScores import FootballScores
    from yowsupwrapper.entities.WrappedTextMessageProtocolEntity import WrappedTextMessageProtocolEntity
except ImportError:
    from whatsbot.plugins.internetServicePlugins.FootballScores import FootballScores
    from whatsbot.yowsupwrapper.entities.WrappedTextMessageProtocolEntity import WrappedTextMessageProtocolEntity


class TestFootballScores(object):
    """
    Unit Test Class that tests the Football Scores Plugin
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
    def test_bundesliga(self):
        """
        Tests the results for the bundesliga
        """
        table_messages = [WrappedTextMessageProtocolEntity(_from=self.sender, body="/table"),
                          WrappedTextMessageProtocolEntity(_from=self.sender, body="/table germany, bundesliga")]
        matchday_messages = [WrappedTextMessageProtocolEntity(_from=self.sender, body="/matchday"),
                             WrappedTextMessageProtocolEntity(_from=self.sender, body="/matchday germany, bundesliga")]

        last = ""
        for message in table_messages:
            plugin = FootballScores(self.layer, message)
            assert_true(plugin.regex_check())
            plugin.parse_user_input()
            if not last:
                last = plugin.get_response().get_body()
            else:
                assert_equal(last, plugin.get_response().get_body())

        last = ""
        for message in matchday_messages:
            plugin = FootballScores(self.layer, message)
            assert_true(plugin.regex_check())
            plugin.parse_user_input()
            if not last:
                last = plugin.get_response().get_body()
            else:
                assert_equal(last, plugin.get_response().get_body())

    @with_setup(setup, teardown)
    def test_england_premier_league(self):
        """
        Tests the results for the english premier league
        """
        table_plugin = FootballScores(self.layer,
                                      WrappedTextMessageProtocolEntity(
                                          _from=self.sender, body="/table england, premier-league"))
        matchday_plugin = FootballScores(self.layer,
                                         WrappedTextMessageProtocolEntity(
                                             _from=self.sender, body="/matchday england, premier-league"))

        assert_true(table_plugin.regex_check())
        assert_true(matchday_plugin.regex_check())
        table_plugin.parse_user_input()
        matchday_plugin.parse_user_input()

        assert_true(len(table_plugin.get_response().get_body().split("\n")) == 21)
        # TODO Make this smarter
        # print(matchday_plugin.get_response().get_body().split("\n"))
        # assert_true(len(matchday_plugin.get_response().get_body().split("\n")) == 11)

    @with_setup(setup, teardown)
    def test_namibia_premier_league(self):
        """
        Tests the results for the namibian premier league
        """
        table_plugin = FootballScores(self.layer,
                                      WrappedTextMessageProtocolEntity(
                                          _from=self.sender, body="/table namibia, premier-league"))
        matchday_plugin = FootballScores(self.layer,
                                         WrappedTextMessageProtocolEntity(
                                             _from=self.sender, body="/matchday namibia, premier-league"))

        assert_true(table_plugin.regex_check())
        assert_true(matchday_plugin.regex_check())
        table_plugin.parse_user_input()
        matchday_plugin.parse_user_input()

        assert_true(len(table_plugin.get_response().get_body().split("\n")) == 17)
        assert_true(len(matchday_plugin.get_response().get_body().split("\n")) == 9)

    @with_setup(setup, teardown)
    def test_spanish_primera_league(self):
        """
        Tests the results for the spanish primera division
        """
        table_plugin = FootballScores(self.layer,
                                      WrappedTextMessageProtocolEntity(
                                          _from=self.sender, body="/table spain, primera-division"))
        matchday_plugin = FootballScores(self.layer,
                                         WrappedTextMessageProtocolEntity(
                                             _from=self.sender, body="/matchday spain, primera-division"))

        assert_true(table_plugin.regex_check())
        assert_true(matchday_plugin.regex_check())
        table_plugin.parse_user_input()
        matchday_plugin.parse_user_input()

        assert_true(len(table_plugin.get_response().get_body().split("\n")) == 21)
        assert_true(len(matchday_plugin.get_response().get_body().split("\n")) == 11)
