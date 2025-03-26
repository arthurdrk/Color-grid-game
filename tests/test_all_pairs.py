from color_grid_game import *
import unittest

class TestAllPairs(unittest.TestCase):
    
    def test_simple_grid(self):
        grid = Grid.grid_from_file("../input/grid00.in", read_values=True)
        expected_pairs = [((0, 0), (0, 1)), ((0, 0), (1, 0)), ((0, 1), (0, 2)), ((0, 1), (1, 1)),
                          ((0, 2), (1, 2)), ((1, 0), (1, 1)), ((1, 1), (1, 2))]
        self.assertEqual(sorted(grid.all_pairs("original_rules")), sorted(expected_pairs))

    def test_with_forbidden_cells(self):
        grid = Grid.grid_from_file("../input/grid01.in", read_values=True)
        expected_pairs = [((0, 0), (1, 0)), ((0, 2), (1, 2)), ((1, 0), (1, 1)), ((1, 1), (1, 2))]
        self.assertEqual(sorted(grid.all_pairs("original_rules")), sorted(expected_pairs))
        
    def test_with_forbidden_cells2(self):
        grid = Grid.grid_from_file("../input/grid02.in", read_values=True)
        expected_pairs = [((0, 0), (1, 0)), ((0, 2), (1, 2)), ((1, 0), (1, 1)), ((1, 1), (1, 2))]
        self.assertEqual(sorted(grid.all_pairs("original_rules")), sorted(expected_pairs))
        
    def test_with_forbidden_cells3(self):
        grid = Grid.grid_from_file("../input/grid05.in", read_values=True)
        expected_pairs = [((0, 0), (1, 0)), ((0, 2), (0, 3)), ((0, 2), (1, 2)), ((0, 5), (1, 5)),
                          ((1, 0), (1, 1)), ((1, 0), (2, 0)), ((1, 1), (1, 2)), ((1, 2), (1, 3)),
                          ((1, 2), (2, 2)), ((1, 3), (1, 4)), ((1, 4), (1, 5)), ((1, 5), (2, 5)),
                          ((2, 1), (2, 2)), ((2, 1), (3, 1)), ((2, 2), (3, 2)), ((2, 5), (3, 5)),
                          ((2, 7), (3, 7)), ((3, 1), (3, 2)), ((3, 2), (3, 3)), ((3, 3), (3, 4)),
                          ((3, 4), (3, 5)), ((3, 6), (3, 7))]
        self.assertEqual(sorted(grid.all_pairs("original_rules")), sorted(expected_pairs))

if __name__ == '__main__':
    unittest.main()

