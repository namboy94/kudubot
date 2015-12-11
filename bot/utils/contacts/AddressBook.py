"""
Class that handles contact identifying
@author Hermann Krumrey<hermann@krumreyh.com>
"""

"""
The AddressBook Class
"""
class AddressBook(object):

    """
    Constructor containing all contacts in an array of arrays.
    """
    def __init__(self):
        self.contacts = [["4915779781557-1418747022", "Land of the very Brave"],
                    ["4917628727937-1448730289", "Bottesting"],
                    ["4917628727937", "Hermann"]]

    """
    Searches for a contact name belonging to a number given via parameter
    @:return the number if no name is found, otherwise the number of the contact
    """
    def getContactName(self, sender):
        for contact in self.contacts:
            if sender == contact[0]:
                return contact[1]
        return sender

    """
    Searches for a contact number belonging to a name given via parameter
    @:return the name if no number is found, otherwise the number of the contact
    """
    def getContactNumber(self, name):
        for contact in self.contacts:
            if name == contact[1]:
                return contact[0]
        return name