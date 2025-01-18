# Copyright 2024 Dell Inc. or its subsidiaries. All Rights Reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

'''
Module to gather amd gpu metrics
'''

import common_parser
import invoke_commands
import common_logging

# --------------------------------AMD GPU metric collection---------------------------------

rocm_bin_path = "/opt/rocm/bin/"

def get_amd_gpu_temp():
    '''
    This method collects amd gpu temp from rocm query output
    and stores it in gpu metric dictionary
    '''
    amd_metrics_query = rocm_bin_path + "rocm-smi -t --csv"
    command_result = invoke_commands.run_command(amd_metrics_query)
    if command_result is not None:
        gpu_temp = {}
        command_result_df = common_parser.get_df_format(command_result)
        try:
            gpu_temp['sensor_junction'] = common_parser.get_col_from_df(command_result_df,
                                                             'Temperature (Sensor junction) (C)')
        except Exception as err:
            gpu_temp['sensor_junction'] = None
            common_logging.log_error("data_collector_amd_proc_acc:get_amd_gpu_temp",
                                "could not parse sensor_junction temp from rocm-smi" + str(err))
        try:
            gpu_temp['sensor_memory'] = common_parser.get_col_from_df(command_result_df,
                                                                 'Temperature (Sensor memory) (C)')
        except Exception as err:
            gpu_temp['sensor_memory'] = None
            common_logging.log_error("data_collector_amd_proc_acc:get_amd_gpu_temp",
                                   "could not parse sensor_memory temp from rocm-smi" + str(err))
        return gpu_temp

    common_logging.log_error("data_collector_amd_proc_acc:get_amd_gpu_temp",
                             "rocm-smi command did not give output for gpu temperature metrics.")
    return None

# -------------------------------AMD GPU health metric collection-------------------------------

def get_gpu_health_power():
    '''
    This method collects amd gpu power health from rocm query output
    '''
    amd_metrics_query = rocm_bin_path + "rocm-smi -P -M --csv"
    command_result = invoke_commands.run_command(amd_metrics_query)
    if command_result is not None:
        try:
            command_result_df = common_parser.get_df_format(command_result)
            gpu_util_list_max = common_parser.get_col_from_df(command_result_df,
                                                              'Max Graphics Package Power (W)')
            gpu_util_list_avg = common_parser.get_col_from_df(command_result_df,
                                                              'Current Socket Graphics Package Power (W)')
            return gpu_util_list_max,gpu_util_list_avg
        except Exception as err:
            common_logging.log_error("data_collector_amd_proc_acc:get_gpu_health_power",
                                     "could not parse gpu power health from rocm-smi. "+str(err))
            return None,None
    return None,None

def get_gpu_health_thermal():
    '''
    This method collects amd gpu thermal health from rocm query output
    '''
    amd_metrics_query = rocm_bin_path + "rocm-smi -t --csv"
    command_result = invoke_commands.run_command(amd_metrics_query)
    if command_result is not None:
        command_result_df = common_parser.get_df_format(command_result)
        try:
            gpu_temp = common_parser.get_col_from_df(command_result_df,
                                                                'Temperature (Sensor junction) (C)')
            return gpu_temp
        except Exception as err:
            common_logging.log_error("data_collector_amd_proc_acc:get_gpu_health_thermal",
                                     "could not parse sensor_edge temp from rocm-smi. " + str(err))
        return None
    return None
