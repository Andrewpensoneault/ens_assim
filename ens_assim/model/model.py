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
    initial_conditions
        The initial condition of the model
    ens_num
        the number of ensemble members

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
        """

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
        """

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
    initial_conditions
        The initial condition of the model
    ens_num
        the number of ensemble members

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

class ODE(Model):
    """
    A Class for a general system of ODEs
    Attributes
    ----------
    initial_conditions
        The initial condition of the model
    ens_num
        The number of ensemble members
    solver
        The solver of the ODE
    rhs
        the function on the right hand side of 
        the equation
    t0
        the initial time
    step_size 
        the size of step for the solver
    
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
        """
        super().__init__(initial_conditions)
        self.solver = None
        self.rhs = None
        self.t0 = None
        self.step_size = None
        self.num_steps = None

    def set_solver(self, solver):
        self.solver = solver

    def set_rhs(self, rhs):
        self.rhs = rhs

    def set_t0(self,t0):
        self.t0 = t0

    def set_step_size(self, step_size):
        self.step_size = step_size

    def set_num_steps(self, num_steps):
        self.num_steps = num_steps


def RK4(t0, x0, rhs, h):
    k1 = h*rhs(t0, x0); 
    k2 = h*rhs(t0 + 0.5*h, x0 + 0.5*k1); 
    k3 = h*rhs(t0 + 0.5*h, x0 + 0.5*k2); 
    k4 = h*rhs(t0 + h, x0 + k3); 
    
    x = x0 + (1.0/6.0)*(k1 + 2*k2 + 2*k3 + k4)
    t = t0 + h; 
    return x,t