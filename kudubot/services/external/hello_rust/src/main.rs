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

extern crate kudubot_bindings;
use kudubot_bindings::structs::Message;
use kudubot_bindings::{load_message,
                       write_is_applicable_response,
                       generate_reply,
                       write_reply_response};
use std::env;

/// The main method of the Service. Fetches the Command line arguments,
/// loads the message from the JSON file and handles the message accordingly.
fn main() {

    let args: Vec<_> = env::args().collect();
    let mode: &str = &args[1];
    let message_file: &str = &args[2];
    let response_file: &str = &args[3];

    let message: Message = load_message(message_file);

    if mode == "handle_message" {
        handle_message(message, message_file, response_file);
    }
    else if mode == "is_applicable_to" {
        is_applicable_to(message, response_file);
    }
}

/// Checks if the message is applicable to this service and writes the
/// result of that analysis to the response JSON file.
///
/// # Arguments
///
/// * `message` - The message to analyze
/// * `response_file` - The file into which the response should be written
fn is_applicable_to(message: Message, response_file: &str) {

    let applicable: bool = message.message_body.to_lowercase() == "hello rust!";
    write_is_applicable_response(response_file, applicable);

}

/// Handles a message. Replies to the sender with 'Hi!'
///
/// # Arguments
///
/// * `message` - The incoming message
/// * `message_file` - The file in which the message was originally stored in and which
///                    will be the destination of the reply message
/// * `response_file` - The file to which to write the response to,
///                     so that kudubot knows how to proceed
fn handle_message(message: Message, message_file: &str, response_file: &str) {

    let reply: Message = generate_reply(message, "Hello Rust", "Hi!");
    reply.write_to(message_file);
    write_reply_response(response_file);

}
