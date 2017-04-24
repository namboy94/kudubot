# Kudubot Anime Reminder

|master|develop|
|:----:|:-----:|
|[![build status](https://gitlab.namibsun.net/namboy94/kudubot-anime-reminder/badges/master/build.svg)](https://gitlab.namibsun.net/namboy94/kudubot-anime-reminder/commits/master)|[![build status](https://gitlab.namibsun.net/namboy94/kudubot-anime-reminder/badges/develop/build.svg)](https://gitlab.namibsun.net/namboy94/kudubot-anime-reminder/commits/develop)|

![Logo](kudubot_anime_reminder/resources/logo/logo-readme.png)

Kudubot Anime Reminder is a Service Module for
[kudubot](https://gitlab.namibsun.net/namboy94/kudubot).

It offers a reminder service for airing anime series, which are determined by listening
to [reddit](https://reddit.com)'s [r/anime](https://reddit.com/r/anime) board.

## Installation

The service can be installed using pip:

    pip install kudubot_anime_reminder

or directly from source:

    python setup.py install

To integrate the service with kudubot, add the following line to the
```services.conf``` file in the ```~/.kudubot``` directory:

    from kudubot_anime_reminder.AnimeReminderService import AnimeReminderService

## Further Information

* [Changelog](https://gitlab.namibsun.net/namboy94/kudubot-anime-reminder/raw/master/CHANGELOG)
* [Gitlab](https://gitlab.namibsun.net/namboy94/kudubot-anime-reminder)
* [Github](https://github.com/namboy94/kudubot-anime-reminder)
* [Python Package Index Site](https://pypi.python.org/pypi/kudubot-anime-reminder)
* [Documentation(HTML)](https://docs.namibsun.net/html_docs/kudubot-anime-reminder/index.html)
* [Documentation(PDF)](https://docs.namibsun.net/pdf_docs/kudubot-anime-reminder.pdf)
* [Git Statistics (gitstats)](https://gitstats.namibsun.net/gitstats/kudubot-anime-reminder/index.html)
* [Git Statistics (git_stats)](https://gitstats.namibsun.net/git_stats/kudubot-anime-reminder/index.html)
* [Test Coverage](https://coverage.namibsun.net/kudubot-anime-reminder/index.html)
