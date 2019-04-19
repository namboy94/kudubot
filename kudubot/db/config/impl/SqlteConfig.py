"""LICENSE
Copyright 2015 Hermann Krumrey <hermann@krumreyh.com>

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
LICENSE"""

from kudubot.db.config.DbConfig import DbConfig


class SqliteConfig(DbConfig):
    """
    Database configuration for SQLite
    """

    def __init__(self, path: str):
        """
        Initializes the database configuration
        :param path: The path to the SQLite database file
        """
        self.path = path

    def to_uri(self) -> str:
        """
        Turns the configuration into an URI that SQLAlchemy can use
        :return: The URI
        """
        return "sqlite:///{}".format(self.path)
