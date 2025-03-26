from color_grid_game import *
import unittest

class Test_Cost(unittest.TestCase):
    
    def test_equal_values(self):
        grid = Grid.grid_from_file("../input/grid05.in", read_values=True)
        pair = ((0, 2), (0, 1)) 
        self.assertEqual(grid.cost(pair), 0)  
        
    def test_different_values(self):
        grid = Grid.grid_from_file("../input/grid00.in", read_values=True)
        pair = ((0, 0), (0, 1))  
        self.assertEqual(grid.cost(pair), 3)
    
    def test_equal_values2(self):
        grid = Grid.grid_from_file("../input/grid02.in", read_values=True)
        pair = ((0, 0), (1, 0))  
        self.assertEqual(grid.cost(pair), 0)   
    
    def test_different_values2(self):
        grid = Grid.grid_from_file("../input/grid01.in", read_values=True)
        pair = ((0, 0), (1, 0))  
        self.assertEqual(grid.cost(pair), 6)   
        
    def test_with_forbidden_cell(self):
        grid = Grid.grid_from_file("../input/grid05.in", read_values=True)
        # Test with a black cell (although this shouldn't happen
        # in practice since black cells are excluded from pairs)
        pair = ((0, 1), (3, 0))
        self.assertEqual(grid.cost(pair), 4) 
        
if __name__ == '__main__':
    unittest.main()