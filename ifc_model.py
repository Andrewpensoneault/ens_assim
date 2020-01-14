import numpy as np
import re
import pandas as pd
import os
import time
import string
import random
import os.path
from itertools import chain
from datetime import datetime
from model.model import Model
import ifc_io

class IFC_Model(Model):
    ## Runs the river model from the IFC
    def __init__(self, initial_conditions):
        super().__init__(self,initial_conditions)
    
    def set_global_parameters(self, global_parameters):
        self.global_parameters = global_parameters

    def set_use_parallel(self,use_parallel):
        self.use_parallel = use_parallel
    
    def set_filename_dict(self,filename_dict):
        self.filename_dict = filename_dict

    def set_directory_dict(self,directory_dict):
        self.directory_dict = directory_dict
    
    def set_num_steps(self,num_steps):
        self.num_steps = num_steps  
    
    def set_model_num(self,model_num):
        self.model_num = model_num

    def set_link_variable_num(self,link_variable_num):
        self.link_variable_num = link_variable_num
    
    def set_start_time(self, start_time):
        self.start_time = start_time

    def set_time_step(self, time_step):
        self.time_step = time_step

    def initialize(self):
        self._read_initial_files()
    
    def advance(self):
        self._get_current_rain()
        self._generate_ensemble_files()
        self._model_run()
        self._check_existance_output()
        final_state = self._make_final()
        self._remove_files()
        return final_state 

    def _get_current_rain(self):
        rain_times = self.initial_dict['rain'][0]
        rain_ids = self.initial_dict['rain'][1]
        rain_values = self.initial_dict['rain'][2]

        HOUR_IN_SECONDS = 3600
        MINUTE_IN_SECONDS = 60
        current_rain = np.zeros((self.total_links,self.num_steps))
        for time in range(self.num_steps):
            time_now = self.start_time + MINUTE_IN_SECONDS*self.time_step*time
            last_hour_time = np.floor(time_now/HOUR_IN_SECONDS)*HOUR_IN_SECONDS
            last_hour_rain_idx = np.nonzero(rain_times == last_hour_time)[0]
            if len(last_hour_rain_idx) == 0:
               current_rain[:,time] = 0.0
            else:
                rain_ids_current = rain_ids[last_hour_rain_idx]
                rain_values_current = rain_values[last_hour_rain_idx]
                for link in range(self.total_links):
                    current_id = self.id_list[link]
                    rain_id_index = np.nonzero(rain_ids_current==current_id)
                    rain_values_current_id = rain_values_current[rain_id_index]
                    if not len(rain_values_current_id) == 0:
                        current_rain[link,time] = rain_values_current_id[0]
                    else:
                        current_rain[link,time] = 0.0
        self.current_rain = current_rain
        self.time_list = np.array([self.start_time+MINUTE_IN_SECONDS*self.time_step*time
                                   for time in range(self.num_steps)])

    def _generate_ensemble_files(self):
        tmp_folder = self.directory_dict['tmp']
        input_folder = self.directory_dict['input']
        output_folder = self.directory_dict['output']

        prm_filename = input_folder + '/' + self.filename_dict['prm']
        rvr_filename = input_folder + '/' + self.filename_dict['rvr']
        sav_filename = input_folder + '/' + self.filename_dict['sav']

        for particle in range(self.ens_num):
            gbl_filename = tmp_folder + '/' + '%05d' % (particle) + '.gbl'
            ini_filename = tmp_folder + '/' + '%05d' % (particle) + '.ini'
            str_filename = tmp_folder + '/' + '%05d' % (particle) + '.str'
            evp_filename = tmp_folder + '/' + '%05d' % (particle) + '.evp'
            output_filename = output_folder + '/' + '%05d' % (particle) + '.csv'

            particle_filename_dict = {'prm':prm_filename, 'rvr':rvr_filename,
                                      'sav':sav_filename, 'gbl':gbl_filename,
                                      'ini':ini_filename, 'str':str_filename,
                                      'evp':evp_filename, 'output': output_filename}

            self._write_files(particle_filename_dict, 
                              self.initial_conditions[:,particle],
                              self.global_parameters[:,particle])     
    
    def _model_run(self):
        tmp_folder = self.directory_dict['tmp']
        output_folder = self.directory_dict['output']
        if self.use_parallel == True:
            STRINGLENGTH = 6
            letters = string.ascii_lowercase

            job_name = ''.join(random.choice(letters) for i in range(STRINGLENGTH))  
            os.system('sh ./model_run.sh ' + str(self.ens_num) + ' ' + tmp_folder + ' ' + output_folder + ' ' + job_name)
            os.system('sh check_queue.sh ' + job_name)
        else:
            for particle in range(self.ens_num):
                os.system('sh model_local.sh ' + str(particle) + ' ' + tmp_folder + ' ' + output_folder)

    def _check_existance_output(self):
        for particle in range(self.ens_num):
            tmp_folder = self.directory_dict['tmp']
            output_folder = self.directory_dict['output']
            output_filename = output_folder + "/%04d" % particle  + ".csv"             
            try:
                os.stat(output_filename) 
            except OSError:
                os.system('sh model_local.sh ' + str(particle) + ' ' + tmp_folder + ' ' + output_folder)

    def _make_final(self):
            output_folder = self.directory_dict['output']
            state_dim = self.initial_conditions.shape[0]
            final_state = np.zeros((state_dim, self.ens_num, self.num_steps))
            for particle in range(self.ens_num):
                output_filename = output_folder + '/' + '%05d' % (particle) + '.csv'
                final_state[:,particle,:] = self._read_output_file(output_filename)
            return final_state

    def _write_files(self, particle_filename_dict, state, global_parameters):
        ini_maker = ifc_io.IniFileWriter()
        str_maker = ifc_io.StrFileWriter()
        gbl_maker = ifc_io.GblFileWriter()
        evp_maker = ifc_io.EvpFileWriter()

        ini_maker.set_model_num(self.model_num)
        ini_maker.set_link_variable_num(self.link_variable_num)
        ini_maker.set_state(state)
        ini_maker.write(particle_filename_dict['ini'])

        str_maker.set_forcing_times(self.time_list)
        str_maker.set_forcing_data(self.current_rain)
        str_maker.write(particle_filename_dict['str'])

        gbl_maker.set_global_parameters(global_parameters)
        gbl_maker.set_gbl_template(self.initial_dict['gbl'])
        gbl_maker.set_time_range(np.array([self.time_list[0],self.time_list[-1]]))
        gbl_maker.set_filename_dict(particle_filename_dict)
        gbl_maker.write(particle_filename_dict['gbl'])
        
        evp_maker.set_evaporation_rate(self.initial_dict['evp'])
        evp_maker.write(particle_filename_dict['evp'])

    def _read_initial_files(self):
        HEADER_ROW = 1
        input_folder = self.directory_dict['input']

        ini_reader = ifc_io.IniFileReader()
        sav_reader = ifc_io.SavFileReader()
        prm_reader = ifc_io.PrmFileReader()
        rvr_reader = ifc_io.RvrFileReader()
        rain_reader = ifc_io.CsvFileReader()
        evp_reader = ifc_io.EvpFileReader() 
        gbl_reader = ifc_io.GblFileReader()

        prm_filename = input_folder + '/' + self.filename_dict['prm']
        rvr_filename = input_folder + '/' + self.filename_dict['rvr']
        ini_filename = input_folder + '/' + self.filename_dict['ini']
        sav_filename = input_folder + '/' + self.filename_dict['sav']
        evp_filename = input_folder + '/' + self.filename_dict['evp']
        gbl_filename = input_folder + '/' + self.filename_dict['gbl']
        rain_filename = input_folder + '/' + self.filename_dict['rain']


        ini_id_list, ini_initial_condition = ini_reader.read(ini_filename)
        sav_id_list = sav_reader.read(sav_filename)
        prm_local_param, prm_total_links, prm_id_list = prm_reader.read(prm_filename)
        rain_reader.set_row_skip = HEADER_ROW
        rain_contents = rain_reader.read(rain_filename)
        evp_values = evp_reader.read(evp_filename)
        gbl_content = gbl_reader.read(gbl_filename)

        rain_times = rain_contents[:,0]
        rain_ids = rain_contents[:.1]
        rain_values = rain_contents[:.2]
    
        read_dict = {'ini': (ini_id_list, ini_initial_condition),
                     'sav': sav_id_list,
                     'prm': (prm_local_param, prm_total_links, prm_id_list),
                     'rvr': (),
                     'rain': (rain_times,rain_ids,rain_values),
                     'evp': evp_values,
                     'gbl': gbl_content}
        self.id_list = sav_id_list
        self.total_links = prm_total_links
        self.initial_dict = read_dict

    def _read_output_file(self,filename):
        HEADER_ROWS = 2
        output_csv_reader = ifc_io.CsvFileReader()
        output_csv_reader.set_row_skip = HEADER_ROWS
        output_csv_contents = output_csv_reader.read(filename)
        return output_csv_contents

    def _remove_files(self):
        tmp_folder = self.directory_dict['tmp']
        output_folder = self.directory_dict['output']
        for particle in range(self.ens_num):
            gbl_filename = tmp_folder + '/' + '%05d' % (particle) + '.gbl'
            ini_filename = tmp_folder + '/' + '%05d' % (particle) + '.ini'
            str_filename = tmp_folder + '/' + '%05d' % (particle) + '.str'
            evp_filename = tmp_folder + '/' + '%05d' % (particle) + '.evp'
            output_filename = output_folder + '/' + '%05d' % (particle) + '.csv'

            os.remove(gbl_filename)
            os.remove(ini_filename)
            os.remove(str_filename)
            os.remove(evp_filename)
            os.remove(output_filename)