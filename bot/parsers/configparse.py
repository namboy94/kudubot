import os
import platform

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
        credentials = (number, password)
        return credentials


def openLinuxConf():
    return open(os.getenv("HOME") + "/.whatsapp-bot/config", 'r')

def openWindoesConf():
    username = os.environ.get("USERNAME")
    return open("C:/Users/" + username + "/Documents/whatsapp-bot/config.txt", 'r')