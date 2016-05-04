# coding=utf-8
"""
Copyright 2015,2016 Hermann Krumrey

This file is part of messengerbot.

    messengerbot makes use of various third-party python modules to serve
    information via the online chat services.

    messengerbot is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    messengerbot is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with messengerbot.  If not, see <http://www.gnu.org/licenses/>.
"""

# imports
import os
import re
import random
import datetime
from typing import List, Tuple, Set

from messengerbot.connection.generic.Message import Message
from messengerbot.services.local_services.CasinoService import CasinoService
from messengerbot.config.LocalConfigChecker import LocalConfigChecker


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

    help_description = {"en": "/roulette\tAllows the sender to play roulette\n"
                              "syntax: /roulette <amount> <bet>\n"
                              "valid bets: 0-36 | red | black | odd | even |"
                              " half 1-2 | group 1-3 | row 1-3 | batch 0-36{2|4}\n"
                              "/roulette time\tDisplays the time left until the wheel is spun again\n"
                              "/roulette board\tSends an image of a Roulette board as reference\n"
                              "/roulette bets\tDisplays all bets of a user\n"
                              "/roulette cancel\tCancels all bet of a user\n"
                              "/roulette spin\tImmediately spins the wheel(admin)",
                        "de": "/roulette\tErmöglicht das Spielen von Roulette\n"
                              "syntax: /roulette <einsatz> <wette>\n"
                              "Mögliche Wetten:"
                              " 0-36 | red | black | odd | even | half 1-2 | group 1-3 | row 1-3 | batch 0-36{2|4}\n"
                              "/roulette time\t"
                              "Zeigt die verbleibende Zeit bis zum nächsten Drehen des Roulette-Rads an.\n"
                              "/roulette board\tSchickt ein Bild eines Roulettebretts als Referenz\n"
                              "/roulette bets\tZeigt alle Wetten eines Nutzers an\n"
                              "/roulette cancel\tBricht alle Wetten des Nutzers ab\n"
                              "/roulette spin\tDreht das Rouletterad(admin)"}
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

    spin_keywords = {"spin": "en",
                     "dreh": "de"}
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

    black_keywords = {"bets": "en",
                      "wetten": "de"}
    """
    Keywords for the 'black' option
    """

    red_keywords = {"bets": "en",
                    "wetten": "de"}
    """
    Keywords for the 'red' option
    """

    even_keywords = {"bets": "en",
                     "wetten": "de"}
    """
    Keywords for the 'even' option
    """

    odd_keywords = {"bets": "en",
                    "wetten": "de"}
    """
    Keywords for the 'odd' option
    """

    group_keywords = {"group": "en",
                      "gruppe": "de"}
    """
    Keywords for the 'group' option
    """

    neighbour_keywords = {"neighbour": "en",
                          "nachbar": "de"}
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

    def initialize(self) -> None:
        """
        Initializes the roulette bets directory

        :return: None
        """
        self.roulette_directory = os.path.join(self.bet_directory, "roulette")
        LocalConfigChecker.validate_directory(self.roulette_directory)

    def process_message(self, message: Message) -> None:
        """
        Process a message according to the service's functionality

        :param message: the message to process
        :return: None
        """
        reply = self.parse_user_input(message.message_body.lower(), message.get_unique_identifier())

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

        regex = "^/roulette (([0-9]+(\.[0-9]{2})?) (" + zero_to_36_regex + "|"
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
                                                                      RouletteService.cancel_keywords,
                                                                      RouletteService.board_keywords,
                                                                      RouletteService.time_keywords,
                                                                      RouletteService.bets_keywords,]) + "$"

        match = re.search(re.compile(regex), message.message_body.lower())

        if match and message.message_body.lower().split(" ")[1] in RouletteService.neighbour_keywords:

            neighbours = message.message_body.lower().split(" ")[2]
            neighbour_set = RouletteService.parse_neighbour_group(neighbours)

            match = neighbour_set in RouletteService.dual_neighbours \
                    or neighbour_set in RouletteService.quad_neighbours

        return match

    def parse_user_input(self, user_input: str, user_identifier: str) -> Stuff:
        """
        Parses the user input

        :param user_input: the user input to be parsed
        :param user_identifier: the user identifier to identify the user's account etc.
        :return: TBD
        """
        user_input = user_input.split("/roulette ")[1]
        options = user_input.split(" ")

        if self.is_spinning():
            return self.is_spinning_message[self.connection.last_used_language]

        if options[0] in self.spin_keywords:
            return self.spin_wheel(self.spin_keywords[options[0]])
        elif options[0] in self.cancel_keywords:
            return self.cancel_bets(self.cancel_keywords[options[0]], user_identifier, int(options[1]))
        elif options[0] in self.board_keywords:
            return self.send_board(user_identifier)
        elif options[0] in self.time_keywords:
            return self.request_time_to_spin(self.time_keywords[0])
        elif options[0] in self.bets_keywords:
            return self.get_bets_as_formatted_string("roulette", user_identifier)
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
            elif re.search(r"", options[1]):
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

            return self.create_bet(user_identifier, selection, money)

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

    def spin_wheel(self, language: str) -> str:
        """
        Spins the roulette wheel, calculating winnings for all users

        :param language: the languag to use
        :return: the spin summary as string
        """
        result = random.randint(0, 36)
        bets = []

        for bet_file_name in os.listdir(self.roulette_directory):
            bet = {"value": int(bet_file_name.split("###BETVAL=")[1]),
                   "user": bet_file_name.split("###BETVAL=")[0],
                   "selection": []}

            file_path = os.path.join(self.roulette_directory, bet_file_name)

            with open(file_path) as bet_file:
                bet_type = bet_file.read()
                selected_tiles, multiplier = bet_type.split("X")
                selected_tiles = selected_tiles.split("-")

                bet["multiplier"] = int(multiplier)
                for tile in selected_tiles:
                    bet['selection'].append(int(tile))

            os.remove(file_path)
            bets.append(bet)

        summary = ""

        for bet in bets:
            if result in bet["selection"]:
                won_value = bet["value"] * bet["multiplier"]
                summary += bet["user"] + self.won_message[language] + self.format_money_string(won_value) + "\n\n"
                self.transfer_funds(bet["user"], won_value)

        return summary.split("\n\n")[0]

    def cancel_bets(self, language: str, user_identifier: str, index: int) -> str:
        """
        Cancels a bet

        :param language: the language to use
        :param user_identifier: the user identifier string
        :param index: the index of the bet to delete
        :return: A message detailing the success or failure of the deletion
        """
        self.connection.last_used_language = language
        return self.delete_bet("roulette", user_identifier, index)

    def send_board(self, address: str) -> None:
        """
        Sends an image of a roulette board to the user

        :param address: the address of the user
        :return:
        """








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





















        # Explanation: Since the board goes in the order 3-2-1 instead of 1-2-3, we have to reverse the order by
        # Subtracting the mod3 result from the length of the columns(=3) minus 1




        # These Combinations shift the index of the roulette board by maximum 1 tile
        if not quad:
            combinations = [[(1,0), (-1, 0), (0, 1), (0, -1)]]
        else:
            combinations = [[(1, 0), (1, 1), (0, 1)],
                            [(1, 0), (1, -1), (0, -1)],
                            [(-1, 0), (-1, -1), (0, -1)],
                            [(-1, 0), (-1, 1), (0, 1)]]

        neighbour_lists = []

        for combination in combinations:
            out_of_bounds = False
            neighbours = []

            for neigbour_config in combination:
                neigbour_column = column_index + neigbour_config[0]
                neighbour_row = row_index + neigbour_config[1]

                if neigbour_column < 0 or neighbour_row < 0:
                    out_of_bounds = True
                    break

                else:
                    neighbours.append(self.roulette_board[neighbour_row][neigbour_column])

            if not out_of_bounds:
                neighbour_lists.append(neighbours)

        return neighbour_lists





    \        def parse_user_input(self):
            """
            Parses the user's input
            :return: void
            """
            self.create_user(self.entity)
            mode = self.message.split(" ")[1]
            if mode == "time":
                self.mode = "time"
            elif mode == "bets":
                self.mode = "bets"
            elif mode == "board":
                self.mode = "board"
            elif mode == "cancel":
                self.mode = "cancel"
            elif mode == "spin":
                self.mode = "spin"
            else:
                self.mode = "newBet"
                dollars, cents = self.decode_money_string(self.message.split(" ")[1])
                if self.has_sufficient_funds(self.user_id, dollars, cents):
                    self.transfer_funds(self.user_id, -1 * dollars, -1 * cents)
                    bet = self.message.split(" ")[2]
                    if len(self.message.split(" ")) == 4:
                        bet += ":" + self.message.split(" ")[3]
                    self.store_bet("roulette", self.user_id, self.sender, dollars, cents, bet)
                else:
                    self.insufficient_funds = True

        def get_response(self):
            """
            Returns the response calculated by the plugin
            :return: the response as a MessageProtocolEntity
            """
            if self.mode == "newBet":
                if self.insufficient_funds:
                    return WrappedTextMessageProtocolEntity("Insufficient Funds", to=self.sender)
                else:
                    return WrappedTextMessageProtocolEntity("Bet Saved", to=self.sender)
            elif self.mode == "bets":
                return WrappedTextMessageProtocolEntity(self.get_bet_strings("roulette", self.user_id), to=self.sender)
            elif self.mode == "spin":
                if AddressBook().is_authenticated(self.user_id):
                    self.parallel_run(True)
                    return None
                else:
                    return WrappedTextMessageProtocolEntity("Sorry.", to=self.sender)
            elif self.mode == "board":
                roulette_image = os.getenv("HOME") + "/.whatsbot/resources/images/rouletteboard.jpg"
                self.send_image(self.sender, roulette_image, "")
                return None
            elif self.mode == "cancel":
                Popen(["rm", self.casino_dir + "roulette/" + self.user_id]).wait()
                return WrappedTextMessageProtocolEntity("Bets cancelled", to=self.sender)
            elif self.mode == "time":
                current_time = datetime.datetime.now()
                current_minute = int(current_time.minute)
                current_second = int(current_time.second)
                time_left = 120 - current_second - 5
                if current_minute % 2 == 1:
                    time_left -= 60
                return WrappedTextMessageProtocolEntity(str(time_left) + "s to turn.", to=self.sender)

        @staticmethod
        def get_description(language):
            """
            Returns a helpful description of the plugin's syntax and functionality
            :param language: the language to be returned
            :return: the description as string
            """
            if language == "en":
                return
            elif language == "de":
                return
            else:
                return "Help not available in this language"

        @staticmethod
        def get_plugin_name():
            """
            Returns the plugin name
            :return: the plugin name
            """
            return "Roulette Plugin"

        def parallel_run(self, once=False):
            """
            Starts a parallel background activity if this class has one.
            :return: void
            """
            while True:
                current_time = datetime.datetime.now()
                minutes = int(current_time.minute)
                seconds = int(current_time.second)

                if (minutes % 2 == 1 and seconds >= 55) or once:
                    recipients = []
                    betters = []
                    self.outcome = random.randint(0, 36)
                    for better in os.listdir(self.casino_dir + "roulette"):
                        win_cents = 0
                        win_dollars = 0

                        bets = self.get_bets("roulette", better)
                        Popen(["rm", self.casino_dir + "roulette/" + better]).wait()

                        user = self.get_user_nick(better)

                        for bet in bets:
                            sender = bet["sender"]
                            if sender not in recipients:
                                recipients.append(sender)

                            dollars, cents = self.evaluate_bet(bet)
                            win_cents += cents
                            while win_cents >= 100:
                                dollars += 1
                                win_cents -= 100
                            win_dollars += dollars

                        self.transfer_funds(better, win_dollars, win_cents)

                        betters.append((user, self.encode_money_string(win_dollars, win_cents, True)))

                    for sender in recipients:
                        if self.outcome in self.red:
                            colour = " (red)\n"
                        elif self.outcome in self.black:
                            colour = " (black)\n"
                        else:
                            colour = "\n"
                        winning_text = "The winning number is " + str(self.outcome) + colour
                        for better in betters:
                            winning_text += "\n" + better[0] + " won " + better[1] + "€"
                        self.send_message(WrappedTextMessageProtocolEntity(winning_text, to=sender))
                    if not once:
                        time.sleep(5)
                if once:
                    break
                time.sleep(1)

        def evaluate_bet(self, bet):
            """
            Evaluates a bet
            :param bet: the bet
            :return: the amount won by the player
            """
            bet_type = bet["bet"]
            bet_dollars, bet_cents = self.decode_money_string(bet["value"])
            try:
                intbet = int(bet_type)
                if self.outcome == intbet:
                    return self.multiply_money(35, bet_dollars, bet_cents)
                else:
                    return 0, 0
            except Exception as e:
                str(e)
                if bet_type == "red":
                    if self.outcome in self.red:
                        return self.multiply_money(2, bet_dollars, bet_cents)
                elif bet_type == "black":
                    if self.outcome in self.black:
                        return self.multiply_money(2, bet_dollars, bet_cents)
                elif bet_type == "even":
                    if self.outcome % 2 == 0:
                        return self.multiply_money(2, bet_dollars, bet_cents)
                elif bet_type == "odd":
                    if self.outcome % 2 == 1:
                        return self.multiply_money(2, bet_dollars, bet_cents)
                elif bet_type.startswith("batch"):
                    bet_string = bet_type.split("batch:")[1]
                    bet_numbers = bet_string.split("-")
                    i = 0
                    while i < len(bet_numbers):
                        bet_numbers[i] = int(bet_numbers[i])
                        i += 1
                    if self.outcome in bet_numbers:
                        if len(bet_numbers) == 2:
                            return self.multiply_money(18, bet_dollars, bet_cents)
                        if len(bet_numbers) == 4:
                            return self.multiply_money(9, bet_dollars, bet_cents)
                elif bet_type.startswith("group"):
                    group_number = int(bet_type.split("group:")[1])
                    group = []
                    i = (group_number - 1) * 4
                    while i < group_number * 4:
                        group.append(self.board[0][i])
                        group.append(self.board[1][i])
                        group.append(self.board[2][i])
                        i += 1
                    if self.outcome in group:
                        return self.multiply_money(3, bet_dollars, bet_cents)
                elif bet_type.startswith("row"):
                    row_number = int(bet_type.split("row:")[1])
                    if self.outcome in self.board[row_number - 1]:
                        return self.multiply_money(3, bet_dollars, bet_cents)
                elif bet_type.startswith("half"):
                    half_number = int(bet_type.split("half:")[1])
                    if half_number == 1:
                        if 0 < self.outcome < 19:
                            return self.multiply_money(2, bet_dollars, bet_cents)
                    else:
                        if self.outcome >= 19:
                            return self.multiply_money(2, bet_dollars, bet_cents)
            return 0, 0
