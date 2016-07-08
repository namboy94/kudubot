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
import re

from kudubot.servicehandlers.Service import Service
from kudubot.connection.generic.Message import Message


class AsciiArtService(Service):
    """
    The AsciiArtService Class that extends the generic Service class.
    It sends an ASCII Art image.
    """

    identifier = "ascii_art"
    """
    The identifier for this service
    """

    help_description = {"en": "/ascii\tSends an image of a specified ASCII art\n"
                              "syntax:\n"
                              "/ascii list (Lists all available images)"
                              "/ascii <image>",
                        "de": "/ascii\tSchickt ein Bild mit ASCII Kunst\n"
                              "syntax:\n"
                              "/ascii liste (Listet alle verfügbaren bilder auf)"
                              "/ascii linux ascii art<bild>"}
    """
    Help description for this service.
    """

    art = {"tux": "         a8888b.\n"
                  "        d888888b.\n"
                  "        8P\"YP\"Y88\n"
                  "        8|o||o|88\n"
                  "        8'    .88\n"
                  "        8`._.' Y8.\n"
                  "       d/      `8b.\n"
                  "     .dP   .     Y8b.\n"
                  "    d8:'   \"   `::88b.\n"
                  "   d8\"           `Y88b\n"
                  "  :8P     '       :888\n"
                  "   8a.    :      _a88P\n"
                  " ._/\"Yaa_ :    .| 88P|\n"
                  " \    YP\"      `| 8P  `.\n"
                  " /     \._____.d|    .'\n"
                  " `--..__)888888P`._.'\n",
           "bigtux": "                         ooMMMMMMMooo\n"
                     "                       oMMMMMMMMMMMMMMMoo\n"
                     "                      MMMMMMMMMMMMMMo\"MMMo\n"
                     "                     \"MMMMMMMMMMMMMMMMMMMMM\n"
                     "                     MMMMMMMMMMMMMMMMMMMMMMo\n"
                     "                     MMMM\"\"MMMMMM\"o\" MMMMMMM\n"
                     "                     MMo o\" MMM\"  oo \"\"MMMMM\n"
                     "                     MM MMo MMM\" MMoM \"MMMMM\n"
                     "                     MMo\"M\"o\" \"\" MMM\" oMMMMM\"\n"
                     "                     oMM M  o\" \" o \"o MMMMMM\"\n"
                     "                     oM\"o \" o \"  o \"o MMMMMMM\n"
                     "                     oMMoM o \" M M \"o MMMM\"MMo\n"
                     "                      Mo \" M \"M \"o\" o  MMMoMMMo\n"
                     "                     MMo \" \"\" M \"       MMMMMMMo\n"
                     "                   oMM\"   \"o o \"         MMMMMMMM\n"
                     "                  MMM\"                    MMMMMMMMo\n"
                     "                oMMMo                     \"MMMMMMMMo\n"
                     "               MMMMM o             \"  \" o\" \"MMMMMMMMMo\n"
                     "              MMMMM          \"            \" \"MMMMMMMMMo\n"
                     "             oMMMM                          \"\"MMMMMMMMMo\n"
                     "            oMMMM         o         o         MMoMMMMMMM\n"
                     "            MMMM               o              \"MMMMMMMMMM\n"
                     "           MMMM\"     o    o             o     \"MMMMMMMMMMo\n"
                     "         oMMMMM                                MMMMMMMMMMo\n"
                     "         MMM\"MM                               \"MMM\"MMMMMMM\n"
                     "         MMMMMM           \"      o   \"         MMMMMMMMMMM\n"
                     "         \"o  \"ooo    o                     o o\"MMMMMMMMoM\"\n"
                     "        \" o \"o \"MMo       \"                o\"  MMMMMMMM\"\n"
                     "    o \"o\" o o \"  MMMo                     o o\"\"\"\"MMMM\"o\" \"\n"
                     " \" o \"o \" o o\" \"  MMMMoo         \"       o \"o M\"\" M \"o \" \"\n"
                     " \"o o\"  \" o o\" \" \" \"MMMM\"   o              M o \"o\" o\" o\" \" o\n"
                     " M  o M \"  o \" \" \" \" MM\"\"           o    oMo\"o \" o o \"o \" \"o \"\n"
                     " o\"  o \" \"o \" \" M \" \" o                MMMMo\"o \" o o o o\" o o\" \"\n"
                     " o\" \"o \" o \" \" o o\" M \"oo         ooMMMMMMM o \"o o o \" o o o \"\n"
                     " M \"o o\" o\" \"o o o \" o\"oMMMMMMMMMMMMMMMMMMMo\" o o \"o \"o o\"\n"
                     "  \"\" \"o\"o\"o\"o o\"o \"o\"o\"oMMMMMMMMMMMMMMMMMMo\"o\"o \"o o\"oo\"\n"
                     "        \"\" M Mo\"o\"oo\"oM\"\" \"               MMoM M M M\n"
                     "               \"\"\" \"\"\"                      \" \"\"\" \"\n",
           "elephant": "              ___.-~\"~-._   __....__\n"
                       "            .'    `    \\ ~\"~        ``-.\n"
                       "           /` _      )  `\\              `\\\n"
                       "          /`  a)    /     |               `\\\n"
                       "         :`        /      |                 \\\n"
                       "    <`-._|`  .-.  (      /   .            `;\\\\\n"
                       "     `-. `--'_.'-.;\\___/'   .      .       | \\\\\n"
                       "  _     /:--`     |        /     /        .'  \\\\\n"
                       " (\"\\   /`/        |       '     '         /    :`;\n"
                       " `\\'\\_/`/         .\\     /`~`=-.:        /     ``\n"
                       "   `._.'          /`\\    |      `\\      /(\n"
                       "                 /  /\\   |        `Y   /  \\\n"
                       "                J  /  Y  |         |  /`\\  \\\n"
                       "               /  |   |  |         |  |  |  |\n"
                       "              \"---\"  /___|        /___|  /__|\n"
                       "                     '\"\"\"         '\"\"\"  '\"\"\"\n",
           "snake_flute": "      ,'._,`.\n"
                          "     (-.___.-)\n"
                          "     (-.___.-)\n"
                          "     `-.___.-'                  \n"
                          "      ((  @ @|              .            __\n"
                          "       \\   ` |         ,\\   |`.    @|   |  |      _.-._\n"
                          "      __`.`=-=mm===mm:: |   | |`.   |   |  |    ,'=` '=`.\n"
                          "     (    `-'|:/  /:/  `/  @| | |   |, @| @|   /---)W(---\\\n"
                          "      \\ \\   / /  / /         @| |   '         (----| |----) ,~\n"
                          "      |\\ \\ / /| / /            @|              \\---| |---/  |\n"
                          "      | \\ V /||/ /                              `.-| |-,'   |\n"
                          "      |  `-' |V /                                 \\| |/    @'\n"
                          "      |    , |-'                                 __| |__\n"
                          "      |    .;: _,-.                         ,--\"\"..| |..\"\"--.\n"
                          "      ;;:::' \"    )                        (`--::__|_|__::--')\n"
                          "    ,-\"      _,  /                          \\`--...___...--'/   \n"
                          "   (    -:--'/  /                           /`--...___...--'\\\n"
                          "    \"-._  `\"'._/                           /`---...___...---'\\\n"
                          "        \"-._   \"---.                      (`---....___....---')\n"
                          "         .' \",._ ,' )                     |`---....___....---'|\n"
                          "         /`._|  `|  |                     (`---....___....---') \n"
                          "        (   \\    |  /                      \\`---...___...---'/\n"
                          "         `.  `,  ^\"\"                        `:--...___...--;'\n"
                          "           `.,'                               `-._______.-'\n"
           }

    def process_message(self, message: Message) -> None:
        """
        Process a message according to the service's functionality

        :param message: the message to process
        :return: None
        """
        image_to_show = message.message_body.lower().split(" ", 1)[1]
        if image_to_show.startswith("list"):
            reply = self.list_images()
        else:
            reply = self.art[image_to_show]

        reply_message = self.generate_reply_message(message, "ASCII Art", reply)

        if self.connection.identifier in ["whatsapp", "telegram"] and not image_to_show.startswith("list"):
            self.send_text_as_image_message(reply_message)
        else:
            self.send_text_message(reply_message)

    @staticmethod
    def regex_check(message: Message) -> bool:
        """
        Checks if the user input is valid for this service to continue

        :return: True if input is valid, False otherwise
        """
        regex = "^/ascii (list(e)?|" \
                + Service.regex_string_from_dictionary_keys([AsciiArtService.art]) + ")$"
        regex = regex.replace("+", "\+")
        return re.search(re.compile(regex), message.message_body.lower())

    def list_images(self) -> str:
        """
        Creates a list of implemented images

        :return: the list of implemented images
        """
        list_string = ""
        for image in self.art:
            list_string += image + "\n"
        return list_string.rstrip("\n")
