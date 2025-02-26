import sys 
sys.path.append("code/")

import unittest
from collections import defaultdict
from solver import SolverFordFulkerson

class TestFordFulkerson(unittest.TestCase):

    def setUp(self):
        self.solver = SolverFordFulkerson(None)

    def test_ford_fulkerson_max_flow(self):
        graph = defaultdict(list)
        graph["s"].append("a")
        graph["a"].append("b")
        graph["b"].append("t")
        self.solver.even_cells = {"a"}
        self.solver.odd_cells = {"b"}
        pairs = self.solver.ford_fulkerson(graph)
        self.assertEqual(pairs, [("a", "b")])

    def test_ford_fulkerson_no_flow(self):
        graph = defaultdict(list)
        self.solver.even_cells = set()
        self.solver.odd_cells = set()
        pairs = self.solver.ford_fulkerson(graph)
        self.assertEqual(pairs, [])

    def test_ford_fulkerson_multiple_flows(self):
        graph = defaultdict(list)
        graph["s"].append("a")
        graph["a"].append("b")
        graph["b"].append("t")
        graph["s"].append("c")
        graph["c"].append("d")
        graph["d"].append("t")
        self.solver.even_cells = {"a", "c"}
        self.solver.odd_cells = {"b", "d"}
        pairs = self.solver.ford_fulkerson(graph)
        self.assertEqual(sorted(pairs), [("a", "b"), ("c", "d")])

if __name__ == '__main__':
    unittest.main()
