from kudubot.config.GlobalConfigHandler import GlobalConfigHandler

class StandardConfigWriter(object):

    @staticmethod
    def write_standard_connection_config():

        with open(GlobalConfigHandler.global_connection_config_location, 'w') as config:
            for connection in ["from kudubot.connections.cli.CliConnection import CliConnection"]:
                config.write(connection + "\n")

    @staticmethod
    def write_standard_service_config():

        with open(GlobalConfigHandler.services_config_location, 'w') as config:
            for service in ["from kudubot.services.simple_responder.SimpleResponderService import SimpleResponderService"]:
                config.write(service + "\n")