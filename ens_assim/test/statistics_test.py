import unittest
import numpy as np
from ens_assim.calc_stats import get_mean, get_std

DATASET_1 = np.array([[1.,1.,1.,1.,1.],[1.,1.,1.,1.,1.]]).T
MEAN_1 = np.mean(DATASET_1,axis=1,keepdims=1,)
DATASET_2 = np.array([[1.,2.,3.,4.,5.],[2.,3.,4.,5.,6.]]).T
MEAN_2 = np.mean(DATASET_2,axis=1,keepdims=1)
WEIGHTS_1 = None
WEIGHTS_2 = np.array([1.,1.])
STD_1 = np.std(DATASET_1,axis=1,keepdims=1,ddof=1)
STD_2 = np.std(DATASET_2,axis=1,keepdims=1,ddof=1)



class TestStatistics(unittest.TestCase):
    """
    Performs tests on the file calc_stats.py

    Attributes
    ----------

    Methods
    -------
    test_get_mean_no_weight()
        Tests the get_mean function with no weight
    test_get_mean_weight()
        Tests the get_mean function with weight
    test_get_std_no_weight()
        Tests the get_std function with no weight
    test_get_std_weight()
        Tests the get_std function with weight
    """

    def test_get_mean_no_weight(self):
        """
        Tests the get_mean function with no weight

        Parameters
        ----------

        Raises
        ------
        """
        mean_1 = get_mean(DATASET_1,WEIGHTS_1)
        self.assertTrue(np.all(mean_1==MEAN_1)) 

    def test_get_mean_weight(self):
        """
        Tests the get_mean function with weight

        Parameters
        ----------

        Raises
        ------
        """
        mean_2 = get_mean(DATASET_2,WEIGHTS_2)
        self.assertTrue(np.all(mean_2==MEAN_2)) 

    def test_get_std_no_weight(self):
        """
        Tests the get_std function with no weight

        Parameters
        ----------

        Raises
        ------
        """
        std_1 = get_std(DATASET_1,WEIGHTS_1)
        self.assertTrue(np.all(std_1==STD_1)) 

    def test_get_std_weight(self):
        """
        Tests the get_std function with weight

        Parameters
        ----------

        Raises
        ------
        """
        std_2 = get_std(DATASET_2,WEIGHTS_2)
        self.assertTrue(np.all(std_2==STD_2)) 
