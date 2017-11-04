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
from kudubot import version


def publish_rust():
    """
    Publishes the Rust Bindings

    :return: None
    """

    cwd = os.getcwd()
    os.chdir(os.path.join("kudubot", "services", "bindings", "rust"))

    with open("Cargo.toml", 'r') as f:
        cargo = f.read().replace(
            "version = \"0.1.0\"", "version = \"" + str(version) + "\"")
    with open("Cargo.toml", 'w') as f:
        f.write(cargo)

    api_token = os.environ["CRATES_API_TOKEN"]

    Popen(["cargo", "login", api_token]).wait()
    Popen(["cargo", "package", "--allow-dirty"]).wait()
    Popen(["cargo", "publish", "--allow-dirty"]).wait()

    os.chdir(cwd)


if __name__ == "__main__":
    publish_rust()
