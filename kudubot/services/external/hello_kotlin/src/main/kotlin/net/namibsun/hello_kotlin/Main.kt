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

    /**
     * Syntax:
     *
     * /weather city
     * /weather city, country, region
     *
     * /wetter *
     *
     *
     */


    val communicator = KudubotCommunicationHandler(args)

    when (communicator.mode) {

        Modes.IS_APPLICABLE_TO -> communicator.setApplicable(isApplicable()
                communicator.incomingMessage.messageBody.toLowerCase() == "hello kotlin!")
        Modes.HANDLE_MESSAGE -> communicator.reply("Hello Kotlin", "Hi!")
    }

    val weather = YahooWeatherService()
    val results = weather.getForecastForLocation("Cape Town", DegreeUnit.CELSIUS).all()

    for (x in results) {

        println(x.title)
        println(x.item.condition)
    }
}