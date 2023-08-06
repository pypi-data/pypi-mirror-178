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

import os
import csv
from appdirs import user_data_dir
import logging
from enum import Enum
import json
import pathlib
import PySimpleGUI as SimGUI


class WiliotDir:
    
    def __init__(self) -> None:
        self.local_appdata_dir = ''
        self.wiliot_root_path = ''
        self.common_dir_path = ''
        self.config_dir_path = ''
        self.user_config_path = ''
        self.tester_subdirectories = ['results', 'logs', 'configs']
        
        self.set_dir()
        self.create_dir(self.local_appdata_dir)
        self.create_dir(self.wiliot_root_path)
        self.create_dir(self.common_dir_path)
        self.create_dir(self.config_dir_path)
    
    def set_dir(self):
        try:
            if 'WILIOT_APP_ROOT_PATH' in os.environ.keys():
                print(os.environ['WILIOT_APP_ROOT_PATH'])
                self.wiliot_root_path = os.environ['WILIOT_APP_ROOT_PATH']
            else:
                self.local_appdata_dir = user_data_dir()
                self.wiliot_root_path = os.path.join(self.local_appdata_dir, 'wiliot')
            
            self.common_dir_path = os.path.join(self.wiliot_root_path, 'common')
            self.config_dir_path = os.path.join(self.common_dir_path, 'configs')
            self.user_config_path = os.path.join(self.config_dir_path, 'user_configs.json')
        
        except Exception as e:
            logging.warning('Error loading environment or getting in from OS, supporting Windows, Linux and MacOS '
                            '({})'.format(e))
    
    @staticmethod
    def create_dir(path):
        if not os.path.exists(path):
            os.makedirs(path)
    
    def create_tester_dir(self, tester_name):
        tester_path = self.get_tester_dir(tester_name)
        self.create_dir(tester_path)
        
        for subdir in self.tester_subdirectories:
            self.create_dir(tester_path + '/' + subdir)
    
    def get_tester_dir(self, tester_name):
        wiliot_path = self.wiliot_root_path
        tester_path = os.path.join(wiliot_path, tester_name)
        return tester_path
    
    def get_dir(self):
        return self.wiliot_root_path, self.common_dir_path, self.config_dir_path, self.user_config_path
    
    def get_wiliot_root_app_dir(self):
        return self.wiliot_root_path
    
    def get_common_dir(self):
        return self.common_dir_path
    
    def get_config_dir(self):
        return self.config_dir_path
    
    def get_user_config_file(self):
        return self.user_config_path


def open_json(folder_path, file_path, default_values=None):
    """
    opens config json
    :type folder_path: string
    :param folder_path: the folder path which contains the desired file
    :type file_path: string
    :param file_path: the file path which contains the json
            (including the folder [file_path = folder_path+"json_file.json"])
    :type default_values: dictionary
    :param default_values: default values for the case of empty json
    :return: the desired json object
    """
    if not os.path.exists(folder_path):
        pathlib.Path(folder_path).mkdir(parents=True, exist_ok=True)
    
    file_exists = os.path.isfile(file_path)
    if not file_exists or os.stat(file_path).st_size == 0:
        # save the default values to json
        with open(file_path, "w") as out_file:
            json.dump(default_values, out_file)
        
        return json.load(open(file_path, "rb"))
    else:
        with open(file_path) as f:
            json_content = f.read()
        if len(json_content) == 0:
            with open(file_path, "w") as out_file:
                json.dump(default_values, out_file)
            json_content = json.load(open(file_path, "rb"))
        else:
            json_content = json.loads(json_content)
        return json_content


def credentials_gui():
    """
    open GUI for getting user_name, password and owner_id from user
    """
    layout = [
        [SimGUI.Text('Please insert FusionAuth Credentials')],
        [SimGUI.Text('User name (email address):'),
         SimGUI.InputText('', key='user_name')],
        [SimGUI.Text('Password:'),
         SimGUI.InputText('', key='password', password_char='*')],
        [SimGUI.Text('Owner Id:'),
         SimGUI.InputText('wiliot-ops', key='owner_id')],
        [SimGUI.Submit()]]
    
    window = SimGUI.Window('User Credentials', layout)
    while True:
        event, values = window.read()
        if event == 'Submit':
            break
        elif event is None:
            print('User exited the program')
            window.close()
            exit()
    
    window.close()
    return values


def check_user_config_is_ok():
    """
    checks if the user_config.json is valid
    :return: file_path, user_name, password, owner_id, is_successful
    (True if user_config_path has the parameters
    ("UserName", "Password", "OwnerId") False otherwise)
    """
    # Create wiliot appdata directory if not exists:
    is_success = False
    user_name, password, owner_id = None, None, None
    env_dirs = WiliotDir()
    config_dir_path = env_dirs.get_config_dir()
    user_config_file_path = env_dirs.get_user_config_file()
    
    if not os.path.isdir(config_dir_path):
        pathlib.Path(config_dir_path).mkdir(parents=True, exist_ok=True)
    auth_gui_is_needed = False
    if os.path.exists(user_config_file_path):
        cfg_data = open_json(folder_path=config_dir_path, file_path=user_config_file_path)
        try:
            user_name = cfg_data['UserName']
            password = cfg_data['Password']
            owner_id = cfg_data['OwnerId']
            if user_name == '' or password == '' or owner_id == '':
                print('user_name or password are empty. Please enter it manually\n')
                is_success = False
                auth_gui_is_needed = True
            else:
                is_success = True
        except Exception as e:
            auth_gui_is_needed = True
            
            print("Config file is not readable at path {}. Exception {}\n Please enter new credentials".format(
                user_config_file_path, e))
    else:
        print("Config file user_configs.json doesn't exist at {}\n".format(config_dir_path))
        auth_gui_is_needed = True
    
    while auth_gui_is_needed:
        auth_gui_is_needed = False
        values = credentials_gui()
        user_name = values['user_name']
        password = values['password']
        owner_id = values['owner_id']
        if user_name == '' or password == '' or owner_id == '':
            print('user_name or password are empty. Please try again\n')
            auth_gui_is_needed = True
        else:
            with open(user_config_file_path, 'w') as cfg:
                json.dump({"UserName": user_name, "Password": password,
                           "OwnerId": owner_id}, cfg)
            is_success = True
    return user_config_file_path, user_name, password, owner_id, is_success


def csv_to_dict(path=None):
    if path:
        with open(path, 'r') as f:
            reader = csv.DictReader(f, delimiter=',')
            col_names = reader.fieldnames
            data_out = {col: [] for col in col_names}
            try:
                for row in reader:
                    for col in col_names:
                        data_out[col].append(row[col])
            except Exception as e:
                print("couldn't load csv due to {}".format(e))
        return data_out
    else:
        print('please provide a path')
        return None


if __name__ == '__main__':
    pass
