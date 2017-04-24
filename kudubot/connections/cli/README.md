# Kudubot Cli

![Logo](resources/logo/logo-readme.png)

Kudubot cli is a Connection plugin for
[Kudubot](https://gitlab.namibsun.net/namboy94/kudubot). It offers
a simple CLI prompt for quickly testing new service modules.

## Installation

To integrate the service with kudubot, add the following line to the
```connections.conf``` file in the ```~/.kudubot``` directory:

    from kudubot.connections.cli.CliConnection import CliConnection
