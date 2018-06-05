# Kudubot

|master|develop|
|:----:|:-----:|
|[![build status](https://gitlab.namibsun.net/namibsun/python/kudubot/badges/master/build.svg)](https://gitlab.namibsun.net/namibsun/python/kudubot/commits/master)|[![build status](https://gitlab.namibsun.net/namibsun/python/kudubot/badges/develop/build.svg)](https://gitlab.namibsun.net/namibsun/python/kudubot/commits/develop)|

![Logo](resources/logo/logo-readme.png)

Kudubot is a chat bot framework designed to work with arbitrary messaging
services, be it Whatsapp, Telegram, IRC or even Email. The framework is
completely modular and can be extended with other connection types
and services.

## Usage

Kudubot can be used using the ```kudubot``` command once it's installed using
the setup.py file or pip. To do so, run one of the following commands, 
optionally with the ```--user``` flag to install it for the current user as
opposed to system-wide:

    python setup.py install
    
    pip install kudubot
    
To use kudubot, a configuration directory must exist in ```~/.kudubot``` or
be provided to the ```kudubot```-command using the ```--config``` option.
A configuration directory can be generated using ```kudubot-config-gen```.
Run ```kudubot-config-gen --help``` to explore the options that tool provides
you.

Sample connection configurations can be found [here](resources/connection-configs)

## Implementing a Connection.

To implement a new Connection, you will have to create a subclass of
the ```kudubot.connections.Connection.Connection``` class and implement the
various abstract methods.

To integrate the connection with Kudubot, make sure your class is in
your system's python path (i.e. importable) and add an import statement
to the config file located at ```$HOME/.kudubot/connections.conf``` 
that would import your Connection class.

For examples look at the [implemented connections](kudubot/connections).

## Implementing a Service

To implement a Service, you will have to create a subclass of the
```kudubot.services.Service.Service``` class and implement the various
abstract methods.

To integrate the service with Kudubot, make sure your class is in
your system's python path (i.e. importable) and add an import statement
to the config file located at ```$HOME/.kudubot/services.conf``` 
that would import your Service class.

For examples look at the [implemented services](kudubot/services/native).

## Creating a standalone Bot Service

To see how to create a single-purpose bot, take a look at the echobot:

* [starter script](bin/echobot)
* [service](kudubot/services/internal/echo)


## Further Information

* [Changelog](CHANGELOG)
* [License (GPLv3)](LICENSE)
* [Gitlab](https://gitlab.namibsun.net/namibsun/python/kudubot)
* [Github](https://github.com/namboy94/kudubot)
* [Progstats](https://progstats.namibsun.net/projects/kudubot)
* [PyPi](https://pypi.org/project/kudubot)
