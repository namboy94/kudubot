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
use kudubot_bindings::{load_message, write_is_applicable_response};
use kudubot_bindings::structs::Message;
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
        println!("A");
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

/*
/// Handles an incoming message. Responds with "Hi" to the original sender
///
/// # Arguments
///
/// * `message` - The original message received via kudubot as a serde_json::Value object
/// * `message_file_path` - The path to the message file to write the response to
/// * `response_file_path` - The path to the response file used to communicate with kudubot
//fn handle_message(message: Message, message_file_path: &str, response_file_path: &str) {

    //let return_message: Value = message.to_json();

    /*
    let response_json = json!({
        "mode": "xreply"
    });

    //write_json_to_file(return_message, message_file_path);
    write_json_to_file(response_json, response_file_path);
    */

//}


/// Checks if a message is applicable to the Hello Rust Service
/// The result of this query is then written to a JSON file which can then be
/// read by kudubot
///
/// # Arguments
///
/// * `message` - The parsed JSON file object which models the message received
/// * `response_file_path` - The path to the response JSON file to write to
//fn handle_message_applicable(message: Message, response_file_path: &str) {

    /*
    let applicable: bool = message.message_body == "hello rust!";

    let json_response = json!({
        "mode": "is_applicable",
        "applicable": applicable
    });

    write_json_to_file(json_response, response_file_path);
    */
//}
*/