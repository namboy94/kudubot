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
from kudubot.services.BaseService import BaseService


class DummyService(BaseService):
    """
    A class that implements a Service for use in unit tests
    """

    @staticmethod
    def define_requirements() -> List[str]:
        return []

    @staticmethod
    def define_identifier() -> str:
        return "dummyservice"

    def handle_message(self, message: Message):
        pass

    def is_applicable_to(self, message: Message) -> bool:
        pass


class DummyServiceWithValidDependency(DummyService):
    """
    A Service that has itself (or DummyService) as its only dependency
    """

    @staticmethod
    def define_requirements() -> List[str]:
        return ["dummyservice"]


class DummyServiceWithInvalidDependency(DummyService):
    """
    A service that has an invalid dependency
    """

    @staticmethod
    def define_requirements() -> List[str]:
        return ["otherservice"]
