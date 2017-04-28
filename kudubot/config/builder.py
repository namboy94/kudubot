"""
LICENSE:
Copyright 2015-2017 Hermann Krumrey

This file is part of kudubot.

    kudubot is a chat bot framework. It allows developers to write
    services for arbitrary chat services.

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

import os
import stat
import json
from subprocess import Popen
from typing import List, Dict


# noinspection PyUnusedLocal
def build(service_directory, config: Dict[str, List[str] or str]):

    current_dir = os.getcwd()
    os.chdir(service_directory)

    Popen(config["build_commands"]).wait()

    st = os.stat(config["output_file"])
    os.chmod(config["output_file"], st.st_mode | stat.S_IEXEC)  # Make executable

    os.chdir(current_dir)

    return os.path.join(service_directory, config["output_file"])


def run_safe_popen(command):
    """
    Runs a Popen command and makes sure to catch any exceptions that may occur.

    :param command: The command to run
    :return: None
    """
    try:
        Popen(command).wait()
    except BaseException as e:
        print(e)


def build_external(move_to: str = "") -> List[str]:
    """
    Builds all external services

    :param move_to: If specified, all built files are moved to that directory
    :return: A list of all generated executable files
    """

    external_dir = os.path.join("kudubot", "services", "external")
    built_executables = []

    for service in os.listdir(external_dir):

        service_dir = os.path.join(external_dir, service)
        if not os.path.isdir(service_dir) or service == "__pycache__":
            continue

        with open(os.path.join(service_dir, "service.json"), 'r') as f:
            service_info = json.load(f)

        result = build(service_dir, service_info)

        if move_to != "" and os.path.isfile(result):
            destination = os.path.join(move_to, service)
            os.rename(result, destination)
            built_executables.append(destination)

        elif os.path.isfile(result):
            built_executables.append(result)

    return built_executables
