from typing import List
from kudubot.services.ExternalService import ExternalService


class TesterService(ExternalService):

    def define_executable_command(self) -> List[str]:
        return ["python"]

    def define_executable_file_url(self):
        return "https://docs.namibsun.net/test.py"

    @staticmethod
    def define_identifier() -> str:
        return "tester"
