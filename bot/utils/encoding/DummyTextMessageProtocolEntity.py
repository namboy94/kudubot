# coding=utf-8
"""
Copyright 2015,2016 Hermann Krumrey

This file is part of whatsapp-bot.

    whatsapp-bot makes use of various third-party python modules to serve
    information via the online chat service Whatsapp.

    whatsapp-bot is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    whatsapp-bot is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with whatsapp-bot.  If not, see <http://www.gnu.org/licenses/>.
"""

"""
The Dummy Class
"""
class DummyTextMessageProtocolEntity(object):

    """
    Constructor
    entity := the original TextmessageProtocolEntity
    @:param message - entity.getBody() (fixed by Unicoder)
    @:param sender - entity.getFrom() (Can also be the recipient)
    @:param senderNumber - entity.getFrom(False) (Can also be the recipient's number)
    @:param participant - entity.getParticipant()
    @:param participantNumber - entity.getParticipant(False)
    @:param notify - entity.getNotify()
    """
    def __init__(self, message, sender, senderNumber, participant, notify):
        self.message = message
        self.sender = sender
        self.senderNumber = senderNumber
        self.participant = participant
        self.notify = notify

    """
    @:return the sender or senderNumber
    """
    def getFrom(self, full=True):
        if full:
            return self.sender
        else:
            return self.senderNumber

    """
    @:return the message body
    """
    def getBody(self):
        return self.message

    """
    @:return the sender or senderNumber
    """
    def getTo(self, full=True):
        return self.getFrom(full)

    """
    @:return the participant or participantNumber
    """
    def getParticipant(self):
        return self.participant

    """
    @:returns the notify/whatsapp username
    """
    def getNotify(self):
        return self.notify