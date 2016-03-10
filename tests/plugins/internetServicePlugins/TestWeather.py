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
    from plugins.internetServicePlugins.Weather import Weather
    from yowsupwrapper.entities.WrappedTextMessageProtocolEntity import WrappedTextMessageProtocolEntity
except ImportError:
    from whatsbot.plugins.internetServicePlugins.Weather import Weather
    from whatsbot.yowsupwrapper.entities.WrappedTextMessageProtocolEntity import WrappedTextMessageProtocolEntity


class TestWeather(object):
    """
    Unit Test Class that tests the Weather Plugin
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
    def test_karlsruhe_with_modes(self):
        """
        Tests the weather for karlsruhe
        """
        karlsruhe_normal = [WrappedTextMessageProtocolEntity(_from=self.sender, body="/wetter"),
                            WrappedTextMessageProtocolEntity(_from=self.sender, body="/wetter karlsruhe"),
                            WrappedTextMessageProtocolEntity(_from=self.sender, body="/wetter karlsruhe, germany"),
                            WrappedTextMessageProtocolEntity(_from=self.sender, body="/wetter karlsruhe, ks, germany")]
        karlsruhe_verbose = [WrappedTextMessageProtocolEntity(_from=self.sender,
                                                              body="/wetter:verbose;"),
                             WrappedTextMessageProtocolEntity(_from=self.sender,
                                                              body="/wetter:verbose; karlsruhe"),
                             WrappedTextMessageProtocolEntity(_from=self.sender,
                                                              body="/wetter:verbose; karlsruhe, germany"),
                             WrappedTextMessageProtocolEntity(_from=self.sender,
                                                              body="/wetter:verbose; karlsruhe, ks, germany")]
        karlsruhe_text = [WrappedTextMessageProtocolEntity(_from=self.sender,
                                                           body="/wetter:text;"),
                          WrappedTextMessageProtocolEntity(_from=self.sender,
                                                           body="/wetter:text; karlsruhe"),
                          WrappedTextMessageProtocolEntity(_from=self.sender,
                                                           body="/wetter:text; karlsruhe, germany"),
                          WrappedTextMessageProtocolEntity(_from=self.sender,
                                                           body="/wetter:text; karlsruhe, ks, germany")]
        karlsruhe_verbose_text = [WrappedTextMessageProtocolEntity(_from=self.sender,
                                                                   body="/wetter:text;verbose;"),
                                  WrappedTextMessageProtocolEntity(_from=self.sender,
                                                                   body="/wetter:text;verbose; karlsruhe"),
                                  WrappedTextMessageProtocolEntity(_from=self.sender,
                                                                   body="/wetter:text;verbose; karlsruhe, germany"),
                                  WrappedTextMessageProtocolEntity(_from=self.sender,
                                                                   body="/wetter:text;verbose; karlsruhe, ks, germany")]

        assert_true(self.__city_results_equal__(karlsruhe_normal))
        assert_true(self.__city_results_equal__(karlsruhe_verbose))
        assert_true(self.__city_results_equal__(karlsruhe_text))
        assert_true(self.__city_results_equal__(karlsruhe_verbose_text))

    @with_setup(setup, teardown)
    def test_windhoek(self):
        """
        Tests the weather for karlsruhe
        """
        windhoek = [WrappedTextMessageProtocolEntity(_from=self.sender, body="/wetter windhoek"),
                    WrappedTextMessageProtocolEntity(_from=self.sender, body="/wetter windhoek, namibia"),
                    WrappedTextMessageProtocolEntity(_from=self.sender, body="/wetter windhoek, kh, namibia")]

        assert_true(self.__city_results_equal__(windhoek))

    @with_setup(setup, teardown)
    def test_salt_lake(self):
        """
        Tests the weather for karlsruhe
        """
        windhoek = [WrappedTextMessageProtocolEntity(_from=self.sender, body="/wetter salt lake city"),
                    WrappedTextMessageProtocolEntity(_from=self.sender, body="/wetter salt lake city, usa"),
                    WrappedTextMessageProtocolEntity(_from=self.sender, body="/wetter salt lake city, ut, usa")]

        assert_true(self.__city_results_equal__(windhoek))

    def __city_results_equal__(self, city_messages):
        """
        Tests if a list of messages return the same string
        :param city_messages: the list of messages
        :return: True, if all are equal, false otherwise
        """
        results = []
        for message in city_messages:
            plugin = Weather(self.layer, message)
            assert_equal(plugin.regex_check(), True)
            plugin.parse_user_input()
            results.append(plugin.get_response().get_body())

        sample_message = results[0]

        for result in results:
            if result != sample_message:
                return False
        return True
