from tools import Connector
import PySimpleGUI as sg

sg.theme('DarkAmber')

connector = Connector()

layout = [
    [sg.Text('Port:'), sg.Combo(connector.get_ports(), enable_events=True, readonly=True, k='-PORT-')],
    [sg.Button('Send'), sg.Button('Exit')]
]

window = sg.Window('Headset GUI', layout)

while True:
    event, values = window.read()
    print(event, values)
    if event == sg.WIN_CLOSED or event == 'Exit':
        break
    if event == 'Show':
        window['-OUTPUT-'].update(values['-IN-'])

window.close()