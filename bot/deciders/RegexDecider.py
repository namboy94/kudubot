"""
Decider for strings that follow a certain regex pattern
@author Hermann Krumrey <hermann@krumreyh.com>
"""

"""
RegexDecider Class
"""
class RegexDecider(object):

    """
    Constructor
    @:param message - the received whatsapp message
    @:param sender - the sender of the received message
    """
    def __init__(self, message, sender, participant):
        self.message = message
        self.sender = sender
        self.participant = participant

    """
    Decides the user input
    """
    def decide(self):

        """
        #Regex Checks
        weatherRegex = re.search(r"", self.message.lower())
        mensaRegex = re.search(r"^/(mensa)( )?(linie (1|2|3|4|5|6)|schnitzelbar|curry queen|abend|cafeteria vormittag|cafeteria nachmittag)?( morgen)?$", self.message.lower())
        footballRegex = re.search(r"^/(table|tabelle|spieltag|matchday)( )?(([^ ]+| ){0,3})?$", self.message.lower())
        binaryRegex = re.search(r"^(0|1)+$", self.message)
        hexRegex = re.search(r"^(0x)(0|1|2|3|4|5|6|7|8|9|a|b|c|d|e|f)+$", self.message.lower())
        custBaseRegex = re.search(r"^[0-9a-z]+ (base|basis) [0-9]+$", self.message.lower())
        tvdbRegex = re.search(r"^/(tvdb) ([^ ]+| )+ s[0-9]{1,2} e[0-9]{1,4}$", self.message.lower())
        remindRegex = re.search(r"^/remind \"[^\"]+\" (tomorrow|morgen|[0-9]+ "
                                r"(years|yahre|months|monate|days|tage|hours|stunden|minutes|minuten|seconds|sekunden)"
                                r"|[0-9]{4}-[0-9]{2}-[0-9]{2}(-[0-9]{2}-[0-9]{2}-[0-9]{2})?)$", self.message.lower())
        helpRegex = re.search(r"^/(help|hilfe)$", self.message.lower())

        if self.message.startswith("/"): self.message = self.message.split("/", 1)[1]

        #Do stuff
        if weatherRegex: return Decision(weather(self.message.lower()).getWeather(), self.sender)
        if mensaRegex: return Decision(Mensa(self.message.lower()).getResponse(), self.sender)
        if footballRegex: return Decision(FootballScores(self.message.lower()).getResult(), self.sender)
        if binaryRegex: return Decision(anyBaseToN(2, self.message), self.sender)
        if hexRegex: return Decision(anyBaseToN(16, self.message.lower().split("0x")[1]), self.sender)
        if custBaseRegex: return Decision(anyBaseToN(int(self.message.rsplit(" ", 1)[1]), self.message.split(" ")[0]), self.sender)
        if tvdbRegex: return Decision(TheTVDB(self.message.lower()).getEpisodeName(), self.sender)
        if remindRegex: Reminder(self.message, self.sender, self.participant).storeRemind(); return False
        if helpRegex: return Decision(CommandHelper(self.message.lower()).generateHelp(), self.sender)
        """

        return False
