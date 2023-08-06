#  """
#    Copyright (c) 2016- 2022, Wiliot Ltd. All rights reserved.
#
#    Redistribution and use of the Software in source and binary forms, with or without modification,
#     are permitted provided that the following conditions are met:
#
#       1. Redistributions of source code must retain the above copyright notice,
#       this list of conditions and the following disclaimer.
#
#       2. Redistributions in binary form, except as used in conjunction with
#       Wiliot's Pixel in a product or a Software update for such product, must reproduce
#       the above copyright notice, this list of conditions and the following disclaimer in
#       the documentation and/or other materials provided with the distribution.
#
#       3. Neither the name nor logo of Wiliot, nor the names of the Software's contributors,
#       may be used to endorse or promote products or services derived from this Software,
#       without specific prior written permission.
#
#       4. This Software, with or without modification, must only be used in conjunction
#       with Wiliot's Pixel or with Wiliot's cloud service.
#
#       5. If any Software is provided in binary form under this license, you must not
#       do any of the following:
#       (a) modify, adapt, translate, or create a derivative work of the Software; or
#       (b) reverse engineer, decompile, disassemble, decrypt, or otherwise attempt to
#       discover the source code or non-literal aspects (such as the underlying structure,
#       sequence, organization, ideas, or algorithms) of the Software.
#
#       6. If you create a derivative work and/or improvement of any Software, you hereby
#       irrevocably grant each of Wiliot and its corporate affiliates a worldwide, non-exclusive,
#       royalty-free, fully paid-up, perpetual, irrevocable, assignable, sublicensable
#       right and license to reproduce, use, make, have made, import, distribute, sell,
#       offer for sale, create derivative works of, modify, translate, publicly perform
#       and display, and otherwise commercially exploit such derivative works and improvements
#       (as applicable) in conjunction with Wiliot's products and services.
#
#       7. You represent and warrant that you are not a resident of (and will not use the
#       Software in) a country that the U.S. government has embargoed for use of the Software,
#       nor are you named on the U.S. Treasury Department’s list of Specially Designated
#       Nationals or any other applicable trade sanctioning regulations of any jurisdiction.
#       You must not transfer, export, re-export, import, re-import or divert the Software
#       in violation of any export or re-export control laws and regulations (such as the
#       United States' ITAR, EAR, and OFAC regulations), as well as any applicable import
#       and use restrictions, all as then in effect
#
#     THIS SOFTWARE IS PROVIDED BY WILIOT "AS IS" AND "AS AVAILABLE", AND ANY EXPRESS
#     OR IMPLIED WARRANTIES OR CONDITIONS, INCLUDING, BUT NOT LIMITED TO, ANY IMPLIED
#     WARRANTIES OR CONDITIONS OF MERCHANTABILITY, SATISFACTORY QUALITY, NONINFRINGEMENT,
#     QUIET POSSESSION, FITNESS FOR A PARTICULAR PURPOSE, AND TITLE, ARE DISCLAIMED.
#     IN NO EVENT SHALL WILIOT, ANY OF ITS CORPORATE AFFILIATES OR LICENSORS, AND/OR
#     ANY CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY,
#     OR CONSEQUENTIAL DAMAGES, FOR THE COST OF PROCURING SUBSTITUTE GOODS OR SERVICES,
#     FOR ANY LOSS OF USE OR DATA OR BUSINESS INTERRUPTION, AND/OR FOR ANY ECONOMIC LOSS
#     (SUCH AS LOST PROFITS, REVENUE, ANTICIPATED SAVINGS). THE FOREGOING SHALL APPLY:
#     (A) HOWEVER CAUSED AND REGARDLESS OF THE THEORY OR BASIS LIABILITY, WHETHER IN
#     CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE);
#     (B) EVEN IF ANYONE IS ADVISED OF THE POSSIBILITY OF ANY DAMAGES, LOSSES, OR COSTS; AND
#     (C) EVEN IF ANY REMEDY FAILS OF ITS ESSENTIAL PURPOSE.
#  """

from os.path import isfile, isdir
from tkinter import Tk, INSERT, END, filedialog
import serial.tools.list_ports
import pygubu
import json
import os
import sys
import multiprocessing
import logging
import datetime
import time
import threading

from wiliot.wiliot_core.local_gateway.local_gateway_core import WiliotGateway, StatType, ActionType, DataType
from wiliot.wiliot_tools.local_gateway_gui.utils.gw_macros import macros
from wiliot.wiliot_core.packet_data.tag_collection import TagCollection
from wiliot.wiliot_core.utils import WiliotDir
from wiliot.wiliot_core.packet_data.packet_list import PacketList
from wiliot.wiliot_core.packet_data.packet import Packet

try:
    from wiliot.wiliot_core.packet_data.extended.decrypted_tag_collection import DecryptedTagCollection
    from wiliot.wiliot_tools.extended.pixie_analyzer.pixie_analyzer import PixieAnalyzer
except Exception as e:
    # print(e)
    pass

import csv
from wiliot.get_version import get_version
import re

# default config values:
EP_DEFAULT = 20  # Energizing pattern
EPs_DEFAULT = (1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28,
               50, 51, 52)  # All Energizing pattern
TP_O_DEFAULT = 5  # timing profile on
TP_P_DEFAULT = 15  # timing profile period
PI_DEFAULT = 0  # pace interval
RC_DEFAULT = 37
RCs_DEFAULT = (37, 38, 39)
DATA_TYPES = ('raw', 'processed', 'statistics', 'decoded_packet')
CONFIG_SUM = "EP:{EP}\nTP_ON:{TP_ON}\nTP_P:{TP_P}\nRC:{RC}\nPI:{PI}\nF:{F}"
baud_rates = ["921600"]
energy_pattern_dict = {18: 'Energizing on channel 39 only',
                       20: '20% channel 37 , 80% channel 39',
                       50: 'Energizing in 915Mhz',
                       51: 'Energizing on both channel 39 and 915Mhz',
                       }

__version__ = get_version()


class GatewayUI(object):
    gwCommandsPath = os.path.join(os.path.abspath('utils'), '.gwCommands.json')
    gwUserCommandsPath = os.path.join(os.path.abspath('utils'), '.gwUserCommands.json')
    gwAllCommands = []
    gwCommands = []
    gwUserCommands = []
    filter_state = False
    show_both_screens = False
    portActive = False
    log_state = False
    autoscroll_state = True
    logger = logging.getLogger('root')
    stat_type = StatType.N_FILTERED_PACKETS
    log_path = datetime.datetime.now().strftime("%d-%m-%Y_%H-%M-%S") + 'gw_log.{}'.format("log")

    def __init__(self, main_app_folder='', array_out=None, tk_frame=None):
        print('GW UI mode is activated')
        print(__version__)
        self.busy_processing = False
        self.close_requested = False
        # 1: Create a builder
        self.builder = builder = pygubu.Builder()
        self.multi_tag = TagCollection()
        self.filter_tag = ['']

        try:
            self.myPixieAnalyzer = PixieAnalyzer()
            self.packet_decoder = self.myPixieAnalyzer.PacketDecoder()
        except Exception as e:
            self.myPixieAnalyzer = None

        self.env_dir = WiliotDir()
        self.logs_dir = os.path.join(self.env_dir.get_tester_dir("local_gateway_gui"), "logs")
        if not isdir(self.logs_dir):
            self.env_dir.create_dir(self.logs_dir)

        # 2: Load an ui file
        uifile = os.path.join(os.path.join(os.path.abspath(os.path.dirname(__file__)), 'utils'), 'gw_debugger_v2.ui')
        builder.add_from_file(uifile)

        if tk_frame:
            self.ttk = tk_frame  # tkinter.Frame , pack(fill="both", expand=True)
        else:
            self.ttk = Tk()
        self.ttk.title(f"Wiliot Radio Tester Board GUI Application (V{__version__})")

        # 3: Create the widget using a self.ttk as parent
        self.mainwindow = builder.get_object('mainwindow', self.ttk)

        self.ttk = self.ttk

        # set the scroll bar of the main textbox
        textbox = self.builder.get_object('recv_box')
        scrollbar = self.builder.get_object('scrollbar')
        textbox.configure(yscrollcommand=scrollbar.set)
        scrollbar.configure(command=textbox.yview)
        self.builder.get_object('scrollbar').set(self.builder.get_object('recv_box').index(INSERT),
                                                 self.builder.get_object('recv_box').index(END))
        self.builder.get_object('recv_box').grid()

        self.builder.connect_callbacks(self)

        # upload pre-defined commands
        self.gwCommandsPath = os.path.join(main_app_folder, self.gwCommandsPath)
        if isfile(self.gwCommandsPath):
            with open(self.gwCommandsPath, 'r') as f:
                self.gwCommands = json.load(f)

        self.gwUserCommandsPath = os.path.join(main_app_folder, self.gwUserCommandsPath)
        if isfile(self.gwUserCommandsPath):
            with open(self.gwUserCommandsPath, 'r') as f:
                self.gwUserCommands = json.load(f)

        self.gwAllCommands = self.gwCommands + self.gwUserCommands

        # define array to export data for other applications
        if array_out is None:
            self.data_out = multiprocessing.Queue()
        else:
            self.data_out = array_out

        self.ttk.lift()
        self.ttk.attributes("-topmost", True)
        self.ttk.attributes("-topmost", False)

        self.ObjGW = WiliotGateway(logger_name='root')
        self.config_param = {}
        self.formatter = logging.Formatter('%(asctime)s,%(msecs)d %(name)s %(levelname)s %(message)s', '%H:%M:%S')
        self.logger_num = 1

        # update ui
        if 'wiliot.wiliot_core.packet_data.extended.decrypted_tag_collection' in sys.modules:
            self.decrypted_multi_tag = DecryptedTagCollection()
            self.decryption_mode = True
        else:
            self.decrypted_multi_tag = None
            self.decryption_mode = False
            self.builder.get_object('plot_log')['state'] = 'disabled'
            self.builder.get_object('load_log')['state'] = 'disabled'
            self.builder.get_object('encrypted_process')['state'] = 'disabled'
        self.ui_update('init')
        self.ui_update('available_ports')

        self.ttk.protocol("WM_DELETE_WINDOW", self.close_window)

        self.ttk.after_idle(self.periodic_call)
        self.ttk.mainloop()

    def get_log_file_name(self, filename=None):
        if filename is None:
            filename = self.builder.get_object('log_path').get()
        if filename:
            filename = filename.strip("\u202a")  # strip left-to-right unicode if exists
            return os.path.join(self.logs_dir, filename)
        else:
            return None

    def get_filter_text(self, text=''):
        if len(text) > 0:
            text = text.replace(' ', '')
            self.filter_tag = text.split(',')
        else:
            self.filter_tag = ['']

    def is_filtered(self, packet):
        for f in self.filter_tag:
            # r = re.compile(f.lower())
            filtered_list = re.findall(f.lower(), packet.decoded_data['tag_id'].lower())
            if len(filtered_list) > 0:
                return True
            else:
                return False

    def close_window(self):
        self.close_requested = True
        print("User requested close at:", time.time(), "Was busy processing:", self.busy_processing)

    def periodic_call(self):
        if not self.close_requested:
            self.busy_processing = True
            self.busy_processing = False
            self.ttk.after(500, self.periodic_call)

        else:
            print("Destroying GUI at:", time.time())
            try:
                self.ObjGW.exit_gw_api()
                if self.log_state:
                    logging.FileHandler(self.get_log_file_name()).close()
                self.ttk.destroy()
            except Exception as e:
                print(e)
                exit(1)

    def on_connect(self):
        if not self.portActive:
            try:
                port = self.builder.get_object('port_box').get().rsplit(' ', 1)[0]
                baud = self.builder.get_object('baud_rate_box').get().rsplit(' ', 1)[0]
                if port == '' or baud == '':
                    return

                if self.ObjGW.open_port(port, baud):  # open and check if succeed
                    self.print_function(str_in="> Port successfully opened")
                    self.portActive = True
                    self.builder.get_object('connect_button').configure(text='Disconnect')
                    # print version:
                    self.print_function(str_in=self.ObjGW.hw_version + '=' + self.ObjGW.sw_version)
                    self.builder.get_object('recv_box').see(END)
                    # config gw to receive packets (and not only manage bridges):
                    self.ObjGW.write('!enable_brg_mgmt 0')
                    self.ObjGW.write('!set_tester_mode 1')
                    # update UI:
                    self.ui_update('connect')
                    self.start_listening()

                else:
                    self.print_function(str_in="> Can't open Port - check connection parameters and try again")
                    self.portActive = False
            except Exception as e:
                self.print_function(str_in="> Encounter a problem during connection")
                print(e)

        else:  # Port is open, close it...
            try:
                self.print_function(str_in="> Disconnecting from Port")
                self.ObjGW.exit_gw_api()
                self.builder.get_object('connect_button').configure(text="Connect")
                self.portActive = False
                self.ui_update('connect')
            except Exception as e:
                print(e)

    def start_listening(self):
        # start listening:
        self.ObjGW.start_continuous_listener()
        data_handler_listener = threading.Thread(target=self.recv_data_handler, args=())
        data_handler_listener.start()

    def on_search_ports(self):
        self.ObjGW.available_ports = [s.device for s in serial.tools.list_ports.comports()]
        if len(self.ObjGW.available_ports) == 0:
            self.ObjGW.available_ports = [s.name for s in serial.tools.list_ports.comports()]
        # update ui:
        self.ui_update('available_ports')

    def on_both_screens(self):
        self.show_both_screens = self.builder.get_variable('autoscroll_state').get()
        if self.show_both_screens:
            self.print_function(str_in="> Show data on both screens")
            init_socket_connection_thread = threading.Thread(target=self.ObjGW.init_socket_connection, args=())
            init_socket_connection_thread.start()
        else:
            self.print_function(str_in="> Show data only here")
            self.ObjGW.close_socket_connection()

    @staticmethod
    def string_to_wrap(return_string):
        try:
            indices = [0, 146, 292, 438, 554]
            parts = [return_string[i:j] for i, j in zip(indices, indices[1:] + [None]) if len(return_string[i:j]) > 0]
            return_string = '\n\t'.join(parts)
        except Exception as e:
            return return_string
        return return_string

    def recv_data_handler(self):
        print("DataHandlerProcess Start")
        consecutive_exception_counter = 0
        while True:
            time.sleep(0)
            try:
                if self.close_requested or not self.portActive:
                    print("DataHandlerProcess Stop")
                    return

                # check if there is data to read
                if self.ObjGW.is_data_available():

                    action_type = ActionType.ALL_SAMPLE
                    # get data
                    data_type = DataType.RAW
                    if self.builder.get_object('data_type').get() == 'raw':
                        data_type = DataType.RAW
                    elif self.builder.get_object('data_type').get() == 'processed':
                        data_type = DataType.PROCESSED
                    elif self.builder.get_object('data_type').get() == 'statistics':
                        data_type = DataType.PACKET_LIST
                    elif self.builder.get_object('data_type').get() == 'decoded_packet' and self.decryption_mode:
                        data_type = DataType.DECODED
                    else:
                        data_type = DataType.PROCESSED

                    data_in = self.ObjGW.get_packets(action_type=action_type, num_of_packets=None,
                                                     data_type=data_type, send_to_additional_app=self.show_both_screens)
                    if data_type == DataType.PACKET_LIST:
                        for packet in data_in.packet_list:
                            if any([True if f.lower() in packet.packet_data['adv_address'].lower() else False for f in
                                    self.filter_tag]):
                                self.multi_tag.append(packet)
                            else:
                                continue
                            # self.print_function(str_in=str(d))

                        if int((time.time() % 5)) == 0:
                            # self.on_clear(restart=False)
                            statistics_df = self.multi_tag.get_statistics_list()
                            all_data_str = statistics_df
                            self.print_function(str_in='---------------------- '
                                                       '{}: Tags Statistics '
                                                       '----------------------'.format(datetime.datetime.now()))
                            for d in all_data_str:
                                self.print_function(str_in=str(d))

                    elif data_type == DataType.DECODED:
                        for packet in data_in.packet_list:
                            if packet.get_packet_version() < 2.1:
                                continue
                            if self.is_filtered(packet):
                                self.decrypted_multi_tag.append(packet)

                                self.update_tags_count_label(self.decrypted_multi_tag.get_tags_count())
                            else:
                                continue
                            decrypted_packet = self.decrypted_multi_tag.get_last_added_packet()
                            log_text = decrypted_packet.to_oneline_log()
                            if log_text is None:
                                continue
                            log_text_wrap = self.string_to_wrap(log_text)

                            self.print_function(log_text_wrap)

                            if self.show_both_screens:
                                packet_dict_to_main = {'time': decrypted_packet.gw_data['time_from_start'],
                                                       'raw': decrypted_packet.get_packet_string()}
                                self.data_out.put(packet_dict_to_main)

                    else:
                        if data_type == DataType.PROCESSED:
                            for pkt in data_in:
                                if any([True if f.lower() in pkt['adv_address'].lower() else False for f in
                                        self.filter_tag]):
                                    data_str = []
                                    for key, value in pkt.items():
                                        data_str.append("{} : {}".format(key, value))
                                    all_data_str = ', '.join(data_str)
                                    self.print_function(str_in=all_data_str)
                                    # add it to the JTAG GUI if needed:
                                    if self.show_both_screens:
                                        self.data_out.put(pkt)
                                else:
                                    continue
                        if data_type == DataType.RAW:
                            for pkt in data_in:
                                data_str = []
                                for key, value in pkt.items():
                                    data_str.append("{} : {}".format(key, value))
                                all_data_str = ', '.join(data_str)
                                self.print_function(str_in=all_data_str)
                                # add it to the JTAG GUI if needed:
                                if self.show_both_screens:
                                    self.data_out.put(pkt)
                    consecutive_exception_counter = 0
            except Exception as e:
                print(e)
                print("DataHandlerProcess Exception")
                consecutive_exception_counter = consecutive_exception_counter + 1
                if consecutive_exception_counter > 10:
                    print("Abort DataHandlerProcess")
                    return

    def on_update_gw_version(self):
        self.print_function(str_in="> Updating GW version, please wait...")
        version_path_entry = self.builder.get_object('version_path').get()
        if version_path_entry:
            version_path_entry = version_path_entry.strip("\u202a")  # strip left-to-right unicode if exists
            if not os.path.isfile(version_path_entry):
                self.print_function(str_in="> cannot find the entered gw version file:")
                return

        success_update = self.ObjGW.update_version(versions_path=version_path_entry)
        # listen again:
        self.start_listening()
        if success_update:
            self.print_function(str_in="> Update GW version was completed [{}]".format(self.ObjGW.sw_version))
        else:
            self.print_function(str_in="> Update GW version was failed ")

    def on_reset(self):
        self.ObjGW.reset_gw()
        time.sleep(1)
        self.ObjGW.write('!enable_brg_mgmt 0')
        self.ObjGW.write('!set_tester_mode 1')

    def on_write(self):
        cmd_value = self.builder.get_object('write_box').get()
        rsp_val = self.ObjGW.write(cmd_value)
        self.print_function(', '.join(['{}: {}'.format(k, v) for k, v in rsp_val.items()]))

        if cmd_value.strip() not in list(self.builder.get_object('write_box')['values']):
            temp = list(self.builder.get_object('write_box')['values'])

            # keep only latest instances
            if temp.__len__() == 20:
                temp.pop(0)
            if len(self.gwUserCommands) >= 20:
                self.gwUserCommands.pop(0)
            self.gwUserCommands.append(cmd_value)
            temp.append(cmd_value)
            self.builder.get_object('write_box')['values'] = tuple(temp)
            with open(self.gwUserCommandsPath, 'w+') as f:
                json.dump(self.gwUserCommands, f)

        self.ui_update(state='config')

    def on_run_macro(self):
        selected_macro = self.builder.get_object('macros_ddl').get()
        if selected_macro in macros.keys():
            data_handler_listener = threading.Thread(target=self.run_macro, args=())
            data_handler_listener.start()
        else:
            self.print_function("Please select a valid macro")

    def run_macro(self):
        selected_macro = self.builder.get_object('macros_ddl').get()
        macro_commands = macros[selected_macro]
        for c in macro_commands:
            command_value = c["command"]
            time_value = c["wait"]
            self.print_function("Command: {c},\t Wait: {t}".format(c=command_value, t=time_value))
            command_start_time = time.time()
            rsp_val = self.ObjGW.write(command_value)
            self.print_function(', '.join(['{}: {}'.format(k, v) for k, v in rsp_val.items()]))
            # self.start_listening()
            while time.time() - command_start_time < time_value:
                time.sleep(1)
        self.print_function('Macro {selected_macro} Done.'.format(selected_macro=selected_macro))

    def on_config(self):
        filter_val = self.filter_state
        pacer_val = int(self.builder.get_object('pace_inter').get())
        energ_ptrn_val = int(self.builder.get_object('energizing_pattern').get())

        time_profile_val = [int(self.builder.get_object('timing_profile_on').get()),
                            int(self.builder.get_object('timing_profile_period').get())]
        received_channel_val = int(self.builder.get_object('received_channel').get())
        self.print_function(str_in="> Setting GW configuration...")
        if energ_ptrn_val in energy_pattern_dict.keys():
            self.print_function(str_in='Setting pattern {energ_ptrn_val} -> {pattern_explanation}'.format(
                energ_ptrn_val=str(energ_ptrn_val), pattern_explanation=energy_pattern_dict[energ_ptrn_val]))

        config_param_set, gateway_response = self.ObjGW.config_gw(filter_val=filter_val, pacer_val=pacer_val,
                                                                  energy_pattern_val=energ_ptrn_val,
                                                                  time_profile_val=time_profile_val,
                                                                  received_channel=received_channel_val)
        # update config parameters:
        for key, value in config_param_set.__dict__.items():
            if key == 'filter' or key == 'modulation':
                self.config_param[key] = str(value)[0]
            else:
                self.config_param[key] = str(value)

        self.ui_update(state='config')
        self.print_function(str_in="> Configuration is set")

    def on_set_filter(self):
        self.filter_state = self.builder.get_variable('filter_state').get()
        self.print_function(str_in='> Setting filter...')
        config_param_set, _ = self.ObjGW.config_gw(filter_val=self.filter_state)
        self.config_param["filter"] = str(config_param_set.filter)[0]

        self.ui_update(state='config')

    def on_clear(self, restart=True):
        self.builder.get_object('recv_box').delete('1.0', END)
        self.builder.get_object('recv_box').see(END)
        self.update_tags_count_label(0)
        if restart:
            self.multi_tag = TagCollection()
            if self.decryption_mode:
                self.decrypted_multi_tag = DecryptedTagCollection()

    def set_logger(self, level=logging.DEBUG):
        """
        setup logger to allow running multiple logger
        """
        handler = logging.FileHandler(self.get_log_file_name())
        handler.setFormatter(self.formatter)

        self.logger = logging.getLogger('logger{}'.format(self.logger_num))
        self.logger.setLevel(level)
        self.logger.addHandler(handler)
        self.logger_num = self.logger_num + 1

    def on_filter_id(self, args):
        if args.char == '\r':
            f_input = self.builder.get_object('filter_id').get()
            if not f_input == 'filter ids' and not f_input == '':
                self.get_filter_text(f_input)

    def on_log(self):
        self.log_state = not self.log_state
        if self.log_state:
            check_log_path = self.get_log_file_name()
            if not check_log_path:
                self.log_state = False
                self.print_function(str_in='> Log path is invalid')
                self.builder.get_object('log_button')['text'] = 'Start Log'
                return
            try:
                self.set_logger()

                self.print_function(str_in='> Start Logging [{}]'.format(self.get_log_file_name()))
                self.builder.get_object('log_button')['text'] = 'Stop Log'
                return
            except Exception as e:
                print(e)
                self.print_function(str_in='> Log path is invalid')
                self.log_state = False
                self.builder.get_object('log_button')['text'] = 'Start Log'
                return
        else:
            self.builder.get_object('log_button')['text'] = 'Start Log'
            self.print_function(str_in='> Stop Logging')
            logging.FileHandler(self.get_log_file_name()).close()
            self.on_processed_data(output_path=self.get_log_file_name())

            self.log_path = datetime.datetime.now().strftime("%d-%m-%Y_%H-%M-%S") + 'gw_log.{}'.format("log")
            self.builder.get_object('log_path').delete(0, 'end')
            self.builder.get_object('log_path').insert(END, self.log_path)

    def on_autoscroll(self):
        self.autoscroll_state = self.builder.get_variable('autoscroll_state').get()

    def on_data_type_change(self, selected):
        if selected.widget.get() == 'decoded_packet':
            self.builder.get_object('plot_log')['state'] = 'enabled'
            self.builder.get_object('filter_id')['state'] = 'enabled'
            self.builder.get_object('filter_id').insert(0, 'filter ids')
            self.builder.get_object('encrypted_process')['state'] = 'enabled'
            self.on_clear()

            self.update_tags_count_label(0)
        else:
            self.builder.get_object('filter_id').delete(0, 'end')
            self.builder.get_object('filter_id')['state'] = 'disabled'
            self.builder.get_object('plot_log')['state'] = 'disabled'
            self.builder.get_object('encrypted_process')['state'] = 'disabled'
            self.update_tags_count_label(clear=True)

    def update_tags_count_label(self, count=0, clear=False):
        text_obj = self.builder.get_object('tags_count')
        text_obj.delete("end")
        if clear:
            text_obj.insert(END, "\n".format(
                tag_format=str(count)))
        else:
            text_obj.insert(END, "\ntags count: {tag_format}".format(
                tag_format=str(count)))
        text_obj.see(END)

    def on_plot_log(self):
        plots_location = filedialog.askdirectory(initialdir="~/Documents",
                                                 title="Choose output location")
        if plots_location != '':
            if len(self.decrypted_multi_tag) > 0:
                try:
                    self.print_function(str_in="Starting plot analyzing")
                    start = time.time()
                    self.myPixieAnalyzer.plot_graphs(plot_data=self.decrypted_multi_tag, user_event=[],
                                                     show_plots=True,
                                                     out_path=plots_location)
                    # PlotGraphsGen2(plot_data, user_event)
                    end = time.time()
                    self.print_function(str_in='PlotGraphsGen2: {t}'.format(t=round(end - start, 2)))
                    self.print_function(
                        str_in='Plot files saved in {plots_location}'.format(plots_location=plots_location))
                except PermissionError as pe:
                    self.print_function(
                        str_in='Got "{strerror}" in folder: {plots_location}'.format(strerror=pe.strerror,
                                                                                     plots_location=plots_location))
                except Exception as e:
                    self.print_function(str_in='Unknown error')

            else:
                self.print_function(str_in='No packets received in decoded_packet mode yet.')
        else:
            self.print_function(str_in='No output location selected.')

    def on_load_log(self):
        file_path_input = filedialog.askopenfilename(initialdir="~/Documents",
                                                     title="Select packet log input file",
                                                     filetypes=[("csv files", "*.csv")])
        plots_location = filedialog.askdirectory(initialdir="~/Documents",
                                                 title="Choose output location")
        if plots_location != '':
            if '_plot.csv' not in file_path_input:
                self.print_function(str_in='Invalid file, choose *_plot.csv file')
            elif file_path_input != '':
                try:
                    self.print_function(str_in="Starting plot analyzing")
                    start = time.time()
                    [_, plot_data, user_event] = self.packet_decoder.parse(
                        input=file_path_input)
                    end = time.time()
                    self.print_function(str_in='PlotGraphsGen2: {t}'.format(t=round(end - start, 2)))

                    start = time.time()
                    self.myPixieAnalyzer.plot_graphs(plot_data=plot_data, user_event=user_event, show_plots=False,
                                                     out_path=plots_location)
                    # PlotGraphsGen2(plot_data, user_event)
                    end = time.time()
                    self.print_function(str_in='PlotGraphsGen2: {t}'.format(t=round(end - start, 2)))
                    self.print_function(
                        str_in='Plot files saved in {plots_location}'.format(plots_location=plots_location))
                except Exception as e:
                    self.print_function(str_in=e.__str__())
            else:
                self.print_function(str_in='No file selected.')
        else:
            self.print_function(str_in='No output location selected.')

    def extract_packet_list_from_log(self, log_path=None):
        packet_list = PacketList()
        packets, packets_time = self.extract_packets_from_log(log_path=log_path)
        for p, t in zip(packets, packets_time):
            packet_list.append(Packet(raw_packet=p, time_from_start=t))
        return packet_list

    def extract_packets_from_log(self, log_path=None):
        if log_path is None:
            self.print_function(str_in='no log path was found. Export csv failed')
            return
        try:
            packets = []
            packets_time = []
            if isfile(log_path):
                f = open(log_path, 'r')
                lines = f.readlines()

                for line in lines:
                    if 'raw : process_packet("' in line or 'is_valid_tag_packet : True' in line:
                        # a data line
                        if 'raw : process_packet("' in line:
                            re_match = re.search("process_packet\(\"(\w+)\"", line)
                            packet_raw = str(re_match.groups(1)[0])
                        else:  # packet: ABCD format (data type = processed
                            re_match = re.search("\spacket\s:\s(\w+)", line)
                            packet_raw = str(re_match.groups(1)[0])
                        if 'time_from_start : ' in line:
                            re_match = re.search("time_from_start\s:\s(\d+.\d+)", line)
                            packet_time = float(re_match.groups(1)[0])
                        else:
                            re_match = re.search("time\s:\s(\d+.\d+)", line)
                            packet_time = float(re_match.groups(1)[0])

                        packets.append(packet_raw)
                        packets_time.append(packet_time)
                f.close()
            return packets, packets_time
        except Exception as e:
            print(e)
            self.print_function(str_in='export packets from log was failed')
            return None, None

    def create_csv(self, log_path=None):

        def create_config_csv(data_in):
            # create config type:
            comments = '-'  # self.builder.get_object('csv_comment').get()
            if comments == 'add comments':
                comments = '-'
            config_data = {'commonRunName': [common_run_name],
                           'comments': [comments]}
            # generate the csv file:
            with open(log_path.replace('.log', '_config.csv'), 'w', newline='') as f_config:
                writer_cld = csv.writer(f_config)
                writer_cld.writerow(list(config_data.keys()))
                writer_cld.writerows(list(map(list, zip(*[val for val in config_data.values()]))))
                f_config.close()

        if log_path is None:
            self.print_function(str_in='no log path was found. Export csv failed')
            return

        common_run_name = 'gw_gui_' + datetime.datetime.now().strftime("%Y%m%d_%H%M%S")

        try:
            if isfile(log_path):
                packets, packets_time = self.extract_packets_from_log(log_path=log_path)
                if packets is None or packets_time is None:
                    self.print_function(str_in='export csv failed')
                    return

                data_to_csv = {'commonRunName': [common_run_name] * len(packets),
                               'encryptedPacket': packets, 'time': packets_time}

                # generate the csv file:
                with open(log_path.replace('.log', '_data.csv'), 'w', newline='') as f:
                    writer = csv.writer(f)
                    writer.writerow(list(data_to_csv.keys()))
                    writer.writerows(list(map(list, zip(*[val for val in data_to_csv.values()]))))
                    f.close()
                # generate config file according to cloud convention:
                create_config_csv(data_to_csv)
            else:
                self.print_function(str_in='invalid log path: {}\nexport csv was failed'.format(log_path))
        except Exception as e:
            print(e)
            self.print_function(str_in='export csv was failed')

    @staticmethod
    def return_time_str():
        now = datetime.datetime.now()
        # dd/mm/YY H:M:S
        dt_string = now.strftime("%d_%m_%Y__%H_%M_%S")
        return dt_string

    def on_processed_data(self, output_path=None):
        if self.decryption_mode and self.builder.get_object('data_type').get() == 'decoded_packet':
            if len(self.decrypted_multi_tag) > 0:
                if output_path is None:
                    csv_location = filedialog.asksaveasfilename(
                        filetypes=[("txt file", ".csv")], defaultextension=".csv", title='Choose location to save csv',
                        initialfile='{current_date}.csv'.format(current_date=self.return_time_str()))
                else:
                    csv_location = output_path
                if csv_location != '':
                    try:
                        if '.log' in csv_location:
                            csv_location = csv_location.replace('.log', '.csv')
                        csv_location = csv_location.replace('.csv', '_plot.csv')
                        self.decrypted_multi_tag.to_csv(csv_location)
                        self.print_function(
                            str_in='Export multi-tag csv - {path}'.format(
                                path=csv_location))
                    except Exception as e:
                        self.print_function(str_in=e.__str__())
                else:
                    self.print_function(str_in='No output location selected.')
            else:
                self.print_function(str_in='No packets received in decoded_packet mode yet.')
        else:
            if output_path is not None:
                log_path = output_path
            else:
                log_path = self.get_log_file_name()
            try:
                if self.decryption_mode and self.builder.get_object('data_type').get() == 'decoded_packet':
                    self.decrypted_multi_tag.to_csv(log_path.replace('.log', '_plot.csv'))
                    self.print_function(
                        str_in='export multi-tag csv - {path}'.format(
                            path=log_path.replace('.log', '_plot.csv')))
                    print(log_path.replace('.log', '_plot.csv'))
                else:
                    processed_log_path = log_path.replace('.log', '_packet_process.csv')
                    packet_list = self.extract_packet_list_from_log(log_path=log_path)
                    packet_list.to_csv(processed_log_path)
                    mt_processed_log_path = log_path.replace('.log', '_statistics_process.csv')
                    mt = TagCollection()
                    for packet in packet_list:
                        mt.append(packet)
                    stat_df = mt.get_statistics()
                    stat_df.to_csv(path_or_buf=mt_processed_log_path)
                    # check if csv file was created
                    if isfile(processed_log_path):
                        self.print_function('processed csv file was created: {}'.format(processed_log_path))
                    else:
                        self.print_function('processed csv file was not created')
                    if isfile(mt_processed_log_path):
                        self.print_function('multi tag csv file was created: {}'.format(mt_processed_log_path))
                    else:
                        self.print_function('multi tag csv file was not created')
            except Exception as e:
                self.print_function('processed csv file was failed due to: {}'.format(e))
                return

    def ui_update(self, state):
        # updating UI according to the new state
        if state == 'init':
            self.builder.get_object('write_box')['values'] = tuple(self.gwAllCommands)
            self.builder.get_object('macros_ddl')['values'] = tuple(macros.keys())
            # default config values:
            self.builder.get_object('energizing_pattern')['values'] = tuple(EPs_DEFAULT)
            self.builder.get_object('energizing_pattern').set(EP_DEFAULT)
            self.builder.get_object('timing_profile_on').set(TP_O_DEFAULT)
            self.builder.get_object('timing_profile_period').set(TP_P_DEFAULT)
            self.builder.get_object('pace_inter').set(PI_DEFAULT)
            self.builder.get_object('received_channel')['values'] = tuple(RCs_DEFAULT)
            self.builder.get_object('received_channel').set(RC_DEFAULT)

            self.config_param = {"energy_pattern": str(EP_DEFAULT),
                                 "received_channel": str(RC_DEFAULT),
                                 "time_profile_on": str(TP_O_DEFAULT),
                                 "time_profile_period": str(TP_P_DEFAULT),
                                 "pacer_val": str(PI_DEFAULT),
                                 "filter": "N"}

            self.builder.get_object('config_sum').insert(END, CONFIG_SUM.format(
                RC="", EP="", TP_ON="", TP_P="", PI="", F=""))
            self.builder.get_object('config_sum').see(END)
            if self.decryption_mode:
                self.builder.get_object('data_type')['values'] = tuple(DATA_TYPES)
            else:
                self.builder.get_object('data_type')['values'] = tuple(DATA_TYPES[:-1])
            self.builder.get_object('data_type').set('raw')

            self.builder.get_object('log_button')['text'] = 'Start Log'
            self.builder.get_object('log_path').insert(END, self.log_path)

            self.builder.get_variable('autoscroll_state').set(self.autoscroll_state)
            self.builder.get_variable('both_screens_state').set(self.show_both_screens)
            self.builder.get_object('encrypted_process')['state'] = 'disabled'
            self.builder.get_object('plot_log')['state'] = 'disabled'
            self.builder.get_object('filter_id').delete(0, 'end')
            self.builder.get_object('filter_id')['state'] = 'disabled'
            if self.decryption_mode:
                self.builder.get_object('load_log')['state'] = 'enabled'
            else:
                self.builder.get_object('load_log')['state'] = 'disabled'

            ver_num, _ = self.ObjGW.get_latest_version_number()
            if ver_num is not None:
                self.builder.get_object('version_num').insert(END, 'new:' + ver_num)
            self.builder.get_object('version_num_cur').insert(END, 'current:')

        elif state == 'available_ports':
            if self.ObjGW.available_ports:
                self.print_function(str_in=f'> Finished searching for ports, available ports: '
                                           f'{", ".join(self.ObjGW.available_ports)}')
                self.builder.get_object('port_box')['values'] = tuple(self.ObjGW.available_ports)
            else:
                self.print_function(str_in="no serial ports were found. please check your connections and refresh")
            self.builder.get_object('baud_rate_box')['values'] = tuple(baud_rates)
            self.builder.get_object('port_box')['state'] = 'enabled'
            self.builder.get_object('baud_rate_box')['state'] = 'enabled'
            self.builder.get_object('baud_rate_box').set(baud_rates[0])

        elif state == 'connect':
            if self.portActive:
                # connected
                enable_disable_str = 'enabled'
                enable_disable_con_str = 'disabled'
                self.builder.get_object('version_num_cur').delete('1.0', END)
                self.builder.get_object('version_num_cur').insert(END, 'current:' + self.ObjGW.sw_version)
            else:
                # disconnected
                enable_disable_str = 'disabled'
                enable_disable_con_str = 'enabled'
                self.builder.get_object('version_num_cur').delete('1.0', END)
                self.builder.get_object('version_num_cur').insert(END, 'current:')

            self.builder.get_object('config_button')['state'] = enable_disable_str
            self.builder.get_object('energizing_pattern')['state'] = enable_disable_str
            self.builder.get_object('timing_profile_on')['state'] = enable_disable_str
            self.builder.get_object('timing_profile_period')['state'] = enable_disable_str
            self.builder.get_object('pace_inter')['state'] = enable_disable_str
            self.builder.get_object('set_filter')['state'] = enable_disable_str
            self.builder.get_object('write_button')['state'] = enable_disable_str
            self.builder.get_object('write_box')['state'] = enable_disable_str
            self.builder.get_object('macros_ddl')['state'] = enable_disable_str
            self.builder.get_object('run_macro')['state'] = enable_disable_str
            self.builder.get_object('reset_button')['state'] = enable_disable_str
            self.builder.get_object('show_both_screen')['state'] = enable_disable_str
            self.builder.get_object('received_channel')['state'] = enable_disable_str
            self.builder.get_object('data_type')['state'] = enable_disable_str
            self.builder.get_object('update_button')['state'] = enable_disable_str
            self.builder.get_object('version_path')['state'] = enable_disable_str

            self.builder.get_object('port_box')['state'] = enable_disable_con_str
            self.builder.get_object('baud_rate_box')['state'] = enable_disable_con_str

        elif state == 'config':
            self.builder.get_object('config_sum').delete(1.0, END)
            self.builder.get_object('config_sum').insert(END,
                                                         CONFIG_SUM.format(RC=self.config_param["received_channel"],
                                                                           EP=self.config_param["energy_pattern"],
                                                                           TP_ON=self.config_param["time_profile_on"],
                                                                           TP_P=self.config_param[
                                                                               "time_profile_period"],
                                                                           PI=self.config_param["pacer_val"],
                                                                           F=self.config_param["filter"]))
            self.builder.get_object('config_sum').see(END)

    def print_function(self, str_in):
        self.builder.get_object('recv_box').insert(END, str_in + '\n')
        if self.autoscroll_state:
            self.builder.get_object('recv_box').see(END)
        if self.log_state:
            self.logger.info(str_in)


if __name__ == '__main__':
    # Run the UI
    GWApp = GatewayUI()
