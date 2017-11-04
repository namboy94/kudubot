"""
Copyright 2015-2017 Hermann Krumrey

This file is part of kudubot.

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
"""

from typing import List
from kudubot.entities.Message import Message
from kudubot.services.Service import Service


class ServiceListerService(Service):
    def is_applicable_to(self, message: Message) -> bool:
        return message.message_body == "/list"

    @staticmethod
    def define_requirements() -> List[str]:
        return []

    @staticmethod
    def define_identifier() -> str:
        return "service_lister"

    def handle_message(self, message: Message):
        self.reply("A", "B", message)

        reply = "List of active Services:"

        services = self.connection.services # type: List[Service]
        for service in services:
            self.reply("Service", service.define_identifier(), message)
