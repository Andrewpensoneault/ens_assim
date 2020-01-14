## This file contains the definition of classes of assimilation algorithms. To add a new algorithm, add a new subclass to
## assimilate.py and give it a method assimilate
##
## Written by: Andrew Pensoneault

import numpy as np
import numpy.linalg as linalg
import scipy as sp
import scipy.linalg
import scipy.stats as spstats
import os
from abc import ABC, abstractmethod

class Assimilate(ABC):
    ## Parent 
    @abstractmethod
    def analyze(self,measure):
        pass

class No_Assimilate(Assimilate):
    ## Preforms no assimilation and returns the forecast states for analysis
    def analyze(self,state,measure):
        return state

class SREnKF(Assimilate):
    ## Performs a deterministic EnKF based on "Whitaker and Hamill 2002" based on kalman identity
    def analyze(self,state,measure):
        if measure.meas_dim == 0:
            ens_anal = state
        else:
            ens_num = state.shape[1]
            ens_bg = state
            H = measure.operator
            y0 = measure.measurment
            R = measure.covariance
            x_mean = np.mean(ens_bg,1,keepdims=1)                                 
            Xb = (ens_bg-x_mean)/np.sqrt(ens_num-1)                             
            Hens_bg = H(ens_bg)
            Yb = (Hens_bg - np.mean(Hens_bg,1,keepdims=1))/np.sqrt(ens_num-1)

            S = (Yb @ Yb.T)+R
            CHt = (Xb @ Yb.T)
            K = np.linalg.solve(S.T,CHt.T).T
            m_anal = x_mean + K @ (y0 - H(x_mean))
            
            T = np.linalg.inv(np.eye(ens_num,ens_num) + (Yb.T @ np.linalg.solve(R,Yb)))
            Tsqrt = scipy.linalg.cholesky(T)           
            
            X_anal =  Xb@Tsqrt
 
            ens_anal = np.real(m_anal + np.sqrt(ens_num-1)*X_anal) #removes any complex part introduced from eig

        return ens_anal

class RSREnKF(Assimilate):
    ## Performs a deterministic EnKF based on "Whitaker and Hamill 2002" based on kalman identity
    def set_regularizer(self, regularize, regularize_prime, w_mat, lam0):
        pass

    def analyze(self,state, measure):
        pass

class EnKF(Assimilate):
    ## Performs a perturbed observation EnKF based on "Evensen 2003"
    def analyze(self,state,measure):
        if measure.meas_dim == 0:
            ens_anal = state
        else:
            meas_dim = measure.meas_dim 
            ens_num = state.shape[1]
            ens_bg = state
            H = measure.operator
            y0 = measure.measurment
            R = measure.covariance
            x_mean = np.mean(ens_bg,1,keepdims=1)                                 
            Xb = (ens_bg-x_mean)/np.sqrt(ens_num-1)                             
            Hens_bg = H(ens_bg)
            Yb = (Hens_bg - np.mean(Hens_bg,1,keepdims=1))/np.sqrt(ens_num-1)
            sqrtR = np.linalg.cholesky(R)
                
            Yo = y0 + sqrtR @ np.random.normal(0,1,(meas_dim,ens_num))
            
            P = ( Yb @ Yb.T + R)
            YTPi = np.linalg.solve(P.T,Yb).T            
            K = Xb @ YTPi
            ens_anal = ens_bg + K @ (Yo - Hens_bg)

        return ens_anal

class SIR(Assimilate):
    def set_weights(self, weights):
        self.weights = weights
    
    def set_likelihood(self, likelihood):
        self.likelihood = likelihood
            
    def set_threshold(self, threshold):
        self.threshold = threshold

    def analyze(self,state,measure):
        if measure.meas_dim == 0:
            ens_anal = state
            weights = self.weights
        else:
            ens_bg = state
            ens_num = state.shape[1]
            w = self.weights*self.likelihood(ens_bg)
            w = w/np.sum(w)
            if (1/np.sum(w**2) < self.threshold):
                xk = np.arange(ens_num)
                resample_dist = spstats.rv_discrete(values=(xk,w))
                choice = resample_dist.rvs(size=ens_num)
                state = ens_bg[:,choice]
                w = (1/ens_num)*np.ones((1,ens_num))
                ens_anal = state
            else:
                ens_anal = state
        return ens_anal, weights
