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

use serde_json;
use files::write_to_file;

/// The Message struct models a Message as defined by the kudubot
/// framework for easy use in rust.
///
/// # Arguments
///
/// * `message_title` - The title of the message
/// * `message_body` - The body of the message
/// * `receiver` - The recipient of the message
/// * `sender` - The sender of the message
/// * `sender_group` - The sender group of the message. May be None.
/// * `timestamp` - The timestamp of the message
#[derive(Serialize, Deserialize)]
pub struct Message {
    pub message_title: String,
    pub message_body: String,
    pub receiver: Contact,
    pub sender: Contact,
    pub sender_group: Option<Contact>,
    pub timestamp: f64
}

/// Implementation of methods for the Message struct
impl Message{

    /// Turns the Message into a String
    ///
    /// # Return value
    ///
    /// The Message in String representation
    pub fn to_string(&self) -> String {
        return serde_json::to_string(&self).unwrap();
    }

    /// Writes the Message to a file
    ///
    /// # Arguments
    ///
    /// * `destination` - The destination file path to which will be written
    pub fn write_to(&self, destination: &str) {
        let data = self.to_string();
        write_to_file(destination, data.as_str())
    }

}

/// The Contact struct models a contact inside a Message struct
///
/// # Argument
///
/// * `database_id` - The contact's ID in the database
/// * `display_name` - The contact's human-readable name
/// * `address` - The contact's address on the connection
#[derive(Serialize, Deserialize, Clone, Debug)]
pub struct Contact {
    pub database_id: i64,
    pub display_name: String,
    pub address: String
}
