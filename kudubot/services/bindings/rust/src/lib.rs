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

mod files;
mod structs;

use structs::Message;


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
fn generate_reply(message: Message, title: &str, body: &str) -> Message {

    // Check if we need to reply to a group or not
    let receiver = match message.sender_group {
        None => message.sender,
        Some(x) => x
    };

    return Message {
        message_title: String::from(title),
        message_body: String::from(body),
        receiver: receiver,
        sender: message.receiver,
        sender_group: None,
        timestamp: message.timestamp,
    }
}

