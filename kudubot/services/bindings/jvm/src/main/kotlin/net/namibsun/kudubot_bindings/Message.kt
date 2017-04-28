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

package net.namibsun.kudubot_bindings

import com.github.salomonbrys.kotson.get
import com.github.salomonbrys.kotson.jsonObject
import com.google.gson.JsonObject
import com.google.gson.JsonParser
import java.io.File

/**
 * This class models a Message object sent by Kudubot.
 *
 * @param messageTitle: The title of the message
 * @param messageBody: The content of the message
 * @param receiver: The receiving [Contact]
 * @param sender: The sending [Contact]
 * @param senderGroup: The sending group [Contact], which may or may not be null
 * @param timestamp: The message's timestamp
 */
data class Message(
        val messageTitle: String,
        val messageBody: String,
        val receiver: Contact,
        val sender: Contact,
        val senderGroup: Contact?,
        val timestamp: Float) {

    /**
     * Serializes the Message object into a JsonObject
     *
     * @return The generated JsonObject
     */
    fun toJson(): JsonObject {

        return jsonObject(
                "message_title" to this.messageTitle,
                "message_body" to this.messageBody,
                "receiver" to this.receiver.toJson(),
                "sender" to this.sender.toJson(),
                "sender_group" to this.senderGroup?.toJson(),
                "timestamp" to this.timestamp
        )
    }

    /**
     * Writes the Message to a JSON file.
     *
     * @param filePath The path to the file to write to
     */
    fun writeToFile(filePath: String) {
        val json = this.toJson()
        File(filePath).writeText(json.toString())
    }

    /**
     * Generates a new Message object with the sender and receiver reversed, as well
     * as a new message title and body
     */
    fun generateReply(title: String, body: String): Message {
        return Message(title, body, this.sender, this.receiver, null, this.timestamp)
    }
}

/**
 * Generates a new Message object from the data stored in a JSON file
 *
 * @param filePath The path to the JSON file
 * @return The generated Message object
 */
fun messageFromFile(filePath: String) : Message {

    val jsonText = File(filePath).readText()
    val parser = JsonParser()
    val parsed = parser.parse(jsonText)

    val senderGroup: Contact? = if (parsed["sender_group"].isJsonNull) {
        null
    } else {
        contactFromJson(parsed["sender_group"])
    }

    return Message(
            parsed["message_title"].asString,
            parsed["message_body"].asString,
            contactFromJson(parsed["receiver"]),
            contactFromJson(parsed["sender"]),
            senderGroup,
            parsed["timestamp"].asFloat
            )
}
