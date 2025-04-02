import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from color_grid_game import *
import unittest

class TestMinimaxBot(unittest.TestCase):

    def setUp(self):
        self.solver = Minimax_Bot()
    
    def test_move_to_play_grid00(self):
        grid = Grid.grid_from_file("input/grid00.in", read_values=True)
        pair = self.solver.move_to_play(grid, "original rules")
        self.assertEqual(grid.cost(pair), 1)    
        
    def test_move_to_play2_grid00(self):
        grid = Grid.grid_from_file("input/grid00.in", read_values=True)
        pair = self.solver.move_to_play2(grid, "original rules")
        self.assertEqual(grid.cost(pair), 1)

    def test_move_to_play_grid01(self):
        grid = Grid.grid_from_file("input/grid01.in", read_values=True)
        pair = self.solver.move_to_play(grid, "original rules")
        self.assertEqual(grid.cost(pair), 1)

    def test_move_to_play2_grid01(self):
        grid = Grid.grid_from_file("input/grid01.in", read_values=True)
        pair = self.solver.move_to_play2(grid, "original rules")
        self.assertEqual(grid.cost(pair), 1)

    def test_move_to_play_grid02(self):
        grid = Grid.grid_from_file("input/grid02.in", read_values=True)
        pair = self.solver.move_to_play(grid, "original rules")
        self.assertEqual(grid.cost(pair), 0)

    def test_move_to_play2_grid02(self):
        grid = Grid.grid_from_file("input/grid02.in", read_values=True)
        pair = self.solver.move_to_play2(grid, "original rules")
        self.assertEqual(grid.cost(pair), 0)

    def test_move_to_play_grid03(self):
        grid = Grid.grid_from_file("input/grid03.in", read_values=True)
        pair = self.solver.move_to_play(grid, "original rules")
        self.assertEqual(grid.cost(pair), 0)   
    
    def test_move_to_play2_grid03(self):
        grid = Grid.grid_from_file("input/grid03.in", read_values=True)
        pair = self.solver.move_to_play2(grid, "original rules")
        self.assertEqual(grid.cost(pair), 0)

    def test_move_to_play_grid04(self):
        grid = Grid.grid_from_file("input/grid04.in", read_values=True)
        pair = self.solver.move_to_play(grid, "original rules")
        self.assertEqual(grid.cost(pair), 0)    
    
    def test_move_to_play2_grid04(self):
        grid = Grid.grid_from_file("input/grid04.in", read_values=True)
        pair = self.solver.move_to_play2(grid, "original rules")
        self.assertEqual(grid.cost(pair), 0)
        
        
if __name__ == '__main__':
    unittest.main()
