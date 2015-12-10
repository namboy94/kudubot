import datetime
import os
import re
import time
from bot.deciders.Decision import Decision

class Reminder(object):

    def __init__(self, userInput="", sender="", participant=""):
        if not userInput and not sender and not participant: return
        self.leapyear = False
        if datetime.datetime.now().year % 4 == 0: self.leapyear = True
        self.capitalUserInput = userInput
        self.userInput = userInput.lower()
        self.sender = sender
        self.participant = participant
        self.year = 0
        self.month = 0
        self.day = 0
        self.hour = 0
        self.minute = 0
        self.second = 0
        self.reminderMessage = ""
        self.parseUserInput()

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
            self.setRemindertime(cYear, cMonth, cDay + 1, cHour, cMin, cSec)
        if re.search(r"^[0-9]+ (years|jahre)$", params):
            self.setRemindertime(cYear + int(params.split(" ")[0]), cMonth, cDay, cHour, cMin, cSec)
        if re.search(r"^[0-9]+ (months|monate)$", params):
            self.setRemindertime(cYear, cMonth + int(params.split(" ")[0]), cDay, cHour, cMin, cSec)
        if re.search(r"^[0-9]+ (days|tage)$", params):
            self.setRemindertime(cYear, cMonth, cDay + int(params.split(" ")[0]), cHour, cMin, cSec)
        if re.search(r"^[0-9]+ (hours|stunden)$", params):
            self.setRemindertime(cYear, cMonth, cDay, cHour + int(params.split(" ")[0]), cMin, cSec)
        if re.search(r"^[0-9]+ (minutes|minuten)$", params):
            self.setRemindertime(cYear, cMonth, cDay, cHour, cMin + int(params.split(" ")[0]), cSec)
        if re.search(r"^[0-9]+ (sekunden|seconds)$", params):
            self.setRemindertime(cYear, cMonth, cDay, cHour, cMin, cSec + int(params.split(" ")[0]))
        if re.search(r"^[0-9]{4}-[0-9]{2}-[0-9]{2}$", params):
            self.setRemindertime(int(params.split("-")[0]), int(params.split("-")[1]), int(params.split("-")[2]), 0, 0, 0)
        if re.search(r"^[0-9]{4}-[0-9]{2}-[0-9]{2}-[0-9]{2}-[0-9]{2}-[0-9]{2}$", params):
            self.setRemindertime(int(params.split("-")[0]), int(params.split("-")[1]), int(params.split("-")[2]), int(params.split("-")[3]), int(params.split("-")[4]), int(params.split("-")[5]))
        self.calendarizeTime()

    def setRemindertime(self, year, month, day, hour, minute, second):
        self.year = year
        self.month = month
        self.day = day
        self.hour = hour
        self.minute = minute
        self.second = second

    def calendarizeTime(self):
        secondsLeft = self.second - self.second % 60
        self.second = self.second % 60
        self.minute += int(secondsLeft / 60)
        minutesLeft = self.minute - self.minute % 60
        self.minute = self.minute % 60
        self.hour += int(minutesLeft / 60)
        hoursLeft = self.hour - self.hour % 24
        self.hour = self.hour % 24
        self.day += int(self.hour / 24)
        monthLength = self.getMonthLength()
        while self.day > monthLength:
            self.day -= monthLength
            self.incrementMonth()

    def getMonthLength(self):
        if self.month in [1,3,5,7,8,10,12]: monthLength = 31
        elif self.month in [4,6,9,11]: monthLength = 30
        elif self.month == 2 and self.leapyear: monthLength = 29
        else: monthLength = 28
        return monthLength

    def incrementMonth(self):
        if self.month < 12: self.month += 1
        elif self.month == 12: self.month = 1; self.year += 1

    def createReminderTimeString(self):
        return str(self.year) + "-" + str(self.month) + "-" + str(self.day) + "-" \
               + str(self.hour) + "-" + str(self.minute) + "-" + str(self.second)

    def storeRemind(self):
        file = open(os.getenv("HOME") + "/.whatsapp-bot/reminders/" + str(int(time.time())), 'w')
        file.write("sender=" + self.sender)
        file.write("\nmessage=" + self.reminderMessage)
        file.write("\ntime=" + self.createReminderTimeString())
        print("Storing Reminder...")
        file.close()

    def findReminder(self):
        reminders = os.listdir(os.getenv("HOME") + "/.whatsapp-bot/reminders")
        reminderDecisions = []
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
            if self.remindDue(timeString):
                os.system("rm " + reminder)
                decision = Decision(message, sender)
                reminderDecisions.append(decision)
        return reminderDecisions

    def remindDue(self, timeString):
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