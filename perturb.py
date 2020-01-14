from numpy.random import normal

def absolute_uncorr_perturb(state, absolute_std):
        return state + absolute_std*normal(loc = 0,
                                           scale = 1,
                                           size = state.shape)

def percent_uncorr_perturb(state, absolute_std):
        return state*(1+state*absolute_std*normal(loc = 0,
                                           scale = 1,
                                           size = state.shape))
                