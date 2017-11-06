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

from kudubot.entities.Message import Message
from kudubot.services.BaseService import BaseService


# noinspection PyAbstractClass
class AuthenticatedService(BaseService):
    """
    Service that can only be used by admin users
    """

    # -------------------------------------------------------------------------
    #                  _,-'/-'/                                Here be dragons!
    #  .      __,-; ,'( '/
    #   \.    `-.__`-._`:_,-._       _ , . ``
    #    `:-._,------' ` _,`--` -: `_ , ` ,' :
    #       `---..__,,--'            ` -'. -'
    # Everything below this should not be overridden by subclasses
    # -------------------------------------------------------------------------

    def is_applicable_to_authenticated(self, message: Message) -> bool:
        """
        Checks if the sender of the message has administrative privileges
        :param message: The message to check
        :return: True if the sender is an admin, False otherwise
        """
        is_admin = self.connection.authenticator.is_admin(message.sender)
        if not is_admin:
            self.logger.info("Authorizaton denied for " +
                             message.sender.address)
        return is_admin
