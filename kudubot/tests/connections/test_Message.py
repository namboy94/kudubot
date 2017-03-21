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
from kudubot.users.Contact import Contact
from kudubot.connections.Message import Message


class UnitTests(unittest.TestCase):

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_creating_message(self):

        message = Message("title", "body", Contact(-1, "A", "Add"), Contact(-2, "B", "Badd"), Contact(-3, "C", "Cadd"),
                          timestamp=1.0)

        self.assertEqual(message.message_title, "title")
        self.assertEqual(message.message_body, "body")
        self.assertEqual(message.receiver.display_name, "A")
        self.assertEqual(message.sender.display_name, "B")
        self.assertEqual(message.sender_group.display_name, "C")
        self.assertEqual(message.timestamp, 1.0)
