import sys
sys.path.append("code/")

import unittest
from grid import Grid

class Test_String_Repr(unittest.TestCase):
    def test_str_representation00(self):
        grid = Grid.grid_from_file("input/grid00.in", read_values=True)
        expected_str = (
            "The grid is 2 x 3. It has the following colors:\n"
            "['w', 'w', 'w']\n"
            "['w', 'w', 'w']\n"
            "and the following values:\n"
            "[5, 8, 4]\n"
            "[11, 1, 3]\n"
        )
        self.assertEqual(str(grid), expected_str)
        
    def test_str_representation01(self):
        grid = Grid.grid_from_file("input/grid01.in", read_values=True)
        expected_str = (
            "The grid is 2 x 3. It has the following colors:\n"
            "['w', 'k', 'g']\n"
            "['b', 'r', 'w']\n"
            "and the following values:\n"
            "[5, 8, 4]\n"
            "[11, 1, 3]\n"
        )
        self.assertEqual(str(grid), expected_str)
            
    def test_str_representation02(self):
        grid = Grid.grid_from_file("input/grid02.in", read_values=True)
        expected_str = (
            "The grid is 2 x 3. It has the following colors:\n"
            "['w', 'k', 'g']\n"
            "['b', 'r', 'w']\n"
            "and the following values:\n"
            "[1, 1, 1]\n"
            "[1, 1, 1]\n"
        )
        self.assertEqual(str(grid), expected_str)

    def test_str_representation03(self):
        grid = Grid.grid_from_file("input/grid03.in", read_values=True)
        expected_str = (
            "The grid is 4 x 8. It has the following colors:\n"
            "['k', 'k', 'w', 'k', 'k', 'k', 'k', 'w']\n"
            "['w', 'w', 'w', 'k', 'w', 'w', 'k', 'w']\n"
            "['k', 'w', 'k', 'k', 'k', 'w', 'w', 'w']\n"
            "['k', 'w', 'w', 'k', 'w', 'w', 'w', 'w']\n"
            "and the following values:\n"
            "[1, 1, 1, 1, 1, 1, 1, 1]\n"
            "[1, 1, 1, 1, 1, 1, 1, 1]\n"
            "[1, 1, 1, 1, 1, 1, 1, 1]\n"
            "[1, 1, 1, 1, 1, 1, 1, 1]\n"
        )
        self.assertEqual(str(grid), expected_str)

if __name__ == '__main__':
    unittest.main()
