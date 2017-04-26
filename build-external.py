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
from subprocess import Popen


def build(service_name: str, service_dir: str, source_file: str, destination_file: str):

    current_dir = os.getcwd()

    if source_file.endswith(".rs"):
        os.chdir(service_dir)
        Popen(["cargo", "build", "--release"]).wait()
        os.rename(os.path.join("target", "release", service_name), os.path.join("build", service_name))

    os.chdir(current_dir)


def build_external():

    external_dir = os.path.join("kudubot", "services", "external")
    built_executables = []

    for service in os.listdir(external_dir):

        service_dir = os.path.join(external_dir, service)
        if not os.path.isdir(service_dir):
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
                built_executables.append(destination_path)

    print(built_executables)

if __name__ == "__main__":
    build_external()
