import numpy as np

def get_mean(state, weights = None):
    """
    Get the mean statistics of the states given weights. 
    If weights is not set, assumes equal weight samples.
    We assume the first dimension is state and second is 
    the samples
        
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
        weights = weights/np.sum(weights)
        means = np.sum(weights*state, axis=1, keepdims=1) 
    return means

def get_std(state, weights = None):
    """
    Get the std statistics of the states given weights. 
    If weights is not set, assumes equal weight samples
    We assume the first dimension is state and second is 
    the samples. Also we use an unbiased standard deviation
        
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
        stds = np.std(state, axis=1, keepdims=1,ddof=1)
    else:
        weights = weights/np.sum(weights)
        ens_num = state.shape[1]
        stds = np.sqrt(np.sum((np.sqrt(weights)*(state-means))**2, axis=1, keepdims=1)*(ens_num/(ens_num-1)))
    return stds

