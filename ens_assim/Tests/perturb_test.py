def_process measure(self):
        meas = np.zeros((1,0))
        ind = np.zeros((1,0), dtype='int')
        R = np.zeros((1,0))
        cycle = np.zeros((1,0),dtype='int')
        for j in range(self.smoother_cycles):
            for i in range(0,self.use_sensor_len):
                time_now = self.current_time + (60*self.time_interval*(j-self.smoother_cycles+1))
                current_meas = self.meas_list[self.use_sensor_sensor_index[i]]
                times = current_meas[:,0]
                val = current_meas[:,1]
                inter = np.intersect1d(times,time_now,return_indices=True)
                meas_index = inter[1]
                if not len(meas_index) == 0:
                    m = val[meas_index]
                    meas = np.append(meas,m)
                    ind = np.append(ind,i)
                    cycle = np.append(cycle,j)
                    R = np.append(R,(m*self.use_std[i])**2)
        self.meas_dim = meas.size
        self.meas = np.expand_dims(meas,1)
        self.R = np.diag(R)
        tind = self.use_sensor_var_index[ind]
        self.ctind = tind + cycle*self.total_links*self.link_var_num
        self.H = lambda X: X[self.ctind,:]

    def __get_sensor_errors(self):
        self.use_std = np.zeros(self.use_sensor_len)
        for i in range(0,self.use_sensor_len):
            cur_sensor_type = self.sensor_list_type[self.use_sensor_sensor_index[i]]
            inter = np.intersect1d(self.sensor_type_names,cur_sensor_type, return_indices=True)
            err_type_ind = inter[1]
            self.use_std[i] = self.sensor_type_p_std[err_type_ind]       
