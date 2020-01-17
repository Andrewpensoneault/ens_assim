import unittest
import numpy as np
from ens_assim.perturb import absolute_uncorr_perturb, percent_uncorr_perturb

STATE_1 = np.array([[1.,1.,1.,1.]]).T
STD_1 = np.array([0.,0.,0.,0.])
STATE_2 = np.array([[1.,2.],[3.,4.]])
STD_2 = np.array([.1,.1])

np.random.seed(1)
PERT_1_1 = STATE_1
PERT_1_2 = STATE_1
PERT_2_1 = np.zeros((2,2))
PERT_2_2 = np.zeros((2,2))
ERR_2 = np.random.normal(0,1,(2,2))
for i in range(2):
    PERT_2_1[:,i] = (np.expand_dims(STATE_2[:,i],1) + np.diag(STD_2) @ np.expand_dims(ERR_2[:,i],1)).flatten()
    PERT_2_2[:,i] = (np.expand_dims(STATE_2[:,i],1) + np.diag(STATE_2[:,i]*STD_2) @ np.expand_dims(ERR_2[:,i],1)).flatten()

class TestPerturb(unittest.TestCase):
    """
    Performs tests on the file calc_stats.py

    Attributes
    ----------

    Methods
    -------
    test_absolute_uncorr_perturb_no_error()
        Tests the absolute_uncorr_perturb with no error
    test_percent_uncorr_perturb_no_error()
        Tests the percent_uncorr_perturb with no error
    test_absolute_uncorr_perturb_error()
        Tests the absolute_uncorr_perturb with error
    test_percent_uncorr_perturb_error()
        Tests the percent_uncorr_perturb with error
    """
    def test_absolute_uncorr_perturb_no_error(self):
        """
        Tests the absolute_uncorr_perturb with no error

        Parameters
        ----------

        Raises
        ------
        """
        state_pert = absolute_uncorr_perturb(STATE_1,STD_1)
        self.assertTrue(np.all(state_pert==PERT_1_1))
        
    def test_percent_uncorr_perturb_no_error(self):
        """
        Tests the percent_uncorr_perturb with no error

        Parameters
        ----------

        Raises
        ------
        """
        state_pert = percent_uncorr_perturb(STATE_1,STD_1)
        self.assertTrue(np.all(state_pert==PERT_1_2))

    def test_absolute_uncorr_perturb_error(self):
        """
        Tests the absolute_uncorr_perturb with error

        Parameters
        ----------

        Raises
        ------
        """
        np.random.seed(1)
        state_pert = absolute_uncorr_perturb(STATE_2,STD_2)
        self.assertTrue(np.all(state_pert==PERT_2_1))

    def test_percent_uncorr_perturb_error(self):
        """
        Tests the percent_uncorr_perturb with error

        Parameters
        ----------

        Raises
        ------
        """
        np.random.seed(1)
        state_pert = percent_uncorr_perturb(STATE_2,STD_2)
        self.assertTrue(np.all(state_pert==PERT_2_2))