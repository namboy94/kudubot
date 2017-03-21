# Kudubot

|master|develop|
|:----:|:-----:|
|[![build status](https://gitlab.namibsun.net/namboy94/kudubot/badges/master/build.svg)](https://gitlab.namibsun.net/namboy94/kudubot/commits/master)|[![build status](https://gitlab.namibsun.net/namboy94/kudubot/badges/develop/build.svg)](https://gitlab.namibsun.net/namboy94/kudubot/commits/develop)|

![Logo](kudubot/resources/logo/logo-readme.png)

Kudubot is a chat bot framework designed to work with arbitrary messaging
services, be it Whatsapp, Telegram, IRC or even Email. The framework is
completely modular and can be extended with other connection types
and services.

## Implementing a Connection.

To implement a new Connection, you will have to create a subclass
the ```kudubot.connections.Connection.Connection``` class and implement the
various abstract methods.

To integrate the connection with Kudubot, make sure your class is in
your system's python path (i.e. importable) and add an import statement
to the config file located at ```$HOME/.kudubot/connections.conf``` 
that would import your Connection class.

For examples see:

* [kudubot-telegram](https://gitlab.namibsun.net/namboy94/kudubot-telegram)

## Implementing a Service

To implement a Service, you will have to create a subclass of the
```kudubot.services.Service.Service``` class and implement the various
abstract methods.

To integrate the service with Kudubot, make sure your class is in
your system's python path (i.e. importable) and add an import statement
to the config file located at ```$HOME/.kudubot/services.conf``` 
that would import your Service class.

For examples see:

* [kudubot-simple-responder](https://gitlab.namibsun.net/namboy94/kudubot-simple-responder)

## Further Information

* [Changelog](https://gitlab.namibsun.net/namboy94/kudubot/raw/master/CHANGELOG)
* [Gitlab](https://gitlab.namibsun.net/namboy94/kudubot)
* [Github](https://github.com/namboy94/kudubot)
* [Python Package Index Site](https://pypi.python.org/pypi/kudubot)
* [Documentation(HTML)](https://docs.namibsun.net/html_docs/kudubot/index.html)
* [Documentation(PDF)](https://docs.namibsun.net/pdf_docs/kudubot.pdf)
* [Git Statistics (gitstats)](https://gitstats.namibsun.net/gitstats/kudubot/index.html)
* [Git Statistics (git_stats)](https://gitstats.namibsun.net/git_stats/kudubot/index.html)
* [Test Coverage](https://coverage.namibsun.net/kudubot/index.html)
