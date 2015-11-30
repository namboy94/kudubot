#!/usr/bin/env python
import sys
import os

commandLoc = os.path.dirname(sys.argv[0])
home = os.getenv("HOME")
os.system(commandLoc + "/yowsup-cli demos -c \"" + home + "/.whatsapp-bot/config\" -e")
