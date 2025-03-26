import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from color_grid_game import *

class SolverBlossom(Solver):
    """
    A solver that uses weighted matching to minimize the score in a grid.
    Adapted to use a NetworkX graph instead of an adjacency dictionary.
    """

    def run(self):
        """
        Builds a NetworkX graph and uses the max_weight_matching algorithm from NetworkX.

        Returns:
        --------
        list[tuple[tuple[int, int], tuple[int, int]]]
            A list of pairs of cells.

        Raises:
        -------
        ValueError: If the graph is empty or if pairs are invalid.
        """
        pairs = self.pairs(self.rules)
        G = nx.Graph()
        for u, v in pairs:
            cost = self.grid.cost((u, v))
            value_u = self.grid.value[u[0]][u[1]]
            value_v = self.grid.value[v[0]][v[1]]
            weight = cost - value_u - value_v
            G.add_edge(u, v, weight=-weight)

        matching = nx.max_weight_matching(G, maxcardinality=False)
        self.pairs = list(matching)

        return self.pairs