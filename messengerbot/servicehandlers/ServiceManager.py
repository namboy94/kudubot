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
from threading import Thread

# required services
from messengerbot.servicehandlers.required_services.HelpService import HelpService
from messengerbot.servicehandlers.required_services.MuterService import MuterService
from messengerbot.servicehandlers.required_services.ServiceSelectorService import ServiceSelectorService

# other services
from messengerbot.services.local_services.ReminderService import ReminderService
from messengerbot.services.local_services.RestarterService import RestarterService
from messengerbot.services.internet_services.TvdbService import TvdbService
from messengerbot.services.internet_services.WeatherService import WeatherService
from messengerbot.services.internet_services.KitMensaService import KitMensaService
from messengerbot.services.internet_services.KickTippService import KickTippService
from messengerbot.services.internet_services.GoogleTtsService import GoogleTtsService
from messengerbot.services.internet_services.EmailSenderService import EmailSenderService
from messengerbot.services.internet_services.ImageSenderService import ImageSenderService
from messengerbot.services.internet_services.FootballInfoService import FootballInfoService
from messengerbot.services.simple_services.SimpleEqualsResponseService import SimpleEqualsResponseService
from messengerbot.services.simple_services.SimpleContainsResponseService import SimpleContainsResponseService

from messengerbot.connection.generic.Message import Message
from messengerbot.servicehandlers.ServiceConfigParser import ServiceConfigParser

# Weird import strucutre due to cyclic imports
try:
    from messengerbot.connection.generic.Connection import Connection
except ImportError:
    Connection = object


class ServiceManager(object):
    """
    The ServiceManager class handles the implemented Services and processes incoming messages
    """

    all_services = [HelpService,
                    MuterService,
                    ServiceSelectorService,
                    RestarterService,
                    ReminderService,
                    KickTippService,
                    FootballInfoService,
                    WeatherService,
                    GoogleTtsService,
                    TvdbService,
                    KitMensaService,
                    EmailSenderService,
                    ImageSenderService,
                    SimpleEqualsResponseService,
                    SimpleContainsResponseService]
    """
    A list of all implemented services
    """

    protected_services = [HelpService,
                          MuterService,
                          ServiceSelectorService]
    """
    A list of services that may not be deactivated
    """

    active_services = []
    """
    A list of active services defined by the Service Config Parser
    """

    connection = None
    """
    The connection used to communicate
    """

    def __init__(self, connection: Connection) -> None:
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
                # noinspection PyCallingNonCallable
                concrete_service = service(self.connection)  # Create a service object
                concrete_service.process_message(message)  # Process the message using the selected service

    def start_background_processes(self) -> None:
        """
        Starts all parallel threads needed by the various services.
        :return: None
        """
        threads = []

        for service in self.active_services:
            if service.has_background_process:
                # noinspection PyCallingNonCallable
                threads.append(Thread(target=service(self.connection).background_process))

        for thread in threads:
            thread.setDaemon(True)
            thread.start()
