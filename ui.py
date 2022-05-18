from tools import Connector
import PySimpleGUI as sg

sg.theme('DarkAmber')

connector = Connector()

layout = [
    [sg.Text('Select Port:'), 
        sg.Combo(connector.get_ports(), enable_events=True, readonly=True, key='PORT')],
    [sg.Text('Set Frequency (HZ): '), 
        sg.Input(default_text='0', key='FREQUENCY', s=3, enable_events=True)],
    [sg.Text('Set Color (RGB):'), 
        sg.Input(default_text="0", key='R', s=3, enable_events=True), 
        sg.Input(default_text="0", key='G', s=3, enable_events=True), 
        sg.Input(default_text="0", key='B', s=3, enable_events=True)],
    [sg.Text('Set Phase (Deg):'), 
        sg.Input(default_text="0", key='PHASE', s=3, enable_events=True)],
    [sg.Button('Send'), sg.Button('Reset'), sg.Button('Exit')]
]

window = sg.Window('Headset GUI', layout)

rgb = ['R', 'G', 'B']
exit = ['Exit', sg.WIN_CLOSED]

while True:
    event, values = window.read()
    print(event, values)

    # set serial/port
    if event == 'PORT':
        connector.set_port(values['PORT'])

    # reset values
    if event == 'Reset':
        window['PORT'].update(values=connector.get_ports())
        window['FREQUENCY'].update('0')
        window['R'].update('0')
        window['G'].update('0')
        window['B'].update('0')
        window['PHASE'].update('0')

    # exits window
    if event in exit:
        break

    # send command
    if event == 'Send':
        connector.send_command(int(values['FREQUENCY']), int(values['R']), int(values['G']), int(values['B']), int(values['PHASE']))

window.close()