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
        self.blacklist = ["4915733871694", "4915202589244", "4915202589168"]
        self.authenticated = ["4917628727937"]

    """
    Searches for a contact name belonging to a number given via parameter
    @:return the number if no name is found, otherwise the number of the contact
    """
    def getContactName(self, entity, received):
        if received:
            sender = entity.getFrom(False)
        else:
            sender = entity.getTo(False)
        for contact in self.contacts:
            if sender == contact[0]:
                return contact[1]
        return str(entity.getNotify())

    """
    Searches for a contact number belonging to a name given via parameter
    @:return the name if no number is found, otherwise the number of the contact
    """
    def getContactNumber(self, name):
        for contact in self.contacts:
            if name == contact[1]:
                return contact[0]
        return name

    """
    Checks if a number is blacklisted
    @:return true if the number is blacklisted, false otherwise
    """
    def isBlackListed(self, number):
        if number in self.blacklist: return True
        else: return False

    """
    Checks if a number is authenticated
    @:return true if the number is authenticated, false otherwise
    """
    def isAuthenticated(self, number):
        pureNumber = number.split("@")[0]
        if pureNumber in self.authenticated: return True
        else: return False
