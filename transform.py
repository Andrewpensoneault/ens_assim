import numpy as np

def model2assim(state,parameters):
    num_variable = state.shape[0]
    ens_num = state.shape[1]
    num_step = state.shape[2]
    assim_state = np.zeros((num_variable*num_step,ens_num))
    for row_seg in range(num_step):
        assim_state[row_seg*num_variable,:] = state[:,:,row_seg]
    assim_state = np.concatenate((assim_state,parameters))
    return assim_state

def assim2model(assim_state,num_variable,num_step):
    last_var_start = (num_step-1)*num_variable
    last_var_end = num_step*num_variable
    state = assim_state[last_var_start:last_var_end,:]
    return state