## This file contains the definition of classes of model algorithms. To add a new algorithm, add a new subclass to
## model.py and give it a method advance
##
## Written by: Andrew Pensoneault
from abc import ABC, abstractmethod
import numpy as np

class Model(ABC):
    """
    The abstract base class used to represent the model

    Attributes
    ----------

    Methods
    -------
    set_initial_conditions(initial_conditions)
        Sets the initial condition, and gets the number of
        ensemble member
    advance(state, measure)
        Advances the model forward one step
    """
    @abstractmethod
    def __init__(self, initial_conditions):
        """
        Initializes Class
        
        Parameters
        ----------
        initial_conditions : np.ndarray
            The initial condition for the model

        Raises
        ------
        TypeError
            If initial_condition is not set or incorrect type
        """
        if not isinstance(initial_conditions,np.ndarray):
            raise TypeError("'initial_condition' must be of type numpy.ndarray")

        self.initial_conditions = initial_conditions
        self.ens_num = initial_conditions.shape[1]
    
    def set_initial_conditions(self, initial_conditions):
        """
        Sets the initial condition for the model

        Parameters
        ----------
        initial_conditions : np.ndarray
            The initial condition for the model

        Raises
        ------
        TypeError
            If initial condition is not set or incorrect type
        """
        if not isinstance(initial_conditions,np.ndarray):
            raise TypeError("'initial_condition' must be of type numpy.ndarray")

        self.initial_conditions = initial_conditions
        self.ens_num = initial_conditions.shape[1]

    def advance(self):
        """
        Advances the model forward one step

        Parameters
        ----------

        Raises
        ------
        """
        pass

class identity(Model):
    """
    The identity mapping for the initial condition

    Attributes
    ----------

    Methods
    -------
    set_initial_conditions(initial_conditions)
        Sets the initial condition, and gets the number of
        ensemble member
    advance(state, measure)
        Advances the model forward one step
    """
    def __init__(self, initial_conditions):
        """
        Initializes Class
        
        Parameters
        ----------
        initial_conditions : np.ndarray
            The initial condition for the model
        Raises
        ------
        TypeError
            If initial condition is not set or incorrect type
        """
        super().__init__(self,initial_conditions)

    def advance(self):
        """
        Advances the model forward one step, returns the 
        initial condition

        Parameters
        ----------

        Raises
        ------
        """
        return self.initial_conditions
