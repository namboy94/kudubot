# coding=utf-8
"""
Copyright 2015,2016 Hermann Krumrey

This file is part of messengerbot.

    messengerbot makes use of various third-party python modules to serve
    information via online chat services.

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
import messengerbot.metadata as metadata
from setuptools import setup, find_packages


def readme() -> str:
    """
    Reads the readme file and converts it from markdown to restructured text

    :return: the readme file as a string
    """
    try:
        # noinspection PyPackageRequirements
        import pypandoc
        with open('README.md') as f:
            # Convert markdown file to rst
            markdown = f.read()
            rst = pypandoc.convert(markdown, 'rst', format='md')
            return rst
    except (OSError, ImportError):
        # If pandoc is not installed, just return the raw markdown text
        with open('README.md') as f:
            return f.read()

setup(name=metadata.project_name,
      version=metadata.version_number,
      description=metadata.project_description,
      long_description=readme(),
      classifiers=[metadata.development_status,
                   'Intended Audience :: End Users/Desktop',
                   'License :: OSI Approved :: GNU General Public License v3 (GPLv3)',
                   'Programming Language :: Python :: 3',
                   'Topic :: Internet',
                   'Natural Language :: English',
                   'Operating System :: POSIX :: Linux'
                   ],
      url='http://namibsun.net/namboy94/messengerbot',
      author='Hermann Krumrey',
      author_email='hermann@krumreyh.com',
      license='GNU GPL3',
      packages=find_packages(),
      install_requires=['tvdb_api',
                        'yowsup2',
                        'beautifulsoup4',
                        'pillow',
                        'pywapi'],
      test_suite='nose.collector',
      tests_require=['nose'],
      scripts=['bin/messengerbot-email',
               'bin/messengerbot-whatsapp'],
      zip_safe=False)

# How to upload to pypi:
# python setup.py register sdist upload
