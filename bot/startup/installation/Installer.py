"""
Module that contains methods that install whatsapp-bot or update an existing installation
@author Hermann Krumrey<hermann@krumreyh.com>
"""

import os
import platform
import sys

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
            if not os.path.isdir(homedir + "/.whatsapp-bot"): return False
            if not os.path.isdir(homedir + "/.whatsapp-bot/logs"): return False
            if not os.path.isdir(homedir + "/.whatsapp-bot/reminders"): return False
            if not os.path.isdir(homedir + "/.whatsapp-bot/program"): return False
            if not os.path.isfile(homedir + "/.whatsapp-bot/config"): return False
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
                os.system("mkdir " + whatsappbotdir)
            if not os.path.isdir(programdir):
                os.system("cp -rf " + Installer.getSourceDir() + " " + programdir)
            if not os.path.isdir(whatsappbotdir + "/logs"):
                os.system("mkdir " + whatsappbotdir + "/logs")
            if not os.path.isfile(whatsappbotdir + "/config"):
                file = open(whatsappbotdir + "/config", "w")
                file.write("number=\npassword=")
                file.close()
            if not os.path.isdir(whatsappbotdir + "/reminders"):
                os.system("mkdir " + whatsappbotdir + "/reminders")
            if not os.path.isfile("/usr/bin/whatsapp-bot"):
                os.system("gksudo cp " + Installer.getSourceDir() + "/bot/continuousscript /usr/bin/whatsapp-bot")
                os.system("gksudo chmod 755 /usr/bin/whatsapp-bot")

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
            os.system("rm -rf " + programdir)
            os.system("cp -rf " + Installer.getSourceDir() + " " + programdir)
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