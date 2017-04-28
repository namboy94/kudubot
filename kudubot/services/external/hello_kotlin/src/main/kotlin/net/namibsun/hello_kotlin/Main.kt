package net.namibsun.hello_kotlin

import net.namibsun.kudubot_bindings.Message
import net.namibsun.kudubot_bindings.messageFromFile

fun main(args: Array<String>) {

    val mode = args[0]
    val message_path = args[1]
    val response_path = args[2]
    val database_path = args[3]

    val message: Message = messageFromFile(message_path)
    println(message.messageBody)

}