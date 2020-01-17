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
    solve_dict 
        the dictionary containing solver dict
    num_steps
        the number of steps for the solver

    Methods
    -------
    set_solver(solver)
        Sets the solver of the ODE
    set_rhs(rhs)
        Sets the RHS function of the ODE
    set_t0(t0)
        Sets the initial time for the ODE
    set_solve_dict(solve_dict)
        Sets the stepsize of the ODE
    set_num_steps(num_steps)
        Sets the number of steps of the ODE
    
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
        self.solver_dict = None
        self.num_steps = None

    def set_solver(self, solver):
        """
        Sets the solver for the ode

        Parameters
        ----------
        Solver: type.LambdaType
            The solver of the ode

        Raises
        ------
        """
        self.solver = solver

    def set_rhs(self, rhs):
        """
        Sets the RHS of the ode

        Parameters
        ----------
        RHS: type.LambdaType
            The right hand side of the ODE

        Raises
        ------
        """
        self.rhs = rhs

    def set_t0(self, t0):
        """
        Sets the initial time

        Parameters
        ----------
        t0: int or float
            The initial time

        Raises
        ------
        """
        self.t0 = t0

    def set_solver_dict(self, solver_dict):
        """
        Sets the solver parameter dictionary

        Parameters
        ----------
        solver_dict: Dict
            The dictionary containing the 
            solver parameters

        Raises
        ------
        """    
        self.solver_dict = solver_dict

    def set_num_steps(self, num_steps):
        """
        Sets the number of steps

        Parameters
        ----------

        Raises
        ------
        """
        self.num_steps = num_steps
    
    def advance(self):
        """
        Advances the model forward n step 
        using the solver

        Parameters
        ----------

        Raises
        ------
        """
        state, t = self.solver(self.t0,self.initial_conditions,self.rhs,self.num_steps,self.solver_dict)
        return state





def rk4(t0, x0, rhs, num_steps,solver_dict):
    """
    Advances the model forward n step 
    using the solver

    Parameters
    ----------
    t0 - int or float
        Initial time
    x0 - np.ndarray
        Initial Condition
    rhs - type.LambdaType
        Right hand side
    solver_dict - Dict
        Dictionary containg parameters
    num_steps - int
        number of steps taken
    Raises
    ------
    KeyError
        If h is a missing key
    """

    if 'h' not in solver_dict:
        raise KeyError('solver_dict is missing key "h"')

    h = solver_dict['h']

    x_dim = x0.shape[0]
    ens_num = x0.shape[1]

    x = np.zeros((x_dim,ens_num,num_steps))

    for ens in range(ens_num):
        xi = np.expand_dims(x0[:,ens],1)
        for time in range(num_steps):
            k1 = h*rhs(t0, xi)
            k2 = h*rhs(t0 + 0.5*h, xi + 0.5*k1)
            k3 = h*rhs(t0 + 0.5*h, xi + 0.5*k2)
            k4 = h*rhs(t0 + h, xi + k3)
    
            xi = xi + (1.0/6.0)*(k1 + 2*k2 + 2*k3 + k4)
            t = t0 + h
            x[:,ens,time] = xi.flatten()

    return x,t