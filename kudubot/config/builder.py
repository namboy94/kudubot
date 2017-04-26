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
from typing import List
from subprocess import Popen


# noinspection PyUnusedLocal
def build(service_name: str, service_dir: str, source_file: str, destination_file: str):
    """
    Builds an executable file for an external service.

    :param service_name: The name of the service
    :param service_dir: The root directory of the external service
    :param source_file: The main source file used for compilation
    :param destination_file: The destination executable file
    :return: None
    """

    current_dir = os.getcwd()

    if source_file.endswith(".rs"):  # Rust
        os.chdir(service_dir)
        run_safe_popen(["cargo", "build", "--release"])
        safe_move(os.path.join("target", "release", service_name), os.path.join("build", service_name))

    os.chdir(current_dir)


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


def safe_move(source: str, destination: str):
    """
    Moves a file to a new location, but makes sure that the move is even possible.

    :param source: The source file
    :param destination: The destination file
    :return: None
    """
    if os.path.isfile(source) and os.path.isdir(os.path.dirname(destination)):
        os.rename(source, destination)


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

        src = os.path.join(service_dir, "src")
        build_dir = os.path.join(service_dir, "build")

        if not os.path.isdir(build_dir):
            os.makedirs(build_dir)

        for source_file in os.listdir(src):

            source_path = os.path.join(src, source_file)
            destination_path = os.path.join(build_dir, service)

            if os.path.isfile(source_path) and source_file.lower().startswith("main"):
                build(service, service_dir, source_path, destination_path)

                if os.path.isfile(destination_path):
                    st = os.stat(destination_path)
                    os.chmod(destination_path, st.st_mode | stat.S_IEXEC)  # Make executable
                    built_executables.append(destination_path)

    if move_to != "":
        for executable in built_executables:
            os.rename(executable, os.path.join(move_to, os.path.basename(executable)))

    return built_executables
