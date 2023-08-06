import os
import pickle
import PySimpleGUI as sg
import sys


#################################################################
#                          GUI functions                        #
#################################################################


def open_session():
    """ opens first GUI for user to config the run
    @rtype: dictionary
    @rvalue: {'wafer_name', 'rows_num', 'columns_num', 'num_of_testers',
                     'packet_threshold', 'inlay_type', 'charging_time', 'time_per_tag'}
    """
    filename = 'tester_gui_inputs_do_not_delete.p'
    file_exists = os.path.isfile(filename)
    
    if file_exists:
        f = open(filename, "rb")
        js = pickle.load(f)
        f.close()
    
    else:
        f = open(filename, "w")
        js = {}
        f.close()
    
    default_values = {}
    # setting the values from previous runs
    values_to_get = {'wafer_name': 'No', 'rows_num': '', 'columns_num': '', 'num_of_testers': '1',
                     'packet_threshold': '1', 'inlay_type': 'Single Band', 'charging_time': '2', 'time_per_tag': '0.25'}
    for val in values_to_get.keys():
        try:
            if js[val] is not None:
                default_values[val] = js[val]
            else:
                default_values[val] = values_to_get[val]
        except Exception:
            default_values[val] = values_to_get[val]
    
    layout = [
        [sg.Text('Wafer name:', font=4)],
        [sg.InputText(default_values['wafer_name'], key='wafer_name', font=4)],
        [sg.Text('Number of tester:', font=4)],
        [sg.InputCombo(('1', '2'), default_value=default_values['num_of_testers'], key='num_of_testers')],
        [sg.Text('inlay type:', font=4)],
        [sg.InputCombo(('Single Band', 'Dual Band'), default_value=default_values['inlay_type'], key='inlay_type')],
        [sg.Text('Rows number (reels number):', font=4)],
        [sg.InputText(default_values['rows_num'], key='rows_num', font=4)],
        [sg.Text('Columns number (at machine direction):', font=4)],
        [sg.InputText(default_values['columns_num'], key='columns_num', font=4)],
        [sg.Text('Packet threshold:', font=4)],
        [sg.InputText(default_values['packet_threshold'], key='packet_threshold', font=4)],
        [sg.Text('Charging time (in seconds):', font=4)],
        [sg.InputText(default_values['charging_time'], key='charging_time', font=4)],
        [sg.Text('Time per tag (in seconds):', font=4)],
        [sg.InputText(default_values['time_per_tag'], key='time_per_tag', font=4)],
        [sg.Submit()]]
    
    window = sg.Window('Settings', layout)
    while True:
        event, values = window.read()
        try:
            if event == 'WIN_CLOSED' or event is None:
                print('Opening GUI was closed, the program will end now.')
                values = 'exit'
                break
            else:
                # make sure the user entered valid values
                int(values['columns_num'])
                int(values['rows_num'])
                int(values['num_of_testers'])
                int(values['packet_threshold'])
                float(values['charging_time'])
                float(values['time_per_tag'])
                break
        except Exception:
            if event == 'WIN_CLOSED' or event is None:
                print('Opening GUI was closed, the program will end now.')
                values = 'exit'
                break
            else:
                print('event = ' + str(event))
                print('please insert an integer number to packet_threshold, rows, columns and testers values')
                print('and float number to charging_time and time_per_tag values')
    window.close()
    # if the user pressed esc.
    if values == 'exit':
        sys.exit(0)
    pickle.dump(values, open(filename, "wb"))
    return values


def conclusion(yield_):
    """ opens conclusion GUI
    @type yield_: float
    @param yield_: final yield in percentage
    """
    if yield_ > 20:
        layout = [
            [sg.Text('Yield = ' + str(yield_) + '%', font=4)],
            [sg.Text('Good job!!', font=4)],
            [sg.Exit()]]
        sg.ChangeLookAndFeel('Green')
    
    else:
        layout = [
            [sg.Text('Yield = ' + str(yield_) + '%', font=4)],
            [sg.Text('Please update Wiliot', font=4)],
            [sg.Exit()]]
        sg.ChangeLookAndFeel('DarkRed')
    
    window2 = sg.Window('Conclusion', layout)
    event, values = window2.read()
    window2.close()


#################################################################
#                      Configurations data                      #
#################################################################

class ConfigDefaults(object):
    """
    contains the default values for the configuration json
    """
    
    def __init__(self):
        self.tester_defaults = {'energizingPattern': '17', 'silenceTimeProfile': [0, 50], 'workTimeProfile': [3, 50]}
        self.charger_defaults = {'energizingPattern': '27', 'silenceTimeProfile': [0, 15], 'workTimeProfile': [7, 15]}
    
    def get_tester_defaults(self):
        return self.tester_defaults
    
    def get_charger_defaults(self):
        return self.charger_defaults
