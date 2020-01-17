## This file contains the definition of classes of measurement algorithms. To add a new algorithm, add a new subclass to
## measure.py and give it a method get_current_meas
##
## Written by: Andrew Pensoneault
import numpy as np

class Measure(object):
    """
    The measurement data structure for 

    Attributes
    ----------

    Methods
    -------
    set_covariance(covariance)
        sets the measurement error covariance
    set_measurement(measure)
        sets the measurement for the data
    set_operator(operator)
        sets the measurement operator for the data
    """
    def __init__(self, covariance=None, measurement=None, operator=None):
        """
        Initializes Class
        
        Parameters
        ----------
        covariance: np.ndarray or None
            the measurement error covariance
        measurement: np.ndarray or None
            the measurement for the data
        operator: np.ndarray or None
            the measurement operator for the data
        """

        self.covariance = covariance
        self.measurement = measurement
        self.operator = operator

    def set_covariance(self, covariance):
        """
        Sets the covariance matrix for the measurement error

        Parameters
        ----------
        covariance: np.ndarray
            the measurement error covariance

        Raises
        ------
        """
        self.covariance = covariance

    def set_measurement(self, measurement):
        """
        Sets the covariance matrix for the measurement error

        Parameters
        ----------
        measurement: np.ndarray
            the measurement of the states

        Raises
        ------
        """
        self.measurement = measurement
    
    def set_operator(self, operator):
        """
        Sets the measurement operator for the measurement error

        Parameters
        ----------
        operator: np.ndarray
            the measurement operator for the data

        Raises
        ------
        """
        self.operator = operator
