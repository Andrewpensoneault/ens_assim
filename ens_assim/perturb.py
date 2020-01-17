from numpy.random import normal
from scipy.sparse import diags
import numpy as np
MEAN = 0
STD = 1

def absolute_uncorr_perturb(state, absolute_std):
    """
    Perturbs the state array given absolute standard
    deviation diagonal of covariance matrix. Thus, it 
    makes an assumption of uncorrelated random noise.
        
    Parameters
    ----------
    state : np.ndarray
        The ensemble of states 
    absolute_std: np.ndarray
        The absolute standard deviation of the states

    Raises
    ------
    """

    return state + diags(absolute_std)@normal(loc = MEAN,
                                              scale = STD,
                                              size = state.shape)

def percent_uncorr_perturb(state, percent_std):
    """
    Perturbs the state array given percent standard
    deviation diagonal of covariance matrix. Thus, it 
    makes an assumption of uncorrelated random noise.
        
    Parameters
    ----------
    state : np.ndarray
        The ensemble of states 
    percent_std: np.ndarray
        The percent standard deviation of the states


    Raises
    ------
    """
    ens_num = state.shape[1]
    x_dim = state.shape[0]
    random_pert = normal(loc = MEAN, scale = STD, size = (x_dim,ens_num))

    for i in range(ens_num):
        state[:,i] = state[:,i] + (diags(state[:,i]*percent_std)@np.expand_dims(random_pert[:,i],1)).flatten()
    return state
