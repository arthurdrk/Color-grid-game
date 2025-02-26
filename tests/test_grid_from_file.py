import sys 
sys.path.append("code/")

import unittest 
from grid import Grid
import numpy as np
import matplotlib.pyplot as plt

class Test_GridLoading(unittest.TestCase):
    def test_grid0(self):
        grid = Grid.grid_from_file("input/grid00.in", read_values=True)
        self.assertEqual(grid.n, 2)
        self.assertEqual(grid.m, 3)
        self.assertEqual(grid.color, [[0, 0, 0], [0, 0, 0]])
        self.assertEqual(grid.value, [[5, 8, 4], [11, 1, 3]])

    def test_grid0_novalues(self):
        grid = Grid.grid_from_file("input/grid00.in", read_values=False)
        self.assertEqual(grid.n, 2)
        self.assertEqual(grid.m, 3)
        self.assertEqual(grid.color, [[0, 0, 0], [0, 0, 0]])
        self.assertEqual(grid.value, [[1, 1, 1], [1, 1, 1]])

    def test_grid1(self):
        grid = Grid.grid_from_file("input/grid01.in", read_values=True)
        self.assertEqual(grid.n, 2)
        self.assertEqual(grid.m, 3)
        self.assertEqual(grid.color, [[0, 4, 3], [2, 1, 0]])
        self.assertEqual(grid.value, [[5, 8, 4], [11, 1, 3]])
        





        
        
class Test_Repr(unittest.TestCase):
    def test_repr(self):
        grid = Grid.grid_from_file("input/grid00.in", read_values=True)
        self.assertEqual(repr(grid), "<grid.Grid: n=2, m=3>")
    def test_repr(self):
        grid = Grid.grid_from_file("input/grid03.in", read_values=False)
        self.assertEqual(repr(grid), "<grid.Grid: n=4, m=8>")
    def test_repr(self):
        grid = Grid.grid_from_file("input/grid11.in", read_values=True)
        self.assertEqual(repr(grid), "<grid.Grid: n=10, m=20>")
        
class Test_Cost(unittest.TestCase):
    def test_equal_values(self):
        grid = Grid.grid_from_file("input/grid05.in", read_values=True)
        pair = ((0, 2), (0, 1)) 
        self.assertEqual(self.grid.cost(pair), 0)  
        
    def test_different_values(self):
        grid = Grid.grid_from_file("input/grid05.in", read_values=True)
        pair = ((0, 0), (1, 0))  
        self.assertEqual(grid.cost(pair), 4)  
        
    def test_with_forbidden_cell(self):
        grid = Grid.grid_from_file("input/grid05.in", read_values=True)
        # Test with a black cell (although this shouldn't happen
        # in practice since black cells are excluded from pairs)
        pair = ((0, 1), (3, 0))
        self.assertEqual(grid.cost(pair), 4) 

if __name__ == '__main__':
    unittest.main()