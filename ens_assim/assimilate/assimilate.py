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
import sys
from ens_assim.measure.measure import Measure
import types

class Assimilate(ABC):
    """
    The abstract base class used to represent an Data Assimilation algorithm

    Attributes
    ----------

    Methods
    -------
    analyze(state, measure)
        Performs the assimilation algorithm
    """
    @abstractmethod
    def __init__(self):
        """
        Initializes Class
        
        Parameters
        ----------
        """
        pass

    def analyze(self, state, measure):
        """Performs the SREnKF on state with given measurements

        Parameters
        ----------
        state: numpy.ndarray
            The given states to perform assimilation on
        measure: Measure
            The given Class containing information about measurement

        Raises
        ------
        """

class No_Assimilate(Assimilate):
    
    """
    The class for performing no data assimilation

    Attributes
    ----------

    Methods
    -------
    analyze(state, measure)
        Performs the assimilation algorithm
    """
    def __init__(self):
        """
        Initializes Class
        
        Parameters
        ----------
        """
        pass
    def analyze(self,state,measure):
        return state

class SREnKF(Assimilate):
    """
    The class for performing the square root EnKF, as seen in
    Law, Stuart, Zygalakis 2015
        

    Attributes
    ----------

    Methods
    -------
    analyze(state, measure)
        Performs the assimilation algorithm
    """
    def __init__(self):
        """
        Initializes Class
        
        Parameters
        ----------
        """
        pass
    def analyze(self,state,measure):
        """
        Performs the SREnKF on state with given measurements

        Parameters
        ----------
        state: numpy.ndarray
            The given states to perform assimilation on
        measure: Measure
            The given Class containing information about measurement

        Raises
        ------
        """
        super().analyze(state, measure)

        if len(measure.measurement) == 0:
            ens_anal = state
        else:
            ens_num = state.shape[1]
            ens_bg = state
            H = measure.operator
            y0 = measure.measurement
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
    """
    The class for performing the square root EnKF with regularization
    term
        
    Attributes
    ----------
    regularize
        the regularization function
    regularize_prime
        the jacobian of the regularization function
    w_mat
        the weight matrix associated with the regularization norm
    lam0 
        the regularization weight

    Methods
    -------
    analyze(state, measure)
        Performs the assimilation algorithm
    set_regularizer(regularize, regularize_prime, w_mat, lam0)
        Sets parameters associated with regularization
    """
    def __init__(self):
        """
        Initializes Class

        Parameters
        ----------
        """
        self.regularize = None
        self.regularize_prime = None
        self.w_mat = None
        self.lam0 = None

    def set_regularizer(self, regularize, regularize_prime, w_mat, lam0):
        """
        Sets the regularization parameters and functions used in the REnKF

        Parameters
        ----------
        regularize: numpy.ndarray
            The given states to perform assimilation on
        regularize_prime: Measure
            The given Class containing information about measurement
        w_mat: numpy.ndarray
            The weight matrix for which the norm is performed in
        lam0: numpy.ndarray
            The base regularizaton parameter

        Raises
        ------
        """
        pass

    def analyze(self,state, measure):
        """
        Performs the RSREnKF on state with given measurements

        Parameters
        ----------
        state: numpy.ndarray
            The given states to perform assimilation on
        measure: Measure
            The given Class containing information about measurement

        Raises
        ------
        """
        super().analyze(state, measure)

class EnKF(Assimilate):
    """
    Performs a perturbed observation EnKF based on 'Evensen 2003'

    Attributes
    ----------

    Methods
    -------
    analyze(state, measure)
        Performs the assimilation algorithm
    """
    def __init__(self):
        """
        Initializes Class
        
        Parameters
        ----------
        """
        pass
    def analyze(self,state,measure):
        """
        Performs the EnKF on state with given measurements

        Parameters
        ----------
        state: numpy.ndarray
            The given states to perform assimilation on
        measure: Measure
            The given Class containing information about measurement

        Raises
        ------
        """
        super().analyze(state, measure)
        if len(measure.measurement) == 0:
            ens_anal = state
        else:
            meas_dim = len(measure.measurement)
            ens_num = state.shape[1]
            ens_bg = state
            H = measure.operator
            y0 = measure.measurement
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
    """
    Performs a Sequential Importance Resampling Particle Filter

    Attributes
    ----------
    weights
        weights for the resampling
    likelihood
        likelihood function of the data
    threshold
        threshold for effective sample size

    Methods
    -------
    set_weights(weights)
        Sets the base weight for each particle
    set_likelihood(likelihood)
        Sets the likelihood function for the data
    set_threshold(threshold)
        Sets the threshold for effective sample size of the SIR
    analyze(state, measure)
        Performs the assimilation algorithm
    """
    def __init__(self):
        """
        Initializes Class

        Parameters
        ----------
        """
        self.weights = None
        self.likelihood = None
        self.threshold = None

    def set_weights(self, weights):
        """
        Sets the weights for the particles

        Parameters
        ----------
        weights: np.ndarray
            weight for each particle

        Raises
        ------
        """

        self.weights = weights
    
    def set_likelihood(self, likelihood):
        """
        Sets the likelihood for the data

        Parameters
        ----------
        likelihood: type.LambdaType
            lambda function for the likelihood function of the data

        Raises
        ------
        TypeError
            If any parameter is not set or incorrect type
        """

        self.likelihood = likelihood
            
    def set_threshold(self, threshold):
        """
        Sets the weights for the particles

        Parameters
        ----------
        threshold: float or int
            Sets the threshold for the minimum effective sample size

        Raises
        ------

        """


        self.threshold = threshold

    def analyze(self,state,measure):
        """
        Performs the SIR on state with given measurements

        Parameters
        ----------
        state : numpy.ndarray:
            The given states to perform assimilation on
        measure: Measure
            The given Class containing information about measurement

        Raises
        ------
        """
        weights = self.weights/np.sum(self.weights)
        
        if len(measure.measurement) == 0:
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
                weights = (1/ens_num)*np.ones((1,ens_num))
                ens_anal = state
            else:
                ens_anal = state
                weights = w
            self.weights = weights
        return ens_anal
