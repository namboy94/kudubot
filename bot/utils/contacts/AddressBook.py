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


class AddressBook(object):
    """
    The AddressBook Class
    """

    def __init__(self):
        """
        Constructor containing all contacts in an array of arrays.
        """
        self.contacts = [["4915779781557-1418747022", "Land of the very Brave"],
                         ["4917628727937-1448730289", "Bottesting"],
                         ["4917628727937", "Hermann"]]
        self.blacklist = ["4915733871694", "4915202589244", "4915202589168"]
        self.authenticated = ["4917628727937"]

    def get_contact_name(self, entity, received):
        """
        Searches for a contact name belonging to a number given via parameter
        :param received: flag that needs to be set to determine if an entity was sent or
                            received
        :param entity: the received/sent message entity
        :return: the number if no name is found, otherwise the number of the contact
        """
        if received:
            sender = entity.get_from(False)
        else:
            sender = entity.get_to(False)
        for contact in self.contacts:
            if sender == contact[0]:
                return contact[1]
        return str(entity.get_notify())

    def get_contact_number(self, name):
        """
        Searches for a contact number belonging to a name given via parameter
        :param name: the name of the contact
        :return: the name if no number is found, otherwise the number of the contact
        """
        for contact in self.contacts:
            if name == contact[1]:
                return contact[0]
        return name

    def is_black_listed(self, number):
        """
        Checks if a number is blacklisted
        :param number: the number to be checked
        :return: true if the number is blacklisted, false otherwise
        """
        if number in self.blacklist: return True
        else: return False

    def is_authenticated(self, number):
        """
        Checks if a number is authenticated
        :param number: the number to be checked
        :return: true if the number is authenticated, false otherwise
        """
        pure_number = number.split("@")[0]
        if pure_number in self.authenticated:
            return True
        else:
            return False
