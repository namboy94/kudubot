# coding=utf-8
"""
LICENSE:
Copyright 2015,2016 Hermann Krumrey

This file is part of kudubot.

    kudubot makes use of various third-party python modules to serve
    information via online chat services.

    kudubot is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    kudubot is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with kudubot.  If not, see <http://www.gnu.org/licenses/>.
LICENSE
"""

# imports
import os
import re
import time
import random
import datetime
from typing import List, Tuple, Set

from kudubot.connection.generic.Message import Message
from kudubot.config.LocalConfigChecker import LocalConfigChecker
from kudubot.services.local_services.CasinoService import CasinoService
from kudubot.resources.images.__init__ import get_location as get_board_image_file


def calculate_neighbour_group(roulette_board: List[List[int]]) -> List[Set[int]]:
    """
    Calculates the neighbouring tiles for a roulette board

    :param roulette_board: the roulette board to be used
    :return: the dual neghbours, the quad neighbours
    """
    board = roulette_board
    pairs = []
    quads = []
    row = 0
    while row < len(board):
        row_crawler = 0
        column_crawler = 1

        while column_crawler < len(board[row]):
            pairs.append([board[row][row_crawler], board[row][column_crawler]])

            if row < (len(board) - 1):
                pairs.append({board[row][row_crawler], board[row + 1][row_crawler]})
                pairs.append({board[row][column_crawler], board[row + 1][column_crawler]})

                quads.append({board[row][row_crawler],
                              board[row + 1][row_crawler],
                              board[row][column_crawler],
                              board[row + 1][column_crawler]})

                row_crawler += 1
            column_crawler += 1
        row += 1

    return pairs, quads


class RouletteService(CasinoService):
    """
    The RouletteService Class that extends the generic Service class.
    The service allows the user to play roulette.
    The board is spun every 2 minutes
    """

    identifier = "roulette"
    """
    The identifier for this service
    """

    has_background_process = True
    """
    Class has a background process.
    """

    help_description = {"en": "/roulette\tAllows the sender to play roulette\n"
                              "syntax: /roulette <amount> <bet>\n"
                              "valid bets: 0-36 | red | black | odd | even |"
                              " half 1-2 | group 1-3 | row 1-3 | batch 0-36{2|4}\n"
                              "/roulette time\tDisplays the time left until the wheel is spun again\n"
                              "/roulette board\tSends an image of a Roulette board as reference\n"
                              "/roulette bets\tDisplays all bets of a user\n"
                              "/roulette cancel <index>\tCancels a bet of a user\n"
                              "/roulette spin\tImmediately spins the wheel(admin)",
                        "de": "/roulette\tErmöglicht das Spielen von Roulette\n"
                              "syntax: /roulette <einsatz> <wette>\n"
                              "Mögliche Wetten:"
                              " 0-36 | rot | schwarz | ungerade | gerade | hälfte 1-2 | gruppe 1-3 | reihe 1-3 |"
                              "nachbarn 0-36{2|4}\n"
                              "/roulette zeit\t"
                              "Zeigt die verbleibende Zeit bis zum nächsten Drehen des Roulette-Rads an.\n"
                              "/roulette bord\tSchickt ein Bild eines Roulettebretts als Referenz\n"
                              "/roulette wetten\tZeigt alle Wetten eines Nutzers an\n"
                              "/roulette abbruch <index>\tBricht eine Wette des Nutzers ab\n"
                              "/roulette drehen\tDreht das Rouletterad(admin)"}
    """
    Help description for this service.
    """

    red_numbers = [1, 3, 5, 7, 9, 12, 14, 16, 18, 19, 21, 23, 25, 27, 30, 32, 34, 36]
    """
    List of numbers on the board that are red
    """

    black_numbers = [2, 4, 6, 8, 10, 11, 13, 15, 17, 20, 22, 24, 26, 28, 29, 31, 33, 35]
    """
    List of numbers on the board that are black
    """

    roulette_board = [[3, 6, 9, 12, 15, 18, 21, 24, 27, 30, 33, 36],
                      [2, 5, 8, 11, 14, 17, 20, 23, 26, 29, 32, 35],
                      [1, 4, 7, 10, 13, 16, 19, 22, 25, 28, 31, 34]]
    """
    The layout of the roulette board
    """

    dual_neighbours, quad_neighbours = calculate_neighbour_group(roulette_board)
    """
    lists of neighbouring tiles
    """

    roulette_directory = ""
    """
    Directory to store the roulette bets
    """

    roulette_board_image = get_board_image_file("rouletteboard.jpg")
    """
    The roulette board image file
    """

    spin_keywords = {"spin": "en",
                     "drehen": "de"}
    """
    Keywords for the 'spin' option
    """

    cancel_keywords = {"cancel": "en",
                       "abbruch": "de"}
    """
    Keywords for the 'cancel' option
    """

    board_keywords = {"board": "en",
                      "bord": "de"}
    """
    Keywords for the 'board' option
    """

    time_keywords = {"time": "en",
                     "zeit": "de"}
    """
    Keywords for the 'time' option
    """

    bets_keywords = {"bets": "en",
                     "wetten": "de"}
    """
    Keywords for the 'bets' option
    """

    black_keywords = {"black": "en",
                      "schwarz": "de"}
    """
    Keywords for the 'black' option
    """

    red_keywords = {"red": "en",
                    "rot": "de"}
    """
    Keywords for the 'red' option
    """

    even_keywords = {"even": "en",
                     "gerade": "de"}
    """
    Keywords for the 'even' option
    """

    odd_keywords = {"odd": "en",
                    "ungerade": "de"}
    """
    Keywords for the 'odd' option
    """

    group_keywords = {"group": "en",
                      "gruppe": "de"}
    """
    Keywords for the 'group' option
    """

    neighbour_keywords = {"neighbours": "en",
                          "nachbarn": "de"}
    """
    Keywords for the 'neighbour' option
    """

    row_keywords = {"row": "en",
                    "reihe": "de"}
    """
    Keywords for the 'row' option
    """

    half_keywords = {"half": "en",
                     "hälfte": "de"}
    """
    Keywords for the 'half' option
    """

    is_spinning_message = {"en": "The wheel is currently spinning, please wait a few seconds",
                           "de": "Das Rouletterad dreht sich gerade, hab einen moment Geduld"}
    """
    Message sent to the user when the roulette wheel is currently
    """

    won_message = {"en": " won ",
                   "de": " hat gewonnen: "}
    """
    Message shown when the user has won.
    """

    time_left_message = {"en": "s left until the board will be spinned",
                         "de": "s noch bis zum Drehen des Rades"}
    """
    Message to be sent when a request for time to next spin was sent
    """

    not_authenticated_method = {"en": "You are not authorized to spin the wheel",
                                "de": "Du hast keine Erlaubniss das Rad zu drehen"}
    """
    Message sent when a non-admin user tries to spin the wheel
    """

    undefined_behaviour = {"en": "This should not happen",
                           "de": "Dies sollte nicht passieren"}
    """
    Message for undefined behavour
    """

    spin_summary = {"en": "The result of the spin is: ",
                    "de": "Das Resultat ist: "}

    def initialize(self) -> None:
        """
        Initializes the roulette bets directory

        :return: None
        """
        super().initialize()
        self.roulette_directory = os.path.join(self.bet_directory, "roulette")
        LocalConfigChecker.validate_directory(self.roulette_directory)

    def process_message(self, message: Message) -> None:
        """
        Process a message according to the service's functionality

        :param message: the message to process
        :return: None
        """
        reply = self.parse_user_input(message)

        if reply:
            reply_message = self.generate_reply_message(message, "Roulette", reply)
            self.send_text_message(reply_message)

    @staticmethod
    def regex_check(message: Message) -> bool:
        """
        Checks if the user input is valid for this service to continue

        :return: True if input is valid, False otherwise
        """
        neighbours = RouletteService.regex_string_from_dictionary_keys([RouletteService.neighbour_keywords])
        group = RouletteService.regex_string_from_dictionary_keys([RouletteService.group_keywords])
        half = RouletteService.regex_string_from_dictionary_keys([RouletteService.half_keywords])
        row = RouletteService.regex_string_from_dictionary_keys([RouletteService.row_keywords])
        zero_to_36_regex = "(([0-9]?[0-3])|3[0-6])"

        regex = "^/roulette (([0-9]+((\.|,)[0-9]{2})?) (" + zero_to_36_regex + "|"
        regex += RouletteService.regex_string_from_dictionary_keys([RouletteService.red_keywords,
                                                                    RouletteService.black_keywords,
                                                                    RouletteService.odd_keywords,
                                                                    RouletteService.even_keywords])
        regex += "|" + neighbours + " " + zero_to_36_regex + "(-" + zero_to_36_regex + "){3}|"
        regex += "|" + neighbours + " " + zero_to_36_regex + "-" + zero_to_36_regex + "|"
        regex += "|" + group + " (1|2|3)|"
        regex += "|" + half + "(1|2)|"
        regex += "|" + row + "(1|2|3))|" \
                 + RouletteService.regex_string_from_dictionary_keys([RouletteService.spin_keywords,
                                                                      RouletteService.board_keywords,
                                                                      RouletteService.time_keywords,
                                                                      RouletteService.bets_keywords]) + "|"
        regex += RouletteService.regex_string_from_dictionary_keys([RouletteService.cancel_keywords]) + " [0-9]+)$"

        match = re.search(re.compile(regex), message.message_body.lower())

        if match and message.message_body.lower().split(" ")[1] in RouletteService.neighbour_keywords:

            neighbours = message.message_body.lower().split(" ")[2]
            neighbour_set = RouletteService.parse_neighbour_group(neighbours)

            match = neighbour_set in RouletteService.dual_neighbours \
                or neighbour_set in RouletteService.quad_neighbours

        return match

    def parse_user_input(self, message: Message) -> str:
        """
        Parses the user input from the message

        :param message: The message to be parsed
        :return: a reply string
        """
        user_input = message.message_body.lower()
        user_address = message.get_individual_address()

        user_input = user_input.split("/roulette ")[1]
        options = user_input.split(" ")

        if self.is_spinning():
            return self.is_spinning_message[self.connection.last_used_language]

        if options[0] in self.spin_keywords:
            if self.connection.authenticator.is_from_admin(message):
                return self.spin_wheel(self.spin_keywords[options[0]])
            else:
                return self.not_authenticated_method[self.spin_keywords[options[0]]]
        elif options[0] in self.cancel_keywords:
            return self.cancel_bets(self.cancel_keywords[options[0]], user_address, int(options[1]))
        elif options[0] in self.board_keywords:
            return self.send_board(user_address)
        elif options[0] in self.time_keywords:
            return str(self.request_time_to_spin()) + self.time_left_message[self.time_keywords[options[0]]]
        elif options[0] in self.bets_keywords:
            return self.get_bets_as_formatted_string("roulette", user_address)
        else:
            money = self.parse_money_string(options[0])

            if options[1] in self.red_keywords:
                selection = self.red_numbers
            elif options[1] in self.black_keywords:
                selection = self.black_numbers
            elif options[1] in self.odd_keywords:
                selection = []
                for number in (self.black_numbers + self.red_numbers):
                    if number % 2 == 1:
                        selection.append(number)
            elif options[1] in self.even_keywords:
                selection = []
                for number in (self.black_numbers + self.red_numbers):
                    if number % 2 == 0:
                        selection.append(number)
            elif re.search(r"(([0-9]?[0-3])|3[0-6])", options[1]):
                selection = [int(options[1])]
            else:
                parameter = options[2]

                if options[1] in self.neighbour_keywords:
                    selection = self.parse_neighbour_group(parameter)
                elif options[1] in self.group_keywords:
                    selection = []
                    start_point = (int(options[1]) - 1) * 12
                    for tile in range(start_point, start_point + 12):
                        selection.append(tile + 1)
                elif options[1] in self.half_keywords:
                    selection = []
                    start_point = (int(options[1]) - 1) * 18
                    for tile in range(start_point, start_point + 18):
                        selection.append(tile + 1)
                elif options[1] in self.row_keywords:
                    selection = self.roulette_board[int(options[1])]
                else:
                    return self.undefined_behaviour[self.connection.last_used_language]

            return self.create_bet(user_address, selection, money)

    @staticmethod
    def parse_neighbour_group(neighbour_group_string: str) -> Set[int]:
        """
        Parses a neighbour-group string and returns it as a set of tiles

        :param neighbour_group_string: the string to parse
        :return: a set of tiles
        """
        neighbours = neighbour_group_string.split("-")
        neighbour_set = set()

        for neigbour in neighbours:
            neighbour_set.add(int(neigbour))

        return neighbour_set

    @staticmethod
    def get_position_on_table(tile: int) -> Tuple[int, int]:
        """
        Gets the coordinates of a tile on the roulette table

        :param tile: the tile to check
        :return: the column, the row
        """
        return int(tile / 3), (2 - (tile - 1) % 3)

    @staticmethod
    def is_spinning() -> bool:
        """
        Checks if the board is spinning/should be spinning (which is a 5 second
        timeframe to avoid racing conditions)

        :return: True if the wheel should be spinning, False otherwise
        """
        current_time = datetime.datetime.utcnow()
        minutes = int(current_time.minute)
        seconds = int(current_time.second)

        return minutes % 2 == 1 and seconds >= 55

    def spin_wheel(self, language: str) -> None:
        """
        Spins the roulette wheel, calculating winnings for all users

        :param language: the languag to use
        :return: None
        """
        result = random.randint(0, 36)
        users = []

        for bet_file_name in os.listdir(self.roulette_directory):
            user = bet_file_name.rsplit("###BETVAL=", 1)[0]
            if user not in users:
                users.append(user)

        bets = []
        addresses = []

        for user in users:
            user_bets = self.get_bets("roulette", user)

            for bet in user_bets:
                if bet["address"] not in addresses:
                    addresses.append(bet["address"])

                selected_tiles, multiplier = bet['bet_type'].split("X")
                selected_tiles = selected_tiles.split("-")

                bet['multiplier'] = int(multiplier)
                bet['selection'] = []

                for tile in selected_tiles:
                    bet['selection'].append(int(tile))

                os.remove(bet["file"])
            bets += user_bets

        summary = ""

        for bet in bets:
            if bet["address"] not in addresses:
                addresses.append(bet["address"])

            if result in bet["selection"]:
                won_value = bet["value"] * bet["multiplier"]
                summary += bet["user"] + self.won_message[language] + self.format_money_string(won_value) + "\n\n"
                self.transfer_funds(bet["user"], won_value)

        if len(addresses) > 0:
            summary = self.spin_summary[language] + str(result) + "\n\n" + summary

            for better in addresses:
                message = Message(message_body=summary, message_title="Roulette", address=better)
                self.send_text_message(message)

    def cancel_bets(self, language: str, user_address: str, index: int) -> str:
        """
        Cancels a bet

        :param language: the language to use
        :param user_address: the user address string
        :param index: the index of the bet to delete
        :return: A message detailing the success or failure of the deletion
        """
        self.connection.last_used_language = language
        return self.delete_bet("roulette", user_address, index)

    def send_board(self, address: str) -> None:
        """
        Sends an image of a roulette board to the user

        :param address: the address of the user
        :return: None
        """
        self.send_image_message(address, self.roulette_board_image)

    @staticmethod
    def request_time_to_spin() -> int:
        """
        Returns the mount of time in seconds until the roulette wheel is spun again

        :return: the time until the next spin in seconds
        """
        current_time = datetime.datetime.utcnow()
        current_minute = int(current_time.minute)
        current_second = int(current_time.second)

        time_left = 120 - current_second - 5
        if current_minute % 2 == 1:
            time_left -= 60

        return time_left

    def create_bet(self, address: str, bet_items: List[int], value: int) -> str:
        """
        Creates a new bet

        :param address: The address used to determine which user made the bet
        :param bet_items: The items for which the user placed a bet
        :param value: the value of the bet
        :return: a message telling the user that the bet was placed succesfully
        """
        multiplier = int(36 / len(bet_items))
        bet_string = ""

        for element in bet_items:
            bet_string += str(element) + "-"

        bet_string = bet_string.rsplit("-", 1)[0]
        bet_string += "X" + str(multiplier)
        reply = self.store_bet("roulette", address, value, bet_string)

        return reply

    def background_process(self) -> None:
        """
        Spins the wheel in periodic intervals

        :return: None
        """
        while True:
            if self.is_spinning():
                self.spin_wheel(self.connection.last_used_language)
                time.sleep(60)
            time.sleep(3)
