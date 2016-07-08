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
import os
import sys
import time

from kudubot.logger.PrintLogger import PrintLogger
from kudubot.servicehandlers.Service import Service
from kudubot.connection.generic.Message import Message
from kudubot.config.LocalConfigChecker import LocalConfigChecker


class RestarterService(Service):
    """
    The RestarterService Class that extends the generic Service class.
    The service can be used to restart the bot remotely by admins
    """

    identifier = "restarter"
    """
    The identifier for this service
    """

    help_description = {"en": "/restart: Restarts the bot",
                        "de": "/neustart: Startet den bot neu"}
    """
    Help description for this service. It's empty, because this service does not act on actual commands
    per say.
    """

    restart_commands = {"/restart": "en",
                        "/neustart": "de"}
    """
    Available commands for the restart service
    """

    restarting_message = {"en": "Restarting bot...",
                          "de": "Starte Bot neu..."}
    """
    Message for the restart i various languages
    """

    restarting_file = os.path.join(LocalConfigChecker.program_directory, "restarting")
    """
    Temporary file to be used to avoid infinite restarting loops
    """

    time_out_message = {"en": "You need to wait 30 seconds before restarting the bot again.",
                        "de": "Du musst 30 Sekunden warten bevor der Bot abermals neugestartet werden soll."}

    unauthorized_warning = {"en": "Sorry, I can't let you do that.",
                            "de": "Sorry, das darfst du nicht."}
    """
    Reply for non-admins
    """

    protected = True
    """
    May not be disabled
    """

    def process_message(self, message: Message) -> None:
        """
        Process a message according to the service's functionality

        :param message: the message to process
        :return: None
        """
        language = self.restart_commands[message.message_body]
        self.connection.last_used_language = language

        if self.connection.authenticator.is_from_admin(message):

            # Do not restart if the bot was restarted in the last 30 seconds
            if os.path.isfile(self.restarting_file):
                restart_file = open(self.restarting_file, 'r')
                last_restart = float(restart_file.read())
                restart_file.close()

                if message.timestamp < last_restart + 30.0:
                    reply = self.time_out_message[language]
                    reply_message = self.generate_reply_message(message, "Restarter", reply)
                    self.send_text_message(reply_message)
                    return
                else:
                    os.remove(self.restarting_file)

            reply = self.restarting_message[language]
            reply_message = self.generate_reply_message(message, "Restarter", reply)
            self.send_text_message(reply_message)

            # Create a temporary file to avoid infinite restarting loops
            restart_file = open(self.restarting_file, 'w')
            restart_file.write(str(message.timestamp))
            restart_file.close()

            PrintLogger.print("Restarting Bot")
            time.sleep(2)

            os.execl(sys.executable, sys.executable, *sys.argv)  # Restart program

        else:
            reply = self.unauthorized_warning[language]
            reply_message = self.generate_reply_message(message, "Restarter", reply)
            self.send_text_message(reply_message)

    @staticmethod
    def regex_check(message: Message) -> bool:
        """
        Checks if the user input is valid for this service to continue

        :return: True if input is valid, False otherwise
        """
        return message.message_body in RestarterService.restart_commands
