import ifc_io
import numpy as np
import numpy.linalg as linalg
import scipy as sp
import pandas as pd

def read_measurements(measure_directory, measure_ids, measure_filename):
    HEADER_ROW = 1
    meas_reader = ifc_io.CsvFileReader()
    meas_reader.set_skip_rows = HEADER_ROW
    measurement_dict = {}
    for id_idx in range(len(measure_ids)):
        current_id = measure_ids[id_idx] 
        filename = measure_directory + '/' + current_id + '_' + measure_filename
        contents = measure_reader.read()
        measurement_dict[current_id] = contents
    return measurement_dict

def get_current_measurements(measurement_dict,id_list,time_start,time_step_size,step_num):
    MINUTE_IN_SECONDS = 60
    meas_ids = measurement_dict.keys()
    measurement = np.zeros((0,1))
    measurement_index = np.zeros((0,1))
    for ids in meas_ids:
        if ids in id_list:
            id_index = np.nonzero(ids == id_list)
            measure = measurement_dict[ids]
            for steps in range(step_num):
                measure_times = measure[:,0]
                current_measurements = measure[:,1]
                time_start = time_start + steps*MINUTE_IN_SECONDS*step_num
                time_end = time_start + steps*MINUTE_IN_SECONDS*(step_num+1)

                current_time_index = np.nonzero((measure_times < time_start) and
                                                (measure_times > time_end))
                
                if len(current_time_index[0]) > 0:
                    current_idx = current_time_index[0]
                    current_meas = np.array([current_measurements[current_idx]])
                    current_meas_index = np.array([ids,steps])
                    measurement = np.stack((measurement,current_meas),axis=0)
                    measurement_index = np.concatenate((measurement_index,current_meas_index),axis=0)
                else:
                    pass
        else:
            pass
    return measurement_index, measurement

def create_operator(measurement_index, variable_num, total_ids, id_list):


def create_covariance(measurement, absolute_error, relative_error):
    HEADER_ROW = 1
    meas_reader = ifc_io.CsvFileReader()
    meas_reader.set_skip_rows = HEADER_ROW
    for id_idx in range(len(measure_ids)):
        filename = measure_directory + '/' + measure_ids[id_idx]
        measure_reader.read()