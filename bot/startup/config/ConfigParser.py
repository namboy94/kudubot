# coding=utf-8

"""
Class that handles config parsing
@author Hermann Krumrey <hermann@krumreyh.com>
"""

import os
import platform
import re

"""
The ConfigParser class
"""
class ConfigParser(object):

    """
    Parses a config file and extracts its password and number
    @:return the number and password as tuple of strings
    """
    @staticmethod
    def configParse():

        file = ""
        if platform.system() == "Linux":
            file = ConfigParser.openLinuxConf()
        elif platform.system() == "Windows":
            file = ConfigParser.openWindoesConf()

        number = ""
        password = ""
        for line in file:
            if line.startswith("number="):
                number = line.split("number=")[1].split("\n")[0]
            if line.startswith("password="):
                password = line.split("password=")[1].split("\n")[0]
        if number and password:
            if not re.search(r"^[0-9]+$", number): raise Exception("Invalid Number")
            if not re.search(r"^[^ ]+$", password): raise Exception("Invalid Password")
            credentials = (number, password)
            return credentials
        else: raise Exception("Invalid Config")

    """
    Opens the config file under Linux
    """
    @staticmethod
    def openLinuxConf():
        return open(os.getenv("HOME") + "/.whatsapp-bot/config", 'r')

    """
    Opens the config file under Windows
    """
    @staticmethod
    def openWindoesConf():
        username = os.environ.get("USERNAME")
        return open("C:/Users/" + username + "/Documents/whatsapp-bot/config.txt", 'r')