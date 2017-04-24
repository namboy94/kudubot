# Kudubot Whatsapp

![Logo](resources/logo/logo-readme.png)

Kudubot Whatsapp is a Connection plugin for
[Kudubot](https://gitlab.namibsun.net/namboy94/kudubot). It offers
access to the Whatsapp Messaging Service via the [yowsup](https://github.com/tgalal/yowsup) library.

## Installation

To integrate the service with kudubot, add the following line to the
```connections.conf``` file in the ```~/.kudubot``` directory:

    from kudubot.connections.whatsapp.WhatsappConnection import WhatsappConnection
