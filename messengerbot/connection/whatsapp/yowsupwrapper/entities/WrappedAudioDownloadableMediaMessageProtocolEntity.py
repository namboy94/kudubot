# coding=utf-8
"""
Copyright 2015,2016 Hermann Krumrey

This file is part of messengerbot.

    messengerbot makes use of various third-party python modules to serve
    information via online chat services.

    messengerbot is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    messengerbot is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with messengerbot.  If not, see <http://www.gnu.org/licenses/>.
"""

# imports
from yowsup.layers.protocol_media.protocolentities import AudioDownloadableMediaMessageProtocolEntity

from messengerbot.connection.whatsapp.yowsupwrapper.entities.EntityAdapter import EntityAdapter


class WrappedAudioDownloadableMediaMessageProtocolEntity(object):
    """
    Wrapper around the Audio Message Entity type
    """

    @staticmethod
    def from_file_path(file_path: str, url: str, ip: str, to: str) -> EntityAdapter:
        """
        Generates an Audio Entity from a file path

        :param file_path: the path to the audio file
        :param url: the whatsapp media URL
        :param ip: the receiver's IP adress
        :param to: the receiver's whatsapp address
        :return: the Audio Entity wrapped with an EntityAdapter
        """
        return EntityAdapter(AudioDownloadableMediaMessageProtocolEntity.fromFilePath(file_path, url, ip, to=to))
