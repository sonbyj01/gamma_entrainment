import serial
import serial.tools.list_ports

class Connector: 
    def __init__(self): 
        self.ports = []
        self.serial = None
        self.port = None
        self.baudrate = 9600

    def get_ports(self) -> list:
        ports = serial.tools.list_ports.comports()

        for port, desc, _ in sorted(ports):
            self.ports.append("{} {}".format(port, desc[0:16]))

        return self.ports 

    def send_command(self):
        pass
    