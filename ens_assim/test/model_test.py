import unittest
import numpy as np
from ens_assim.model.model import ODE, Identity, rk4
T0 = 0
T = np.array([.1,.2])
X0 = np.array([[1.,2.,3.],[2.,3.,4.]]).T
SOLVER = rk4
STEP_SIZE = .1
NUM_STEP = 2
RHS_0 = lambda t,x: np.zeros(x.shape)
RHS_1 = lambda t,x: np.ones(x.shape)
SOL_0 = np.zeros((3,2,2))
SOL_0[:,:,0] = X0
SOL_0[:,:,1] = X0

FUNC_1 = lambda t,x: x+t*np.ones(x.shape)
SOL_1 = np.zeros((3,2,2))
SOL_1[:,:,0] = FUNC_1(T0+STEP_SIZE,X0)
SOL_1[:,:,1] = FUNC_1(T0+2*STEP_SIZE,X0)

SOLVER_DICT = {'h':STEP_SIZE}


class TestModel(unittest.TestCase): 
    """
    Performs tests on the file ./model/model.py

    Attributes
    ----------

    Methods
    -------
    test_rk4()
        Tests the runga kutta function with constant function
    test_ode_const()
        Tests the class ODE with linear function
    test_identity()
        Tests the identity Model
    """
    def test_rk4(self):
        """
        Tests the RK4 function

        Parameters
        ----------

        Raises
        ------
        """
        x, t = rk4(T0, X0, RHS_0, NUM_STEP, SOLVER_DICT)
        self.assertTrue(np.all(x==SOL_0))
        self.assertTrue(np.all(t==T))

    def test_ode_const(self):
        """
        Tests the class ODE with constant ODE

        Parameters
        ----------

        Raises
        ------
        """
        model = ODE(X0)
        model.set_solver(SOLVER)
        model.set_rhs(RHS_1)
        model.set_t0(T0)
        model.set_solver_dict(SOLVER_DICT)
        model.set_num_steps(NUM_STEP)

        x, t = model.advance()

        self.assertTrue(np.all(np.abs(x-SOL_1)<10e-12))
        self.assertTrue(np.all(t==T))

    def test_identity(self):
        """
        Tests the class Identity

        Parameters
        ----------

        Raises
        ------
        """
        model = Identity(X0)
        x = model.advance()
        self.assertTrue(np.all(x==X0))
