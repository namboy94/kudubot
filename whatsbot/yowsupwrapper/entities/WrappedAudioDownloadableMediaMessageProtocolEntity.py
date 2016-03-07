# coding=utf-8
"""
Copyright 2015,2016 Hermann Krumrey

This file is part of whatsbot.

    whatsbot makes use of various third-party python modules to serve
    information via the online chat service Whatsapp.

    whatsbot is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    whatsbot is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with whatsbot.  If not, see <http://www.gnu.org/licenses/>.
"""

# imports
from yowsup.layers.protocol_media.protocolentities import AudioDownloadableMediaMessageProtocolEntity

try:
    from yowsupwrapper.entities.EntityAdapter import EntityAdapter
except ImportError:
    from whatsbot.yowsupwrapper.entities.EntityAdapter import EntityAdapter


class WrappedAudioDownloadableMediaMessageProtocolEntity(EntityAdapter):
    """

    """

    @staticmethod
    def from_file_path(file_path, url, ip, to):
        """

        :param file_path:
        :param url:
        :param ip:
        :param to:
        :return:
        """
        super().__init__(AudioDownloadableMediaMessageProtocolEntity.fromFilePath(file_path, url, ip, to=to))
