"""
@author Hermann Krumrey<hermann@krumreyh.com>
"""

"""
Matches a Whatsapp-number with a contact name
@:return the name of the established contact, or the original number if no contact was found
"""
def getContact(sender):

    number = sender.split("@")[0]

    if number == "4915779781557-1418747022": return "Land of the very Brave"
    elif number == "4917628727937-1448730289": return "Bottesting"
    elif number == "4917628727937": return "Hermann"
    else: return number