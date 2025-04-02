import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from color_grid_game import *
import unittest

class TestMinimaxBot(unittest.TestCase):


    def test_mcts_move_grid00(self):
        grid = Grid.grid_from_file("input/grid00.in", read_values=True)
        self.solver = MCTS_Bot(grid)
        pair = self.solver.mcts_move()
        self.assertEqual(grid.cost(pair), 2)

    def test_mcts_move_grid01(self):
        grid = Grid.grid_from_file("input/grid01.in", read_values=True)
        self.solver = MCTS_Bot(grid)
        pair = self.solver.mcts_move()
        self.assertEqual(grid.cost(pair), 1)
    
    def test_simulate_from_pair_grid00(self):
        grid = Grid.grid_from_file("input/grid00.in", read_values=True)
        self.solver = MCTS_Bot(grid)
        all_pairs = grid.all_pairs()
        pair = all_pairs[0]
        res = self.solver.simulate_from_pair(pair, all_pairs)
        self.assertIsInstance(res, int)

    def test_epsilon_greedy_from_pairs_grid00(self):
        grid = Grid.grid_from_file("input/grid02.in", read_values=True)
        self.solver = MCTS_Bot(grid)
        all_pairs = grid.all_pairs()
        res = self.solver.epsilon_greedy_from_pairs(all_pairs)
        self.assertIsInstance(res, tuple)
        

if __name__ == '__main__':
    unittest.main()
