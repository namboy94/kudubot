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
    along with whatsbot.  If not, see <http://www.gnu.org/licenses/>.
"""

# imports
from threading import Thread

from messengerbot.connection.generic.Connection import Connection


class ServiceManager(object):
    """
    The ServiceManager class handles the implemented Services and processes incoming messages
    """

    all_plugins = []
    """
    A list of all implemented plugins
    """

    active_plugins = []
    """
    A list of active plugins defined by the Service Config Parser
    """

    connection = None
    """
    The connection used to communicate
    """

    def __init__(self, connection: Connection) -> None:
        """
        Constructor for the ServiceManager class. It stores the connection as a class variable and parses
        local config files to determine which plugins should be active.

        :param connection: The connection that handles the communication for the services
        :return: None
        """
        self.connection = connection
        self.active_plugins = ServiceConfigParser.read_plugin_config(self.all_plugins, connection.identifier)
        self.start_background_processes()

    def process_message(self, sender: str, message_body: str) -> None:
        """
        Processes an incoming message using the active services
        :param sender: The sender of the message
        :param message_body: The text of the message, used to determine which service to use
        :return: None
        """
        for plugin in self.active_plugins:
            if plugin.regex_check(message_body):  # Check every plugin if the message matches the plugin-specific regex
                concrete_plugin = plugin(self.connection)  # Create a plugin object
                concrete_plugin.process_message(sender, message_body)  # Process the message using the selected plugin

    def start_background_processes(self) -> None:
        """
        Starts all parallel threads needed by the various services.
        :return: None
        """
        threads = []

        for plugin in self.active_plugins:
            if plugin.has_background_process:
                threads.append(Thread(target=plugin(self.connection).background_process))

        for thread in threads:
            thread.setDaemon(True)
            thread.start()
