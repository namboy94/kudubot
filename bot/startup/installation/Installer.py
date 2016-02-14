# coding=utf-8
"""
Copyright 2015,2016 Hermann Krumrey

This file is part of whatsapp-bot.

    whatsapp-bot makes use of various third-party python modules to serve
    information via the online chat service Whatsapp.

    whatsapp-bot is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    whatsapp-bot is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with whatsapp-bot.  If not, see <http://www.gnu.org/licenses/>.
"""

import os
import platform
import sys
from subprocess import Popen


class Installer(object):
    """
    The Installer Class
    """

    @staticmethod
    def is_installed():
        """
        Checks if whatsapp-bot is installed correctly
        :return: True, if installed correctly, otherwise False
        """

        if platform.system() == "Linux":
            homedir = os.getenv("HOME")
            if not os.path.isdir(homedir + "/.whatsapp-bot/logs/exceptions"):
                return False
            if not os.path.isdir(homedir + "/.whatsapp-bot/logs/users"):
                return False
            if not os.path.isdir(homedir + "/.whatsapp-bot/logs/groups"):
                return False
            if not os.path.isdir(homedir + "/.whatsapp-bot/logs/bugs"):
                return False
            if not os.path.isdir(homedir + "/.whatsapp-bot/images/temp"):
                return False
            if not os.path.isdir(homedir + "/.whatsapp-bot/reminders/continuous"):
                return False
            if not os.path.isdir(homedir + "/.whatsapp-bot/casino/users"):
                return False
            if not os.path.isdir(homedir + "/.whatsapp-bot/casino/roulette"):
                return False
            if not os.path.isdir(homedir + "/.whatsapp-bot/program"):
                return False
            if not os.path.isfile(homedir + "/.whatsapp-bot/config"):
                return False
            if not os.path.isfile(homedir + "/.whatsapp-bot/plugins"):
                return False
            if not os.path.isfile("/usr/bin/whatsapp-bot"):
                return False
            return True

        elif platform.system() == "Windows":
            return False

    @staticmethod
    def install():
        """
        Installs whatsapp-bot
        :return: void
        """

        if platform.system() == "Linux":
            homedir = os.getenv("HOME")
            whatsapp_bot_dir = homedir + "/.whatsapp-bot"
            program_dir = whatsapp_bot_dir + "/program"
            if not os.path.isdir(whatsapp_bot_dir):
                Popen(["mkdir", whatsapp_bot_dir]).wait()
            if not os.path.isdir(program_dir):
                Popen(["cp", "-rf", Installer.get_source_dir(), program_dir]).wait()
            if not os.path.isdir(whatsapp_bot_dir + "/logs"):
                Popen(["mkdir", "-p", whatsapp_bot_dir + "/logs/exceptions"]).wait()
                Popen(["mkdir", "-p", whatsapp_bot_dir + "/logs/users"]).wait()
                Popen(["mkdir", "-p", whatsapp_bot_dir + "/logs/groups"]).wait()
                Popen(["mkdir", "-p", whatsapp_bot_dir + "/logs/bugs"]).wait()
            if not os.path.isdir(whatsapp_bot_dir + "/images"):
                Popen(["mkdir", "-p", whatsapp_bot_dir + "/images/temp"]).wait()
                Popen(["cp", "-rf", Installer.get_source_dir() + "/resources/images/", whatsapp_bot_dir]).wait()
            if not os.path.isfile(whatsapp_bot_dir + "/config"):
                file = open(whatsapp_bot_dir + "/config", "w")
                file.write("number=\npassword=")
                file.close()
            if not os.path.isfile(whatsapp_bot_dir + "/plugins"):
                file = open(whatsapp_bot_dir + "/plugins", "w")
                file.write("Weather Plugin=1\n")
                file.write("Roulette Plugin=1\n")
                file.write("Muter Plugin=1\n")
                file.write("TVDB Plugin=1\n")
                file.write("KinoZKM Plugin=1\n")
                file.write("XKCD Plugin=1\n")
                file.write("Terminal Plugin=1\n")
                file.write("Football Scores Plugin=1\n")
                file.write("Simple Contains Plugin=1\n")
                file.write("KVV Plugin=1\n")
                file.write("Simple Equals Plugin=1\n")
                file.write("Reminder Plugin=1\n")
                file.write("Mensa Plugin=1\n")
                file.write("Kicktipp Plugin=1\n")
                file.write("Casino Plugin=1\n")
                file.write("Text To Speech Plugin=1\n")
                file.write("Continuous Reminder Plugin=1\n")
                file.write("ImageSender Plugin=1")
                file.close()
            if not os.path.isdir(whatsapp_bot_dir + "/reminders/continuous"):
                Popen(["mkdir", "-p", whatsapp_bot_dir + "/reminders/continuous"]).wait()
            if not os.path.isdir(whatsapp_bot_dir + "/casino/users"):
                Popen(["mkdir", "-p", whatsapp_bot_dir + "/casino/users"]).wait()
            if not os.path.isdir(whatsapp_bot_dir + "/casino/roulette"):
                Popen(["mkdir", "-p", whatsapp_bot_dir + "/casino/roulette"]).wait()
            if not os.path.isfile("/usr/bin/whatsapp-bot"):
                Popen(["sudo", "cp", Installer.get_source_dir() + "/bot/startup/continuousscript",
                       "/usr/bin/whatsapp-bot"]).wait()
                Popen(["sudo", "chmod", "755", "/usr/bin/whatsapp-bot"]).wait()

        elif platform.system() == "Windows":
            return False

    @staticmethod
    def update():
        """
        Updates installed whatsapp-bot
        :return: void
        """
        if platform.system() == "Linux":
            homedir = os.getenv("HOME")
            whatsapp_bot_dir = homedir + "/.whatsapp-bot"
            program_dir = whatsapp_bot_dir + "/program"
            Popen(["rm", "-rf", program_dir]).wait()
            Popen(["cp", "-rf", Installer.get_source_dir(), program_dir]).wait()
            Popen(["rm", "-rf", whatsapp_bot_dir + "/images"]).wait()
            Popen(["cp", "-rf", Installer.get_source_dir() + "/resources/images", whatsapp_bot_dir]).wait()
            Popen(["mkdir", whatsapp_bot_dir + "/images/temp"]).wait()
        elif platform.system() == "Windows":
            return False

    @staticmethod
    def get_source_dir():
        """
        Gets the source directory of the python program running
        :return: the source directory
        """
        directory = os.path.dirname(sys.argv[0])
        return str(os.path.abspath(directory).rsplit("/", 1)[0])
