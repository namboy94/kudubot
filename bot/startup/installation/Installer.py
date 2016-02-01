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

"""
The Installer Class
"""
class Installer(object):

    """
    Checks if whatsapp-bot is installed corectly
    @:return True, if installed correctly, otherwise False
    """
    @staticmethod
    def isInstalled():

        if platform.system() == "Linux":
            homedir = os.getenv("HOME")
            if not os.path.isdir(homedir + "/.whatsapp-bot/logs/exceptions"): return False
            if not os.path.isdir(homedir + "/.whatsapp-bot/logs/users"): return False
            if not os.path.isdir(homedir + "/.whatsapp-bot/logs/groups"): return False
            if not os.path.isdir(homedir + "/.whatsapp-bot/logs/bugs"): return False
            if not os.path.isdir(homedir + "/.whatsapp-bot/images/temp"): return False
            if not os.path.isdir(homedir + "/.whatsapp-bot/reminders/continuous"): return False
            if not os.path.isdir(homedir + "/.whatsapp-bot/casino/users"): return False
            if not os.path.isdir(homedir + "/.whatsapp-bot/casino/roulette"): return False
            if not os.path.isdir(homedir + "/.whatsapp-bot/program"): return False
            if not os.path.isfile(homedir + "/.whatsapp-bot/config"): return False
            if not os.path.isfile(homedir + "/.whatsapp-bot/plugins"): return False
            if not os.path.isfile("/usr/bin/whatsapp-bot"): return False
            return True

        elif platform.system() == "Windows":
            return False

    """
    Installs whatsapp-bot
    """
    @staticmethod
    def install():

        if platform.system() == "Linux":
            homedir = os.getenv("HOME")
            whatsappbotdir = homedir + "/.whatsapp-bot"
            programdir = whatsappbotdir + "/program"
            if not os.path.isdir(whatsappbotdir):
                Popen(["mkdir", whatsappbotdir]).wait()
            if not os.path.isdir(programdir):
                Popen(["cp", "-rf", Installer.getSourceDir(), programdir]).wait()
            if not os.path.isdir(whatsappbotdir + "/logs"):
                Popen(["mkdir", "-p", whatsappbotdir + "/logs/exceptions"]).wait()
                Popen(["mkdir", "-p", whatsappbotdir + "/logs/users"]).wait()
                Popen(["mkdir", "-p", whatsappbotdir + "/logs/groups"]).wait()
                Popen(["mkdir", "-p", whatsappbotdir + "/logs/bugs"]).wait()
            if not os.path.isdir(whatsappbotdir + "/images"):
                Popen(["mkdir", "-p", whatsappbotdir + "/images/temp"]).wait()
                Popen(["cp", "-rf", Installer.getSourceDir() + "/resources/images/", whatsappbotdir]).wait()
            if not os.path.isfile(whatsappbotdir + "/config"):
                file = open(whatsappbotdir + "/config", "w")
                file.write("number=\npassword=")
                file.close()
            if not os.path.isfile(whatsappbotdir + "/plugins"):
                file = open(whatsappbotdir + "/plugins", "w")
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
            if not os.path.isdir(whatsappbotdir + "/reminders/continuous"):
                Popen(["mkdir", "-p", whatsappbotdir + "/reminders/continuous"]).wait()
            if not os.path.isdir(whatsappbotdir + "/casino/users"):
                Popen(["mkdir", "-p", whatsappbotdir + "/casino/users"]).wait()
            if not os.path.isdir(whatsappbotdir + "/casino/roulette"):
                Popen(["mkdir", "-p", whatsappbotdir + "/casino/roulette"]).wait()
            if not os.path.isfile("/usr/bin/whatsapp-bot"):
                Popen(["sudo", "cp", Installer.getSourceDir() + "/bot/startup/continuousscript", "/usr/bin/whatsapp-bot"]).wait()
                Popen(["sudo", "chmod", "755", "/usr/bin/whatsapp-bot"]).wait()

        elif platform.system() == "Windows":
            return False

    """
    Updates installed whatsapp-bot
    """
    @staticmethod
    def update():
        if platform.system() == "Linux":
            homedir = os.getenv("HOME")
            whatsappbotdir = homedir + "/.whatsapp-bot"
            programdir = whatsappbotdir + "/program"
            Popen(["rm", "-rf", programdir]).wait()
            Popen(["cp", "-rf", Installer.getSourceDir(), programdir]).wait()
            Popen(["rm", "-rf", whatsappbotdir + "/images"]).wait()
            Popen(["cp", "-rf", Installer.getSourceDir() + "/resources/images", whatsappbotdir]).wait()
            Popen(["mkdir", whatsappbotdir + "/images/temp"]).wait()
        elif platform.system() == "Windows":
            return False

    """
    Gets the source directory of the python program running
    @:return the source directory
    """
    @staticmethod
    def getSourceDir():
        directory = os.path.dirname(sys.argv[0])
        return str(os.path.abspath(directory).rsplit("/", 1)[0])