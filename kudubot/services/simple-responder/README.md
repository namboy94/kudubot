# Kudubot Simple Responder

|master|develop|
|:----:|:-----:|
|[![build status](https://gitlab.namibsun.net/namboy94/kudubot-simple-responder/badges/master/build.svg)](https://gitlab.namibsun.net/namboy94/kudubot-simple-responder/commits/master)|[![build status](https://gitlab.namibsun.net/namboy94/kudubot-simple-responder/badges/develop/build.svg)](https://gitlab.namibsun.net/namboy94/kudubot-simple-responder/commits/develop)|

![Logo](kudubot_simple_responder/resources/logo/logo-readme.png)

Kudubot Simple Responder is a Service Module for
[kudubot](https://gitlab.namibsun.net/namboy94/kudubot).

It analyzes incoming messages and responds to certain strings with pre-defined
messages.

For example, if the Service receives a message with the text ```"Ping"```,
the Service will respond with ```"Pong"```.

## Installation

The service can be installed using pip:

    pip install kudubot_simple_responder
    
or directly from source:

    python setup.py install
    
To integrate the service with kudubot, add the following line to the
```services.conf``` file in the ```~/.kudubot``` directory:

    from kudubot_simple_responder.SimpleResponderService import SimpleResponderService
    
## Further Information

* [Changelog](https://gitlab.namibsun.net/namboy94/kudubot-simple-responder/raw/master/CHANGELOG)
* [Gitlab](https://gitlab.namibsun.net/namboy94/kudubot-simple-responder)
* [Github](https://github.com/namboy94/kudubot-simple-responder)
* [Python Package Index Site](https://pypi.python.org/pypi/kudubot-simple-responder)
* [Documentation(HTML)](https://docs.namibsun.net/html_docs/kudubot-simple-responder/index.html)
* [Documentation(PDF)](https://docs.namibsun.net/pdf_docs/kudubot-simple-responder.pdf)
* [Git Statistics (gitstats)](https://gitstats.namibsun.net/gitstats/kudubot-simple-responder/index.html)
* [Git Statistics (git_stats)](https://gitstats.namibsun.net/git_stats/kudubot-simple-responder/index.html)
* [Test Coverage](https://coverage.namibsun.net/kudubot-simple-responder/index.html)