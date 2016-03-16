# Whatsbot

This is a bot built on the [Yowsup2](https://github.com/tgalal/yowsup) framework.

It allows responding to Whatsapp messages with useful or useless but fun replies.

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

Plugins marked with (parasitic) make use of [redacted]'s whatsapp bot. They won't work outside of a Whatsapp group
where an instance of his bot is registered.

Registering a number can be either accomplished via using yowsup-cli (consult the project's Github page for 
further information) or via using a rooted Android smartphone. It is currently planned to implement a registration
feature, this has however not been implemented yet.


[Git Statistics](http://krumreyh.com/git_stats_pages/whatsapp-bot/general.html)