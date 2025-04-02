import sys
import os
import unittest

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from color_grid_game import *
from color_grid_game.solvers.solver_blossom import Solver_Blossom

class TestSolverBlossom(unittest.TestCase):

    def build_grid(self, colors, values):
        n = len(colors)
        m = len(colors[0])
        return Grid(n, m, colors, values)

    def test_small_grid_original_rules(self):
        colors = [
            [0, 1],
            [1, 0]
        ]
        values = [
            [1, 2],
            [3, 4]
        ]
        grid = self.build_grid(colors, values)
        solver = Solver_Blossom(grid, rules="original rules")
        pairs = solver.run()

        self.assertIsInstance(pairs, list)
        for pair in pairs:
            self.assertIsInstance(pair, tuple)
            self.assertEqual(len(pair), 2)
            for cell in pair:
                self.assertIsInstance(cell, tuple)
                self.assertEqual(len(cell), 2)

    def test_small_grid_new_rules(self):
        colors = [
            [0, 0],
            [0, 0]
        ]
        values = [
            [1, 2],
            [3, 4]
        ]
        grid = self.build_grid(colors, values)
        solver = Solver_Blossom(grid, rules="new rules")
        pairs = solver.run()

        self.assertIsInstance(pairs, list)
        for pair in pairs:
            self.assertIsInstance(pair, tuple)
            self.assertEqual(len(pair), 2)

    def test_empty_grid(self):
        colors = [
            [4, 4],
            [4, 4]
        ]
        values = [
            [0, 0],
            [0, 0]
        ]
        grid = self.build_grid(colors, values)
        solver = Solver_Blossom(grid, rules="original rules")
        pairs = solver.run()
        self.assertEqual(pairs, [])

if __name__ == '__main__':
    unittest.main()
