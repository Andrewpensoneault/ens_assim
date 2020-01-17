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

    return state+state*(diags(percent_std)@normal(loc = MEAN,
                                                  scale = STD,
                                                  size = state.shape))
                
