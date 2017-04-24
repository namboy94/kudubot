"""
LICENSE:
Copyright 2017 Hermann Krumrey

This file is part of kudubot-anime-reminder.

    kudubot-anime-reminder is an extension module for kudubot. It provides
    a Service that can send messages whenever a newly aired anime episode
    has aired.

    kudubot-reminder is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    kudubot-reminder is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with kudubot-reminder.  If not, see <http://www.gnu.org/licenses/>.
LICENSE
"""

from kudubot.services.HelperService import HelperService
from kudubot_anime_reminder.database import initialize_database
from kudubot_anime_reminder.AnimeReminderService import AnimeReminderService


class DummyAnimeReminderService(AnimeReminderService):
    """
    Dummy class that does not start a thread once initialized, but initializes the database
    """
    # noinspection PyMissingConstructor
    def __init__(self, connection):
        super(HelperService, self).__init__(connection)
        initialize_database(self.connection.db)
