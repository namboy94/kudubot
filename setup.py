"""
Copyright 2015-2017 Hermann Krumrey

This file is part of kudubot.

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
"""

import os
import sys
from kudubot import version
from setuptools import setup, find_packages
from kudubot.config.builder import build_external
from kudubot.config.GlobalConfigHandler import GlobalConfigHandler
from kudubot.config.StandardConfigWriter import StandardConfigWriter


def readme():
    """
    Reads the readme file and converts it to RST if pypandoc is
    installed. If not, the raw markdown text is returned
    :return: the readme file as a string
    """
    # noinspection PyBroadException
    try:
        # noinspection PyPackageRequirements,PyUnresolvedReferences
        import pypandoc
        with open("README.md") as f:
            # Convert markdown file to rst
            markdown = f.read()
            rst = pypandoc.convert(markdown, "rst", format="md")
            return rst

    except ModuleNotFoundError:
        # If pandoc is not installed, just return the raw markdown text
        with open("README.md") as f:
            return f.read()


def find_scripts():
    """
    Returns a list of scripts in the bin directory
    :return: the list of scripts
    """
    scripts = []

    for file_name in os.listdir("bin"):

        path = os.path.join("bin", file_name)
        if file_name == "__init__.py":
            continue
        elif not os.path.isfile(path):
            continue
        else:
            scripts.append(os.path.join("bin", file_name))

    return scripts


def run_setup():
    """
    Runs the setup method, taking care of all setuptools functionality
    :return: None
    """

    setup(name="kudubot",
          version=version,
          description="A messaging bot framework",
          long_description=readme(),
          classifiers=[
              "Environment :: Console",
              "Natural Language :: English",
              "Intended Audience :: Developers",
              "Development Status :: 4 - Beta",
              "Operating System :: POSIX :: Linux",
              "Topic :: Communications :: Chat",
              "Programming Language :: Python",
              "License :: OSI Approved :: "
              "GNU General Public License v3 (GPLv3)"
          ],
          url="https://gitlab.namibsun.net/namboy94/kudubot",
          download_url="https://gitlab.namibsun.net/namboy94/kudubot/"
                       "repository/archive.zip?ref=master",
          author="Hermann Krumrey",
          author_email="hermann@krumreyh.com",
          license="GNU GPL3",
          packages=find_packages(),
          install_requires=[
              "typing",
              "python-telegram-bot",
              "yowsup2",
              "requests",
              "bs4"],
          dependency_links=[],
          test_suite="nose.collector",
          tests_require=["nose"],
          scripts=find_scripts(),
          zip_safe=False)


def main():
    """
    Starts the setup.py script
    Writes standard config files if none exist yet
    Also attempts to build and install external services
    :return: None
    """

    if sys.argv[1] == "install":

        handler = GlobalConfigHandler()
        if not handler.validate_config_directory():
            handler.generate_configuration(False)
            StandardConfigWriter(handler).write_standard_connection_config()
            StandardConfigWriter(handler).write_standard_service_config()

        # noinspection PyBroadException
        try:
            executables = build_external()
            for executable in executables:
                os.rename(
                    executable,
                    os.path.join(
                        handler.external_services_executables_directory,
                        os.path.basename(executable)
                    )
                )
        except BaseException as e:
            print(str(e))

    run_setup()


if __name__ == "__main__":
    main()
