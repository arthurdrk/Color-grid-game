from collections import deque, defaultdict
from grid import Grid
import numpy as np
import math
from max_weight_matching import max_weight_matching

class Solver:
    """
    A solver class for finding optimal pairs in a grid.

    Attributes:
    -----------
    grid : Grid
        The grid to be solved.
    pairs : list[tuple[tuple[int, int], tuple[int, int]]]
        A list of pairs, each being a tuple ((i1, j1), (i2, j2)) representing paired cells.
    """

    def __init__(self, grid: Grid, rules="original rules"):
        """
        Initializes the solver with a grid.

        Parameters:
        -----------
        grid : Grid
            The grid to be solved.

        Time Complexity: O(1)
        Space Complexity: O(1)
        """
        self.grid = grid
        self.pairs = []
        self.rules = rules

    def score(self) -> int:
        """
        Computes the score of the list of pairs in self.pairs.

        The score is calculated as the sum of the values of unpaired cells
        excluding black cells, plus the sum of the cost of each pair of cells.

        Returns:
        --------
        int
            The computed score.

        Time Complexity: O(n * m)
        Space Complexity: O(p) where p is the number of pairs
        """

        # Add all paired cells to the set and calculate the cost of each pair
        score = sum(self.grid.cost(pair) for pair in self.pairs)
        taken = set([cell for pair in self.pairs for cell in pair])
        score += sum(self.grid.value[i][j] for i in range(self.grid.n) 
                     for j in range(self.grid.m) 
                     if (i, j) not in taken and not self.grid.is_forbidden(i, j))
        return score
    
    
    
class SolverEmpty(Solver):
    """
    A subclass of Solver that does not implement any solving logic.
    """

    def run(self):
        """
        Placeholder method for running the solver. Does nothing.
        """
        pass
    
"""
Question 4, SolverGreedy:

Complexity of SolverGreedy:
   - Time Complexity: O(n * m)
     The `run` method iterates over each cell in the grid, checking its neighbors to find the best pair.
     The dominant term is iterating over all cells, which is O(n * m).
   - Space Complexity: O(n * m)
     The space complexity is O(n * m) due to storing the pairs and the results.

Optimality:
    The greedy algorithm pairs cells based on minimizing the immediate cost without considering the global optimum.
    This approach can lead to suboptimal solutions, especially in grids where local decisions affect the overall outcome significantly.
    Consider the following 2x3 grid (grid00.in):

    Colors:
    [
    [0, 0, 0],  # Row 1
    [0, 0, 0]   # Row 2
    ]

    Values:
    [
    [5, 8, 4],  # Row 3
    [11, 1, 3]  # Row 4
    ]

    The greedy algorithm pairs (0, 0) with (0, 1) due to immediate cost minimization, missing the optimal global configuration.
    Optimal Solution: Pair (0, 0) with (1, 0), (0, 1) with (0, 2) and (1, 1) with (1, 2), achieving a lower score (score = 12 instead of 14 with the greedy algorithm).

Possible solution (brute force) and complexity:
   - A possible solution (brute force) would be to consider all possible pairings and selecting the one with the minimum score.
     - Time Complexity: O(2^(n * m))
       -> In the worst case, each cell could potentially be paired with any of its neighbors, leading to an exponential number of configurations.
     - Space Complexity: O(2^(n * m))
       Due to the need to store all possible configurations of pairs.

Other possible solutions:
   - Bipartite Matching (e.g., Ford-Fulkerson) in the case of a grid with a unique value:
     This approach can find an optimal matching in polynomial time, specifically O(E * V), where E is the number of edges and V is the number of vertices in the bipartite graph representation of the grid.
   - Consider it as a maximum weight matching problem, can be solved using the Hungarian algorithm in O(n^3) time complexity.
"""

class SolverGreedy(Solver):
    """
    A subclass of Solver that implements a greedy algorithm to find pairs.
    """

    def run(self) -> list[tuple[tuple[int, int], tuple[int, int]]]:
        """
        Runs the greedy algorithm to find pairs of cells.

        Returns:
        --------
        list[tuple[tuple[int, int], tuple[int, int]]]
            A list of pairs of cells.

        Time Complexity: O((n * m) * log(n * m)
        Space Complexity: O((n * m) * log(n * m))
        """
        used = set()  # Cells that have already been visited
        res = []
        pairs = self.grid.all_pairs()

        # Create a dictionary to quickly access pairs by cell
        pair_dict = defaultdict(list)
        for pair in pairs:
            pair_dict[pair[0]].append(pair)
            pair_dict[pair[1]].append(pair)

        for i in range(self.grid.n):
            for j in range(self.grid.m):
                case = (i, j)
                if case not in used:
                    used.add(case)
                    if case in pair_dict:
                        # Find the neighboring cell that minimizes the cost
                        try:
                            best_pair = min(
                                (pair for pair in pair_dict[case] if pair[0] not in used or pair[1] not in used),
                                key=lambda x: self.grid.cost(x))
                            if best_pair[0] == case:  # indentify what is the index of the best cell in pair and what is the one of case
                                res.append((case, best_pair[1]))
                                used.add(best_pair[1])
                            else:
                                res.append((case, best_pair[0]))
                                used.add(best_pair[0])
                        except ValueError:
                            pass
        self.pairs = res
        return res

class SolverGreedy_upgraded(Solver):
    """
    Improvement of SolverGreedy that tries all possible starting points and keeps the pairing with the minimum score.
    """

    def run(self) -> list[tuple[tuple[int, int], tuple[int, int]]]:
        """
        Runs the greedy algorithm from all possible starting cells and selects the best pairing.

        Returns:
            list[tuple[tuple[int, int], tuple[int, int]]: List of pairs with the lowest score.
        """
        pairs = self.grid.all_pairs()
        pair_dict = defaultdict(list)
        for pair in pairs:
            pair_dict[pair[0]].append(pair)
            pair_dict[pair[1]].append(pair)

        best_score = float('inf')
        best_pairs = []

        # Iterate over all possible starting cells (k, l)
        for k in range(self.grid.n):
            for l in range(self.grid.m):
                used = set()
                current_pairs = []
                # Traverse grid in shifted order based on k and l
                for row_shift in range(self.grid.n):
                    for col_shift in range(self.grid.m):
                        i = (row_shift + k) % self.grid.n
                        j = (col_shift + l) % self.grid.m
                        current_cell = (i, j)
                        if current_cell not in used and not self.grid.is_forbidden(i, j):
                            used.add(current_cell)
                            # Find all possible pairs for current_cell not yet used
                            available_pairs = []
                            for pair in pair_dict.get(current_cell, []):
                                other = pair[0] if pair[1] == current_cell else pair[1]
                                if other not in used and not self.grid.is_forbidden(other[0], other[1]):
                                    available_pairs.append(pair)
                            if available_pairs:
                                best_pair = min(available_pairs, key=lambda p: self.grid.cost(p))
                                other_cell = best_pair[0] if best_pair[1] == current_cell else best_pair[1]
                                current_pairs.append((current_cell, other_cell))
                                used.add(other_cell)
                # Calculate score for current_pairs
                self.pairs = current_pairs
                score = self.score()
                # Update best if current score is better
                if score < best_score:
                    best_score = score
                    best_pairs = current_pairs.copy()
        self.pairs = best_pairs
        return best_pairs
 
class SolverFordFulkerson(Solver):
    """
    A subclass of Solver that implements a bipartite matching algorithm to find pairs.
    """
    
    def run(self) -> list[tuple[tuple[int, int], tuple[int, int]]]:
        """
        Runs the bipartite matching algorithm to find pairs of cells.

        Returns:
        --------
        list[tuple[tuple[int, int], tuple[int, int]]]
            A list of pairs of cells.

        Time Complexity: O(E * V) where E is the number of edges and V is the number of vertices
        Space Complexity: O(E + V)
        """
        graph = defaultdict(list)
        even_cells = set()
        odd_cells = set()

        # Add edges between cells (direction: from even to odd)
        for cell1, cell2 in self.grid.all_pairs():
            even, odd = (cell1, cell2) if sum(cell1) % 2 == 0 else (cell2, cell1)
            even_cells.add(even)
            odd_cells.add(odd)
            graph[even].append(odd)

        # Add edges from source "s" to even cells
        for even in even_cells:
            graph["s"].append(even)

        # Add edges from odd cells to sink "t"
        for odd in odd_cells:
            graph[odd].append("t")

        # Sets of cells for later extraction of the matching
        self.even_cells = even_cells
        self.odd_cells = odd_cells
        # Get optimal pairs
        self.pairs = self.ford_fulkerson(graph, even_cells, odd_cells)
        return self.pairs

    @staticmethod
    def bfs(graph: dict, s: str, t: str) -> list[int]:
        """
        Performs a BFS to find a path from source 's' to sink 't' in the graph.

        Parameters:
        -----------
        graph : dict
            The graph represented as an adjacency list.
        s : str
            The source node.
        t : str
            The sink node.

        Returns:
        --------
        list[int]
            The path from 's' to 't' if found, otherwise None.

        Time Complexity: O(V + E)
        Space Complexity: O(V)
        """
        queue = deque([s])
        parents = {s: None}

        while queue:
            u = queue.popleft()
            for v in graph.get(u, []):
                if v not in parents:
                    parents[v] = u
                    if v == t:
                        return SolverFordFulkerson.reconstruct_path(parents, s, t)
                    queue.append(v)

        return None

    @staticmethod
    def reconstruct_path(parents: dict, s: str, t: str) -> list[int]:
        """
        Reconstructs the path from 's' to 't' using the parents dictionary.

        Parameters:
        -----------
        parents : dict
            A dictionary where parents[v] is the predecessor of v on the path from 's' to 'v'.
        s : str
            The source node.
        t : str
            The sink node.

        Returns:
        --------
        list[int]
            The reconstructed path from 's' to 't'.

        Time Complexity: O(V)
        Space Complexity: O(V)
        """
        path = []
        current = t
        while current is not None:
            path.append(current)
            current = parents[current]
        return path[::-1]

    @classmethod
    def ford_fulkerson(cls, graph: dict, even_cells: set, odd_cells: set) -> list[tuple[tuple[int, int], tuple[int, int]]]:
        """
        Computes the maximum flow (maximum matching) in the bipartite graph using the Ford-Fulkerson method.

        Parameters:
        -----------
        graph : dict
            The graph represented as an adjacency list.

        Returns:
        --------
        list[tuple[tuple[int, int], tuple[int, int]]]
            The maximum matching as a list of pairs of cells.

        Time Complexity: O(E * V)
        Space Complexity: O(E + V)
        """
        while True:
            path = cls.bfs(graph, "s", "t")
            if path is None:
                break
            for u, v in zip(path, path[1:]):
                graph[u].remove(v)
                graph[v].append(u)

        return [(u, odd) for odd in odd_cells for u in graph[odd] if u in even_cells]


################################################################################
#                               WORK IN PROGRESS                               #
################################################################################

import networkx as nx
from collections import defaultdict

from max_weight_matching import max_weight_matching

class SolverBlossom(Solver):
    """
    Un solveur qui utilise un appariement pondéré pour minimiser le score dans une grille.
    Adapté pour utiliser un graphe NetworkX au lieu d'un dictionnaire d'adjacence.
    """

    def run(self):
        """
        Construit un graphe NetworkX et utilise l'algorithme max_weight_matching de NetworkX.
        """
        if self.rules == "original rules":
            pairs = self.grid.all_pairs()
        elif self.rules == "new rules":
            pairs = self.grid.all_pairs_new_rules()
         
        G = nx.Graph()
        for u,v in pairs:
                cost = self.grid.cost((u, v))
                value_u = self.grid.value[u[0]][u[1]]
                value_v = self.grid.value[v[0]][v[1]]
                weight = cost - value_u - value_v
                G.add_edge(u, v, weight=-weight)

        matching = nx.max_weight_matching(G, maxcardinality=False)
        self.pairs = list(matching)
        
        return self.pairs

from hungarian_algorithm import linear_sum_assignment
import numpy as np

class SolverHungarian(Solver):

    def run(self):
        """
        Builds a bipartite cost matrix using only cells present in valid pairs.
        Applies the Hungarian algorithm to find optimal pairs.
        """
        if self.rules == "original rules":
            # Collect all unique cells from valid pairs
            valid_pairs = self.grid.all_pairs()
            all_cells = set()
            for u, v in valid_pairs:
                all_cells.add(u)
                all_cells.add(v)
            
            # Split into even/odd based on coordinate parity
            even_cells = [cell for cell in all_cells if (cell[0] + cell[1]) % 2 == 0]
            odd_cells = [cell for cell in all_cells if (cell[0] + cell[1]) % 2 == 1]
            
            # Create mappings for matrix indices
            even_to_idx = {cell: i for i, cell in enumerate(even_cells)}
            odd_to_idx = {cell: j for j, cell in enumerate(odd_cells)}
            
            # Build cost matrix with valid pairs only
            cost_matrix = np.full((len(even_cells), len(odd_cells)), 0)
            for u, v in valid_pairs:
                # Ensure u is even and v is odd
                if (u[0] + u[1]) % 2 != 0:
                    u, v = v, u
                if u in even_to_idx and v in odd_to_idx:
                    cost = self.grid.cost((u, v))
                    weight = cost - self.grid.value[u[0]][u[1]] - self.grid.value[v[0]][v[1]]
                    cost_matrix[even_to_idx[u], odd_to_idx[v]] =  weight
            
            # Apply Hungarian algorithm
            row_ind, col_ind = linear_sum_assignment(cost_matrix)
            
            # Rebuild pairs from matrix indices
            self.pairs = []
            for i, j in zip(row_ind, col_ind):
                if cost_matrix[i][j] !=0:
                    self.pairs.append((even_cells[i], odd_cells[j]))
                    
        elif self.rules == "new rules":
            # Handle new rules (implementation omitted)
            pass
            
        return self.pairs

class SolverHungarian2(Solver):
    def run(self):
        if self.rules == "original rules":
            valid_pairs = self.grid.all_pairs()
        elif self.rules == "new rules":
            valid_pairs = self.grid.all_pairs_new_rules()

        # Split cells into even and odd partitions based on coordinates
        even_cells = []
        odd_cells = []
        for cell in {cell for pair in valid_pairs for cell in pair}:
            if (cell[0] + cell[1]) % 2 == 0:
                even_cells.append(cell)
            else:
                odd_cells.append(cell)

        # Create bipartite cost matrix (even rows, odd columns)
        cost_matrix = np.full((len(even_cells), len(odd_cells)), 0)
        even_to_idx = {cell: i for i, cell in enumerate(even_cells)}
        odd_to_idx = {cell: j for j, cell in enumerate(odd_cells)}

        for u, v in valid_pairs:
            if (u[0] + u[1]) % 2 != 0:
                u, v = v, u  # Ensure u is even, v is odd
            if u in even_to_idx and v in odd_to_idx:
                cost = self.grid.cost((u, v))
                value_u = self.grid.value[u[0]][u[1]]
                value_v = self.grid.value[v[0]][v[1]]
                weight = cost - value_u - value_v
                cost_matrix[even_to_idx[u], odd_to_idx[v]] = weight

        # Apply Hungarian algorithm on the bipartite matrix
        row_ind, col_ind = linear_sum_assignment(cost_matrix)
        
        # Rebuild valid pairs from the result
        self.pairs = []
        for i, j in zip(row_ind, col_ind):
            if cost_matrix[i, j] < 0:
                u = even_cells[i]
                v = odd_cells[j]
                if ((u, v) in valid_pairs) or ((v, u) in valid_pairs):
                    self.pairs.append((u, v))

        return self.pairs


