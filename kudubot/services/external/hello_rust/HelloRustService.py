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

from typing import List
from kudubot.services.ExternalService import ExternalService


class HelloRustService(ExternalService):
    """
    A service that responds with 'Hello!' if you send it 'Hello Rust!'
    More a proof of concept than anything.
    """

    def define_executable_file_url(self):
        self.resolve_github_release_asset_url("namboy94", "kudubot", "hello-rust")

    def define_executable_command(self) -> List[str]:
        return []

    @staticmethod
    def define_identifier() -> str:
        return "hello_rust"
