# Kudubot

|master|develop|
|:----:|:-----:|
|[![build status](https://gitlab.namibsun.net/namboy94/kudubot/badges/master/build.svg)](https://gitlab.namibsun.net/namboy94/kudubot/commits/master)|[![build status](https://gitlab.namibsun.net/namboy94/kudubot/badges/develop/build.svg)](https://gitlab.namibsun.net/namboy94/kudubot/commits/develop)|

![Logo](resources/logo/logo-readme.png)

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

For examples look at the implemented connections in
[services](kudubot/connections).

## Implementing a Service

To implement a Service, you will have to create a subclass of the
```kudubot.services.Service.Service``` class and implement the various
abstract methods.

To integrate the service with Kudubot, make sure your class is in
your system's python path (i.e. importable) and add an import statement
to the config file located at ```$HOME/.kudubot/services.conf``` 
that would import your Service class.

For examples look at the implemented services in
[services](kudubot/services/native).

## Implementing an external Service

Kudubot enables you to write a Service in any language you would like.
For this to be possible, you first need to implement a very basic python
class that inherits from `kudubot.services.ExternalService` and implement
its abstract methods, which are:

1. define_executable_file_url
    
   Defines a URL from which the Service's executable file can be downloaded
   if necessary. there is a helper method called `resolve_github_release_asset_url`
   which makes it easy to provide a Github release asset as the executable
   file.
     
2. define_executable_command

   Defines the commands *preceeding* the actual executable if called from the
   command line.
   
   For example, for a `.jar` file to run, one would have to return `["java","-jar"].`

3. define_identifier

    Simply a unique string which acts as an identifier for a service.
    

Once that has been settled, you may start implementing the service in your
preferred language. Your program needs to be runnable as a single executable.

The kudubot framework will call your executable whenever it receives a message,
then checks if the message is applicable to your service and then, if it is
applicable, asks your executable to process the message.

**In detail**:

Your executable will be provided with 4 command line arguments:

1. The mode in which your program should run. Can be either `is_applicable_to`
   or `handle_message`. Your program must act accordingly.
2. A file location containing the message information in JSON format. You will
   need to parse this yourself if no bindings exist for your language.
3. A file location which is used to tell the kudubot program the result of
   your program's execution.
   
   For example, if the `is_applicable_to` query was successful, i.e. the Service
   is aplicable to the message, the following JSON data should be written to
   the file:
   
       {"is_applicable": true}
   
   or when your program handled a message sucessfully and want to reply
   with a message of its own:
   
       {"mode": "reply"}
    
4. The location of the Connection's SQlite database file.


Should you want to reply to a message, the original message file
must be overwritten with a new Message JSON string, which needs to
have the exact same attributes as the original, just different values.
To actually make kudubot reply, `{"mode": "reply"}` must be written
into the response file.

Your executable file must be located in `.kudubot/external/bin` and
have the exact same name as your service's identifier, including the
file extension. If it is not there at runtime, kudubot will try to
download the executable from the download URL specified in
`define_executable_file_url`.

**Bindings**

There are common bindings available for the following languages:

* Rust ([crates.io](https://crates.io/crates/kudubot-bindings))


## Further Information

* [Changelog](https://gitlab.namibsun.net/namboy94/kudubot/raw/master/CHANGELOG)
* [License (GPLv3)](https://gitlab.namibsun.net/namboy94/kudubot/raw/master/LICENSE)
* [Gitlab](https://gitlab.namibsun.net/namboy94/kudubot)
* [Github](https://github.com/namboy94/kudubot)
* [Documentation(HTML)](https://docs.namibsun.net/html_docs/kudubot/index.html)
* [Documentation(PDF)](https://docs.namibsun.net/pdf_docs/kudubot.pdf)
* [Git Statistics (gitstats)](https://gitstats.namibsun.net/gitstats/kudubot/index.html)
* [Git Statistics (git_stats)](https://gitstats.namibsun.net/git_stats/kudubot/index.html)
* [Test Coverage](https://coverage.namibsun.net/kudubot/index.html)
* [Python Package Index Site](https://pypi.python.org/pypi/kudubot)

