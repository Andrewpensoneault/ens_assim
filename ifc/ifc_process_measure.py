import ifc.ifc_io as ifc_io
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
        contents = meas_reader.read(filename)
        measurement_dict[current_id] = contents
    return measurement_dict

def get_current_measurements(measurement_dict,id_list,use_list,time_start,time_step_size,step_num):
    MINUTE_IN_SECONDS = 60
    measurement = np.zeros((0,1))
    measurement_index = np.zeros((0,1))
    for ids in use_list:
        if ids in id_list:
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

def create_operator(measurement_index, link_variable_num, total_links, id_list):
    num_measurements = measurement_index.shape[0]
    total_variables = total_links * link_variable_num
    index_list = []
    for meas_num in range(len(num_measurements)): 
        current_link_id  = measurement_index[meas_num,0]
        current_time_num = measurement_index[meas_num,1]
        link_id_idx = np.nonzero(current_link_id == num_measurements)
        current_index = link_id_idx*link_variable_num + current_time_num*total_variables
        index_list.append(current_index)
    operator = lambda x: x[index_list,:]
    return operator

def augment_operators(operator_1,operator_2):
    return lambda x: np.stack((operator_1(x),operator_2(x)),axis=0)

def create_covariance(measurement, index, absolute_std, relative_std):
    return np.diag(absolute_std[index]**2) + np.diag((relative_std[index]*measurement)**2)
