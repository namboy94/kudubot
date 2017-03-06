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
from setuptools import setup, find_packages
from kudubot.metadata import version


def readme():
    """
    Reads the readme file.

    :return: the readme file as a string
    """
    # noinspection PyBroadException
    try:
        # noinspection PyPackageRequirements
        import pypandoc
        with open('README.md') as f:
            # Convert markdown file to rst
            markdown = f.read()
            rst = pypandoc.convert(markdown, 'rst', format='md')
            return rst
    except:
        # If pandoc is not installed, just return the raw markdown text
        with open('README.md') as f:
            return f.read()


def find_scripts():
    """
    Returns a list of scripts in the bin directory

    :return: the list of scripts
    """
    try:
        scripts = []
        for file_name in os.listdir("bin"):
            if not file_name == "__init__.py" and os.path.isfile(os.path.join("bin", file_name)):
                scripts.append(os.path.join("bin", file_name))
        return scripts
    except OSError:
        return []


setup(name="kudubot",
      version=version,
      description="A messaging bot framework",
      long_description=readme(),
      classifiers=[
        "Environment :: Other Environment",
        "Natural Language :: English",
        "Intended Audience :: Developers",
        "Development Status :: 3 - Alpha",
        "Operating System :: POSIX :: Linux",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 2",
        "Topic :: Internet",
        "License :: OSI Approved :: GNU General Public License v3 (GPLv3)"
      ],
      url="https://gitlab.namibsun.net/namboy94/kudubot",
      download_url="https://gitlab.namibsun.net/namboy94/kudubot/repository/archive.zip?ref=master",
      author="Hermann Krumrey",
      author_email="hermann@krumreyh.com",
      license="GNU GPL3",
      packages=find_packages(),
      install_requires=['typing', 'raven'],
      dependency_links=[],
      test_suite='nose.collector',
      tests_require=['nose'],
      scripts=find_scripts(),
      zip_safe=False)
