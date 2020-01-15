import numpy as np
import sys
sys.path.insert(0, '../')
from assimilate.assimilate import SREnKF, SIR, EnKF, No_Assimilate

assim_dict ={"seed": 1,
             "assimilation_algo": SREnKF,
             "ens_num": 100,
             "rainfall_percent_std":.3,
             "model_num": 252,
             "link_variable_num": 4,
             "use_parallel":True,
             "evap_error":0,

             "measure_dict": {'use': np.array([272678]),
                              'list': np.array([313504,292251,272678,309970,277945,
                                                301218,293976,322807,295259,295251,
                                                319668,285182,285178,279791,289936,
                                                286370,311903,280498,278636,292254,
                                                292246,292227,307864,307846,316705,
                                                279783,313514,313466,305680,269719]),
                              'percent':np.array([.02,.02,.02,.05,.05,
                                              .05,.05,.05,.05,.05,
                                              .05,.05,.05,.05,.05,
                                              .05,.05,.05,.05,.05,
                                              .05,.05,.05,.05,.05,
                                              .05,.05,.05,.05,.05,]),
                              'abs':np.array([.00,.00,.00,.00,.00,
                                              .00,.00,.00,.00,.00,
                                              .00,.00,.00,.00,.00,
                                              .00,.00,.00,.00,.00,
                                              .00,.00,.00,.00,.00,
                                              .00,.00,.00,.00,.00,])},

             "directory_dict": {"tmp": "/nfsscratch/Users/apensoneault/SREnKF",
                                "storage": "../Output/SREnKF",
                                "input": "../Input/NFS",
                                "output": "/nfsscratch/Users/apensoneault/SREnKF/Output",
                                "measure": "../Input/NFS"},
             
             "filename_dict": {"rain" : "south_skunk_2_rainfall.csv",
                               "sensor" : "south_skunk_2_sensor_2.txt",
                               "prm": "south_skunk_2.prm",
                               "rvr": "south_skunk_2.rvr",
                               "sav": "south_skunk_2.sav",
                               "gbl": "gbl.txt",
                               "evp": "evap.mon",
                               "meas" : "meas.csv",
                               "ini": "south_skunk_2_sensor_2.ini"},
             
             "statistics_dict": {"mean_filename": "mean.csv",
                                 "var_filename": "var.csv",
                                 "time_filename": "time.csv"},
             
             "parameter_dict": {"global_parameters":np.array([.751, .129, -.1, .002, 2.0425e-6, .028, 0.5, .10, 0., 99.0, 3.0]),
                               "initial_parameter_abs_std":np.array([.001, .001, .001, .00001, 0, .0001, .001, 0, 0, 0, .001]),
                               "initial_parameter_percent_std":np.array([0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]),
                               "parameter_abs_std":np.array([.001, .001, .001, .00001, 0, .0001, .001, 0, 0, 0, .001]),
                               "parameter_percent_std":np.array([0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0])},

             "error_dict": {"initial_state_percent_std": np.array([5.0, 1.0, 1.0, 1.0]),
                            "state_percent_std": np.array([0.05, 0.0, 0.05, 0.01]),
                            "baseflow_percent_std": np.array([0.05, 0, 0.05, 0.01]),},
             
             "time_dict": {"time_step": 60,
                           "time_start": 1427846400, 
                           "time_stop": 1448928000,
                           "time_plot": 1427846400,
                           "num_step":48,},
             
             "ploting_dict": {"river_name": "South Skunk River",
                              "param_names":["v_0","lambda_1","lambda_2","v_h","k_3","k_I_factor","h_b","S_L","A","B","exponent"],
                              "units":["m/s","units","units","m/s","1/min","units","m","m","units","units","units"]},
             
             "mean_var_dict": {"mean_var_list":[2],
                               "mean_var_title":["s_t"],
                               "mean_var_units":["m"]}
            }
