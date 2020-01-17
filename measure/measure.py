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
        if not isinstance(covariance,(np.ndarray,None)):
            raise TypeError("'covariance' must be of type int or float")
        if not isinstance(measurement,(np.ndarray,None)):
            raise TypeError("'measurement' must be of type int or float")
        if not isinstance(operator,(np.ndarray,None)):
            raise TypeError("'operator' must be of type int or float")

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
        TypeError
            If covariance is not set or incorrect type
        """
        if not isinstance(covariance,(np.ndarray,None)):
            raise TypeError("'covariance' must be of type int or float")
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
        TypeError
            If measurement is not set or incorrect type
        """
        if not isinstance(measurement,(np.ndarray,None)):
            raise TypeError("'measurement' must be of type int or float")
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
        TypeError
            If operator is not set or incorrect type
        """
        if not isinstance(operator,(np.ndarray,None)):
            raise TypeError("'operator' must be of type int or float")
        self.operator = operator
