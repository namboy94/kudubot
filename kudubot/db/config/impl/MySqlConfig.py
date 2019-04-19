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


class MySqlConfig(DbConfig):
    """
    Database configuration for MySQL
    """

    def __init__(
            self,
            address: str,
            port: str,
            name: str,
            user: str,
            password: str,
    ):
        """
        Initializes the database configuration
        :param address: The database address
        :param port: The database port
        :param name: The database name
        :param user: The database user
        :param password: The database password
        """
        self.address = address
        self.port = port
        self.name = name
        self.user = user
        self.password = password

    def to_uri(self) -> str:
        """
        Turns the configuration into an URI that SQLAlchemy can use
        :return: The URI
        """
        return "mysql://{}:{}@{}:{}/{}".format(
            self.user, self.password, self.address, self.port, self.name
        )
