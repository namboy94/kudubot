package net.namibsun.weather_kotlin

import net.namibsun.kudubot_bindings.KudubotCommunicationHandler
import net.namibsun.kudubot_bindings.Modes
import com.github.fedy2.weather.YahooWeatherService
import com.github.fedy2.weather.data.Channel
import com.github.fedy2.weather.data.unit.DegreeUnit
import net.namibsun.kudubot_bindings.Message
import java.util.regex.Pattern


/**
 * The main method that starts the execution of the program
 *
 * @param args The command line arguments passed to this program
 */
fun main(args: Array<String>) {


    val communicator = KudubotCommunicationHandler(args)

    when (communicator.mode) {
        Modes.IS_APPLICABLE_TO -> communicator.setApplicable(isApplicable(communicator.incomingMessage))
        Modes.HANDLE_MESSAGE -> handleMessage(communicator)
    }
}

/**
 * Replaces any non-English keywords in a message, converts the message
 * to lower-case and strips away any leading or trailing whitespace
 */
fun prepareMessage(message: Message): String {
    var text = message.messageBody.toLowerCase()

    // Replace non-english keywords
    text = text.replace("/wetter", "/weather")
    text = text.replace("morgen", "tomorrow")

    return text
}

/**
 * Checks if the Service is applicable to the message using regular expressions
 * @param message The message to analyze
 * @return true if the message is applicable, false otherwise
 */
fun isApplicable(message: Message): Boolean {

    val text = prepareMessage(message)
    val pattern = Pattern.compile("/weather [a-z]+(( )*,( )*[a-z]+){0,2}(( )+tomorrow)?")
    val matcher = pattern.matcher(text)
    return matcher.matches()

}

/**
 * Handles an applicable message
 */
fun handleMessage(communicator: KudubotCommunicationHandler) {

    val text = prepareMessage(communicator.incomingMessage).split("/weather ")[1]

    val tomorrow = text.endsWith("tomorrow")
    val locationInfo = text.split(" tomorrow")[0].split(",")




    val weather = YahooWeatherService()

    println(locationInfo)

    val results = weather.getForecastForLocation(locationInfo[0], DegreeUnit.CELSIUS).all()

    for (x in results) {
        println(x.title)
        println(x.item.condition)
    }

}