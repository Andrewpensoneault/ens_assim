import numpy as np
import pandas as pd
from abc import ABC, abstractmethod

class FileReader(ABC):
    @abstractmethod
    def read(self,filename):
        #reads, removes all blank lines, lines which start with #
        with open(filename) as f:
            lines = f.readlines() 
            lines = [x for y in lines for x in y.split("\n")]
            lines = [x.strip() for x in lines]
            lines = [x for x in lines if x != '']
            lines = [x for x in lines if '#' not in x]
        return lines

class CsvFileReader(FileReader):
    def set_row_skip(self, skip_rows):
        self.skip_rows = skip_rows
    def read(self, filename):
        contents = pd.read_csv(filename, delimiter=",",
                               skiprows = self.skip_rows)
        contents = np.array(contents.values)
        return contents

class IniFileReader(FileReader):
    def read(self,filename):
        lines = super().read(filename)
        id_list = np.array(lines[3::2])
        id_list = id_list.astype('int')
        initial_condition = lines[4::2]
        initial_condition = [x.split() for x in initial_condition]
        initial_condition = np.array(initial_condition)
        initial_condition = initial_condition.astype(np.float)
        initial_condition = initial_condition.flatten(order="C")
        return id_list, initial_condition

class GblFileReader(FileReader):
    def read(self,filename):
        with open(filename,'r') as f:
            contents = f.read().split("\n")
        return contents

class RvrFileReader(FileReader):
    def read(self,filename):
        pass

class EvpFileReader(FileReader):
    def read(self, filename):
        evap_values = np.expand_dims(np.loadtxt(filename),1)
        return evap_values

class SavFileReader(FileReader):
    def read(self, filename):
        id_list = np.loadtxt(filename)
        return id_list

class PrmFileReader(FileReader):
    def read(self, filename):
        lines = super().read(filename)
        id_list = np.array(lines[1::2])
        id_list = id_list.astype('int')

        local_param = lines[2::2]
        local_param = [x.split() for x in local_param]
        local_param = np.array(local_param).astype('float')
        total_links = np.array(lines[0]).astype('int')
        return local_param, total_links, id_list

class FileWriter(ABC):
    @abstractmethod
    def __init__(self):
        pass
    def set_link_ids(self,link_ids):
        self.link_ids = link_ids
    def set_total_links(self,total_links):
        self.total_links = total_links


class IniFileWriter(FileWriter):
    def __init__(self):
        pass
    def set_model_num(self,model_num):
        self.model_num = model_num
    def set_link_variable_num(self,link_variable_num):
        self.link_variable_num = link_variable_num
    def set_state(self,state):
        self.state = state
    def write(self,filename):
        var_matrix = np.zeros((self.total_links,self.link_variable_num))
        id_list = self.link_ids.tolist()
        content_id = [str(x) for x in id_list]
        total_variables = self.total_links*self.link_variable_num
        for j in range(self.link_variable_num):
                var_matrix[:,j] = self.state[j:total_variables:self.link_variable_num]       
        content_var = [' '.join(map(str, x)) for x in var_matrix.tolist()]
        content = [val for pair in zip(content_id, content_var) for val in pair] #joins ids and values 
        content = "\n".join(content)
        with open(filename,'w') as f:
            f.write("%s\n"%str(self.model_num))
            f.write("%s\n"%str(self.total_links))
            f.write("%s\n"%str(0))
            f.write("%s\n"% content)

class StrFileWriter(FileWriter):
    def __init__(self):
        pass
    def set_forcing_times(self,forcing_times):
        self.forcing_times = forcing_times
    def set_forcing_data(self,forcing_data):
        self.forcing_data = forcing_data
    def write(self,filename):
        num_times = len(self.forcing_times)
        time_list = num_times*np.ones(self.total_links,dtype="int")
        id_contents = np.array([self.link_ids,time_list]).T
        id_list = id_contents.tolist()
        id_contents = [' '.join(map(str, x)) for x in id_list]
        cycle_num = np.array([i*self.time_interval for i in range(id_list)])
        time_rain = np.tile(cycle_num,self.total_links)

        rain_content = np.array([time_rain, self.forcing_data.flatten()]).T
        rain_content = [' '.join(map(str, x)) for x in rain_content.tolist()]
        tmp_rain = []
        for j in range(num_times):
            tmp_rain += [rain_content[j::num_times]]
        content = [val for pair in zip(id_contents, *tmp_rain) for val in pair] # weaves id and rain
        content = "\n".join(content)
        with open(filename,'w') as f:
            f.write("%s\n"%str(self.total_links))
            f.write("%s\n"%content)   

class GblFileWriter(FileWriter):
    def __init__(self):
        pass
    def set_global_parameters(self,global_parameters):
        self.global_parameters = global_parameters
    def set_gbl_template(self,gbl_template):
        self.gbl_template = gbl_template
    def set_time_range(self,time_range):
        self.time_range = time_range
    def set_filename_dict(self,filename_dict):
        self.filename_dict = filename_dict
    def write(self,filename):
        contents = self.gbl_template
        contents[1] = str(self.model_num)
        contents[4] = str(self.time_range[0])
        contents[5] = str(self.time_range[1])
        contents[30] = "0 " + self.filename_dict['rvr']
        contents[33] = "0 " + self.filename_dict['prm']
        current_global_parameters = ' '.join(map(str,self.global_parameters))
        global_length = str(len(self.global_parameters))
        contents[22] = global_length + ' ' +  current_global_parameters
        contents[37] = "0 " + self.filename_dict['ini']
        contents[42] = "1 " + self.filename_dict['str']
        contents[45] = "7 " + self.filename_dict['evp']
        contents[55] = "2 " + self.filename_dict['output']
        contents[63] = "1 " + self.filename_dict['sav']
        contents[70] = self.filename_dict['tmp']
        with open(filename,'w') as f:
            for items in contents:
                f.write("%s\n" % items)
    

class EvpFileWriter(FileWriter):
    def __init__(self):
        pass 
    def set_evaporation_rate(self,evaporation_rate):
        self.evaporation_rate = evaporation_rate
    def write(self,filename):
        np.savetxt(filename, self.evaporation_rate, fmt="%3.1f") 

class SavFileWriter(FileWriter):
    def __init__(self):
        pass
    def write(self,filename):
        contents = map(str,self.link_ids)
        with open(filename,'w') as f:
            for item in contents:
                f.write("%s\n" % item)

class FileDeleter(object):
    def __init__(self):
        pass
    def remove_files(self, files):
        for f in files:
            try:
                os.remove(f)
            except:
                print(f'Failed to delete {f}')