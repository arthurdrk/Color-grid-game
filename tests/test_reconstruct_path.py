import sys 
sys.path.append("code/")

import unittest
from solver import SolverFordFulkerson

class TestReconstructPath(unittest.TestCase):

    def setUp(self):
        self.solver = SolverFordFulkerson(None)

    def test_reconstruct_path_valid(self):
        parents = {
            "s": None,
            "a": "s",
            "b": "a",
            "t": "b"
        }
        path = self.solver.reconstruct_path(parents, "s", "t")
        self.assertEqual(path, ["s", "a", "b", "t"])

    def test_reconstruct_path_single_node(self):
        parents = {"s": None}
        path = self.solver.reconstruct_path(parents, "s", "s")
        self.assertEqual(path, ["s"])

    def test_reconstruct_path_no_path(self):
        parents = {
            "s": None,
            "a": "s"
        }
        path = self.solver.reconstruct_path(parents, "s", "b")
        self.assertEqual(path, ["b"])

if __name__ == '__main__':
    unittest.main()
