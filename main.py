import ifc.ifc_model as ifc_model
import ifc.ifc_process_measure as ifc_meas
import assimilate.assimilate as assimilate
from measure.measure import Measure
import numpy as np
import sys
import perturb
import transform

sys.path.insert(0, sys.argv[1])
new_module = __import__(sys.argv[2])
assim_dict = new_module.assim_dict
np.random.seed(assim_dict['seed'])

assim = assimilate.SREnKF()
model = ifc_model.IFC_Model(np.array([[]]))

time_step = assim_dict['time_dict']['time_step']
time_start = assim_dict['time_dict']['time_start']
time_stop = assim_dict['time_dict']['time_stop']
num_step = assim_dict['time_dict']['num_step']
current_time = time_start

MINUTE_IN_SECONDS = 60
time_step_seconds = time_step*MINUTE_IN_SECONDS

model.set_use_parallel(assim_dict['use_parallel'])
model.set_filename_dict(assim_dict['filename_dict'])
model.set_directory_dict(assim_dict['directory_dict'])
model.set_num_step(assim_dict['time_dict']['num_step'])
model.set_model_num(assim_dict['model_num'])
model.set_model_num(assim_dict['link_variable_num'])
model.set_start_time(assim_dict['time_dict']['time_start'])
model.set_time_step(assim_dict['time_dict']['time_step'])

global_parameters = assim_dict['parameter_dict']['global_parameters']
global_parameters = np.expand_dims(global_parameters,axis=1)
global_parameters = np.tile(global_parameters,assim_dict['ens_num'])
global_parameters = perturb.percent_uncorr_perturb(global_parameters,assim_dict['parameter_dict']['initial_parameter_percent_std'])
global_parameters = perturb.absolute_uncorr_perturb(global_parameters,assim_dict['parameter_dict']['initial_parameter_abs_std'])


initial_conditions = model.initialize()
initial_conditions = np.tile(initial_conditions,assim_dict['ens_num'])

link_num = len(initial_conditions)/assim_dict['link_variable_num']

initial_state_percent_std = np.matlib.tile(assim_dict['error_dict']['initial_state_percent_std'],link_num)
state_percent_std = np.matlib.tile(assim_dict['error_dict']['state_percent_std'],link_num)

initial_conditions = perturb.percent_uncorr_perturb(global_parameters,initial_state_percent_std)

initial_state_abs_std = np.matlib.tile(assim_dict['error_dict']['baseflow_percent_std'],link_num)
state_abs_std = initial_state_abs_std*initial_conditions[:,0].flatten()

error_dict = {'state_percent_std':state_percent_std, 'state_abs_std':state_abs_std, 
              'parameter_percent_std': assim_dict['parameter_dict']['parameter_percent_std'],
              'parameter_abs_std': assim_dict['parameter_dict']['parameter_abs_std']}

model.set_initial_conditions(initial_conditions)
import pdb; pdb.set_trace()

meas_dir = assim_dict['directory_dict']['measure']
meas_filename = assim_dict['filename_dict']['meas']
measure_dict = ifc_meas.read_measurements(meas_dir, assim_dict['measure_dict']['list'], meas_filename)
measure = Measure()


id_list = model.initial_dict['sav']
total_links = model.initial_dict['prm'][1]
link_variable_num = assim_dict['link_variable_num']

while current_time < time_stop:
    measurement_index, measurement = ifc_meas.get_current_measurements(measure_dict,id_list,
                                                                       assim_dict['measure_dict']['use'],
                                                                       current_time,time_step,num_step)
    operator = ifc_meas.create_operator(measurement_index, link_variable_num, total_links, id_list)
    index = np.intersect1d(assim_dict['measure_dict']['use'],measurement_index[:,0],return_indices=1)
    covariance = ifc_meas.create_covariance(measurement, index, assim_dict['measure_dict']['abs'], assim_dict['measure_dict']['percent'])
                    
    measure.set_measurements(measurement)
    measure.set_operator(operator)
    measure.set_covariance(covariance)
    state = model.advance()
    state = perturb.percent_uncorr_perturb(global_parameters,state_percent_std)
    state = perturb.absolute_uncorr_perturb(global_parameters,state_abs_std)
    assim_state = transform.assim2model(state,global_parameters,num_step)
    assim_state = assim.analyze(assim_state,measure)
    state = transform.assim2model(assim_state,link_variable_num,num_step)
    current_time += num_step*time_step_seconds

