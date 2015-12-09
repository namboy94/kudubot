"""
@author Hermann Krumrey <hermann@krumreyh.com>
"""

import os
import platform
import re

"""
Parses a config file and extracts its password and number
@:return the number and password as tuple of strings
"""
def configParse():

    file = ""
    if platform.system() == "Linux":
        file = openLinuxConf()
    elif platform.system() == "Windows":
        file = openWindoesConf()

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
def openLinuxConf():
    return open(os.getenv("HOME") + "/.whatsapp-bot/config", 'r')

"""
Opens the config file under Windows
"""
def openWindoesConf():
    username = os.environ.get("USERNAME")
    return open("C:/Users/" + username + "/Documents/whatsapp-bot/config.txt", 'r')