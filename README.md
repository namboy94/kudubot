# Whatsapp Bot

This is a bot built on the [Yowsup2](https://github.com/tgalal/yowsup) framework.

It allows responding to Whatsapp messages with useful, useless but funny and other replies.

The structure of the bot is designed to support easy addition of plugins. To add a new plugin, only 2-3 lines have to be
changed in the PluginManager class.

Current plugins are:

* Football Scores Plugin
* Image Sender Plugin
* Kicktipp Plugin
* KinoZKM Plugin
* KVV Plugin (parasitic)
* Mensa Plugin
* TheTVDB Plugin
* Weather Plugin
* XKCD Plugin (parasitic)
* Casino Plugin
    * Roulette Plugin
* Continuous Reminder Plugin
* Reminder Plugin
* Terminal Plugin
* Text to Speech Plugin
* Muter Plugin
* Simple "Contains" Responder Plugin
* Simple "Equals" Responder Plugin

Plugins marked with (parasitic) make use of Johannes Bucher's whatsapp bot. They won't work outside of a Whatsapp group
where an instance of his bot is registered.