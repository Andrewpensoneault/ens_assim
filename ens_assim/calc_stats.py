import numpy as np

def get_mean(state, weights = None):
    """
    Get the mean statistics of the states given weights. 
    If weights is not set, assumes equal weight samples
        
    Parameters
    ----------
    state : np.ndarray
        The ensemble of states 
    weights: np.ndarray or none
        The weights associated with the ensemble
        set to None implies equal weight

    Raises
    ------
    """
    
    if weights is None:
        means = np.mean(state, axis=1, keepdims=1)
    else:
        means = np.sum(weights*state, axis=1, keepdims=1) 
    return means

def get_std(state, weights = None):
    """
    Get the std statistics of the states given weights. 
    If weights is not set, assumes equal weight samples

    Parameters
    ----------
    state : np.ndarray
        The ensemble of states 
    weights: np.ndarray or none
        The weights associated with the ensemble
        set to None implies equal weight

    Raises
    ------
    """

    means = get_mean(state, weights)
    if weights is None:
        stds = np.std(state, axis=1, keepdims=1)
    else:
        ens_num = state.size[1]
        stds = np.sum((np.sqrt(weights)*(state-means))**2)*(ens_num/(ens_num-1))
    return stds

