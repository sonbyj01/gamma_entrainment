import serial
import serial.tools.list_ports

class Connector: 
    def __init__(self): 
        self.ports = []
        self.serial = None
        self.port = None
        self.baudrate = 9600

    def set_port(self, port):
        port = port.split(' ')[0]
        
        if port == None or port == self.port:
            print('same port')
        else:
            self.serial = serial.Serial(port, self.baudrate)
            self.port = port
            print(port)

    def get_ports(self) -> list:
        ports = serial.tools.list_ports.comports()

        for port, desc, _ in sorted(ports):
            self.ports.append("{} {}".format(port, desc[0:16]))

        return self.ports 

    def send_command(self, freq, red, green, blue, phase) -> str:
        if self.serial is None:
            return "No port has been selected!"
        
        command = "{},{},{},{},{}".format(freq, red, green, blue, phase)
        self.serial.write(
            command.encode('ascii')
        )
        return "Write sucessful!"
        