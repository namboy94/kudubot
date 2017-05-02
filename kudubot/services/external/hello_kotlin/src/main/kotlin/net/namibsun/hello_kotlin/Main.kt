package net.namibsun.hello_kotlin

import net.namibsun.kudubot_bindings.KudubotCommunicationHandler
import net.namibsun.kudubot_bindings.Modes
import com.github.fedy2.weather.YahooWeatherService
import com.github.fedy2.weather.data.Channel
import com.github.fedy2.weather.data.unit.DegreeUnit


/**
 * The main method that starts the execution of the program
 *
 * @param args The command line arguments passed to this program
 */
fun main(args: Array<String>) {

    /*
    val communicator = KudubotCommunicationHandler(args)

    when (communicator.mode) {

        Modes.IS_APPLICABLE_TO -> communicator.setApplicable(
                communicator.incomingMessage.messageBody.toLowerCase() == "hello kotlin!")
        Modes.HANDLE_MESSAGE -> communicator.reply("Hello Kotlin", "Hi!")
    }
    */

    val weather = YahooWeatherService()
    val results = weather.getForecastForLocation("Windhoek", DegreeUnit.CELSIUS).all()

    println(results[0].image)
    println(results[0].units)
    println(results[0].astronomy)
    println(results[0].ttl)
    println(results[0].wind)
    println(results[0].item.condition)
}