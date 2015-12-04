from yowsup.demos.echoclient.utils.emojicode import *

def ue(group):
    if group: return convertToBrokenUnicode("ü")
    else: return "ü"

def capUe(group):
    if group: return convertToBrokenUnicode("Ü")
    else: return "Ü"

def oe(group):
    if group: return convertToBrokenUnicode("ö")
    else: return "ö"

def capOe(group):
    if group: return convertToBrokenUnicode("Ö")
    else: return "Ö"

def ae(group):
    if group: return convertToBrokenUnicode("ä")
    else: return "ä"

def capAe(group):
    if group: return convertToBrokenUnicode("Ä")
    else: return "ä"

def ss(group):
    if group: return convertToBrokenUnicode("ß")
    else: return "ß"