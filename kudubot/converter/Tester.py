from threading import Thread

from kudubot.connection.whatsapp.WhatsappConnection import WhatsappConnection
from kudubot.connection.telegram.TelegramConnection import TelegramConnection
from kudubot.servicehandlers.ServiceManager import ServiceManager


class Servicer(ServiceManager):
    pass

class Whatsapp(WhatsappConnection):



    def initialize(self):
        self.service_manager = Servicer()

    pass


class TelegramHost(TelegramConnection):

    class Servicer(ServiceManager)

    pass

class TelegramSlave(TelegramConnection):

    pass

def start_whatsapp():
    Whatsapp.establish_connection()

if __name__ == '__main__':
    t = Thread(target=start_whatsapp)
    t.daemon = True
    t.run()
    TelegramHost.establish_connection()