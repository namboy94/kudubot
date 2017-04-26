import os
import json
import time
from subprocess import Popen
from typing import List, Tuple, Dict
from kudubot.services.Service import Service
from kudubot.entities.Message import Message, from_dict as message_from_dict


class ExternalService(Service):

    # noinspection PyAttributeOutsideInit
    def init(self):
        self.message_dir = ""
        self.target_command = []


    @staticmethod
    def define_identifier() -> str:
        raise NotImplementedError()

    def define_binary_file(self):
        raise NotImplementedError()

    @staticmethod
    def define_requirements() -> List[str]:
        return []

    def handle_message(self, message: Message):

        message_file, response_file = self.store_message_in_file(message)

        Popen(self.target_command + ["handle_message", message_file]).wait()

        response = self.load_response(response_file)

        if response["mode"] == "reply":
            self.connection.send_message(self.retrieve_message_from_file(message_file))

        os.remove(message_file)
        os.remove(response_file)

    def is_applicable_to(self, message: Message) -> bool:

        message_file, response_file = self.store_message_in_file(message)
        Popen(self.target_command + ["is_applicable"]).wait()
        response = self.load_response(response_file)

        return response["mode"] == "applicable_check" and response["value"]

    def store_message_in_file(self, message: Message) -> Tuple[str, str]:

        json_data = message.to_dict()

        while True:  # Make sure that file does not exist
            message_file = os.path.join(self.message_dir, str(time.time()))
            if not os.path.isfile(message_file):
                with open(message_file, 'w') as json_file:
                    json.dump(json_data, json_file)
                return message_file + ".json", message_file + "-response.json"

    def retrieve_message_from_file(self, message_file: str) -> Message:

        with open(message_file, 'r') as json_file:
            message = json.load(json_file)

        return message_from_dict(message)

    def load_response(self, response_file: str) -> Dict[str, type]:

        with open(response_file, 'r') as f:
            content = json.load(f)

        return content
