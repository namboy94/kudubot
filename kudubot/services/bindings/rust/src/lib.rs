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

extern crate serde;
#[macro_use]
extern crate serde_json;
#[macro_use]
extern crate serde_derive;

pub mod files;
pub mod structs;

use files::{read_from_file, write_json_to_file};
use structs::Message;


/// Loads a Message struct from a .json file
///
/// # Arguments
///
/// * `source` - The path to the source .json file
///
/// # Return value
///
/// Returns the generated Message struct
pub fn load_message(source: &str) -> Message {
    let data = read_from_file(source);
    return serde_json::from_str(data.as_str()).unwrap()
}


/// Generates a reply Message struct for a given Message.
/// For this, the receiver and sender are flipped and the body as well as
/// the title are replaced.
///
/// # Arguments
///
/// * `message` - The Message to reply to
/// * `title` - The message title to send
/// * `body` - The message body to send
///
/// # Return value
///
/// Returns the generated reply message
pub fn generate_reply(message: &Message, title: &str, body: &str) -> Message {

    // Check if we need to reply to a group or not
    let receiver = match message.sender_group.clone() {
        None => message.sender.clone(),
        Some(x) => x
    };

    return Message {
        message_title: String::from(title),
        message_body: String::from(body),
        receiver: receiver.clone(),
        sender: message.receiver.clone(),
        sender_group: None,
        timestamp: message.timestamp,
    }
}


/// Writes a response to the is_applicable_to query by kudubot.
///
/// # Arguments
///
/// * `response_file` - The file to which to write to
/// * `value` - The value to write into the response
pub fn write_is_applicable_response(response_file: &str, value: bool) {
    write_json_to_file(response_file, json!({ "is_applicable": value }))
}

/// Writes a reply response for the handle_message query by kudubot.
///
/// # Arguments
///
/// * `response_file` - The file to which to write to
pub fn write_reply_response(response_file: &str) {
    write_json_to_file(response_file, json!({ "mode": "reply" }))
}
