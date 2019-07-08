# Kudubot

|master|develop|
|:----:|:-----:|
|[![build status](https://gitlab.namibsun.net/namibsun/python/kudubot/badges/master/build.svg)](https://gitlab.namibsun.net/namibsun/python/kudubot/commits/master)|[![build status](https://gitlab.namibsun.net/namibsun/python/kudubot/badges/develop/build.svg)](https://gitlab.namibsun.net/namibsun/python/kudubot/commits/develop)|

![Logo](resources/logo/logo-readme.png)

Kudubot is a chat bot framework designed to work with arbitrary messaging
services based on
[bokkichat](https://gitlab.namibsun.net/namibsun/python/bokkichat)
connections.

# Installation

Installing bokkichat is as simple as running ```pip install kudubot```, or
```python setup.py install``` when installing from source.

# Implementing a kudubot

To implement a kudubot, you'll need to create a class that inherits from
```kudubot.Bot.Bot``` and implement the various on_X methods in the way
you want the bot to react.

Kudubot is meant to react on commands like ```/send 123```. Those are
modelled using CommandParser and Command objects. Those are used to
automatically parse incoming text messages and are sent to ```on_command```.

If you want complete manual control over what happens with incoming messages,
override the ```on_msg``` method. If you only care about text messages, do the
same for ```on_text```.

To get an idea of how to implement a kudubot, have a look at some of these
sample projects:

* [football-bot](https://gitlab.namibsun.net/namibsun/python/football-bot)
* [securiphant](https://gitlab.namibsun.net/namibsun/python/securiphant)


## Further Information

* [Changelog](CHANGELOG)
* [License (GPLv3)](LICENSE)
* [Gitlab](https://gitlab.namibsun.net/namibsun/python/kudubot)
* [Github](https://github.com/namboy94/kudubot)
* [Progstats](https://progstats.namibsun.net/projects/kudubot)
* [PyPi](https://pypi.org/project/kudubot)
