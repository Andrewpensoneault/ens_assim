from numpy.random import normal
from scipy.sparse import diags
MEAN = 0
STD = 1

def absolute_uncorr_perturb(state, absolute_std):
        return state + diags(absolute_std)@normal(loc = MEAN,
                                                  scale = STD,
                                                  size = state.shape)

def percent_uncorr_perturb(state, absolute_std):
        return state+state*(diags(absolute_std)@normal(loc = MEAN,
                                                         scale = STD,
                                                         size = state.shape))
                