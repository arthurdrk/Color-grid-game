import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from color_grid_game import *
import unittest

class Test_Constructor(unittest.TestCase):
    
    def test_constructor_with_parameters(self):
        color = [[0, 1], [2, 3]]
        value = [[5, 6], [7, 8]]
        grid = Grid(2, 2, color, value)
        self.assertEqual(grid.n, 2)
        self.assertEqual(grid.m, 2)
        self.assertEqual(grid.color, color)
        self.assertEqual(grid.value, value)
        
    def test_constructor_without_color(self):
        grid = Grid(3, 2)
        self.assertEqual(grid.n, 3)
        self.assertEqual(grid.m, 2)
        self.assertEqual(grid.color, [[0, 0], [0, 0], [0, 0]])
        self.assertEqual(grid.value, [[1, 1], [1, 1], [1, 1]])
        
    def test_constructor_without_value(self):
        color = [[0, 1], [2, 3]]
        grid = Grid(2, 2, color)
        self.assertEqual(grid.n, 2)
        self.assertEqual(grid.m, 2)
        self.assertEqual(grid.color, color)
        self.assertEqual(grid.value, [[1, 1], [1, 1]])
        
if __name__ == '__main__':
    unittest.main()