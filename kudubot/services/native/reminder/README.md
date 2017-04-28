# Kudubot Reminder

![Logo](resources/logo/logo-readme.png)

Kudubot Reminder is a Service Module for
[kudubot](https://gitlab.namibsun.net/namboy94/kudubot).

It offers a reminder service for arbitrary messages to be re-sent
at a later time.

## Installation
    
To integrate the service with kudubot, add the following line to the
```services.conf``` file in the ```~/.kudubot``` directory:

    from kudubot.services.reminder.ReminderService import ReminderService
