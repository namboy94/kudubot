# coding=utf-8
"""
Copyright 2015,2016 Hermann Krumrey

This file is part of messengerbot.

    messengerbot makes use of various third-party python modules to serve
    information via the online chat services.

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
from messengerbot.servicehandlers.Service import Service
from messengerbot.connection.generic.Message import Message


class HelpService(Service):
    """
    The HelpService Class that extends the generic Service class.
    The service lists the help strings for all running dervices
    """

    identifier = "help"
    """
    The identifier for this service
    """

    help_description = {"en": "",
                        "de": ""}
    """
    Help description for this service. No description since this is the class generating the help\
    messages anyway.
    """

    help_keywords = {"help": "en",
                     "hilfe": "de"}
    """
    Keywords that trigger the help service, which can also be used to determine the language
    """

    def process_message(self, message: Message) -> None:
        """
        Process a message according to the service's functionality

        :param message: the message to process
        :return: None
        """
        language = self.help_keywords[message.message_body.split("/")[1].split(" ")[0]]

        try:
            selected_service = message.message_body.split(" ")[1]
        except IndexError:
            selected_service = None

        indexed_services = {}
        for service_count in range(0, len(self.connection.service_manager.active_services)):
            indexed_services[service_count] = self.connection.service_manager.active_services[service_count]

        if selected_service is None:
            reply = "Services\n\n"

            for service_count in range(0, len(self.connection.service_manager.active_services)):
                reply += str(service_count + 1) + ": " + indexed_services[service_count].identifier + "\n"

            if language == "en":
                reply += "\nFor detailed instructions, enter \n/help <service-name> \nor \n/help <service-index>"
            elif language == "de":
                reply += "\nFür detailierte Anweisungen, geb \n/hilfe <service-name> \noder" \
                                 " \n/hilfe <service-index> ein"

        else:
            reply = ""
            try:
                reply = self.get_service_description(indexed_services[int(selected_service) - 1], language)
            except (ValueError, KeyError):
                for service in self.connection.service_manager.active_services:
                    if service.identifier == selected_service:
                        reply = self.get_service_description(service, language)
                if not reply:
                    reply = "Sorry, service \"" + selected_service + "\" not found"

        reply_message = self.generate_reply_message(message, "Help", reply)
        self.send_text_message(reply_message)

    @staticmethod
    def regex_check(message: Message) -> bool:
        """
        Checks if the user input is valid for this service to continue

        :return: True if input is valid, False otherwise
        """
        match = False

        for keyword in HelpService.help_keywords:
            if message.message_body.startswith("/" + keyword + " ") or message.message_body == "/" + keyword:
                match = True

        return match

    @staticmethod
    def get_service_description(service: Service, language: str) -> str:
        """
        Method that returns the help description of a service in a particular language.
        If the selected language has no description, the string
        "No help available for this language"
        will be returned instead

        :param service: the service for which the help message should be returnes
        :param language: the language to be returned
        :return: the description in that language
        """
        try:
            return service.help_description[language.lower()]
        except KeyError:
            return "No help available for this language"
