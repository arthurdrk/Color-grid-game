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
        
class Test_is_forbidden(unittest.TestCase):
    def test_grid0(self):
        grid = Grid.grid_from_file("input/grid00.in", read_values=True)
        self.assertEqual(grid.is_forbidden(1, 1), False)
        
    def test_grid1_black(self):
        grid = Grid.grid_from_file("input/grid01.in", read_values=True)
        self.assertEqual(grid.is_forbidden(0, 1), True)    
        
    def test_grid1_nonblack(self):
        grid = Grid.grid_from_file("input/grid01.in", read_values=False)
        self.assertEqual(grid.is_forbidden(1, 1), False)

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

class Test_String_Repr(unittest.TestCase):
    def test_str_representation(self):
        grid = Grid.grid_from_file("input/grid02.in", read_values=True)
        expected_str = "The grid is 2 x 3. It has the following colors:\n['w', 'b', 'g']\n['b', 'r', 'w']\nand the following values:\n[1, 1, 1]\n[1, 1, 1]\n"
        self.assertEqual(str(grid), expected_str)
        
    def test_str_representation2(self):
        grid = Grid.grid_from_file("input/grid02.in", read_values=True)
        expected_str = "The grid is 4 x 8. It has the following colors:\n"
        expected_str += "['w', 'r', 'r', 'w', 'w', 'w', 'g', 'g']\n"
        expected_str += "['k', 'w', 'k', 'r', 'b', 'k', 'g', 'k']\n"
        expected_str += "['k', 'g', 'b', 'k', 'k', 'g', 'g', 'k']\n"
        expected_str += "['w', 'k', 'w', 'r', 'k', 'k', 'r', 'k']\n"
        expected_str += "and the following values:\n"
        expected_str += "[1, 1, 1, 1, 1, 1, 1, 1]\n"
        expected_str += "[1, 1, 1, 1, 1, 1, 1, 1]\n"
        expected_str += "[1, 1, 1, 1, 1, 1, 1, 1]\n"
        expected_str += "[1, 1, 1, 1, 1, 1, 1, 1]\n" 
        self.assertEqual(str(grid), expected_str)
        
    def test_str_with_values(self):
        grid = Grid.grid_from_file("input/grid01.in", read_values=True)
        expected_str = "The grid is 2 x 3. It has the following colors:\n['w', 'k', 'g']\n['b', 'r', 'w']\nand the following values:\n[5, 8, 4]\n[11, 1, 3]\n"
        self.assertEqual(str(grid), expected_str)
        
        
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

class TestAllPairs(unittest.TestCase):
    def test_simple_grid(self):
        grid = Grid.grid_from_file("input/grid00.in", read_values=True)
        expected_pairs = [((0, 0), (0, 1)), ((0, 1), (0, 2)), ((1, 0), (1, 1)), ((1, 1), (1, 2))]
        self.assertEqual(sorted(grid.all_pairs()), sorted(expected_pairs))

    def test_with_forbidden_cells(self):
        grid = Grid.grid_from_file("input/grid01.in", read_values=True)
        expected_pairs = [((0, 0), (0, 1)), ((0, 1), (0, 2)), ((1, 0), (1, 1)), ((1, 1), (1, 2))]
        self.assertEqual(sorted(grid.all_pairs()), sorted(expected_pairs))

    def test_with_forbidden_cells2(self):
        grid = Grid.grid_from_file("input/grid05.in", read_values=True)
        expected_pairs = [
            ((0, 0), (0, 1)), ((0, 1), (0, 2)), ((0, 2), (0, 3)), ((0, 3), (0, 4)),
            ((0, 4), (0, 5)), ((0, 5), (0, 6)), ((0, 6), (0, 7)), ((1, 0), (1, 1)),
            ((1, 1), (1, 2)), ((1, 2), (1, 3)), ((1, 3), (1, 4)), ((1, 4), (1, 5)),
            ((1, 5), (1, 6)), ((1, 6), (1, 7)), ((2, 0), (2, 1)), ((2, 1), (2, 2)),
            ((2, 2), (2, 3)), ((2, 3), (2, 4)), ((2, 4), (2, 5)), ((2, 5), (2, 6)),
            ((2, 6), (2, 7)), ((3, 0), (3, 1)), ((3, 1), (3, 2)), ((3, 2), (3, 3)),
            ((3, 3), (3, 4)), ((3, 4), (3, 5)), ((3, 5), (3, 6)), ((3, 6), (3, 7))
        ]
        self.assertEqual(sorted(grid.all_pairs()), sorted(expected_pairs))


class TestVois(unittest.TestCase):
    def test_grid00_center_cell(self):
        grid = Grid.grid_from_file("input/grid00.in", read_values=True)
        expected_neighbors = [(0, 1), (1, 0), (1, 2)]
        self.assertEqual(sorted(grid.vois(0, 1)), sorted(expected_neighbors))

    def test_grid00_corner_cell(self):
        grid = Grid.grid_from_file("input/grid00.in", read_values=True)
        expected_neighbors = [(0, 1), (1, 0)]
        self.assertEqual(sorted(grid.vois(0, 0)), sorted(expected_neighbors))

    def test_grid05_center_cell(self):
        grid = Grid.grid_from_file("input/grid05.in", read_values=True)
        expected_neighbors = [(2, 3), (2, 5), (3, 4), (4, 4)]
        self.assertEqual(sorted(grid.vois(3, 4)), sorted(expected_neighbors))

    def test_grid05_corner_cell(self):
        grid = Grid.grid_from_file("input/grid05.in", read_values=True)
        expected_neighbors = [(0, 1), (1, 0)]
        self.assertEqual(sorted(grid.vois(0, 0)), sorted(expected_neighbors))

    def test_grid05_edge_cell(self):
        grid = Grid.grid_from_file("input/grid05.in", read_values=True)
        expected_neighbors = [(0, 1), (2, 1), (1, 0)]
        self.assertEqual(sorted(grid.vois(1, 0)), sorted(expected_neighbors))

if __name__ == '__main__':
    unittest.main()