# coding=utf-8

"""
Plugin that handles reminders
@:author Hermann Krumrey <hermann@krumreyh.com>
"""

import datetime
import os
import re
import time

from yowsup.layers.protocol_messages.protocolentities import TextMessageProtocolEntity
from plugins.GenericPlugin import GenericPlugin

"""
The ContinuousReminder Class
"""
class ContinuousReminder(GenericPlugin):

    """
    Constructor
    @:param layer - the overlying yowsup layer
    @:param messageProtocolEntity - the received message information
    @:override
    """
    def __init__(self, layer, messageProtocolEntity=None):
        if messageProtocolEntity is None: self.layer = layer; return

        self.layer = layer
        self.entity = messageProtocolEntity

        self.capitalUserInput = self.entity.getBody()
        self.userInput = self.capitalUserInput.lower()
        self.sender = self.entity.getFrom()
        self.participant = self.entity.getParticipant()

        self.reminderMessage = ""
        self.params = ""

        self.continuous = False

    """
    Checks if the user input matches the regex needed for the plugin to function correctly
    @:override
    """
    def regexCheck(self):
        if "---endofmessage---" in self.userInput: return False
        if "@@@DONE@@@" in self.capitalUserInput: return False
        regex = r"^/cremind \"[^\"]+\" (monday|tuesday|wednesday|thursday|friday|saturday|sunday|" \
                r"montag|dienstag|mittwoch|donnerstag|freitag|samstag|sonntag) ([0-9]{2}-[0-9]{2}-[0-9]{2})$"
        if re.search(regex, self.userInput): return True
        else: return False

    """
    Parses the user input
    @:override
    """
    def parseUserInput(self):
        self.reminderMessage = self.capitalUserInput.split("\"", 1)[1].rsplit("\"", 1)[0]
        self.params = self.userInput.split("\" ", 1)[1]

    """
    Sends a confirmation back to the sender that the message was stored
    @:return the confirmation as a TextMessageProtocolEntity
    @:override
    """
    def getResponse(self):
        self.__setContinuousReminder__(self.params)
        return TextMessageProtocolEntity("Reminder Stored", to=self.sender)

    """
    Continuously checks if reminders are due and sends them to the intended recipient if needed.
    @:override
    """
    def parallelRun(self):
        while True:
            reminders = self.__findContinuousReminders__()
            for reminder in reminders:
                self.sendMessage(reminder)
                time.sleep(1)
            time.sleep(1)

    """
    Returns a description about this plugin
    @:override
    """
    @staticmethod
    def getDescription(language):
        if language == "en":
            return "/cremind"
        elif language == "de":
            return "/cremind"
        else:
            return "Help not available in this language"

### Private Methods ###


    """
    Stores a continuous (weekly) reminder
    @:param - the user input split as parameters
    """
    def __setContinuousReminder__(self, params):
        weekday = params.split(" ")[0]

        if weekday == "montag": weekday = "monday"
        if weekday == "dienstag": weekday = "tuesday"
        if weekday == "mittwoch": weekday = "wednesday"
        if weekday == "donnerstag": weekday = "thursday"
        if weekday == "freitag": weekday = "friday"
        if weekday == "samstag": weekday = "saturday"
        if weekday == "sonntag": weekday = "sunday"

        timeString = params.split(" ")[1]

        file = open(os.getenv("HOME") + "/.whatsapp-bot/reminders/continuous/" + self.sender, 'a')
        file.write("message=" + self.reminderMessage)
        file.write("---endofmessage---time=" + timeString + "@" + weekday)
        file.write("\n")

        file.close()

    """
    Searches all continuous reminders
    """
    def __findContinuousReminders__(self):

        weekday = datetime.date.today().strftime("%A").lower()
        currentTime = datetime.datetime.now()
        cHour = int(currentTime.hour)
        cMin = int(currentTime.minute)
        cSec = int(currentTime.second)

        recipients = os.listdir(os.getenv("HOME") + "/.whatsapp-bot/reminders/continuous")
        reminderEntities = []
        receiverPaths = []
        for receiver in recipients:
            if os.path.isdir(os.getenv("HOME") + "/.whatsapp-bot/reminders/continuous/" + receiver): continue
            receiverPaths.append(os.getenv("HOME") + "/.whatsapp-bot/reminders/continuous/" + receiver)
        for receiver in receiverPaths:
            receiverName = receiver.rsplit("/", 1)[1]
            file = open(receiver, "r")
            fileContent = file.read()
            file.close()

            reminders = fileContent.split("\n")
            if not reminders[len(reminders) - 1]: reminders.pop()
            refreshedReminders = []
            for reminder in reminders:
                reminderDay = reminder.split("---endofmessage---")[1].split("@")[1]

                if not "@@@DONE@@@" in reminder:
                    message = reminder.split("---endofmessage---")[0].split("message=")[1]
                    reminderTime = reminder.split("---endofmessage---")[1].split("@")[0].split("time=")[1]
                    hour = int(reminderTime.split("-")[0])
                    min = int(reminderTime.split("-")[1])
                    sec = int(reminderTime.split("-")[2])

                    outgoingEntity = TextMessageProtocolEntity(message, to=receiverName)

                    if not reminderDay == weekday: refreshedReminders.append(reminder)
                    else:
                        if cHour < hour: refreshedReminders.append(reminder);
                        elif cMin < min: refreshedReminders.append(reminder);
                        elif cSec < sec: refreshedReminders.append(reminder);
                        else:
                            refreshedReminders.append(reminder + "@@@DONE@@@")
                            reminderEntities.append(outgoingEntity)

                else:
                    if not weekday == reminderDay:
                        reminder = reminder.replace("@@@DONE@@@", "")
                        refreshedReminders.append(reminder)
                    else:
                        refreshedReminders.append(reminder)

            file = open(receiver, 'w')
            print(refreshedReminders)
            for reminder in refreshedReminders:
                file.write(reminder + "\n")
            file.close()

        return reminderEntities