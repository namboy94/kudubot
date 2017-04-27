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

use serde_json::Value;

use std::fs::File;
use std::io::{Read, Write};
use std::env;
use serde_json::Value::Null;

#[derive(Serialize, Deserialize)]
pub struct Message {
    pub message_title: String,
    pub message_body: String,
    pub receiver: Contact,
    pub sender: Contact,
    pub sender_group: Option<Contact>,
    pub timestamp: f64
}

#[derive(Serialize, Deserialize)]
pub struct Contact {
    pub database_id: i64,
    pub display_name: String,
    pub address: String
}


pub fn read_message_from_file(message_file_path: &str) -> Message {

    return serde_json::from_str(read_json_file_to_string(message_file_path)).unwrap();

    /*
    let json = read_json_file(message_file_path);

    return Message {
        message_title: json_to_string(json.get("message_title").unwrap()),
        message_body: json_to_string(json.get("message_body").unwrap()),
        receiver: load_contact_from_json_data(json.get("receiver").unwrap()).unwrap(),
        sender: load_contact_from_json_data(json.get("sender").unwrap()).unwrap(),
        sender_group: load_contact_from_json_data(json.get("sender_group").unwrap()),
        timestamp: json.get("timestamp").unwrap().as_f64().unwrap()
    };
    */

}

fn json_to_string(json_string: &Value) -> String {
    return String::from(json_string.as_str().unwrap());
}

pub fn load_contact_from_json_data(json_data: &Value) -> Option<Contact> {

    if !json_data.is_null() {
        return Some(Contact {
            database_id: json_data.get("database_id").unwrap().as_i64().unwrap(),
            display_name: json_data.get("display_name").unwrap().to_string(),
            address: json_data.get("address").unwrap().to_string()
        });
    }
    else {
        return None;
    }


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
pub fn read_json_file(json_file_path: &str) -> Value {

    // Read message file content
    let mut json_file: File = File::open(json_file_path).unwrap();
    let mut json_data: String = String::new();
    json_file.read_to_string(&mut json_data).unwrap();

    let json: Value = serde_json::from_str(json_data.as_str()).unwrap();

    return json;

}

fn read_json_file_to_string(json_file_path: &str) -> &str {
    // Read message file content
    let mut json_file: File = File::open(json_file_path).unwrap();
    let mut json_data: String = String::new();
    json_file.read_to_string(&mut json_data).unwrap();
    let data = Strin::from(json_data.as_str());
    return data.as_str();
}

/// Writes a serde_json:Value object to a file.
///
/// # Arguments
///
/// * `json_data` - The JSON Data to write into the file
/// * `json_file_location` - The destination file to write to
pub fn write_json_to_file(json_data: Value, json_file_location: &str) {

    let mut json_file: File = File::create(json_file_location).unwrap();
    json_file.write_all(json_data.to_string().as_bytes()).unwrap();

}