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
import re

from kudubot.servicehandlers.Service import Service
from kudubot.connection.generic.Message import Message


class ServiceSelectorService(Service):
    """
    The ServiceSelectorService Class that extends the generic Service class.
    The service allows admin users to enable and disable services
    """

    identifier = "service_selector"
    """
    The identifier for this service
    """

    protected = True
    """
    May not be disabled
    """

    help_description = {"en": "/service\tallows activation/deactivation of services (admin)\n"
                              "/service activate <service|service-index>\tactivates a service\n"
                              "/service deactivate <service|service-index>\tdeactivates a service\n",
                        "de": "/service\tErmöglicht das Aktivieren/Deaktivieren von einem Service (admin)\n"
                              "/service an <service|service-index>\tAktiviert ein Service\n"
                              "/service aus <service|service-index>\tDeaktiviert ein Service\n"}
    """
    Help description for this service.
    """

    activation_keywords = {"activate": ("en", "activate"),
                           "deactivate": ("en", "deactivate"),
                           "an": ("de", "activate"),
                           "aus": ("de", "deactivate")}
    """
    Keywords that trigger a plugin activation or deactivation
    """

    already_activated = {"en": "is already activated or does not exist.",
                         "de": "ist bereits aktiviert oder existiert nicht."}
    """
    Reply for when a plugin was already activated
    """

    already_deactivated = {"en": "is already deactivated or does not exist.",
                           "de": "ist bereits deaktiviert oder existiert nicht."}
    """
    Reply for when a plugin was already deactivated
    """

    service_activated = {"en": "has been activated.",
                         "de": "wurde aktiviert."}
    """
    Reply for when a plugin was activated
    """

    service_deactivated = {"en": "has been deactivated.",
                           "de": "wurde deaktiviert."}
    """
    Reply for when a plugin was deactivated
    """

    protected_service_warning = {"en": "can not be deactivated",
                                 "de": "kann nicht deaktiviert werden"}
    """
    Reply when an attempt at deactivating a protected service is done
    """

    unauthorized_warning = {"en": "Sorry, I can't let you do that.",
                            "de": "Sorry, das darfst du nicht."}
    """
    Reply for non-admins
    """

    def process_message(self, message: Message) -> None:
        """
        Process a message according to the service's functionality

        :param message: the message to process
        :return: None
        """
        authenticated = self.connection.authenticator.is_from_admin(message)

        parsed = message.message_body.lower().split("/service ", 1)[1]
        mode, selected_service_identifier = parsed.split(" ", 1)
        language = self.activation_keywords[mode][0]

        if authenticated:

            try:
                selected_service_identifier = \
                    self.connection.service_manager.all_services[int(selected_service_identifier) - 1].identifier
            except (IndexError, ValueError):
                pass

            selected_service_class = None
            for service in self.connection.service_manager.all_services:
                if service.identifier == selected_service_identifier:
                    selected_service_class = service

            is_active = False
            for service in self.connection.service_manager.active_services:
                if service.identifier == selected_service_identifier:
                    is_active = True

            if self.activation_keywords[mode][1] == "activate":
                if is_active or selected_service_class is None:
                    reply = selected_service_identifier + " " + self.already_activated[language]
                else:
                    self.connection.service_manager.active_services.append(selected_service_class)
                    reply = selected_service_identifier + " " + self.service_activated[language]
            else:
                if selected_service_class is None \
                        or selected_service_class not in self.connection.service_manager.active_services:
                    reply = selected_service_identifier + " " + self.already_deactivated[language]
                elif selected_service_class in self.connection.service_manager.protected_services:
                    reply = selected_service_identifier + " " + self.protected_service_warning[language]
                else:
                    self.connection.service_manager.active_services.remove(selected_service_class)
                    reply = selected_service_identifier + " " + self.service_deactivated[language]

        else:
            reply = self.unauthorized_warning[language]

        reply_message = self.generate_reply_message(message, "Help", reply)
        self.send_text_message(reply_message)

    @staticmethod
    def regex_check(message: Message) -> bool:
        """
        Checks if the user input is valid for this service to continue

        :return: True if input is valid, False otherwise
        """
        regex = "^/service ("

        first = True
        for key in ServiceSelectorService.activation_keywords:
            if first:
                regex += key
                first = False
            else:
                regex += "|" + key

        regex += ") ([0-9]+|[a-zA-Z]+(( [a-zA-Z]+)+)?)$"

        return re.search(re.compile(regex), message.message_body.lower())
