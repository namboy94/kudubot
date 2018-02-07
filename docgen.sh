#!/bin/bash
# Copyright 2015-2017 Hermann Krumrey
#
# This file is part of kudubot.
#
# kudubot is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# kudubot is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with kudubot.  If not, see <http://www.gnu.org/licenses/>.

cd doc
make buildsource
make latexpdf
make html
cd ..

mv doc/build/latex/kudubot.pdf documentation.pdf
mv doc/build/html documentation
