import numpy as np
import pandas as pd
from pandas.core.series import Series
import re
import datetime

from wiliot.wiliot_core.packet_data.extended.decrypted_tag_collection import DecryptedTagCollection
from wiliot.wiliot_core.packet_data.extended.decrypted_packet_list import DecryptedPacketList
from wiliot.wiliot_core.packet_data.extended.decrypted_packet import DecryptedPacket
from wiliot.wiliot_testers.post_process.utils.process_table_config import table_config
from wiliot.wiliot_testers.wiliot_tester_tag_result import FailureCodes
from wiliot.wiliot_testers.post_process.utils.column_name_map import column_name_map
from wiliot.wiliot_core.local_gateway.local_gateway_core import valid_output_power_vals
from wiliot.get_version import get_version

alpha_packet_fields = ['common_run_name', 'external_id', 'selected_tag', 'fail_bin_str',
                       'test_start_time', 'trigger_time', 'test_end_time']


def time_diff_between_two_strings(late=None, early=None):
    time_to_covert = [late, early]
    t_conv_arr = []
    for t_str in time_to_covert:
        if t_str is None or t_str == '':
            return None
        try:
            t_conv = datetime.datetime.strptime(t_str, "%Y-%m-%d %H:%M:%S.%f")
        except ValueError:
            try:
                t_conv = datetime.datetime.strptime(t_str, "%Y-%m-%d %H:%M:%S")
            except Exception as e:
                print('could not convert time string:{}, due to {}'.format(t_str, e))
                return None
        except Exception as e:
            print('could not convert time string:{}, due to {}'.format(t_str, e))
            return None
        t_conv_arr.append(t_conv)
    time_diff = t_conv_arr[0] - t_conv_arr[1]
    return time_diff.total_seconds()


def string_to_number(list_in, name):
    """

    :param list_in:
    :type list_in:
    :param name:
    :type name:str
    :return:
    :rtype: list
    """
    if isinstance(list_in, list):
        pass
    elif isinstance(list_in, np.ndarray):
        list_in = list_in.tolist()
    elif isinstance(list_in, str) or isinstance(list_in, np.str_):
        list_in = [str(list_in)]
    elif isinstance(list_in, int) or isinstance(list_in, float) or list_in is None:
        return [list_in]
    else:
        raise Exception('pp: string_to_number: unsupported list_in type: {} for list:{}'.format(type(list_in), list_in))
    
    if name in alpha_packet_fields:
        return list_in
    
    converted_list = []
    for element in list_in:
        if element == '':
            converted_list.append(None)
        elif (isinstance(element, str) or isinstance(list_in, np.str_)) and element.lower() != element.upper():
            # element contains letters
            converted_list.append(element)
        else:
            try:
                num_element = float(element)
                if num_element == float('nan') or num_element == float('inf'):
                    converted_list.append(element)
                else:
                    converted_list.append(num_element)
            except ValueError:
                converted_list.append(element)
    
    return converted_list


def snake_to_camel_dict_keys(dict_in):
    """
    this function copied the input dictionary and replace the keys to camel case
    :param dict_in: input dictionary
    :type dict_in: dict
    :return: same dictionary with camel case keys
    :rtype: dict
    """
    dict_out = {}
    for key, val in dict_in.items():  # copy the raw data
        if '_' in key:
            key = ''.join(x.capitalize() for x in key.split('_'))
            key = key[:1].lower() + key[1:]
        dict_out[key] = val
    return dict_out


def get_payload(packet):
    if (isinstance(packet, str) or isinstance(packet, np.str_)) and len(packet) >= 74:
        return packet[16:74]
    else:
        raise Exception('pp: get_payload: Try to extract payload from invalid packet: {}'.format(packet))


def get_group_id_reversed(group_id_list=None):
    """

    :param group_id_list: list of group ids
    :type group_id_list: list
    :return:
    :rtype:
    """
    if group_id_list is None:
        return None
    return [group_id[-2:] + group_id[-4:-2] + group_id[-6:-4] for group_id in group_id_list]


def get_converted_flow_version(flow_ver_list=None):
    if flow_ver_list is None:
        return None
    converted_flow_ver = []
    for fv in flow_ver_list:
        fv = fv[2::]  # removing the '0x'
        converted_flow_ver.append((fv[:-2] + "." + fv[-2:]).upper())
    return converted_flow_ver


def reformat_columns_to_row(dict_in):
    """
    This function reformat dict of columns to rows
    :param dict_in: each key of the dict_in is the column name and all the keys contains the same number of elements
    :type dict_in: dict
    :return: dict with key of the column name ('col_name') and key with a list of all the rows ('rows'),
             so each list's element is a row
    :rtype: dict
    """
    dict_out = {'col_name': [], 'rows': []}
    
    dict_out['col_name'] = list(dict_in.keys())
    all_values = []
    # calculate the number of rows
    rows_length = [len(x) for x in dict_in.values() if isinstance(x, list)]
    if rows_length:
        n_rows = max(rows_length)
    else:
        n_rows = 1
    for val in dict_in.values():
        # check if all the columns has the same number of elements:
        if not (isinstance(val, list) or isinstance(val, tuple)):
            val = [val] * n_rows
        elif not len(val):
            val = [None] * n_rows
        else:
            if len(val) != n_rows:
                print('expect for {} rows, but val contain {} rows\nval:{}'.format(n_rows, len(val), val))
                return None
        
        all_values.append(val)
    dict_out['rows'] = list(map(list, zip(*all_values)))
    
    return dict_out


def check_table_type(dict_in, table_type):
    """
    This function check if all element in each column has the desired data type. If not it fixes it
    :param dict_in: dictionary contains all the table columns, each key is a different column
    :type dict_in: dict
    :param table_type: dictionary so each key is the column name and each key's value is the column data type
    :type table_type: dict
    :return: list of the columns type (fixed the dict_in as a mutable variable)
    :rtype: list
    """
    col_type = []
    # check if a value is numpy:
    for key, col in dict_in.items():
        # check if column name exists in the process_table_config.py
        if key not in table_type.keys():
            print('the following parameter will not be inserted to the table: {}'.format(key))
            continue
        for j, element in enumerate(col):
            error_msg = 'pp: check_table_type: we expected to get {} type for {} key, but got: {} (type {})'. \
                format(table_type[key], key, col[j], type(col[j]).__name__)
            # clean numpy types
            if type(element).__module__ == np.__name__:
                if 'str' in type(element).__name__:
                    col[j] = ''.join([char for char in element])
                elif 'float' in type(element).__name__:
                    col[j] = float(element)
                elif 'int' in type(element).__name__:
                    col[j] = int(element)
                elif 'ndarray' in type(element).__name__ and element.size == 1:
                    if 'float' in element.dtype.name:
                        col[j] = float(element)
                    elif 'int' in element.dtype.name:
                        col[j] = int(element)
                    else:
                        col[j] = str(element)
                else:
                    raise Exception("pp: check_table_type: element contains numpy type "
                                    "we didn't handle: " + type(element).__name__)
            # check the type:
            if type(col[j]).__name__ != table_type[key]:  # fix the dict if data type is not according to the config
                if table_type[key] == 'str':
                    if pd.isnull(col[j]):
                        col[j] = ''
                    else:
                        col[j] = str(col[j])
                else:
                    if table_type[key] == 'int' and type(col[j]).__name__ == 'float':
                        if np.isnan(element):
                            col[j] = None
                        elif col[j] is not None and col[j] % 1 == 0:
                            col[j] = int(col[j])  # fix pandas issue when empty cells exist, col is converted to float
                        else:
                            raise Exception(error_msg)
                    
                    elif table_type[key] == 'float' and type(col[j]).__name__ == 'int':
                        col[j] = float(col[j])
                    elif table_type[key] == 'int' and type(col[j]).__name__ == 'NoneType':
                        pass  # None type is considered as int
                    elif table_type[key] == 'int' and type(col[j]).__name__ == 'bool':
                        col[j] = int(col[j])
                    elif table_type[key] == 'float' and type(col[j]).__name__ == 'NoneType':
                        col[j] = float('nan')
                    elif table_type[key] == 'long' and type(col[j]).__name__ == 'int':
                        pass
                    elif table_type[key] == 'bool' and type(col[j]).__name__ == 'NoneType':
                        pass
                    elif table_type[key] == 'timestamp' and type(col[j]).__name__ == 'NoneType':
                        pass
                    elif table_type[key] == 'timestamp' and type(col[j]).__name__ == 'str' and col[j] == '':
                        col[j] = None
                    elif type(col[j]).__name__ == 'str':
                        try:
                            if table_type[key] == 'int' or table_type[key] == 'long':
                                if col[j]:
                                    col[j] = int(float(col[j]))
                                else:
                                    col[j] = None
                            elif table_type[key] == 'float':
                                if col[j]:
                                    col[j] = float(col[j])
                                else:
                                    col[j] = float('nan')
                            elif table_type[key] == 'bool':
                                if col[j].lower() == 'no' or col[j].lower() == 'false':
                                    col[j] = False
                                elif col[j].lower() == 'yes' or col[j].lower() == 'true':
                                    col[j] = True
                                else:
                                    raise Exception(error_msg)
                            elif table_type[key] == 'timestamp':
                                try:
                                    col[j] = datetime.datetime.strptime(col[j], '%Y-%m-%d %H:%M:%S.%f')
                                except ValueError:
                                    raise Exception(error_msg + '(expected format: %Y-%m-%d %H:%M:%S.%f)')
                        
                        except Exception as e:
                            raise Exception(error_msg)
                    
                    else:
                        raise Exception(error_msg)
            if table_type[key] == 'float':
                col[j] = round(col[j], 2)

        col_type.append(table_type[key])
    
    return col_type


def arrange_table_col(dict_in, table_col):
    """
    This function order the input dictionary according to the config file and makes sure all columns exist
    :param dict_in: dictionary contains all the data. each key is the column name and each key's value is a list
                    with all the elements
    :type dict_in: dict
    :param table_col: list with all the columns names with the correct order
    :type table_col: list
    :return: ordered dictionary with all the data
    :rtype: dict
    """
    ordered_dict = {}
    n_rows = max([1] + [len(v) for v in dict_in.values() if isinstance(v, list) or isinstance(v, Series)])
    for k in table_col:
        if k in dict_in.keys():
            ordered_dict[k] = list(dict_in[k])
        else:
            ordered_dict[k] = [''] * n_rows
    
    return ordered_dict


def build_table_for_cloud(dict_in=None, table_type=None):
    if dict_in is None or table_type is None:
        return None
    
    # rearrange dictionary to fit table config:
    sorted_data = arrange_table_col(dict_in=dict_in, table_col=list(table_type.keys()))
    # check col type
    col_type = check_table_type(sorted_data, table_type=table_type)
    # reformat to cloud structure:
    results_out = reformat_columns_to_row(sorted_data)
    if results_out is None or col_type is None:
        print('problem occurred during build_table_for_cloud function')
        return None
    results_out['col_type'] = col_type
    results_out['table_scheme'] = {k: v for k, v in zip(results_out['col_name'], results_out['col_type'])}
    del results_out['col_name'], results_out['col_type']
    
    return results_out


def extract_unique_data(dict_in, name):
    """
    check if name exists in the dict_in according to the column_name_map,
    if it does, it check all values are the same and return the unique value
    :param dict_in:
    :type dict_in: dict or pd.DataFrame
    :param name:
    :type name: str
    :return:
    :rtype:
    """
    
    if name in column_name_map.keys():
        optional_names = column_name_map[name]
    else:
        optional_names = [name]
    
    name_str = None
    for name in optional_names:
        if name in dict_in.keys():
            name_str = name
            break
    
    if name_str is None:
        return None
    
    if isinstance(dict_in[name_str], list) or \
            (isinstance(dict_in[name_str], np.ndarray) and dict_in[name_str].size > 1) or \
            isinstance(dict_in[name_str], Series):
        unique_data = set(dict_in[name_str].copy())
        if len(unique_data) == 1:
            return unique_data.pop()
        else:
            # print('packets from the same sprinkler have different {} data'.format(optional_names))
            return None
    elif isinstance(dict_in[name_str], np.ndarray):
        return dict_in[name_str].item()
    else:
        return dict_in[name_str]


def extract_unique_data_per_tag(decoded_multi_tag, name):
    list_out = []
    for tag_data in decoded_multi_tag.tags.values():
        if name in tag_data.packet_df.keys():
            unique_data = tag_data.packet_df[name].unique()
            unique_data_wo_nan = [x for x in unique_data if not pd.isnull(x)]
            if len(unique_data_wo_nan) == 1:
                list_out.append(unique_data_wo_nan[0])
            else:
                print('tag {} has packets with different {} {}'.format(name, tag_data.packet_df['tag_id'],
                                                                       unique_data_wo_nan))
                list_out.append(None)
        else:
            list_out.append(None)
    
    return list_out


def check_external_id(decoded_packet, process_type=None):
    if process_type == 'offline_test':
        if isinstance(decoded_packet.custom_data['external_id'], np.ndarray):
            for ind, s in enumerate(decoded_packet.custom_data['status_offline']):
                if s == '' or s is None or int(s) == 0:
                    decoded_packet.custom_data['external_id'][ind] = None
        else:
            if decoded_packet.custom_data['status_offline'] == '' or \
                    decoded_packet.custom_data['status_offline'] is None or \
                    int(decoded_packet.custom_data['status_offline']) == 0:
                decoded_packet.custom_data['external_id'] = None


def process_decoded_data(decoded_data=None, run_data=None, process_type=None):
    """

    :param decoded_data:
    :type decoded_data: DecryptedPacketList
    :param run_data:
    :type run_data: dict
    :return:
    :rtype:
    """
    
    # add custom data and generate the multi tag class
    decoded_multi_tag = DecryptedTagCollection()
    
    for decoded_packet in decoded_data:
        decoded_packet.set_inlay_type(extract_unique_data(run_data, 'inlay_type'))
        decoded_packet.decoded_data['tag_id'] = decoded_packet.decoded_data['tag_id'].lower()
        check_external_id(decoded_packet, process_type)
        for k in decoded_packet.custom_data.keys():
            decoded_packet.custom_data[k] = string_to_number(decoded_packet.custom_data[k], k)
        decoded_multi_tag.append(decoded_packet)
    
    return decoded_data, decoded_multi_tag


def parse_test_param(test_param_str):
    """

    :param test_param_str:
    :type test_param_str: str
    :return:
    :rtype: dict
    """
    
    def check_if_array_and_convert(str):
        
        if str[0] == '[':
            arr_str = str.split('[')[1].split(']')[0].split(',')
            if len(arr_str):
                arr = []
                for element in arr_str:
                    arr.append(convert_str(element))
                return True, arr
            else:
                return False, str
        else:
            return False, str
    
    def convert_str(str):
        """
        convert struing to array, int or float
        :param str:
        :type str: str
        :return:
        :rtype:
        """
        p_str = None
        try:
            p_str = int(str)
        except Exception as e:
            pass
        if p_str is None:
            try:
                p_str = float(str)
            except Exception as e:
                pass
        if p_str is None:
            p_str = str.strip("'")
        return p_str
    
    test_param_dict = {}
    names_out_of_dict = ['tests', 'stop_criteria', 'quality_param', 'gw_commands']
    all_keys = re.findall(r"\'([^']+)\':", test_param_str)
    # clean all keys:
    all_keys = [k for k in all_keys if k not in names_out_of_dict]
    test_param_dict = {k: [] for k in all_keys}
    test_param_str_cut = test_param_str
    for key in all_keys:
        try:
            test_param_str_cut = (key + "': ").join(test_param_str_cut.split(key + "': ")[1::])
            if test_param_str_cut[0] == '[':
                val = test_param_str_cut.split(']')
            else:
                val = test_param_str_cut.split(',')
            if len(val) == 1:  # we didn't find the sub-string - maybe the last value:
                val = test_param_str_cut.split('}')
            is_array, p_val = check_if_array_and_convert(val[0])
            if is_array:
                if len(p_val) == 2:
                    if key + '_l' in test_param_dict:
                        test_param_dict[key + '_l'].append(p_val[0])
                        test_param_dict[key + '_u'].append(p_val[1])
                        if key in test_param_dict.keys():
                            del test_param_dict[key]
                    else:
                        test_param_dict[key + '_l'] = [p_val[0]]
                        test_param_dict[key + '_u'] = [p_val[1]]
                        if key in test_param_dict.keys():
                            del test_param_dict[key]
                else:
                    print('got unexpected value from {} (value:{}), if array expect to get range '
                          '(lower and upper limit)')
            else:
                test_param_dict[key].append(convert_str(p_val))
        except Exception as e:
            raise Exception('pp: parse_test_param: from the follow string: {}, '
                            'we got the following exception:{}'.format(test_param_str_cut, e))
    
    # fix length if needed:
    n_test = max([len(v) for v in test_param_dict.values()])
    for key in test_param_dict.keys():
        if len(test_param_dict[key]) != n_test:
            if len(test_param_dict[key]) != 1:
                print('encounter a problem while parsing the test parameters from the following str: ' + test_param_str)
            else:
                test_param_dict[key] = test_param_dict[key] * n_test
    
    return test_param_dict


def create_run_data_table(run_data=None, packet_data=None, processed_dict=None, process_type=None,
                          decoded_packet_list=None,
                          output_dict=None,
                          manufacturing_ver=None, tester_run_id=None):
    """
    the run data is the data of all the test run which include summary of the results, config param and more.
    one row per each run, where run can contains several tests which each test examine several tags

    :param run_data: dictionary of the run data
    :type run_data: dict
    :param process_type: the tester or process type: sample_test, offline_test
    :type process_type: str
    :param decoded_packet_list: output df from the group data calculation
    :type decoded_packet_list: DecryptedPacketList
    :param output_dict: the dictionary output filled with the new tables
    :type output_dict: dict or None
    :param manufacturing_ver: the cloud code version
    :type manufacturing_ver:
    :param tester_run_id: the unique run id received by the cloud
    :type tester_run_id: imt
    :return:
    :rtype: dict
    """
    
    def import_run_data():
        run_table = {}
        for k, v in run_data.items():
            if isinstance(v, list) and len(v) == 1:
                run_table[k] = [str(v[0])]
            else:
                run_table[k] = [str(v)]
        # add run_id and cloud ver:
        if manufacturing_ver:
            run_table['manufacturing_version'] = [str(manufacturing_ver)]
        if tester_run_id:
            run_table['tester_run_id'] = [int(tester_run_id)]
        run_table['post_process_version'] = [get_version()]
        
        return run_table
    
    tables_names = []
    run_results = []
    if run_data is not None and len(run_data):
        # we have data in the input data
        if process_type == 'sample_test':
            table_name = list(table_config[process_type].keys())[0]
            run_data = snake_to_camel_dict_keys(run_data)
            run_table = import_run_data()
            run_results.append(
                build_table_for_cloud(dict_in=run_table, table_type=table_config[process_type][table_name]))
            tables_names.append(table_name)
        
        elif process_type == 'offline_test':
            table_name = list(table_config[process_type].keys())[0]
            table_run_dict = table_config[process_type][table_name]
            run_table = import_run_data()
            if 'reel_run_end_time' in run_table.keys():
                if not run_table['reel_run_end_time'][0]:
                    optional_end_time = [packet_data['test_end_time'][-1], packet_data['test_start_time'][-1],
                                         packet_data['trigger_time'][-1]]
                    for t in optional_end_time:
                        if t:
                            run_table['reel_run_end_time'] = [t]
                            break
            tables_names.append(table_name)
            
            # create run test table:
            table_name = list(table_config[process_type].keys())[1]
            table_run_test_dict = table_config[process_type][table_name]
            run_test_table = {k: [] for k in table_run_test_dict.keys()}
            
            # adding the test param:
            test_param = parse_test_param(run_data['test_suite_dict'][0])
            
            decoded_packet_df = decoded_packet_list.get_df()
            all_tests = list(set(packet_data['test_num'].copy()))
            all_tests = [int(t) for t in all_tests if t != '']
            all_tests.sort()
            packet_df = pd.DataFrame(data=packet_data)
            test_group = packet_df.groupby('test_num')
            for i, test in enumerate(all_tests):
                cur_run_test_table = {}
                test_param_per_test = {k: v[test] for k, v in test_param.items()}
                
                test_df = decoded_packet_df.loc[decoded_packet_df['test_num'] == test]
                test_df_selected = test_df[test_df['selected_tag'].values == test_df['adv_address'].values]
                test_loc_df = test_group.get_group(str(test)).drop_duplicates(subset=['tag_run_location'])
                
                # create the table:
                for col_name in table_run_test_dict.keys():
                    cur_run_test_table[col_name] = extract_unique_data(dict_in=test_param_per_test, name=col_name)
                # calc values:
                cur_run_test_table['tester_run_id'] = int(tester_run_id)
                cur_run_test_table['common_run_name'] = extract_unique_data(test_loc_df, 'common_run_name')
                cur_run_test_table['test_num'] = test
                cur_run_test_table['test_tested'] = \
                    len(test_loc_df) - sum(test_loc_df['fail_bin'] == str(FailureCodes.MISSING_LABEL.value))
                cur_run_test_table['test_passed_offline'] = sum([s == 'True' or s is True or s == 1
                                                                 for s in test_loc_df['is_test_pass'].values])
                if 'absGwTxPowerIndex' in test_param_per_test:
                    cur_run_test_table['test_tx_power_ble_dbm'] = \
                        float(valid_output_power_vals[test_param_per_test['absGwTxPowerIndex']]['abs_power'])
                elif 'absGwTxPower' in test_param_per_test:
                    cur_run_test_table['test_tx_power_ble_dbm'] = float(test_param_per_test['absGwTxPowerIndex'])
                if 'sub1gGwTxPower' in test_param_per_test:
                    cur_run_test_table['test_tx_power_lora_dbm'] = float(test_param_per_test['sub1gGwTxPower'])
                
                if cur_run_test_table['test_post_delay'] is None:
                    cur_run_test_table['test_post_delay'] = 0
                # adding stat
                if len(test_df_selected):
                    test_packet_list = DecryptedPacketList()
                    test_stat = test_packet_list.get_df_statistics(packet_df=test_df_selected)
                    cur_run_test_table['test_min_packets'] = test_param_per_test['num_packets_l']
                    cur_run_test_table['test_res_rssi_avg'] = test_stat['rssi_mean']
                    cur_run_test_table['test_res_tbp_avg'] = test_stat['tbp_mean']
                    all_selected_tags = [tag for tag in set(test_df_selected['selected_tag']) if str(tag) != 'nan']
                    tag_test_df = test_df_selected.groupby('selected_tag')
                    all_min_tx = []
                    for tag in all_selected_tags:
                        stat_cur = test_packet_list.get_df_statistics(packet_df=tag_test_df.get_group(tag))
                        if 'min_tx_last' in stat_cur:
                            all_min_tx.append(stat_cur['min_tx_last'])
                    if len(all_min_tx):
                        cur_run_test_table['test_res_min_tx_frequency_last_avg'] = np.mean(all_min_tx)
                
                # adding cur table to the total table:
                for k, v in cur_run_test_table.items():
                    run_test_table[k].append(v)
            
            # add run dict pp processed:
            fail_bin_per_loc = packet_df.drop_duplicates(subset=['tag_run_location'])['fail_bin']
            run_table['total_run_tested'] = [sum(fail_bin_per_loc != str(FailureCodes.MISSING_LABEL.value))]
            run_table['total_run_responding_tags'] = [sum(processed_dict['num_responding_tags'])]
            run_table['total_run_passed_offline'] = [sum(fail_bin_per_loc == str(FailureCodes.PASS.value))]
            run_table['total_run_passed_post_process'] = [sum([p == 1 for p in processed_dict['status_post_process']])]
            run_table['total_missing_labels'] = [sum([p is None for p in processed_dict['status_post_process']])]
            run_table['run_responsive_tags_yield'] = \
                [100 * (int(run_table['total_run_responding_tags'][0]) / int(run_table['total_run_tested'][0]))]
            run_table['run_offline_yield'] = \
                [100 * (int(run_table['total_run_passed_offline'][0]) / int(run_table['total_run_tested'][0]))]
            run_table['run_post_process_yield'] = \
                [100 * (int(run_table['total_run_passed_post_process'][0]) / int(run_table['total_run_tested'][0]))]
            
            # generate tables for cloud:
            tables_names.append(table_name)
            run_results.append(build_table_for_cloud(dict_in=run_table, table_type=table_run_dict))
            run_results.append(build_table_for_cloud(dict_in=run_test_table, table_type=table_run_test_dict))
        
        else:
            raise Exception('the selected process type ({}) is not supported! '
                            'please select one of the following ["sample_test", "offline_test"]'.format(process_type))
    
    if len(run_results):
        if output_dict is None or output_dict == {}:
            output_dict = {table_name: run_result
                           for run_result, table_name in zip(run_results, tables_names)}
        else:
            for run_result, table_name in zip(run_results, tables_names):
                output_dict[table_name] = run_result
    
    return output_dict


def create_packet_data_tables(decoded_packet_list=None, decoded_multi_tag=None, process_type=None, output_dict=None,
                              tester_run_id=None):
    """

    :param decoded_packet_list:
    :type decoded_packet_list: DecryptedPacketList
    :param decoded_multi_tag:
    :type decoded_multi_tag: DecryptedTagCollection
    :param process_type:
    :type process_type: str
    :param output_dict:
    :type output_dict: dict or None
    :param tester_run_id: the unique run id received by the cloud
    :type tester_run_id: int
    :return:
    :rtype:
    """
    tables_names = []
    packet_results = []
    
    if decoded_packet_list is not None and decoded_multi_tag is not None:
        # we have data in the input data
        
        if process_type == 'sample_test':
            def results_table():
                results_dict = {key: list(value) for key, value in decoded_packet_list.get_df().items()}
                results_dict_camel = snake_to_camel_dict_keys(results_dict)
                # fix according to sample test convention where encryptedPacket is a flag if the packet id
                if 'decryptedPacket' in results_dict_camel.keys():
                    results_dict_camel['encryptedPacket'] = []
                    for decrypted_packet in results_dict_camel['decryptedPacket']:
                        results_dict_camel['encryptedPacket'].append(int(decrypted_packet is not None or
                                                                         not decrypted_packet == ''))
                if 'originalEncryptedPacket' in results_dict_camel.keys():
                    raw_packets = results_dict_camel['originalEncryptedPacket']
                    results_dict_camel['encryptedPayload'] = [get_payload(p) for p in raw_packets]
                
                # fix according to sample test convention tagId -> tagID
                if 'tagId' in results_dict_camel.keys():
                    results_dict_camel['tagID'] = results_dict_camel.pop('tagId')
                # fix according to sample test convention time from start -> time
                if 'timeFromStart' in results_dict_camel.keys():
                    results_dict_camel['time'] = results_dict_camel.pop('timeFromStart')
                # fix according to sample test convention packetVer -> packetVersion
                if 'packetVer' in results_dict_camel.keys():
                    results_dict_camel['packetVersion'] = results_dict_camel.pop('packetVer')
                # fix according to sample test convention packetCntr -> packetCntrVal
                if 'packetCntr' in results_dict_camel.keys():
                    results_dict_camel['packetCtrVal'] = results_dict_camel.pop('packetCntr')
                # fix according to sample test convention flow version
                if 'flowVer' in results_dict_camel.keys():
                    results_dict_camel['vFlow'] = [int(s[2:4], 16) for s in results_dict_camel['flowVer']]
                    results_dict_camel['vMinor'] = [int(s[4::], 16) for s in results_dict_camel['flowVer']]
                if 'groupId' in results_dict_camel.keys():
                    results_dict_camel['groupId'] = get_group_id_reversed(group_id_list=results_dict_camel['groupId'])
                
                return results_dict_camel
            
            def analysis_table():
                analysis_dict = {}
                
                tags_stat = decoded_multi_tag.get_statistics(id_name='tag_id')
                
                analysis_dict['commonRunName'] = \
                    [decoded_packet_list[0].custom_data['common_run_name'][0]] * decoded_multi_tag.__len__()
                analysis_dict['tagID'] = list(tags_stat['tag_id'])
                analysis_dict['TTFP'] = list(tags_stat['ttfp'])
                analysis_dict['timeBetweenSuccessivePacketMs'] = list(tags_stat['tbp_min'])
                analysis_dict['firstPacketCounterValue'] = list(tags_stat['packet_counter_first'])
                analysis_dict['minTXLast'] = list(tags_stat['min_tx_last'])
                analysis_dict['TimeBetweenCyclesAvg'] = list(tags_stat['tbc_mean'])
                analysis_dict['rssiAvg'] = list(tags_stat['rssi_mean'])
                analysis_dict['externalId'] = extract_unique_data_per_tag(decoded_multi_tag, 'external_id')
                analysis_dict['chamber'] = extract_unique_data_per_tag(decoded_multi_tag, 'chamber')
                analysis_dict['state'] = extract_unique_data_per_tag(decoded_multi_tag, column_name_map['state'][0])

                return analysis_dict
            
            # build table for cloud:
            # results table:
            results_table_dict = results_table()
            table_name = list(table_config[process_type].keys())[1]
            packet_results.append(build_table_for_cloud(dict_in=results_table_dict,
                                                        table_type=table_config[process_type][table_name]))
            tables_names.append(table_name)
            # analysis table:
            analysis_packet_list = analysis_table()
            table_name = list(table_config[process_type].keys())[2]
            packet_results.append(build_table_for_cloud(dict_in=analysis_packet_list,
                                                        table_type=table_config[process_type][table_name]))
            tables_names.append(table_name)
        
        elif process_type == 'offline_test':
            table_name = list(table_config[process_type].keys())[4]
            packet_df = decoded_packet_list.get_df()
            packet_df.insert(loc=len(packet_df.columns), column='tester_run_id', value=tester_run_id)
            
            if 'original_encrypted_packet' in packet_df.keys():
                raw_packets = packet_df['original_encrypted_packet']
            else:
                raw_packets = packet_df['raw_packet']
                packet_df.insert(loc=len(packet_df.columns), column='original_encrypted_packet', value=raw_packets)
            encrypted_payload = [get_payload(p) for p in raw_packets]
            packet_df.insert(loc=len(packet_df.columns), column='encrypted_payload', value=encrypted_payload)
            
            if 'time_from_start' in packet_df.keys():
                packet_df.insert(loc=len(packet_df.columns), column='packet_time', value=packet_df['time_from_start'])
            decrypted_packet = []
            for p in packet_df['decrypted_packet']:
                decrypted_packet.append(decoded_packet_list[0].get_packet_content(raw_packet=p, get_gw_data=True))
            
            packet_df['group_id'] = get_group_id_reversed(packet_df['group_id'].values)
            packet_df['flow_ver'] = get_converted_flow_version(packet_df['flow_ver'].values)
            packet_df.drop('decrypted_packet', axis=1, inplace=True)
            packet_df.insert(loc=len(packet_df.columns), column='decrypted_packet', value=decrypted_packet)
            packet_results.append(build_table_for_cloud(dict_in=packet_df.to_dict('series'),
                                                        table_type=table_config[process_type][table_name]))
            tables_names.append(table_name)
        
        else:
            raise Exception('the selected process type ({}) is not supported! '
                            'please select one of the following ["sample_test", "offline_test"]'.format(process_type))
    
    else:
        print('packet data and/or decoded data are empty')
    
    if len(packet_results):
        if output_dict is None or output_dict == {}:
            output_dict = {table_name: packet_result
                           for packet_result, table_name in zip(packet_results, tables_names)}
        else:
            for packet_result, table_name in zip(packet_results, tables_names):
                output_dict[table_name] = packet_result
    
    return output_dict


def check_duplication(df_loc, df_all):
    selected_tag = extract_unique_data(df_loc, 'selected_tag')
    if selected_tag is None:
        raise Exception('pp: check_duplication: tester selected more than one tag '
                        'in loc {}'.format(int(df_loc['tag_run_location'].unique()[0])))
    
    all_tag_id = df_all.loc[df_all['adv_address'] == selected_tag]['tag_id']
    if len(all_tag_id.unique()) == 1:
        return all_tag_id.iloc[0]
    else:
        return None


def create_group_data_tables(decoded_packet_list=None, packet_data=None, process_type=None, output_dict=None):
    """

    :param decoded_packet_list:
    :type decoded_packet_list: DecryptedPacketList
    :param packet_data: dict of all the raw data of packet data file
    :type packet_data: dict
    :param process_type: tester name
    :type process_type: str
    :param output_dict:
    :type output_dict: dict
    :return:
    :rtype:
    """
    tables_names = []
    packet_results = []
    processed_dict = None
    
    if decoded_packet_list is not None:
        # we have data in the input data
        
        if process_type == 'offline_test':
            table_loc_name = list(table_config[process_type].keys())[2]
            table_loc_dict = table_config[process_type][table_loc_name]
            table_test_name = list(table_config[process_type].keys())[3]
            table_test_dict = table_config[process_type][table_test_name]
            # calc tag location table
            packet_df = decoded_packet_list.get_df()
            all_locations = [int(loc) for loc in set(packet_data['tag_run_location'].copy())]
            tag_location_df = {k: [] for k in table_loc_dict.keys()}
            tag_location_test_df = {k: [] for k in set(list(table_loc_dict.keys()) + list(table_test_dict.keys()))}
            processed_dict = {'num_responding_tags': [], 'status_post_process': [], 'tag_id': []}
            common_run_name = extract_unique_data(packet_df, 'common_run_name')
            tester_run_id = extract_unique_data(packet_df, 'tester_run_id')
            
            for loc in range(min(all_locations), max(all_locations) + 1):
                cur_tag_location_df = {k: None for k in table_loc_dict.keys()}
                loc_df = decoded_packet_list.filter_df_by(column='tag_run_location',
                                                          values=loc)
                if len(loc_df) == 0:
                    try:
                        fail_bin = int(packet_data['fail_bin'][packet_data['tag_run_location'].index(str(loc))])
                    except Exception as e:
                        print('pp: could not extract fail bin from the empty line at tag run location {}, '
                              'assuming missing label'.format(loc))
                        fail_bin = FailureCodes.MISSING_LABEL.value
                    
                    cur_tag_location_df['status_post_process'] = False
                    if fail_bin == FailureCodes.NO_RESPONSE.value:
                        processed_dict['status_post_process'].append(False)
                    elif fail_bin == FailureCodes.MISSING_LABEL.value:
                        processed_dict['status_post_process'].append(None)
                    else:
                        print('pp: create_group_data_table: empty line {} with failure code different '
                              'from NO_RESPONSE or MISSING_LABEL (can be a corrupted packet)'.format(loc))
                    cur_tag_location_df['tag_run_location'] = loc
                    cur_tag_location_df['fail_bin'] = fail_bin
                    cur_tag_location_df['fail_bin_str'] = FailureCodes(fail_bin).name
                    cur_tag_location_df['common_run_name'] = common_run_name
                    cur_tag_location_df['tester_run_id'] = tester_run_id
                    cur_tag_location_df['num_responding_tags'] = 0
                    cur_tag_location_df['status_offline'] = False
                    
                    try:
                        cur_tag_location_df['total_test_duration'] = \
                            float(packet_data['total_test_duration'][packet_data['tag_run_location'].index(str(loc))])
                    except Exception as e:
                        pass
                    
                    if loc < max(all_locations):
                        loc_start_time = packet_data['trigger_time'][packet_data['tag_run_location'].index(str(loc))]
                        loc_end_time = packet_data['trigger_time'][packet_data['tag_run_location'].index(str(loc + 1))]
                        cur_tag_location_df['total_location_duration'] = time_diff_between_two_strings(loc_end_time,
                                                                                                       loc_start_time)
                    else:
                        cur_tag_location_df['total_location_duration'] = None  # we reach to the end of the run
                    
                    # append to tables
                    for k, v in cur_tag_location_df.items():
                        tag_location_df[k].append(v)
                    
                    cur_tag_location_df['test_num'] = packet_data['test_num'][
                        packet_data['tag_run_location'].index(str(loc))]
                    cur_tag_location_df['test_status_offline'] = False
                    cur_tag_location_df['test_duration'] = cur_tag_location_df['total_test_duration']
                    cur_tag_location_df['received_packet_count'] = packet_data['num_packets'][
                        packet_data['tag_run_location'].index(str(loc))]

                    for k in table_test_dict.keys():
                        if k not in cur_tag_location_df.keys():
                            cur_tag_location_df[k] = None
                    for k, v in cur_tag_location_df.items():
                        tag_location_test_df[k].append(v)

                    # update process dict:
                    processed_dict['num_responding_tags'].append(cur_tag_location_df['num_responding_tags'])
                    processed_dict['tag_id'].append('')
                    continue
                
                # copy all the data from the packet_data file
                for col_name in table_loc_dict.keys():
                    val = extract_unique_data(dict_in=loc_df, name=col_name)
                    if val is not None:
                        cur_tag_location_df[col_name] = val

                # calculate post process status
                cur_tag_location_df['status_post_process'] = cur_tag_location_df['status_offline']
                if cur_tag_location_df['status_offline'] == 1:
                    selected_tag = check_duplication(loc_df, packet_df)
                    if selected_tag is None:
                        cur_tag_location_df['status_post_process'] = 0
                        if cur_tag_location_df['fail_bin'] == FailureCodes.PASS.value:
                            cur_tag_location_df['fail_bin'] = FailureCodes.DUPLICATION_POST_PROCESS.value
                        else:
                            raise Exception('pp: create_group_data_table:at loc {} offline status is pass '
                                            'while the failure code is not PASS'.format(loc))
                    else:
                        tag_id = loc_df[loc_df['selected_tag'] == loc_df['adv_address']]['tag_id']
                        tag_id_unique = list(set(tag_id.values))
                        if len(tag_id_unique) == 1:
                            cur_tag_location_df['tag_id'] = tag_id_unique[0]
                        else:
                            raise Exception('pp: create_group_data_table: at loc {} tag id is different for the same '
                                            'selected tag (by adv_address)'.format(loc))
                    
                    cur_tag_location_df['num_responding_tags'] = 1
                elif cur_tag_location_df['fail_bin'] != FailureCodes.NO_RESPONSE.value:
                    cur_tag_location_df['num_responding_tags'] = 1
                else:
                    cur_tag_location_df['num_responding_tags'] = 0
                
                cur_tag_location_df['fail_bin_str'] = FailureCodes(cur_tag_location_df['fail_bin']).name
                cur_tag_location_df['last_executed_test'] = np.nanmax(loc_df['test_num'])
                
                loc_start_time = extract_unique_data(packet_df.loc[packet_df['tag_run_location'] == loc],
                                                     'trigger_time')
                loc_end_time = extract_unique_data(packet_df.loc[packet_df['tag_run_location'] == loc + 1],
                                                   'trigger_time')
                try:
                    if loc_start_time is None:
                        loc_start_time = packet_data['trigger_time'][packet_data['tag_run_location'].index(str(loc))]
                    if loc_end_time is None:
                        loc_end_time = packet_data['trigger_time'][packet_data['tag_run_location'].index(str(loc + 1))]
                except Exception as e:
                    loc_start_time, loc_end_time = [None, None]
                cur_tag_location_df['total_location_duration'] = time_diff_between_two_strings(loc_end_time,
                                                                                               loc_start_time)
                # cur_tag_location_df['group_id'] = get_group_id_reversed([cur_tag_location_df['group_id']])[0]

                for k, v in cur_tag_location_df.items():
                    tag_location_df[k].append(v)

                # update process dict:
                if cur_tag_location_df['num_responding_tags'] is None:
                    cur_tag_location_df['num_responding_tags'] = 0
                processed_dict['num_responding_tags'].append(cur_tag_location_df['num_responding_tags'])
                processed_dict['status_post_process'].append(cur_tag_location_df['status_post_process'])
                processed_dict['tag_id'].append(cur_tag_location_df['tag_id'])

                # build table per test:
                all_tests = loc_df['test_num'].unique()
                for test in all_tests:
                    test_df = decoded_packet_list.filter_df_by(packet_df=loc_df, column='test_num',
                                                               values=test)
                    test_df_selected = test_df[test_df['selected_tag'] == test_df['adv_address']]
                    test_stat = decoded_packet_list.get_df_statistics(packet_df=test_df_selected)
                    # copy all the data from the packet_data file
                    for col_name in table_test_dict.keys():
                        if col_name not in table_loc_dict.keys():
                            val = extract_unique_data(dict_in=test_stat, name=col_name)
                            if val is None:
                                val = extract_unique_data(dict_in=test_df_selected, name=col_name)
                            cur_tag_location_df[col_name] = val
                    
                    # calc param:
                    test_end_time = extract_unique_data(dict_in=test_df, name='test_end_time')
                    test_start_time = extract_unique_data(dict_in=test_df, name='test_start_time')
                    cur_tag_location_df['test_duration'] = time_diff_between_two_strings(test_end_time, test_start_time)

                    for k, v in cur_tag_location_df.items():
                        tag_location_test_df[k].append(v)

                    if cur_tag_location_df['fail_bin'] != FailureCodes.PASS.value:
                        break  # if on test is failed no more tested were done
            
            # generate tables
            packet_results.append(
                build_table_for_cloud(dict_in=tag_location_df, table_type=table_loc_dict))
            tables_names.append(table_loc_name)
            packet_results.append(
                build_table_for_cloud(dict_in=tag_location_test_df, table_type=table_test_dict))
            tables_names.append(table_test_name)
        
        elif process_type == 'sample_test':
            pass
        else:
            raise Exception('the selected process type ({}) is not supported! '
                            'please select one of the following ["sample_test", "offline_test"]'.format(process_type))
    
    else:
        print('decoded_packet_list is empty')
    
    if len(packet_results):
        if output_dict is None or output_dict == {}:
            output_dict = {table_name: packet_result
                           for packet_result, table_name in zip(packet_results, tables_names)}
        else:
            for packet_result, table_loc_name in zip(packet_results, tables_names):
                output_dict[table_loc_name] = packet_result
    
    return output_dict, processed_dict


def create_serialization_and_status_change_table(process_type='', packet_data=None, decoded_packet_list=None,
                                                 processed_dict=None, owner_id=None):
    if process_type != 'offline_test':
        return None, None
    
    if packet_data is None or decoded_packet_list is None or processed_dict is None or owner_id is None:
        return None, None

    decoded_packet_df = decoded_packet_list.get_df()
    all_tags_id = list(set(processed_dict['tag_id'].copy()))
    all_tags_id = [t_id for t_id in all_tags_id if t_id]
    decoded_tags_df = decoded_packet_df[decoded_packet_df['tag_id'].isin(all_tags_id)]
    decoded_unique_tags_df = decoded_tags_df.drop_duplicates(subset=['tag_id'])
    serialization_data = []
    change_status_list = []
    empty_ex_id = 0
    for ind, tag_id in enumerate(all_tags_id):
        status = all([s for i, s in enumerate(processed_dict['status_post_process'])
                      if processed_dict['tag_id'][i] == tag_id])
        if status:
            external_id = decoded_unique_tags_df[decoded_unique_tags_df['tag_id'] == tag_id]['external_id'].values[0]
            if external_id == '' or str(external_id) == 'nan' or str(external_id) == 'None':
                empty_ex_id += 1
            else:
                raw_packet = decoded_packet_df[
                    decoded_packet_df['external_id'] == external_id]['original_encrypted_packet'].values[0]
                serialization_data.append({'tagId': external_id, 'payload': get_payload(raw_packet)})
        else:
            if tag_id:
                group_id = decoded_unique_tags_df[decoded_unique_tags_df['tag_id'] == tag_id][
                    'group_id']
                # group_id_reversed = get_group_id_reversed(group_id.values)
                change_status_list.append({'tagId': tag_id.lower(), 'groupId': group_id.values[0],
                                           'ownerId': owner_id, 'status': 'failed'})
    
    serialization_list = {'owner_id': owner_id, 'data': serialization_data}
    if empty_ex_id:
        print(' {} tags with empty external id were dropped from the serialization list'.format(empty_ex_id))
        if empty_ex_id == len(processed_dict['status_post_process']):
            return None, None
    if len(serialization_list['data']) == 0:
        serialization_list = None
    if len(change_status_list) == 0:
        change_status_list = None
    
    return serialization_list, change_status_list


def generate_testers_database(run_data=None, packet_data=None, decoded_data=None,
                              process_type=None, manufacturing_ver=None, tester_run_id=None):
    """
    This function run the specific process on a list of cakes according to the process type.
    For all processes, first a basic process of combining PixieAnalyzer output with the raw data is done.
    :param run_data:
    :type run_data: dict
    :param decoded_data:
    :type decoded_data: PacketList or DecryptedPacketList
    :param process_type:
    :type process_type: str
    :param tester_run_id: the unique run id received by the cloud
    :type tester_run_id: int
    :return: results
    :rtype: dict
    """
    # add custom data and generate the multi tag class
    decoded_packet_list, decoded_multi_tag = process_decoded_data(decoded_data=decoded_data, run_data=run_data,
                                                                  process_type=process_type)

    # construct the results output:
    results = None
    
    # create packet data tables:
    results = create_packet_data_tables(decoded_packet_list=decoded_packet_list, decoded_multi_tag=decoded_multi_tag,
                                        process_type=process_type, output_dict=results, tester_run_id=tester_run_id)
    # create test data tables:
    results, processed_dict = create_group_data_tables(decoded_packet_list=decoded_packet_list, packet_data=packet_data,
                                                       process_type=process_type,
                                                       output_dict=results)

    # create run data table:
    results = create_run_data_table(run_data=run_data, packet_data=packet_data, processed_dict=processed_dict,
                                    process_type=process_type, decoded_packet_list=decoded_packet_list,
                                    output_dict=results, manufacturing_ver=manufacturing_ver,
                                    tester_run_id=tester_run_id)

    # serialization and status change:
    if process_type == 'offline_test':
        if 'to_print' not in run_data or ('to_print' in run_data and str(run_data['to_print'][0]).lower() == 'no'):
            print('run without printing - no need for serialization nor status change')
            serialization_table = None
            change_status_table = None
        else:
            serialization_table, change_status_table = \
                create_serialization_and_status_change_table(process_type=process_type, packet_data=packet_data,
                                                             decoded_packet_list=decoded_packet_list,
                                                             processed_dict=processed_dict,
                                                             owner_id=run_data['owner_id'][0])
    else:
        serialization_table, change_status_table = [None, None]
    return results, serialization_table, change_status_table


if __name__ == '__main__':
    import csv
    
    
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
                    print("couldn't load csv due to: {}".format(e))
            return data_out
        else:
            print('please provide a path')
            return None
    
    
    def do_decryption(raw_data):
        dict_in = {}
        for k, v in raw_data.items():
            dict_in[k] = v.copy()
        if 'encryptedPacket' in dict_in.keys():
            packet_str = 'encryptedPacket'
        elif 'raw_packet' in dict_in.keys():
            packet_str = 'raw_packet'
        else:
            raise Exception('pp: do_decryption: '
                            'could not find packet data (not encryptedPacket nor raw_packet were found)')
        dict_in['original_encrypted_packet'] = dict_in[packet_str].copy()
        delete_ind = []
        for ind, enc_packet in enumerate(dict_in[packet_str]):
            # decryption
            dec_packet_str = ''
            if enc_packet != '' and str(enc_packet) != 'None' and str(enc_packet) != 'nan':
                if 'gw_packet' in dict_in:
                    enc_packet += dict_in['gw_packet'][ind]
                dec_packet = DecryptedPacket(raw_packet=enc_packet)

                if not dec_packet.is_decrypted_packet or len(dec_packet.decoded_data) == 0:
                    delete_ind.append(ind)
                    continue
                dec_packet_str = \
                    dec_packet.decoded_data['decrypted_packet'].split('process_packet("')[1].split('")')[0]
                dec_packet_str = dec_packet_str + dec_packet.gw_data['gw_packet'].item()
                # add decrypted flag:
                if str(dec_packet_str) != 'None' and str(dec_packet_str) != 'nan':
                    dec_packet_str = dec_packet_str[0:46] + "0" * 12 + dec_packet_str[58:]
            dict_in[packet_str][ind] = dec_packet_str
        for v in dict_in.values():
            for index in sorted(delete_ind, reverse=True):
                del v[index]

        # change keys to snake case:
        if 'commonRunName' in dict_in:
            dict_in['common_run_name'] = dict_in.pop('commonRunName')
        if 'encryptedPacket' in dict_in:
            dict_in['encrypted_packet'] = dict_in.pop('encryptedPacket')
        if 'externalId' in dict_in:
            dict_in['external_id'] = dict_in.pop('externalId')
        
        return dict_in
    

    new_table_run_path18 = 'C:/Users/WiliotLAB/AppData/Local/wiliot/offline/logs/VERSION_TEST_DATA' \
                           '/VERSION_TEST_DATA_20220921_110245/VERSION_TEST_DATA_20220921_110245@run_data.csv '
    new_table_data_path18 = 'C:/Users/WiliotLAB/AppData/Local/wiliot/offline/logs/VERSION_TEST_DATA' \
                            '/VERSION_TEST_DATA_20220921_110245/VERSION_TEST_DATA_20220921_110245@packets_data.csv '
    
    run_path = new_table_run_path18
    packet_path = new_table_data_path18
    process_type = 'sample_test'
    print('pywiliot version: {}'.format(get_version()))
    # de_packet_list = DecryptedPacketList()
    # de_packet_list = de_packet_list.import_packet_df(path=packet_path, import_all=True)
    packet_data = csv_to_dict(path=packet_path)
    run_data = csv_to_dict(path=run_path)
    # # # #### example for cloud ####
    # packet_list_df = pd.read_csv(packet_path)
    packets_decrypted_df = do_decryption(packet_data)
    print("Decryption done")
    
    # create packets decrypted list
    de_packet_list = DecryptedPacketList()
    de_packet_list = de_packet_list.import_packet_df(packet_df=pd.DataFrame(data=packets_decrypted_df), import_all=True)
    # # ### end of example #####
    
    res, serialization_table, change_status_table = \
        generate_testers_database(run_data=run_data, packet_data=packet_data,
                                  decoded_data=de_packet_list, process_type=process_type,
                                  tester_run_id=5100210002, manufacturing_ver="0.0.0")
    
    # generate the csv files:
    for key in res.keys():
        with open(packet_path.replace('.csv', '_{}.csv'.format(key)), 'w', newline='') as f:
            writer = csv.writer(f)
            writer.writerow(list(res[key]['table_scheme'].keys()))
            writer.writerow(list(res[key]['table_scheme'].values()))
            writer.writerows(res[key]['rows'])
            f.close()
    
    # print serialization and status_change tables:
    if serialization_table is not None:
        with open(packet_path.replace('.csv', '_serialization_table.csv'), 'w', newline='') as f:
            csv_writer = csv.DictWriter(f, serialization_table['data'][0].keys())
            csv_writer.writeheader()
            for serialization_dict in serialization_table['data']:
                csv_writer.writerow({k: v for k, v in serialization_dict.items()})
            f.close()
    
    if change_status_table is not None:
        with open(packet_path.replace('.csv', '_status_change_table.csv'), 'w', newline='') as f:
            csv_writer = csv.DictWriter(f, change_status_table[0].keys())
            csv_writer.writeheader()
            for change_status_dict in change_status_table:
                csv_writer.writerow({k: v for k, v in change_status_dict.items()})
            f.close()
    print('done')
