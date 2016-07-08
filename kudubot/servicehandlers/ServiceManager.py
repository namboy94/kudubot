# coding=utf-8
"""
LICENSE:
Copyright 2015,2016 Hermann Krumrey

This file is part of kudubot.

    kudubot makes use of various third-party python modules to serve
    information via online chat services.

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
LICENSE
"""

# imports
from threading import Thread

# required services
from kudubot.servicehandlers.required_services.HelpService import HelpService
from kudubot.servicehandlers.required_services.MuterService import MuterService
from kudubot.servicehandlers.required_services.ServiceSelectorService import ServiceSelectorService

# other services
# from services.thirdparty.ResetService import ResetService
# from services.thirdparty.BotMuteService import BotMuteService
from kudubot.services.local_services.CasinoService import CasinoService
from kudubot.services.local_services.XkcdRngService import XkcdRngService
from kudubot.services.local_services.RouletteService import RouletteService
from kudubot.services.local_services.ReminderService import ReminderService
from kudubot.services.local_services.AsciiArtService import AsciiArtService
from kudubot.services.local_services.RestarterService import RestarterService
from kudubot.services.local_services.HelloWorldService import HelloWorldService
from kudubot.services.local_services.WeeklyReminderService import WeeklyReminderService
from kudubot.services.local_services.RandomKeyGeneratorService import RandomKeyGeneratorService
from kudubot.services.internet_services.KvvService import KvvService
from kudubot.services.internet_services.XkcdService import XkcdService
from kudubot.services.internet_services.TvdbService import TvdbService
from kudubot.services.internet_services.CinemaService import CinemaService
from kudubot.services.internet_services.ZkmKinoService import ZkmKinoService
from kudubot.services.internet_services.WeatherService import WeatherService
from kudubot.services.internet_services.KitMensaService import KitMensaService
from kudubot.services.internet_services.KickTippService import KickTippService
from kudubot.services.internet_services.GoogleTtsService import GoogleTtsService
from kudubot.services.internet_services.EmailSenderService import EmailSenderService
from kudubot.services.internet_services.ImageSenderService import ImageSenderService
from kudubot.services.internet_services.FootballInfoService import FootballInfoService
from kudubot.services.simple_services.SimpleCommandsService import SimpleCommandsService
from kudubot.services.simple_services.SimpleEqualsResponseService import SimpleEqualsResponseService
from kudubot.services.simple_services.SimpleContainsResponseService import SimpleContainsResponseService

from kudubot.logger.PrintLogger import PrintLogger
from kudubot.connection.generic.Message import Message
from kudubot.servicehandlers.ServiceConfigParser import ServiceConfigParser

# Weird import strucutre due to cyclic imports
try:
    from kudubot.connection.generic.Connection import Connection
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
                    WeeklyReminderService,
                    CasinoService,
                    RouletteService,
                    KvvService,
                    XkcdService,
                    XkcdRngService,
                    KickTippService,
                    FootballInfoService,
                    WeatherService,
                    GoogleTtsService,
                    TvdbService,
                    CinemaService,
                    ZkmKinoService,
                    KitMensaService,
                    EmailSenderService,
                    ImageSenderService,
                    RandomKeyGeneratorService,
                    HelloWorldService,
                    AsciiArtService,
                    SimpleCommandsService,
                    SimpleEqualsResponseService,
                    SimpleContainsResponseService,
                    # ResetService,
                    # BotMuteService
                    ]
    """
    A list of all implemented services
    """

    protected_services = []
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
        for service in self.all_services:
            if service.protected:
                self.protected_services.append(service)

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
            PrintLogger.print("Checking Regex for service " + service.identifier, 4)
            if service.regex_check(message):
                PrintLogger.print("Message passed regex check for service " + service.identifier, 3)
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
            thread.daemon = True
            thread.start()
