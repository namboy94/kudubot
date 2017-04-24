# Kudubot Reminder

|master|develop|
|:----:|:-----:|
|[![build status](https://gitlab.namibsun.net/namboy94/kudubot-reminder/badges/master/build.svg)](https://gitlab.namibsun.net/namboy94/kudubot-reminder/commits/master)|[![build status](https://gitlab.namibsun.net/namboy94/kudubot-reminder/badges/develop/build.svg)](https://gitlab.namibsun.net/namboy94/kudubot-reminder/commits/develop)|

![Logo](kudubot_reminder/resources/logo/logo-readme.png)

Kudubot Reminder is a Service Module for
[kudubot](https://gitlab.namibsun.net/namboy94/kudubot).

It offers a reminder service for arbitrary messages to be re-sent
at a later time.

## Installation

The service can be installed using pip:

    pip install kudubot_reminder
    
or directly from source:

    python setup.py install
    
To integrate the service with kudubot, add the following line to the
```services.conf``` file in the ```~/.kudubot``` directory:

    from kudubot_reminder.ReminderService import ReminderService
    
## Further Information

* [Changelog](https://gitlab.namibsun.net/namboy94/kudubot-reminder/raw/master/CHANGELOG)
* [Gitlab](https://gitlab.namibsun.net/namboy94/kudubot-reminder)
* [Github](https://github.com/namboy94/kudubot-reminder)
* [Python Package Index Site](https://pypi.python.org/pypi/kudubot-reminder)
* [Documentation(HTML)](https://docs.namibsun.net/html_docs/kudubot-reminder/index.html)
* [Documentation(PDF)](https://docs.namibsun.net/pdf_docs/kudubot-reminder.pdf)
* [Git Statistics (gitstats)](https://gitstats.namibsun.net/gitstats/kudubot-reminder/index.html)
* [Git Statistics (git_stats)](https://gitstats.namibsun.net/git_stats/kudubot-reminder/index.html)
* [Test Coverage](https://coverage.namibsun.net/kudubot-reminder/index.html)