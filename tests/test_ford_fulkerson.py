from color_grid_game import *
import unittest

class TestFordFulkerson(unittest.TestCase):

    def setUp(self):
        self.solver = SolverFordFulkerson(None)

    def test_ford_fulkerson_max_flow(self):
        graph = {"s": ["a"], "a": ["b"], "b": ["t"], "t": []}
        self.solver.even_cells = {"a"}
        self.solver.odd_cells = {"b"}
        pairs = self.solver.ford_fulkerson(graph, self.solver.even_cells, self.solver.odd_cells)
        self.assertEqual(pairs, [("a", "b")])

    def test_ford_fulkerson_no_flow(self):
        graph = {}
        self.solver.even_cells = set()
        self.solver.odd_cells = set()
        pairs = self.solver.ford_fulkerson(graph, self.solver.even_cells, self.solver.odd_cells)
        self.assertEqual(pairs, [])

    def test_ford_fulkerson_multiple_flows(self):
        graph = {"s": ["a", "c"], "a": ["b"], "b": ["t"], "c": ["d"], "d": ["t"], "t": []}
        self.solver.even_cells = {"a", "c"}
        self.solver.odd_cells = {"b", "d"}
        pairs = self.solver.ford_fulkerson(graph, self.solver.even_cells, self.solver.odd_cells)
        self.assertEqual(sorted(pairs), [("a", "b"), ("c", "d")])

if __name__ == '__main__':
    unittest.main()
