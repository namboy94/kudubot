#!/usr/bin/env python
import sys
import os
import argparse

#INSTALL
#We need:
#   config file in .whatsapp-bot
#   program in .whatsapp-bot
#   startscript in /usr/bin

thisDir = os.path.dirname(sys.argv[0])
homeDir = os.getenv("HOME")

#argument parser
parser = argparse.ArgumentParser()
parser.add_argument("-i", "--install", help="installs the program", action="store_true")
parser.add_argument("-u", "--update", help="updates installed program", action="store_true")
args = parser.parse_args()

if args.install:
    if not os.path.isdir(homeDir + "/.whatsapp-bot"):
        os.system("mkdir " + homeDir + "/.whatsapp-bot")
        print("Please put a valid config file in ~/.whatsapp-bot")
        sys.exit(0)
    if not os.path.isfile("/usr/bin/whatsapp-bot"):
        startScript = open(thisDir + "/whatsapp-bot", "w")
        startScript.write("#!/bin/bash\n")
        startScript.write("python " + homeDir + "/.whatsapp-bot/program/whatsapp-bot.py")
        startScript.close()
        os.system("gksudo mv " + thisDir + "/whatsapp-bot /usr/bin/whatsapp-bot")
        os.system("gksudo chmod 755 /usr/bin/whatsapp-bot")
        os.system("rm " + thisDir + "/whatsapp-bot")
    if not os.path.isdir(homeDir + "/.whatsapp-bot/program"):
        os.system("cp -r " + thisDir + " " + homeDir + "/.whatsapp-bot/program")
elif args.update:
    os.system("rm -rf " + homeDir + "/.whatsapp-bot/program")
    os.system("cp -r " + thisDir + " " + homeDir + "/.whatsapp-bot/program")
else:
    os.system("python " + thisDir + "/yowsup-cli demos -c \"" + homeDir + "/.whatsapp-bot/config\" -e")
