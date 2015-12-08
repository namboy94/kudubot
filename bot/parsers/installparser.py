import os
import platform

def isInstalled():

    if platform.system() == "Linux":
        homedir = os.getenv("HOME")
        if not os.path.isdir(homedir + "/.whatsapp-bot"): return False
        if not os.path.isfile(homedir + "/.whatsapp-bot/config"): return False
        if not os.path.isfile("/usr/bin/whatsapp-bot"): return False

    elif platform.system() == "Windows":
        return False


def install():

    if platform.system() == "Linux":
        homedir = os.getenv("HOME")
        if not os.path.isdir(homedir + "/.whatsapp-bot"):
            os.system("mkdir " + homedir + "/.whatsapp-bot")
        if not os.path.isfile(homedir + "/.whatsapp-bot/config"):

            return False
        if not os.path.isfile("/usr/bin/whatsapp-bot"):
            return False

    elif platform.system() == "Windows":
        return False