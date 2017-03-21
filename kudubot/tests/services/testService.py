"""
LICENSE:
Copyright 2015-2017 Hermann Krumrey

This file is part of kudubot.

    kudubot is a chat bot framework. It allows developers to write
    services for arbitrary chat services.

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

import unittest
from kudubot.services.Service import Service
from kudubot.tests.helpers.DummyService import DummyService


class UnitTests(unittest.TestCase):
    """
    Tests the Service class
    """

    def setUp(self):
        """
        :return: None
        """
        pass

    def tearDown(self):
        """
        :return: None
        """
        pass

    def test_abstract_methods(self):
        """
        Tests if the methods of the Service class are abstract
        :return: None
        """
        dummy = DummyService([])

        for method in [(Service.handle_message, 1),
                       (Service.is_applicable_to, 1)]:
            try:

                if method[1] == 0:
                    method[0](dummy)
                elif method[1] == 1:
                    method[0](dummy, dummy)
                self.fail()
            except NotImplementedError:
                pass
