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
    TypeError
        If state or absolute_std is not set or incorrect type
    """

    if not isinstance(state,np.ndarray):
        raise TypeError("'state' must be of type numpy.ndarray")
    if not isinstance(absolute_std,np.ndarray):
        raise TypeError("'absolute_std' must be of type numpy.ndarray")

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
    TypeError
        If state or weights is not set or incorrect type
    """

    if not isinstance(state,np.ndarray):
        raise TypeError("'state' must be of type numpy.ndarray")
    if not isinstance(percent_std,np.ndarray):
        raise TypeError("'percent_std' must be of type numpy.ndarray")

    return state+state*(diags(percent_std)@normal(loc = MEAN,
                                                  scale = STD,
                                                  size = state.shape))
                
