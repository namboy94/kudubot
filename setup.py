# coding=utf-8
"""
Copyright 2015,2016 Hermann Krumrey

This file is part of whatsapp-whatsbot.

    whatsapp-whatsbot makes use of various third-party python modules to serve
    information via the online chat service Whatsapp.

    whatsapp-whatsbot is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    whatsapp-whatsbot is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with whatsapp-whatsbot.  If not, see <http://www.gnu.org/licenses/>.
"""

# imports
from setuptools import setup


def readme():
    """
    Reads the readme file.
    :return: the readme file as a string
    """
    with open('README.md') as f:
        return f.read()


setup(name='whatsbot',
      version='0.1.1',
      description='An automated Whatsapp bot',
      long_description=readme(),
      classifiers=['Development Status :: 2 - Pre-Alpha',
                   'Intended Audience :: End Users/Desktop',
                   'License :: OSI Approved :: GNU General Public License v3 (GPLv3)',
                   'Programming Language :: Python :: 3',
                   'Topic :: Internet',
                   'Natural Language :: English',
                   'Operating System :: POSIX :: Linux'
                   ],
      url='http://namibsun.net/namboy94/whatsapp-bot',
      author='Hermann Krumrey',
      author_email='hermann@krumreyh.com',
      license='GNU GPL3',
      packages=['whatsbot',
                'whatsbot.layers',
                'whatsbot.plugins',
                'whatsbot.plugins.internetServicePlugins',
                'whatsbot.plugins.localServicePlugins',
                'whatsbot.plugins.localServicePlugins.casino',
                'whatsbot.plugins.restrictedAccessPlugins',
                'whatsbot.plugins.simpleTextResponses',
                'whatsbot.startup',
                'whatsbot.startup.config',
                'whatsbot.startup.installation',
                'whatsbot.utils',
                'whatsbot.utils.contacts',
                'whatsbot.utils.encoding',
                'whatsbot.utils.logging',
                'whatsbot.utils.math',
                'whatsbot.yowsupwrapper',
                'whatsbot.yowsupwrapper.entities'],
      install_requires=['tvdb_api',
                        'yowsup2',
                        'beautifulsoup4',
                        'pillow', 'pywapi'],
      test_suite='nose.collector',
      tests_require=['nose'],
      scripts=['bin/whatsbot',
               'bin/whatsbot-instance'],
      zip_safe=False)

# How to upload to pypi:
# python setup.py register sdist upload
