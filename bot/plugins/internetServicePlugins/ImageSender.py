"""
Plugin that allows the sending of images from links
@author Hermann Krumrey <hermann@krumreyh.com>
"""
import os
import re
from threading import Thread

from yowsup.layers.protocol_messages.protocolentities import TextMessageProtocolEntity
from plugins.GenericPlugin import GenericPlugin
from subprocess import Popen, PIPE
from PIL import Image

"""
The ImageSender Class
"""
class ImageSender(GenericPlugin):
    """
    Constructor
    Defines parameters for the plugin.
    @:param layer - the overlying yowsup layer
    @:param messageProtocolEntity - the received message information
    @:override
    """

    def __init__(self, layer, messageProtocolEntity=None):
        if messageProtocolEntity is None: self.layer = layer; return
        self.layer = layer
        self.entity = messageProtocolEntity
        self.message = self.entity.getBody()
        self.sender = self.entity.getFrom()

        self.imagesDir = os.getenv("HOME") + "/.whatsapp-bot/images/temp/"
        self.link = ""
        self.imageName = ""
        self.error = ""
        self.threadIsDone = False

    """
    Checks if the user input is valid for this plugin to continue
    @:return True if input is valid, False otherwise
    @:override
    """
    def regexCheck(self):
        if re.search(r"^/img (http(s)?://|www.)[^;>\| ]+(.png|.jpg)$", self.message):
            if "&&" in self.message:
                self.sendMessage(TextMessageProtocolEntity("Nice try.", to=self.sender))
                return False
            else: return True
        else: return False

    """
    Parses the user's input
    @:override
    """
    def parseUserInput(self):
        self.link = self.message.split("/img ")[1]
        self.imageName = self.link.rsplit("/", 1)[1]
        thread = Thread(target=self.__wgetImage__)
        thread.start()
        thread.join(timeout=5)



    """
    Returns the response calculated by the plugin
    @:return the response as a MessageProtocolEntity
    @:override
    """
    def getResponse(self):
        if self.error: return TextMessageProtocolEntity(self.error, to=self.sender)
        try:
            imageFile = self.imagesDir + self.imageName
            if not os.path.isfile(imageFile) or os.path.getsize(imageFile) > 8000000:
                raise Exception("File too large or does not exist")
            elif not self.threadIsDone:
                raise Exception("Second thread didn't finish (Timeout)")
            else:
                im = Image.open(imageFile)
                if im.size[0] > 8000 or im.size[1] > 4000:
                    raise Exception("Resolution too high")
                else:
                    self.sendImage(self.entity.getFrom(), self.imagesDir + self.imageName, self.link)
        except:
            return TextMessageProtocolEntity("Sorry, image could not be sent", to=self.sender)

    """
    Returns a helpful description of the plugin's syntax and functionality
    @:param language - the language to be returned
    @:return the description as string
    @:override
    """
    @staticmethod
    def getDescription(language):
        if language == "en":
            return ""
        elif language == "de":
            return ""
        else:
            return "Help not available in this language"

    """
    Starts a parallel background activity if this class has one.
    Defaults to False if not implemented
    @:return False, if no parallel activity defined, should be implemented to return True if one is implmented.
    @:override
    """
    def parallelRun(self):
        return False

    """
    Wgets the image from the link
    """
    def __wgetImage__(self):
        try:
            spiderProcessCommand = ['wget', '--spider', self.link]
            spiderProcess = Popen(spiderProcessCommand, stdout=PIPE, stderr=PIPE)
            spider, spiderErr = spiderProcess.communicate()
            spiderErr = spiderErr.decode()
            filesize = int(spiderErr.split("Length: ")[1].split(" ")[0])
            if filesize > 8000000: raise Exception("File size too large")
            os.system("wget " + self.link + " -O " + self.imagesDir + self.imageName)
        except Exception as e:
            if str(e) == "File size too large":
                self.error = str(e)
            else:
                self.error = "Error loading image from source."
        self.threadIsDone = True
