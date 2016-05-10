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
import re

from messengerbot.servicehandlers.Service import Service
from messengerbot.connection.generic.Message import Message


class HelloWorldService(Service):
    """
    The HelloWorldService Class that extends the generic Service class.
    The service parses www.kicktipp.de to get a kicktipp group's current standings
    """

    identifier = "hello_world"
    """
    The identifier for this service
    """

    help_description = {"en": "/helloworld\tSends a message containing how to write a 'Hello World'"
                              "Program in a specific language\n"
                              "syntax:\n"
                              "/helloworld <language>",
                        "de": "/helloworld\tSchickt eine Nachricht mit einem 'Hello World' Codeschnipsel für eine"
                              "spezifische Programmiersprache\n"
                              "synatx:\n"
                              "/helloworld <sprache>"}
    """
    Help description for this service.
    """

    implementations = {"python": "if __name__ == \"main\":\n"
                                 "    print(\"Hello World!\")",
                       "java": "pubic class Main {\n"
                               "    public static void main(String[] args) {\n"
                               "        System.out.println(\"Hello World!\");\n"
                               "    }\n"
                               "}",
                       "c": "#include <stdio.h>\n\n"
                            "int main() {"
                            "    printf(\"Hello World!\\n\");\n"
                            "    return 0;"
                            "}",
                       "c++": "#include <iostream>\n\n"
                              "int main() {"
                              "    std::cout << \"Hello World!\";\n"
                              "    return 0;\n"
                              "}",
                       "bash": "#!/bin/bash\n\n"
                               "echo \"Hello World\""}
    """
    The actual implementations of hello world in the different languages
    """

    language_not_found_error = {"en": "Programming Language not found",
                                "de": "Programmiersprache nicht gefunden"}
    """
    Error message sent when the programming language could not be found.
    """

    def process_message(self, message: Message) -> None:
        """
        Process a message according to the service's functionality

        :param message: the message to process
        :return: None
        """
        prog_language = message.message_body.lower().split(" ")[1]
        try:
            reply = self.implementations[prog_language]
        except KeyError:
            reply = self.language_not_found_error[self.connection.last_used_language]

        reply_message = self.generate_reply_message(message, "Hello World", reply)
        self.send_text_message(reply_message)

    @staticmethod
    def regex_check(message: Message) -> bool:
        """
        Checks if the user input is valid for this service to continue

        :return: True if input is valid, False otherwise
        """
        regex = "^/helloworld " + Service.regex_string_from_dictionary_keys([HelloWorldService.implementations]) + "$"
        return re.search(re.compile(regex), message.message_body.lower())
