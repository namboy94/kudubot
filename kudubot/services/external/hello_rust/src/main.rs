/*
LICENSE:
Copyright 2015-2017 Hermann Krumrey

This file is part of kudubot.

    kudubot is a chat bot framework. It allows developers to write
    services for arbitrary chat services.

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
*/

extern crate rustc_serialize;

use std::env;

/// The main method of the Service
fn main() {

    let args: Vec<_> = env::args().collect();

    let mode = &args[1];
    let message_file = &args[2];
    let response_file = &args[3];
    let database_file = &args[4];

    if mode == "handle_message" {
        println!("Hello World!");
        handle_message(message_file, response_file, database_file);
    }
    else if mode == "is_applicable_to" {
        println!("Hallo Welt!")
    }

    //println!("{} {} {} {}", mode, message_file, response_file, database_file)

}


fn handle_message(message_file: &str, response_file: &str, database_file: &str) {

    println!("{} {} {}", message_file, response_file, database_file)

}