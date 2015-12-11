"""
Class that emulates an incoming TextMessageProtocolEntity, to enable correct handling of unicode characters with
enabled encryption
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
    """
    def __init__(self, message, sender, senderNumber, participant):
        self.message = message
        self.sender = sender
        self.senderNumber = senderNumber
        self.participant = participant

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