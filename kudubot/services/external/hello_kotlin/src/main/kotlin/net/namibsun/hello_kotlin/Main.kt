package net.namibsun.hello_kotlin

import net.namibsun.kudubot_bindings.KudubotCommunicationHandler
import net.namibsun.kudubot_bindings.Modes


/**
 * The main method that starts the execution of the program
 *
 * @param args The command line arguments passed to this program
 */
fun main(args: Array<String>) {

    val communicator = KudubotCommunicationHandler(args)

    when (communicator.mode) {

        Modes.IS_APPLICABLE_TO -> communicator.setApplicable(
                communicator.incomingMessage.messageBody.toLowerCase() == "hello kotlin!")
        Modes.HANDLE_MESSAGE -> communicator.reply("Hello Kotlin", "Hi!")
    }

}