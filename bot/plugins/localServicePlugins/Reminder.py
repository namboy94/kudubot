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
from utils.encoding.Unicoder import Unicoder
from utils.logging.LogWriter import LogWriter

"""
The Reminder Class
"""
class Reminder(GenericPlugin):

    """
    Constructor
    @:param layer - the overlying yowsup layer
    @:param messageProtocolEntity - the received message information
    @:override
    """
    def __init__(self, layer, messageProtocolEntity=None):
        if messageProtocolEntity is None: self.layer = layer; return
        self.leapyear = False
        if datetime.datetime.now().year % 4 == 0: self.leapyear = True

        self.layer = layer
        self.entity = messageProtocolEntity

        self.capitalUserInput = self.entity.getBody()
        self.userInput = self.capitalUserInput.lower()
        self.sender = self.entity.getFrom()
        self.participant = self.entity.getParticipant()

        self.year = 0
        self.month = 0
        self.day = 0
        self.hour = 0
        self.minute = 0
        self.second = 0
        self.reminderMessage = ""

    """
    Checks if the user input matches the regex needed for the plugin to function correctly
    @:override
    """
    def regexCheck(self):
        regex = r"^/remind \"[^\"]+\" (tomorrow|morgen|" \
                r"[0-9]+ (years|yahre|months|monate|days|tage|hours|stunden|minutes|minuten|seconds|sekunden)|" \
                r"[0-9]{4}-[0-9]{2}-[0-9]{2}(-[0-9]{2}-[0-9]{2}-[0-9]{2})?)$"
        if re.search(regex, self.userInput): return True
        else: return False

    """
    Parses the user input
    @:override
    """
    def parseUserInput(self):
        self.reminderMessage = self.capitalUserInput.split("\"", 1)[1].rsplit("\"", 1)[0]

        currentTime = datetime.datetime.now()
        cYear = int(currentTime.year)
        cMonth = int(currentTime.month)
        cDay = int(currentTime.day)
        cHour = int(currentTime.hour)
        cMin = int(currentTime.minute)
        cSec = int(currentTime.second)
        params = self.userInput.split("\" ", 1)[1]
        if params in ["morgen", "tomorrow"]:
            self.__setRemindertime__(cYear, cMonth, cDay + 1, cHour, cMin, cSec)
        if re.search(r"^[0-9]+ (years|jahre)$", params):
            self.__setRemindertime__(cYear + int(params.split(" ")[0]), cMonth, cDay, cHour, cMin, cSec)
        if re.search(r"^[0-9]+ (months|monate)$", params):
            self.__setRemindertime__(cYear, cMonth + int(params.split(" ")[0]), cDay, cHour, cMin, cSec)
        if re.search(r"^[0-9]+ (days|tage)$", params):
            self.__setRemindertime__(cYear, cMonth, cDay + int(params.split(" ")[0]), cHour, cMin, cSec)
        if re.search(r"^[0-9]+ (hours|stunden)$", params):
            self.__setRemindertime__(cYear, cMonth, cDay, cHour + int(params.split(" ")[0]), cMin, cSec)
        if re.search(r"^[0-9]+ (minutes|minuten)$", params):
            self.__setRemindertime__(cYear, cMonth, cDay, cHour, cMin + int(params.split(" ")[0]), cSec)
        if re.search(r"^[0-9]+ (sekunden|seconds)$", params):
            self.__setRemindertime__(cYear, cMonth, cDay, cHour, cMin, cSec + int(params.split(" ")[0]))
        if re.search(r"^[0-9]{4}-[0-9]{2}-[0-9]{2}$", params):
            self.__setRemindertime__(int(params.split("-")[0]), int(params.split("-")[1]), int(params.split("-")[2]), 0, 0, 0)
        if re.search(r"^[0-9]{4}-[0-9]{2}-[0-9]{2}-[0-9]{2}-[0-9]{2}-[0-9]{2}$", params):
            self.__setRemindertime__(int(params.split("-")[0]), int(params.split("-")[1]), int(params.split("-")[2]), int(params.split("-")[3]), int(params.split("-")[4]), int(params.split("-")[5]))
        self.__calendarizeTime__()

    """
    Sends a confirmation back to the sender that the message was stored
    @:return the confirmation as a TextMessageProtocolEntity
    @:override
    """
    def getResponse(self):
        file = open(os.getenv("HOME") + "/.whatsapp-bot/reminders/" + str(int(time.time())), 'w')
        file.write("sender=" + self.sender)
        file.write("\nmessage=" + self.reminderMessage)
        file.write("\ntime=" + self.__createReminderTimeString__())
        file.close()
        return TextMessageProtocolEntity("Reminder Stored", to=self.sender)

    """
    Continuously checks if reminders are due and sends them to the intended recipient if needed.
    @:override
    """
    def parallelRun(self):
        while True:
            reminders = self.__findReminders__()
            for reminder in reminders:
                LogWriter.writeEventLog("sent", reminder)
                message = Unicoder.fixOutgoingEntity(reminder)
                self.layer.toLower(message)
                time.sleep(1)
            time.sleep(1)

    """
    Returns a description about this plugin
    @:override
    """
    @staticmethod
    def getDescription(language):
        if language == "en":
            return "/remind\tSaves a reminder and sends it back at the specified time\n" \
                   "syntax: /remind \"<message>\" <time>\n" \
                   "time syntax: <YYYY-MM-DD-hh-mm-ss>\n" \
                   "or: <amount> [years|months|days|hours|minutes|seconds]"
        elif language == "de":
            return "/remind\tSpeichert eine Erinnerung und verschickt diese zum angegebenen Zeitpunkt\n" \
                   "syntax: /remind \"<nachricht>\" <zeit>\n" \
                   "zeit syntax: YYYY-MM-DD-hh-mm-ss\n" \
                   "oder: <anzahl> [jahre|monate|tage|stunden|minuten|sekunden]"
        else:
            return "Help not available in this language"

### Private Methods ###

    """
    Sets the local reminder time to a specified date and time
    @:param year - the year
    @:param month - the month
    @:param day - the day
    @:param hour - the hour
    @:param minute - the minute
    @:param second - the second
    """
    def __setRemindertime__(self, year, month, day, hour, minute, second):
        self.year = year
        self.month = month
        self.day = day
        self.hour = hour
        self.minute = minute
        self.second = second

    """
    Makes sure that only values valid in the Gregorian Calendar and metric time measurement systems
    """
    def __calendarizeTime__(self):
        secondsLeft = self.second - self.second % 60
        self.second = self.second % 60
        self.minute += int(secondsLeft / 60)
        minutesLeft = self.minute - self.minute % 60
        self.minute = self.minute % 60
        self.hour += int(minutesLeft / 60)
        hoursLeft = self.hour - self.hour % 24
        self.hour = self.hour % 24
        self.day += int(self.hour / 24)
        monthLength = self.__getMonthLength__()
        while self.day > monthLength:
            self.day -= monthLength
            self.__incrementMonth__()

    """
    calculates the lenth of the current month in days
    @:return the amount of days in the current month
    """
    def __getMonthLength__(self):
        if self.month in [1,3,5,7,8,10,12]: monthLength = 31
        elif self.month in [4,6,9,11]: monthLength = 30
        elif self.month == 2 and self.leapyear: monthLength = 29
        else: monthLength = 28
        return monthLength

    """
    increments the month by one
    """
    def __incrementMonth__(self):
        if self.month < 12: self.month += 1
        elif self.month == 12: self.month = 1; self.year += 1

    """
    Turns the current reminder time into a string
    @:return the reminder time string
    """
    def __createReminderTimeString__(self):
        return str(self.year) + "-" + str(self.month) + "-" + str(self.day) + "-" \
               + str(self.hour) + "-" + str(self.minute) + "-" + str(self.second)



    """
    Searches all currently saved reminders and checks if they are due. If they are, they are returned
    @:return a list of due reminders as TextMessageProtocolEntities
    """
    def __findReminders__(self):
        reminders = os.listdir(os.getenv("HOME") + "/.whatsapp-bot/reminders")
        reminderEntities = []
        reminderPaths = []
        for reminder in reminders:
            reminderPaths.append(os.getenv("HOME") + "/.whatsapp-bot/reminders/" + reminder)
        for reminder in reminderPaths:
            file = open(reminder, "r")
            fileContent = file.read()
            file.close()
            sender = fileContent.split("\n")[0].split("sender=")[1]
            message = fileContent.split("\n")[1].split("message=")[1]
            timeString = fileContent.split("\n")[2].split("time=")[1]
            if self.__remindDue__(timeString):
                os.system("rm " + reminder)
                outgoingEntity = TextMessageProtocolEntity(message, to=sender)
                reminderEntities.append(outgoingEntity)
        return reminderEntities

    """
    Checks if a timestring is due
    @:return True if it is due, False if not.
    """
    def __remindDue__(self, timeString):
        currentTime = datetime.datetime.now()
        cYear = int(currentTime.year)
        cMonth = int(currentTime.month)
        cDay = int(currentTime.day)
        cHour = int(currentTime.hour)
        cMin = int(currentTime.minute)
        cSec = int(currentTime.second)
        remindTime = timeString.split("-")
        remindYear = int(remindTime[0])
        remindMonth = int(remindTime[1])
        remindDay = int(remindTime[2])
        remindHour = int(remindTime[3])
        remindMinute = int(remindTime[4])
        remindSecond = int(remindTime[5])

        if cYear < remindYear: return False
        elif cMonth < remindMonth: return False
        elif cDay < remindDay: return False
        elif cHour < remindHour: return False
        elif cMin < remindMinute: return False
        elif cSec < remindSecond: return False
        else: return True