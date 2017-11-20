"""
Copyright 2015-2017 Hermann Krumrey

This file is part of kudubot.

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
"""

import os
import sys
from kudubot.config.builder import build_external
from kudubot.config.GlobalConfigHandler import GlobalConfigHandler


if __name__ == "__main__":

    if len(sys.argv) < 2:
        build_external(
            GlobalConfigHandler().external_services_executables_directory)
    else:

        target_dir = sys.argv[1]

        if not os.path.isdir(target_dir):
            os.makedirs(target_dir)

        build_external(target_dir)
