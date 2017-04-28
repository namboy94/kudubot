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
import com.google.gson.JsonElement
import com.google.gson.JsonObject

/**
 * This class models a Contact in the Message JSON file.
 *
 * @param databaseId The ID of the contact in the local SQLite databse
 * @param displayName The name of the contact
 * @param address The contact's address
 */
data class Contact(val databaseId: Int, val displayName: String, val address: String) {

    /**
     * Converts the Contact object into a JsonObject
     *
     * @return The generated JsonObject
     */
    fun toJson(): JsonObject {
        return jsonObject(
                "database_id" to this.databaseId,
                "display_name" to this.displayName,
                "address" to this.address
        )
    }

}

/**
 * Creates a new Contact object from a JsonElement object.
 * @param json The JsonElement object to turn into a Contact
 * @return The generated Contact object
 */
fun contactFromJson(json: JsonElement): Contact {
    return Contact(
            json["database_id"].asInt,
            json["display_name"].asString,
            json["address"].asString
    )
}