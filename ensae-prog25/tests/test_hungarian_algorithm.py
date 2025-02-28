import sys 
sys.path.append("code/")

import unittest
import numpy as np
from solver import SolverGeneral

class TestHungarianAlgorithm(unittest.TestCase):

    def setUp(self):
        self.solver = SolverGeneral(None)

    def test_hungarian_algorithm_simple(self):
        # Simple 2x2 cost matrix
        cost_matrix = np.array([[4, 1], [2, 3]])
        row_ind, col_ind = self.solver.hungarian_algorithm(cost_matrix)
        self.assertEqual(row_ind, [0, 1])
        self.assertEqual(col_ind, [1, 0])

    def test_hungarian_algorithm_identity(self):
        # Identity matrix should return diagonal pairs
        cost_matrix = np.array([[0, 1, 2], [1, 0, 3], [2, 3, 0]])
        row_ind, col_ind = self.solver.hungarian_algorithm(cost_matrix)
        self.assertEqual(row_ind, [0, 1, 2])
        self.assertEqual(col_ind, [0, 1, 2])

    def test_hungarian_algorithm_large_values(self):
        # Matrix with large values
        cost_matrix = np.array([[1000, 2000], [3000, 4000]])
        row_ind, col_ind = self.solver.hungarian_algorithm(cost_matrix)
        self.assertEqual(row_ind, [0, 1])
        self.assertEqual(col_ind, [0, 1])

    def test_hungarian_algorithm_zero_matrix(self):
        # Matrix with all zeros
        cost_matrix = np.array([[0, 0], [0, 0]])
        row_ind, col_ind = self.solver.hungarian_algorithm(cost_matrix)
        self.assertEqual(row_ind, [0, 1])
        self.assertEqual(col_ind, [0, 1])

if __name__ == '__main__':
    unittest.main()
