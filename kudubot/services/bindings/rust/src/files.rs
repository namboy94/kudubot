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

use serde_json::Value;
use std::fs::File;
use std::io::{Read, Write};


/// Reads a file and returns the file's content as a String.
///
/// # Arguments
///
/// * `file_path` - The path to the file
///
/// # Return value
///
/// Returns the file's content
pub fn read_from_file(file_path: &str) -> String {

    let mut file: File = File::open(file_path).unwrap();
    let mut data: String = String::new();
    file.read_to_string(&mut data).unwrap();
    return data;

}


/// Writes a string to a file
///
/// # Arguments
///
/// * `file_path` - The path to the file
/// * `content` - The String to write to the file
pub fn write_to_file(file_path: &str, content: &str) {

    let mut file: File = File::create(file_path).unwrap();
    file.write_all(content.as_bytes()).unwrap();

}

/// Directly writes a JSON Value struct to a file.
///
/// # Arguments
///
/// * `file_path` - The path to the file
/// * `content` - The JSON Value struct to write into the file
pub fn write_json_to_file(file_path: &str, content: Value) {

    let mut json_file: File = File::create(file_path).unwrap();
    json_file.write_all(content.to_string().as_bytes()).unwrap();

}