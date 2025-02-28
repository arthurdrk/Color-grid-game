import sys 
sys.path.append("code/")

import unittest
from grid import Grid
from solver import Solver

class TestSolverScore(unittest.TestCase):
    
    def test_score_empty_pairs(self):
        grid = Grid.grid_from_file("input/grid00.in", read_values=True)
        solver = Solver(grid)
        self.assertEqual(solver.score(), 32)  # Correct sum of all values

    def test_score_with_pairs(self):
        grid = Grid.grid_from_file("input/grid01.in", read_values=True)
        solver = Solver(grid)
        solver.pairs = [((0, 0), (1, 0)), ((1, 1), (1, 2))]
        self.assertEqual(solver.score(), 12)  # Correct score calculation

    def test_score_without_values(self):
        grid = Grid.grid_from_file("input/grid02.in", read_values=True)
        solver = Solver(grid)
        solver.pairs = [((0, 0), (1, 0)), ((1, 1), (1, 2))]
        self.assertEqual(solver.score(), 1)  # Correct score calculation


if __name__ == '__main__':
    unittest.main()
