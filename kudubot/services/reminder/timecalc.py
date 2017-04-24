"""
LICENSE:
Copyright 2017 Hermann Krumrey

This file is part of kudubot-reminder.

    kudubot-reminder is an extension module for kudubot. It provides
    a Service that can send messages at specified times.

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

from datetime import datetime


def convert_datetime_to_string(to_convert: datetime) -> str:
    """
    Converts a datetime object to a string that can be stored in the database

    :param to_convert: The datetime object to convert
    :return: The datetime as a string
    """
    return to_convert.strftime("%Y-%m-%d:%H-%M-%S")


def convert_string_to_datetime(to_convert: str) -> datetime:
    """
    Converts a string of the form '%Y-%m-%d:%H-%M-%S' to a datetime object

    :param to_convert: The string to convert
    :return: the resulting datetime object
    """
    return datetime.strptime(to_convert, "%Y-%m-%d:%H-%M-%S")
