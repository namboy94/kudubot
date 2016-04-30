# messengerbot

This project was formerly known as whatsbot and whatsapp-bot.

messengerbot is a bot framework that allows running a bot on a multitude of messaging services. It is completely
modular, adding new bot services and new connection types is trivial.

The framework ensures that all properly implemented bot services work with different types of connections, like Email,
Telegram, Whatsapp or IRC for example.

To install the program, either run

    sudo pip install messenger_bot
    
or download the sources and run

    sudo python setup.py install

Currently supported connection types are:

* Email
* Telegram
* Whatsapp via Yowsup (currently broken)

Currently implemented bot services are:

* Help Service
* Muter
* Service Selector
* Simple Equals Responder
* Simple Contains Responder
* Kicktipp Info Service
* Football Info Service
* Weather Service

##Links

[Changelog](http://gitlab.namibsun.net/namboy94/messengerbot/raw/master/CHANGELOG)

[Python Package Index Site](https://pypi.python.org/pypi/messenger_bot)

[Git Statistics](http://gitlab.namibsun.net/namboy94/messengerbot/wikis/git_stats/general.html)

[Documentation](http://gitlab.namibsun.net/namboy94/messengerbot/wikis/html/index.html)