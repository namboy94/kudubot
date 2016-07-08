# Kudubot

Kudubot is a bot framework that allows running a bot on a multitude of messaging services. It is completely
modular, adding new bot services and new connection types is relatively trivial.

The framework offers abstractions that allow all properly implemented bot services to work with different types of
connections (Email, Telegram, Whatsapp or IRC for example) without having to change the code.
 
## Installation

To install the program, either run

    sudo pip install kudubot
    
or download the sources and run

    sudo python setup.py install
    
Setuptools should automatically download all required dependencies without further input.

The program is being developed on Linux, it should in theory work on Windows and Mac OS X, though this has not been
tested.

## Usage

You can start the bot using the 'kudubot' command (setuptools should have installed it for you).

You will need to specify a connection type, which is the identifier string for one of the implemented
connections or 'all', which starts the bot using all services.

You can also specify the output verbosity using the --verbosity. 0 disables all input, and there's no real
upper limit (Though to keep it sane, the highest verbosity that actually changes things is 5)

You can also directly run the bot without setting options by using one of these commands (again, they should be
installed by setuptools automatically)

    kudubot-email     # For the email connection
    kudubot-telegram  # For the Telegram Connection
    kudubot-whatsapp  # For the Whatsapp Connection  (Doesn't work right now)
    kudubot-all       # For all connections
    
After starting the program for the first time, you will be notified that config files were created.
The program creates a directory called '.kudubot' (which is a hidden directory on Linux). it contains
all configs, logs and other files/directories used by the bot services.

To be able to connect to a service, you will have to enter login credentials into the config file of the chosen
connection type, which will be located under

    ~/.kudubot/config
    
The credential types are different for all types of connections and need to be set accordingly. The program creates
template files when first run, so figuring out which kind of information to enter should not be all that difficult.

Once the credentials are entered, you can adjust which services will be run on startup by editing the
<connection-type>-services file in the same directory.

As a last step you may want to adjust the admin and blacklist files in the 

    ~/.kudubot/contacts
    
directory to give yourself admin rights for the bot and ignore things like other bots.


## Developing
    
If you are not viewing this on gitlab.namibsun.net, this is only a mirror of that repository, active development
is only being done on gitlab.namibsun.net. Issues are being checked on all mirrors though, so feel free to open
issues on your version control hoster of choice.

For a guide on how to extend the bot, see [this](doc/hand_crafted/extending_guide.md).

## Contributing

This project is automatically mirrored to [github](https://github.com/namboy94/kudubot), however all development
is conducted at a privately hosted [Gitlab instance](http://gitlab.namibsun.net/namboy94/kudubot). Issues
on both services are taken unto consideration.

## Documentation

Sphinx Documentation can be found [here](http://krumreyh.eu/kudubot/documentation/html/index.html).
A [PDF version](http://krumreyh.eu/kudubot/documentation/documentation.pdf) is also available

## Support

If you have any questions about kudubot, feel free to open an issue or contact me directly at
hermann@krumreyh.com.

## Statistics

Automatically generated git statistics can be found [here](http://krumreyh.eu/kudubot/git_stats/index.html)

[Changelog](http://gitlab.namibsun.net/namboy94/kudubot/raw/master/CHANGELOG)