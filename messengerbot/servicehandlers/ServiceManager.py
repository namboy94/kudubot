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

# from messengerbot.connection.generic.Connection import Connection
Connection = None
from messengerbot.connection.generic.Message import Message
from messengerbot.servicehandlers.ServiceConfigParser import ServiceConfigParser


class ServiceManager(object):
    """
    The ServiceManager class handles the implemented Services and processes incoming messages
    """

    all_services = []
    """
    A list of all implemented services
    """

    active_services = []
    """
    A list of active services defined by the Service Config Parser
    """

    connection = None
    """
    The connection used to communicate
    """

    def __init__(self, connection: 'Connection') -> None:
        """
        Constructor for the ServiceManager class. It stores the connection as a class variable and parses
        local config files to determine which services should be active.

        :param connection: The connection that handles the communication for the services
        :return: None
        """
        self.connection = connection
        self.active_services = ServiceConfigParser.read_config(self.all_services, connection.identifier)
        self.start_background_processes()

    def process_message(self, message: Message) -> None:
        """
        Processes an incoming message using the active services
        :param message: The received message to process
        :return: None
        """
        # Check every service if the message matches the service-specific regex
        for service in self.active_services:
            if service.regex_check(message):
                concrete_service = service.__init__(self.connection)  # Create a service object
                concrete_service.process_message(message)  # Process the message using the selected service

    def start_background_processes(self) -> None:
        """
        Starts all parallel threads needed by the various services.
        :return: None
        """
        threads = []

        for service in self.active_services:
            if service.has_background_process:
                threads.append(Thread(target=service.__init__(self.connection).background_process))

        for thread in threads:
            thread.setDaemon(True)
            thread.start()
