package net.namibsun.kudubot_bindings

import com.github.salomonbrys.kotson.get
import com.google.gson.JsonElement
import com.google.gson.JsonParser
import java.io.File

data class Message(
        val messageTitle: String,
        val messageBody: String,
        val receiver: Contact,
        val sender: Contact,
        val senderGroup: Contact?,
        val timestamp: Float) {

    fun storeInFile(file: String) {

    }

    fun generateReply(title: String, body: String): Message {
        return Message(title, body, this.sender, this.receiver, null, this.timestamp)
    }
}

data class Contact(val databaseId: Int, val displayName: String, val address: String)

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

fun contactFromJson(json: JsonElement): Contact {
    return Contact(
            json["database_id"].asInt,
            json["display_name"].asString,
            json["address"].asString
    )
}