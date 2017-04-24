# Kudubot Simple Responder

![Logo](resources/logo/logo-readme.png)

Kudubot Simple Responder is a Service Module for
[kudubot](https://gitlab.namibsun.net/namboy94/kudubot).

It analyzes incoming messages and responds to certain strings with pre-defined
messages.

For example, if the Service receives a message with the text ```"Ping"```,
the Service will respond with ```"Pong"```.

## Installation

To integrate the service with kudubot, add the following line to the
```services.conf``` file in the ```~/.kudubot``` directory:

    from kudubot.services.simple_responder.SimpleResponderService import SimpleResponderService
