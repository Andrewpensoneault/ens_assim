import unittest
import numpy as np
import scipy.linalg
from ens_assim.assimilate.assimilate import No_Assimilate, EnKF, SREnKF, SIR
from ens_assim.measure.measure import Measure
WEIGHTS = np.array([1.,1.])
DATA_COV = np.array([[.25]])
DATA_STD = np.array([[.5]])
DATA_MEAS = np.array([[1.5]])
STATE = np.array([[1,2],[1,2]])

H = lambda x: np.array([[1,0]]) @ x
LIKELIHOOD = lambda x: np.exp(-(1/2)*(np.diag((H(x)-DATA_MEAS).T @ np.linalg.inv(DATA_COV) @ (H(x)-DATA_MEAS))))
THRESHOLD = 1
MEASURE = Measure(DATA_COV,DATA_MEAS,H)
ENS_NUM=2

class TestAssimilate(unittest.TestCase):
    """
    Performs tests on the file ./assimilate/assimilate.py

    Attributes
    ----------

    Methods
    -------
    test_no_assimilate()
        Tests the no assimilation algorithm
    test_srenkf()
        Tests the SREnKF algorithm
    test_enkf()
        Tests the EnKF algorithm
    test_sir()
        Tests the SIR algorithm
    """
    def test_no_assimilate(self):
        """
        Tests the no assimilation algorithm

        Parameters
        ----------

        Raises
        ------
        """
        model = No_Assimilate()
        x = model.analyze(STATE,MEASURE)
        self.assertTrue(np.all(x==STATE))

    def test_srenkf(self):
        """
        Tests the SREnKF algorithm

        Parameters
        ----------

        Raises
        ------
        """
        xmean = np.mean(STATE,axis=1, keepdims=1)
        pert = (STATE-xmean)/np.sqrt(ENS_NUM-1)
        xpostmean = xmean + (pert@H(pert).T)@np.linalg.inv(H(pert)@H(pert).T+DATA_COV)@(DATA_MEAS-H(xmean))
        Tinv = np.linalg.inv(np.eye(ENS_NUM,ENS_NUM) + (H(pert).T @ np.linalg.solve(DATA_COV,H(pert))))
        Tsqrtinv = scipy.linalg.cholesky(Tinv) 
        xpost = xpostmean + np.sqrt(ENS_NUM-1)*pert @ Tsqrtinv 
        model = SREnKF()
        x = model.analyze(STATE,MEASURE)
        self.assertTrue(np.all(x==xpost))

    def test_enkf(self):
        """
        Tests the EnKF algorithm

        Parameters
        ----------

        Raises
        ------
        """
        np.random.seed(1)
        rand = np.random.normal(0,1,(1,2))
        xmean = np.mean(STATE,axis=1, keepdims=1)
        pert = (STATE-xmean)/np.sqrt(ENS_NUM-1)
        xpost = STATE + (pert@H(pert).T)@np.linalg.inv(H(pert)@H(pert).T+DATA_COV)@(DATA_MEAS+DATA_STD@rand-H(STATE))
        np.random.seed(1)
        model = EnKF()
        x = model.analyze(STATE,MEASURE)
        self.assertTrue(np.all(x==xpost))

    def test_sir(self):
        """
        Tests the SIR algorithm

        Parameters
        ----------

        Raises
        ------
        """
        np.random.seed(1)
        model = SIR()
        model.set_likelihood(LIKELIHOOD)
        model.set_threshold(THRESHOLD)
        model.set_weights(WEIGHTS)
        x = model.analyze(STATE,MEASURE)
        weights = model.weights
        self.assertTrue(np.all(x==STATE))
        self.assertTrue(np.all(weights == WEIGHTS/np.sum(WEIGHTS)))
