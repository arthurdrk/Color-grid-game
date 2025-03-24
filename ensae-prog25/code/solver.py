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

    def __init__(self, grid: Grid):
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
    
class SolverGreedy2(Solver):
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

        Time Complexity: O(n * m)
        Space Complexity: O(n * m)
        """
        used = set()  # Cells that have already been visited
        res = []
        pairs = self.grid.all_pairs()

        # Create a dictionary to quickly access pairs by cell
        pair_dict = defaultdict(list)
        for pair in pairs:
            pair_dict[pair[0]].append(pair)
            pair_dict[pair[1]].append(pair)

        for case in pair_dict:
                if not case in used:
                    used.add(case)
                    # Find the neighboring cell that minimizes the cost
                    try:
                        best_pair = min(
                            (pair for pair in pair_dict[case] if pair[0] not in used or pair[1] not in used),
                            key=lambda x: self.grid.cost(x))
                        if best_pair[0] == case:
                            res.append((case, best_pair[1]))
                            used.add(best_pair[1])
                        else:
                            res.append((case, best_pair[0]))
                            used.add(best_pair[0])
                    except ValueError:
                        pass
        self.pairs = res
        return res

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

class SolverBlossom(Solver):
    """
    Un solveur qui utilise un appariement pondéré pour minimiser le score dans une grille.
    Adapté pour utiliser un dictionnaire d'adjacence au lieu de NetworkX.
    """

    def run(self):
        """
        Construit un graphe sous forme de dictionnaire d'adjacence et utilise
        l'algorithme max_weight_matching personnalisé.
        """
        graph = self.grid.bipartite_graph()
        G = {}  
        for u in graph['even']:
            for v in graph['even'][u]:
                cost = self.grid.cost((u, v))
                value_u = self.grid.value[u[0]][u[1]]
                value_v = self.grid.value[v[0]][v[1]]
                weight = cost - value_u - value_v
                
                # Ajout bidirectionnel des arêtes
                G.setdefault(u, {})[v] = -weight
                G.setdefault(v, {})[u] = -weight

        # Calcul de l'appariement maximal
        matching = max_weight_matching(G)
        
        # Conversion du résultat
        self.pairs = list(matching)


from scipy.optimize import linear_sum_assignment
from hungarian_algorithm import hungarian_algorithm

class SolverHungarian1(Solver):
    def run(self) -> list[tuple[tuple[int, int], tuple[int, int]]]:
        """
        Runs the general solver using the Hungarian algorithm to find optimal pairs, allowing unpaired cells.
        """
        pairs = self.grid.all_pairs()
        taken = list(set([cell for pair in pairs for cell in pair]))
        # Include all non-forbidden cells in 'taken'
        l = len(taken)
        if l == 0:
            self.pairs = []
            return []
        cell_to_idx = {cell: idx for idx, cell in enumerate(taken)}
        # Build adjacency list from allowed pairs
        d = defaultdict(list)
        for u, v in pairs:
            d[u].append(v)
            d[v].append(u)
        # Initialize cost matrix with infinity and set diagonal to 0
        large_value = np.inf
        cost_matrix = np.full((l, l), large_value)
        for i in range(l):
            u = taken[i]
            for v in d.get(u, []):
                j = cell_to_idx[v]
                cost = self.grid.cost((u, v)) - self.grid.value[u[0]][u[1]] - self.grid.value[v[0]][v[1]]
                cost_matrix[i][j] = cost
            cost_matrix[i][i] = self.grid.value[u[0]][u[1]] - min([self.grid.value[v[0]][v[1]] for v in d[u]])
        

        # Apply Hungarian algorithm
        row_ind, col_ind = linear_sum_assignment(cost_matrix)
        
        # Collect mutual pairs
        matched_pairs = []
        seen = set()
        for i, j in zip(row_ind, col_ind):
            if i in seen or j in seen:
                continue
            if i == j:
                seen.add(i)  # Unpaired
            else:
                if col_ind[j] == i:  # Check mutual assignment
                    u, v = taken[i], taken[j]
                    if (u, v) in pairs or (v, u) in pairs:
                        matched_pairs.append((u, v))
                        seen.update([i, j])
        
        self.pairs = matched_pairs
        return matched_pairs
    

import heapq
from collections import defaultdict
import math

class Edge:
    def __init__(self, to, rev, cap, cost):
        self.to = to
        self.rev = rev
        self.cap = cap
        self.cost = cost

class SolverMinCost(Solver):
    def run(self):
        """Runs the minimum-cost flow algorithm to find optimal pairs with minimal total cost."""
        graph = defaultdict(list)
        source = 's'
        sink = 't'
        even_cells = set()
        odd_cells = set()
        allowed_pairs = self.grid.all_pairs()

        # Build the graph with allowed pairs
        for cell1, cell2 in allowed_pairs:
            # Determine even and odd cells based on coordinate sum parity
            if (sum(cell1) % 2) == 0:
                even, odd = cell1, cell2
            else:
                even, odd = cell2, cell1
            even_cells.add(even)
            odd_cells.add(odd)
            pair_cost = self.grid.cost((cell1, cell2))
            self.add_edge(graph, even, odd, 1, pair_cost)

        # Connect source to even cells and odd cells to sink
        for even in even_cells:
            self.add_edge(graph, source, even, 1, 0)
        for odd in odd_cells:
            self.add_edge(graph, odd, sink, 1, 0)

        # Initialize prices
        prices = {cell: 0 for cell in even_cells}
        prices.update({cell: min(self.grid.cost((cell, other)) for other in self.grid.vois(*cell)) for cell in odd_cells})

        # Calculate maximum possible flow (number of even cells)
        max_flow = min(len(even_cells), len(odd_cells))
        flow, total_cost = self.min_cost_flow(graph, source, sink, max_flow, prices)

        # Extract pairs from the residual graph
        self.pairs = []
        for even in even_cells:
            for e in graph[even]:
                if isinstance(e.to, tuple) and e.cap == 0 and e.to in odd_cells:
                    self.pairs.append((even, e.to))
        return self.pairs

    def add_edge(self, graph, u, v, cap, cost):
        """Adds a directed edge and its reverse to the residual graph."""
        forward = Edge(v, len(graph[v]), cap, cost)
        backward = Edge(u, len(graph[u]), 0, -cost)
        graph[u].append(forward)
        graph[v].append(backward)

    def min_cost_flow(self, graph, s, t, max_flow, prices):
        """Computes the minimum-cost maximum flow using successive shortest paths with potentials."""
        flow = 0
        total_cost = 0

        while flow < max_flow:
            dist, prev, prev_edge = self.dijkstra(graph, s, t, prices)
            if dist[t] == math.inf:
                break  # No augmenting path found

            # Update prices based on the shortest paths
            for v in dist:
                if dist[v] < math.inf:
                    prices[v] += dist[v]

            # Determine the maximum possible augmenting flow
            path_flow = max_flow - flow
            v = t
            path = []
            while v != s:
                u = prev.get(v)
                if u is None:
                    break  # Path is invalid
                e = prev_edge[v]
                path_flow = min(path_flow, e.cap)
                path.append(e)
                v = u
            if v != s:
                break  # Incomplete path

            # Update flow and cost
            flow += path_flow
            actual_cost = sum(e.cost for e in path) * path_flow
            total_cost += actual_cost

            # Update residual capacities
            v = t
            while v != s:
                u = prev[v]
                e = prev_edge[v]
                e.cap -= path_flow
                graph[e.to][e.rev].cap += path_flow
                v = u

        return flow, total_cost

    def dijkstra(self, graph, s, t, prices):
        """Performs Dijkstra's algorithm to find the shortest path from s to t with reduced costs."""
        dist = defaultdict(lambda: math.inf)
        dist[s] = 0
        prev = {}
        prev_edge = {}
        heap = [(0, s)]

        while heap:
            d, u = heapq.heappop(heap)
            if d > dist[u]:
                continue
            for e in graph[u]:
                if e.cap > 0:
                    v = e.to
                    reduced_cost = e.cost + prices[u] - prices[v]
                    if dist[v] > d + reduced_cost:
                        dist[v] = d + reduced_cost
                        prev[v] = u
                        prev_edge[v] = e
                        heapq.heappush(heap, (dist[v], v))

        return dist, prev, prev_edge