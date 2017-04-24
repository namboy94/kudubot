# Kudubot Anime Reminder

![Logo](resources/logo/logo-readme.png)

Kudubot Anime Reminder is a Service Module for
[kudubot](https://gitlab.namibsun.net/namboy94/kudubot).

It offers a reminder service for airing anime series, which are determined by listening
to [reddit](https://reddit.com)'s [r/anime](https://reddit.com/r/anime) board.

## Installation

To integrate the service with kudubot, add the following line to the
```services.conf``` file in the ```~/.kudubot``` directory:

    from kudubot.services.anime_reminder.AnimeReminderService import AnimeReminderService
