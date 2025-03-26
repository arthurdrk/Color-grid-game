from color_grid_game import *
import unittest

class TestBFS(unittest.TestCase):

    def setUp(self):
        self.solver = SolverFordFulkerson(None)

    def test_bfs_path_found(self):
        graph = {
            "s": ["a"],
            "a": ["b"],
            "b": ["t"],
            "t": []
        }
        path = self.solver.bfs(graph, "s", "t")
        self.assertEqual(path, ["s", "a", "b", "t"])

    def test_bfs_no_path(self):
        graph = {
            "s": ["a"],
            "a": [],
            "b": ["t"],
            "t": []
        }
        path = self.solver.bfs(graph, "s", "t")
        self.assertIsNone(path)

    def test_bfs_empty_graph(self):
        graph = {}
        path = self.solver.bfs(graph, "s", "t")
        self.assertIsNone(path)

if __name__ == '__main__':
    unittest.main()
