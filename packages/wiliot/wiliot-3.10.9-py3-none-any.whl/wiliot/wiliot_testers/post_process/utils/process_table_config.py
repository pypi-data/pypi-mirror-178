table_config = \
    {
        'conversion':
            {
                'commonRunName': 'str',
                'timeWindow': 'float',
                'chargeTimeMean': 'float',
                'chargeTimeStd': 'float',
                'nAboveDcoThr': 'int',
                'nTags': 'int',
                'nPacketsPerTagMean': 'float',
                'nPacketsPerTagStd': 'float'
            },
        'sample_test':
            {
                'run_data':
                    {
                        'testerStationName': 'str',
                        'commonRunName': 'str',
                        'batchName': 'str',
                        'testerType': 'str',
                        'comments': 'str', 'errors': 'str',
                        'timeProfile': 'str', 'txPower': 'str', 'energizingPattern': 'str',
                        'rssiThreshold': 'str', 'packetThreshold': 'str',
                        'tested': 'str', 'passed': 'str', 'includingUnderThresholdPassed': 'str',
                        'includingUnderThresholdYield': 'str', 'yield': 'str', 'yieldOverTime': 'str',
                        'yieldOverTimeInterval': 'str', 'yieldOverTimeOn': 'str',
                        'inlayType': 'str', 'inlay': 'str',
                        'testTime': 'str', 'maxTtfp': 'str', 'gwVersion': 'str',
                        'bleAttenuation': 'str', 'loraAttenuation': 'str', 'antennaType': 'str',
                        'operator': 'str',
                        'runStartTime': 'str', 'runEndTime': 'str',
                        'surface': 'str', 'numChambers': 'str', 'pyWiliotVersion': 'str',
                        'testTimeProfilePeriod': 'str', 'testTimeProfileOnTime': 'str',
                        'ttfpAvg': 'str', 'tbpAvg': 'str', 'rssiAvg': 'str',
                        'tester_run_id': 'long', 'manufacturing_version': 'str',
                        'responded': 'str', 'responding[%]': 'str', 'passed[%]': 'str',
                        'testStatus': 'bool', 'controlLimits': 'str'
                    },
                'results':
                    {
                        'commonRunName': 'str', 'time': 'float', 'decryptedPacket': 'str', 'tagID': 'str',
                        'groupId': 'str',
                        'encryptedPacket': 'int',
                        'packetCtrVal': 'int', 'chargeTime': 'int',
                        'vMinor': 'int', 'vFlow': 'int',
                        'packetVersion': 'str',
                        'totalDco': 'float', 'dcoCoarse': 'int', 'dcoFine': 'int', 'dcoEfine': 'int',
                        'symdcoGapInd': 'int',
                        'wkupPos': 'int', 'eawkupSilent': 'int', 'eawkupEnergy': 'int', 'wkupNeg': 'int',
                        'auxMeasStr': 'float', 'auxFreqStr': 'float', 'auxFreqInt': 'float', 'auxMeasInt': 'float',
                        'auxMeasExceptionTimeoutCtr': 'int', 'succAuxMeasInd': 'int', 'goodAuxMeasCtr': 'int',
                        'auxMeasStatusPrevPrevPrev': 'int', 'auxMeasCh': 'int', 'auxMeasChPrevPrevPrev': 'int',
                        'auxMeasStatusPrevPrev': 'int', 'auxMeasStatus': 'int', 'auxMeasStatusPrev': 'int',
                        'badAuxMeasCtr': 'int', 'auxMeasChPrevPrev': 'int', 'auxMeasChPrev': 'int', 'auxMeasCtr': 'int',
                        'temperature': 'float', 'temperatureRange': 'int',
                        'idac': 'int', 'idacX2': 'int',
                        'txLpmHpm': 'int',
                        'packetTime': 'float', 'timeDiff': 'float',
                        'gpio4Sense': 'int',
                        'proximity': 'int',
                        'loVrefVbpCalibFailInd': 'int', 'loVrefTx': 'int', 'loVbpTx': 'int',
                        'modIdx': 'int',
                        'maxTimeSprinklerCtr': 'int', 'maxFreqSprinklerCtr': 'int',
                        'avgNumPackets': 'int', 'cyclesLost': 'int',
                        'compAndTuneToggle': 'int', 'loBufCtl': 'int',
                        'currentCer': 'int',
                        'calibCycle': 'int',
                        'tunerIdx': 'int',
                        'testModePacketInd': 'int',
                        'statParam': 'int',
                        'externalId': 'str',
                        'chamber': 'str', 'originalEncryptedPacket': 'str', 'encryptedPayload': 'str',
                        'rssi': 'int'
                    },
                'analysis':
                    {
                        'commonRunName': 'str',
                        'tagID': 'str',
                        'externalId': 'str',
                        'TTFP': 'float',
                        'timeBetweenSuccessivePacketMs': 'int',
                        'firstPacketCounterValue': 'int',
                        'minTXLast': 'float',
                        'TimeBetweenCyclesAvg': 'float',
                        'chamber': 'str', 'rssiAvg': 'float',
                        'state': 'int'
                    }
            },
        'offline_test':
            {
                'runs':
                    {
                        'tester_run_id': 'long', 'common_run_name': 'str', 'tester_station_name': 'str',
                        'operator': 'str', 'reel_run_start_time': 'timestamp', 'reel_run_end_time': 'timestamp',
                        'batch_name': 'str', 'tester_type': 'str', 'comments': 'str',
                        'total_run_tested': 'int', 'total_run_responding_tags': 'int',
                        'total_run_passed_offline': 'int', 'total_run_passed_post_process': 'int',
                        'total_missing_labels': 'int', 'run_responsive_tags_yield': 'float',
                        'run_offline_yield': 'float', 'run_post_process_yield': 'float',
                        'ttfp_avg': 'float', 'conversion_type': 'str', 'inlay': 'str', 'test_suite': 'str',
                        'surface': 'str', 'to_print': 'bool', 'qr_validation': 'bool',
                        'print_pass_job_name': 'str', 'printing_format': 'str', 'external_id_prefix': 'str',
                        'external_id_suffix_init_value': 'int',
                        'coupler_partnumber': 'str',
                        'gw_version': 'str', 'py_wiliot_version': 'str', 'post_process_version': 'str',
                        'manufacturing_version': 'str', 'upload_date': 'timestamp'
                    },
                'run_tests':
                    {
                        'tester_run_id': 'long', 'common_run_name': 'str', 'test_num': 'int', 'test_name': 'str',
                        'test_tested': 'int', 'test_passed_offline': 'int',
                        'test_time_profile_period': 'int', 'test_time_profile_on_time': 'int',
                        'test_tx_power_ble_dbm': 'float', 'test_tx_power_lora_dbm': 'float',
                        'test_energizing_pattern': 'int', 'test_receive_ch': 'int',
                        'test_pl_delay': 'int', 'test_rssi_hw_threshold': 'int',
                        'test_rssi_acceptable_threshold': 'int',
                        'test_min_packets': 'int', 'test_max_time': 'float', 'test_post_delay': 'float',
                        'test_ttfp_lsl': 'float', 'test_ttfp_usl': 'float', 'test_tbp_min_lsl': 'float',
                        'test_tbp_min_usl': 'float', 'test_tbp_max_lsl': 'float', 'test_tbp_max_usl': 'float',
                        'test_tbp_avg_lsl': 'float', 'test_tbp_avg_usl': 'float',
                        'test_sprinkler_counter_max_lsl': 'int', 'test_sprinkler_counter_max_usl': 'int',
                        'test_time_between_cycles_lsl': 'float', 'test_time_between_cycles_usl': 'float',
                        'test_res_rssi_avg': 'float', 'test_res_tbp_avg': 'float',
                        'test_res_min_tx_frequency_last_avg': 'float'
                    },
                'tag_locations':
                    {
                        'tester_run_id': 'long', 'common_run_name': 'str', 'tag_run_location': 'int',
                        'tag_reel_location': 'int', 'total_test_duration': 'float', 'total_location_duration': 'float',
                        'status_offline': 'int', 'status_post_process': 'int', 'fail_bin': 'int', 'fail_bin_str': 'str',
                        'last_executed_test': 'int', 'tag_id': 'str',
                        'external_id': 'str', 'qr_validated': 'bool', 'group_id': 'str',
                        'packet_version': 'str', 'flow_version': 'str', 'num_responding_tags': 'int'
                        
                    },
                'tag_location_tests':
                    {
                        'tester_run_id': 'long', 'common_run_name': 'str', 'tag_run_location': 'int', 'test_num': 'int',
                        'test_status_offline': 'int', 'test_duration': 'float',
                        'received_packet_count': 'int', 'ttfp': 'float', 'charge_time_max': 'int',
                        'charge_time_min': 'int', 'tbp_avg': 'float', 'tbp_min': 'float', 'tbp_max': 'float',
                        'rssi_avg': 'float', 'rssi_std': 'float', 'first_packet_counter': 'int',
                        'last_packet_counter': 'int', 'dco_coarse_last': 'int', 'dco_fine_last': 'int',
                        'dco_efine_last': 'int', 'min_tx_frequency_last': 'float', 'packets_per_cycle_avg': 'float',
                        'packets_per_cycle_std': 'float', 'time_between_cycles_avg': 'float', 'aux_meas_avg': 'float',
                        'temperature_from_sensor': 'float', 'internal_temperature_avg': 'float', 'tag_id': 'str'
                    },
                'tag_test_packets':
                    {
                        'tester_run_id': 'long', 'common_run_name': 'str', 'tag_run_location': 'int', 'test_num': 'int',
                        'packet_time': 'float', 'original_encrypted_packet': 'str', 'packet_status': 'str',
                        'encrypted_payload': 'str', 'adv_address': 'str', 'group_id': 'str',
                        'decrypted_packet': 'str', 'gw_packet': 'str',
                        'decrypted_packet_type': 'int', 'tag_id': 'str',
                        'flow_ver': 'str', 'test_mode': 'int',
                        'rssi': 'int', 'stat_param': 'int', 'time_from_start': 'float',
                        'packet_ver': 'str', 'packet_cntr': 'int', 'temperature_range': 'int',
                        'temperature': 'float', 'temperature_sensor': 'float',
                        'dco_coarse': 'int', 'dco_fine': 'int', 'dco_efine': 'int',
                        'total_dco': 'float', 'min_tx': 'float', 'gpio4_sense': 'int', 'remainder4': 'int',
                        'lo_vref_tx': 'int', 'lo_vref_vbp_calib_fail_ind': 'int',
                        'comp_and_tune_toggle': 'int', 'lo_buf_ctl': 'int', 'idac_x2': 'int',
                        'idac': 'int', 'symdco_gap_ind': 'int', 'wkup_pos': 'int', 'wkup_neg': 'int', 'mod_idx': 'int',
                        'aux_meas_val': 'float', 'proximity': 'int',
                        'eawkup_silent': 'int', 'eawkup_energy': 'int', 'reserved': 'int', 'charge_time': 'int',
                        'good_aux_meas_ctr': 'int', 'bad_aux_meas_ctr': 'int', 'max_time_sprinkler_ctr': 'int',
                        'max_freq_sprinkler_ctr': 'int', 'succ_aux_meas_ind': 'int',
                        'aux_meas_exception_timeout_ctr': 'int', 'aux_meas_ch_str': 'str', 'aux_meas_channel_n': 'int',
                        'aux_meas_status_n': 'int', 'aux_meas_channel_n_1': 'int', 'aux_meas_status_n_1': 'int',
                        'aux_meas_channel_n_2': 'int', 'aux_meas_status_n_2': 'int', 'aux_meas_channel_n_3': 'int',
                        'aux_meas_status_n_3': 'int'
                    }
                
            }
    }
