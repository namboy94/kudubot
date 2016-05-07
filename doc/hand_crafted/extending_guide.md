# How to extend the bot's functionality

(WORK IN PROGRESS)

## Preparation

First, clone or fork the repository to get all the sources. Then, install all dependencies listed
in messengerbot/metadata.py (or let setup.py do it for you).

Now you can modify the projet files to extend the bot's funtionality.

To do this effectively, you need to understand how the project is structured:


## Project Structure

The project is seperatd into three parts. There are the Services, the Connections and the Framework.

The Services are individual modules that provide a bot service, for example, a service could listen to incoming
messages that are 'ping' and then respond with 'pong'. These services are self-contained and should not do anything
connection-depenent, but rather use the messengerbot.servicehandlers.Service Interface to send messages.

The Connections are modules that handle the actual connections to the messaging servives.
It enables listening to new incoming messages continuously and sending messages using the service as well.

The framework manages the communication between the Service and Connection modules, providing an abstraction
layer to make all connections and services exchangeable.

## Creating a new Service

Create a class with the following structure:

```python
from messengerbot.connection.generic.Service import Service

class <ServiceName>Service(Service):
	# Required Attributes:
	identifier = str  # provide a unique identifier string for your service
	help_description = dict(str: str)  # A dictionary that defines help messages. The dictionary keys should be language
									   # identifiers (For example, "en" for English or "de" for German), and the value
									   # they map to is the help description itself.
									   # The help description is used by the built-in Help service.
	
	# Optional Attributes:
	has_background_process = bool  # (default=False) Can be used to tell the ServiceManager that this Service
	                               # has a background process. If this is set to true, the method
	                               # background_process will be run in a seperate thread
	protected = bool  # (default=False) this tells the ServiceSelectorService that this Service can not be deactivated
					  # if this is set to true
	
	
	# Required Methods:
	# Optional Methods
```





    help_description = {"en": "A Generic Service Interface",
                        "de": "Eine Generische Dienstleistungsschnittstelle"}
    """
    A dictionary containing help messages in various languages on the use of the service
    """

    identifier = "Service"
    """
    A unique identifier assigned to the plugin.
    """

    protected = False
    """
    Can be set to true if the service requires admin privileges
    """

## Creating a new Connection

Create a class with the following structure:

```python
from messengerbot.connection.generic.Connection import Connection

class <ConnectionName>Connection(Connection):
	# Required Attributes:
	identifier = str  # provide a unique identifier string for your service
	
	# Optional Attributes:
	has_background_process = False
	help
	# Required Methods:
	# Optional Methods
```

## Integrating a Service or a Connection into messengerbot