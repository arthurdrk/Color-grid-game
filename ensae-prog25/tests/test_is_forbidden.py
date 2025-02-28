import sys 
sys.path.append("code/")

import unittest 
from grid import Grid

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

    def test_grid1_nonblack2(self):
        grid = Grid.grid_from_file("input/grid02.in", read_values=False)
        self.assertEqual(grid.is_forbidden(1, 2), False)
        
        
if __name__ == '__main__':
    unittest.main()