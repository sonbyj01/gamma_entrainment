import wx
import serial
import serial.tools.list_ports


# ---------------------------------------------------------------------------- #
# Serial connection

BAUDRATE = 9600
SERIAL = None
PORT = None

def send2mc(data : bytes):
    if SERIAL == None:
        print("Port not yet selected")
        return
    SERIAL.write(data)

# ---------------------------------------------------------------------------- #
# GUI

class GUI(wx.Frame):
    def __init__(self):
        super().__init__(None, title="Headset Interface")
        self.InitGUI()
        self.port = None
    
    def InitGUI(self):
        self.SetSize(400,250)
        self.SetMaxSize(wx.Size(400,290))
        self.SetMinSize(wx.Size(400,290))

        panel = wx.Panel(self)
        self.InitBody(panel)

    def InitBody(self, panel : wx.Panel):
        body_sizer = wx.BoxSizer(wx.VERTICAL)

        # connect to microcontroller
        serial_sizer = wx.BoxSizer(wx.HORIZONTAL)

        com_ports = self.GetCOMPorts() 
        # ['COM1', 'COM2', 'COM3', 'COM4']

        text = wx.StaticText(panel, label="Select Port: ")
        serial_sizer.Add(text, 0, wx.LEFT | wx.BOTTOM | wx.TOP, 15)
        self.ports= wx.ComboBox(panel, id=wx.ID_ANY, choices=com_ports, 
                               value="Port")
        self.ports.Bind(wx.EVT_TEXT, self.PortChange)
        self.ports.Bind(wx.EVT_COMBOBOX_DROPDOWN, self.UpdateCOMPorts)
        serial_sizer.Add(self.ports, 0, wx.LEFT | wx.BOTTOM | wx.TOP, 15)

        body_sizer.Add(serial_sizer, 0, wx.EXPAND)

        # --- #

        # set frequency 
        freq_sizer = wx.BoxSizer(wx.HORIZONTAL)
        text = wx.StaticText(panel, label="Set Frequency (Hz): ")
        freq_sizer.Add(text, 0, wx.LEFT | wx.BOTTOM | wx.TOP, 15)

        self.freq_txt = wx.TextCtrl(panel, value="", size=(100, -1))
        freq_sizer.Add(self.freq_txt, 0, wx.ALL, 10)

        body_sizer.Add(freq_sizer, 0, wx.EXPAND)

        # --- #

        # set color
        color_sizer = wx.BoxSizer(wx.HORIZONTAL)
        text = wx.StaticText(panel, label="Set Color (RGB): ")
        color_sizer.Add(text, 0, wx.LEFT | wx.BOTTOM | wx.TOP, 15)

        self.color_txt_r = wx.TextCtrl(panel, value="", size=(50, -1))
        color_sizer.Add(self.color_txt_r, 0, wx.ALL, 10)
        # body_sizer.Add(color_sizer, 0, wx.EXPAND)

        self.color_txt_g = wx.TextCtrl(panel, value="", size=(50, -1))
        color_sizer.Add(self.color_txt_g, 0, wx.ALL, 10)
        # body_sizer.Add(color_sizer, 0, wx.EXPAND)

        self.color_txt_b = wx.TextCtrl(panel, value="", size=(50, -1))
        color_sizer.Add(self.color_txt_b, 0, wx.ALL, 10)
        body_sizer.Add(color_sizer, 0, wx.EXPAND)

        # --- #

        # set phase 
        phase_sizer = wx.BoxSizer(wx.HORIZONTAL)
        text = wx.StaticText(panel, label="Set Phase (Deg): ")
        phase_sizer.Add(text, 0, wx.LEFT | wx.BOTTOM | wx.TOP, 15)

        self.phase_txt = wx.TextCtrl(panel, value="", size=(100, -1))
        phase_sizer.Add(self.phase_txt, 0, wx.ALL, 10)

        body_sizer.Add(phase_sizer, 0, wx.EXPAND)

        # --- #

        # submit button
        submit_sizer = wx.BoxSizer(wx.HORIZONTAL)

        btn = wx.Button(panel, label="Send Command")
        btn.Bind(wx.EVT_BUTTON, self.SendCommand)
        body_sizer.Add(btn, 0, wx.ALL, 10)

        panel.SetSizer(body_sizer)

    def PortChange(self, event):
        global SERIAL, PORT
        print(event.GetString())
        port = event.GetString().split(' ')[0]
        if port == PORT or port == '':
            print("Selecting Same Port")
        elif port != None:
            SERIAL = serial.Serial(port, BAUDRATE)
            PORT = port


        print("Port: ", PORT)

    # slow if bluetooth is enabled
    def UpdateCOMPorts(self, event):
        coms = self.GetCOMPorts()
        self.ports.Set(coms)

    # https://stackoverflow.com/questions/12090503/listing-available-com-ports-with-python
    def GetCOMPorts(self) -> list:
        ports = serial.tools.list_ports.comports()
        ret_list = []
        for port, desc, hwid in sorted(ports):
            ret_list.append("{} {}".format(port, desc[0:16]))
        return ret_list

    def SendCommand(self, event):
        print("Sending Command")
        freq = self.freq_txt.GetValue()
        red = self.color_txt_r.GetValue()
        green = self.color_txt_g.GetValue()
        blue = self.color_txt_b.GetValue()
        phase = self.phase_txt.GetValue()
        print("Frequency: " + freq)
        print("Color: {} {} {}".format(red, green, blue))
        print("Phase: " + phase)
        send2mc("{},{},{},{},{}".format(freq, red, green, blue, phase).encode('ascii'))
        pass

    def Nothing(self, event):
        self.port = event.GetString()
        print("Port: ", self.port)
        pass

    

if __name__ == "__main__":
    app = wx.App()
    frame = GUI()
    frame.Show(True)
    app.MainLoop()
