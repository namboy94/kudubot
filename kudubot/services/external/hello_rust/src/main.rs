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
extern crate kudubot_bindings;

use serde_json::Value;
use kudubot_bindings::{write_json_to_file,
                       read_json_file,
                       Contact,
                       Message,
                       load_contact_from_json_data,
                       read_message_from_file};

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

    /**
    for i in ["message_title", "message_body", "receiver", "sender", "sender_group", "timestamp"].iter() {
        println!("{}", message.get(i).unwrap());
    }
    println!("{}", message.get("timestamp").unwrap().as_f64().unwrap());
    println!("OK");

    for i in ["receiver", "sender", "sender_group"].iter() {
        println!("{}", message.get(i).unwrap());
        for j in ["database_id", "display_name", "address"].iter() {
            println!("{}", message.get(i).unwrap().get(j).unwrap());
        }
    }

    **/

    let message_object: Message = read_message_from_file(message_file);
    //println!("{}", message.message_body);


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
