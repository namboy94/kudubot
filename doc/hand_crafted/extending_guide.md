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

All messages are abstracted as a member of the messengerbot.connection.generic.Message class by the Connection modules,
allowing for a connection-independent handling of messages.

## Creating a new Service

Create a class with the following structure:

```python
from messengerbot.connection.generic.Service import Service
from messengerbot.connection.generic.Message import Message

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
	
	@staticmethod
	def regex_check(Message) -> bool:
		# This method checks if a message is valid to be used by the service. It is called before running process_message
		# to ensure that only valid commands reach the service's logic.
	
	def process_message(self, Message):
		# This method is called if the regex_check returned True. The functionalty of the service should be bundled here
	
	# Optional Methods
	
	def background_process(self):
		# This method should contain an infinite loop that is to be called as a seperate thread (the threading does not
		# need to be handled by the Service, it is done by the ServiceManager class for you) that runs a background
		# process for the Service.
		# Note that this method will not be called if has_background_process is set to False
```

Then implement your service as you see fit. You can use the self.send_text_message, self.send_image_message and
self.send_audio_message methods of the Service class to send messages.

To integrate the Service into the bot, edit the ServiceManager class as follows:

* add the created Service to the imports
* Add the Service into the 'all_services' list at the position you want it to appear in the help message

## Creating a new Connection

Create a class with the following structure:

```python
from messengerbot.connection.generic.Connection import Connection
from messengerbot.connection.generic.Message import Message

class <ConnectionName>Connection(Connection):
	# Required Attributes:
	
	identifier = str  # provide a unique identifier string for your connection

	# Required Methods:
	
	def send_text_message(Message):
		# Implementation of sending a text message
	
	def send_image_message(file_path, recever_address, optional_caption):
		# Implementation of sending an image message
	
	def send_audio_message(file_path, receiver_address, optional_caption):
		# Implementation of sending an audio message
	
	@staticmethod
	def establish_connection():
		# This is a static method that establishes a new connection. It should:
		# 	- load authentication credentials
		#	- enter an infinite loop that listens for incoming messages, converts them into a Message object
		#		and then calls self.on_incoming_message with the generate message as the parameter
		#	Generally, you would want to create a new Connection object and start its mainloop defined elsewhere
	
	
	# Optional Methods
	
	def initialize():
		# Can be used to extend the functionality of the constructor. Don't forget to call super().initialize() in this
		# method. You hould probably extend this method instead of __init__, especially if you extend another class
		# besides the 
	
```

To integrate the Connection into the bot, edit the main module as follows:

* add the created Connection to the imports
* Add the Connection into the 'connections' list
