package net.namibsun.kudubot_bindings

import com.github.salomonbrys.kotson.jsonObject
import com.sun.org.apache.xpath.internal.operations.Bool
import java.io.File

/**
 * This is a class which offers an abstraction over the Kudubot communication.
 *
 * @param args The command line arguments which should be provided by the Main method
 */
class KudubotCommunicationHandler(args: Array<String>) {

    /**
     * The mode that Kudubot has requested
     */
    val mode = Modes.valueOf(args[0].toUpperCase())

    /**
     * The path to the original message file
     */
    val messageFilePath = args[1]

    /**
     * The path to the response file used to communicate with Kudubot
     */
    val responseFilePath = args[2]

    /**
     * The path to the SQlite database used by Kudubot
     */
    val sqliteFilePath = args[3]

    /**
     * The incoming message information
     */
    val incomingMessage = messageFromFile(messageFilePath)

    /**
     * Replies to the message with a nes title and body.
     * Afterwards, the program always exits
     *
     * @param title The title of the reply message
     * @param body The body of the reply message
     */
    fun reply(title: String, body: String) {
        val replyMessage = this.incomingMessage.generateReply(title, body)
        respondToMessageHandling(replyMessage)
        System.exit(0)
    }

    /**
     * Ends the program after letting Kudubot know that no reply will be sent
     */
    fun dontReply() {
        respondToMessageHandling(null)
        System.exit(0)
    }

    /**
     * Writes the result of the applicability check to the response file and quits
     * the program.
     *
     * @param isApplicable Indicates if the message is applicable to this service or not.
     */
    fun setApplicable(isApplicable: Bool) {
        val json = jsonObject("is_applicable" to isApplicable).toString()
        File(this.responseFilePath).writeText(json)
        System.exit(0)
    }

    /**
     * Handles saving a message back into the message file and notifying Kudubot
     *
     * @param message The message to send. Can be null, in which case only 'noreply'
     *                will be written to the response file instead of 'reply'.
     */
    private fun respondToMessageHandling(message: Message?) {

        val json = jsonObject("mode" to (if (message == null) "noreply" else "reply"))
        File(this.responseFilePath).writeText(json.toString())
        message?.writeToFile(this.messageFilePath)

    }

}
