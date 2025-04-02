import sys
import os
import unittest
from collections import deque

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from color_grid_game.solvers.solver_ford_fulkerson import Solver_Ford_Fulkerson


class TestBFS(unittest.TestCase):

    def setUp(self):
        self.solver = Solver_Ford_Fulkerson(None)

    def reconstruct_path(self, parents, start, end):
        if end not in parents:
            return None
        path = []
        current = end
        while current is not None:
            path.append(current)
            current = parents[current]
        return path[::-1]

    def test_bfs_path_found(self):
        graph = {
            "s": ["a"],
            "a": ["b"],
            "b": ["t"],
            "t": []
        }
        parents = self.solver.bfs(graph, "s", "t")
        path = self.reconstruct_path(parents, "s", "t")
        self.assertEqual(path, ["s", "a", "b", "t"])

    def test_bfs_no_path(self):
        graph = {
            "s": ["a"],
            "a": [],
            "b": ["t"],
            "t": []
        }
        parents = self.solver.bfs(graph, "s", "t")
        path = self.reconstruct_path(parents, "s", "t")
        self.assertIsNone(path)

    def test_bfs_empty_graph(self):
        graph = {}
        parents = self.solver.bfs(graph, "s", "t")
        path = self.reconstruct_path(parents, "s", "t")
        self.assertIsNone(path)


if __name__ == '__main__':
    unittest.main()
