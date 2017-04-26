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

#[macro_use]
extern crate serde_json;

use serde_json::Value;

use std::fs::File;
use std::io::{Read, Write};
use std::env;


/// The main method of the Service
fn main() {

    // Fetch the command line arguments
    let args: Vec<_> = env::args().collect();
    let mode: &str = &args[1];
    let message_file: &str = &args[2];
    let response_file: &str = &args[3];

    let message: Value = read_json_file(message_file);

    if mode == "handle_message" {
        handle_message(message, message_file, response_file);
    }

    else if mode == "is_applicable_to" {
        handle_message_applicable(message, response_file)
    }
}


/// Handles an incoming message. Responds with "Hi" to the original sender
///
/// # Arguments
///
/// * `message` - The original message received via kudubot as a serde_json::Value object
/// * `message_file_path` - The path to the message file to write the response to
/// * `response_file_path` - The path to the response file used to communicate with kudubot
fn handle_message(message: Value, message_file_path: &str, response_file_path: &str) {

    let return_message = json!({
        "message_title": "Hello Rust",
        "message_body": "Hi!",
        "sender": message["receiver"],
        "sender_group": null,
        "receiver": message["sender"],
        "timestamp": message["timestamp"]
    });

    let response_json = json!({
        "mode": "reply"
    });

    write_json_to_file(return_message, message_file_path);
    write_json_to_file(response_json, response_file_path);

}


/// Checks if a message is applicable to the Hello Rust Service
/// The result of this query is then written to a JSON file which can then be
/// read by kudubot
///
/// # Arguments
///
/// * `message` - The parsed JSON file object which models the message received
/// * `response_file_path` - The path to the response JSON file to write to
fn handle_message_applicable(message: Value, response_file_path: &str) {

    let body: String = message["message_body"].as_str().unwrap().to_lowercase();
    let applicable: bool = body == "hello rust!";

    let json_response = json!({
        "mode": "is_applicable",
        "applicable": applicable
    });

    write_json_to_file(json_response, response_file_path);

}

/// Reads a JSON file and generate a serde_json::Value object from it.
///
/// # Arguments
///
/// * `json_file_path` - The path to the JSON file to read
///
/// # Return value
///
/// Returns the parsed serde_json::Value object
fn read_json_file(json_file_path: &str) -> Value {

    // Read message file content
    let mut json_file: File = File::open(json_file_path).unwrap();
    let mut json_data: String = String::new();
    json_file.read_to_string(&mut json_data).unwrap();

    let json: Value = serde_json::from_str(json_data.as_str()).unwrap();

    return json;

}

/// Writes a serde_json:Value object to a file.
///
/// # Arguments
///
/// * `json_data` - The JSON Data to write into the file
/// * `json_file_location` - The destination file to write to
fn write_json_to_file(json_data: Value, json_file_location: &str) {

    let mut json_file: File = File::create(json_file_location).unwrap();
    json_file.write_all(json_data.to_string().as_bytes()).unwrap();

}
