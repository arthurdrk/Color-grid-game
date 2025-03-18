from collections import deque, defaultdict
from grid import Grid
import numpy as np

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
        paired = set()  # Set of paired cells
        res = 0  # The score

        # Add all paired cells to the set and calculate the cost of each pair
        for pair in self.pairs:
            paired.add(pair[0])
            paired.add(pair[1])
            res += self.grid.cost(pair)

        # Calculate the sum of values for unpaired cells that are not black
        for i in range(self.grid.n):
            for j in range(self.grid.m):
                if (i, j) not in paired and not self.grid.is_forbidden(i, j):
                    res += self.grid.value[i][j]

        return res

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

from scipy.optimize import linear_sum_assignment #(Hungarian algorithm, it will be implemented later)

class SolverGeneral(Solver):
    def run(self) -> list[tuple[tuple[int, int], tuple[int, int]]]:
        """
        Runs the general solver to find pairs of cells using the Hungarian algorithm.

        Returns:
        --------
        list[tuple[tuple[int, int], tuple[int, int]]]
            A list of pairs of cells representing the optimal matching.

        Time Complexity: O(n^3)
        Space Complexity: O(n^2)
        """
        pairs = self.grid.all_pairs()
        even_cells = []
        odd_cells = []
        
                    
        for cell1, cell2 in pairs:
            even, odd = (cell1, cell2) if sum(cell1) % 2 == 0 else (cell2, cell1)
            even_cells.append(even)
            odd_cells.append(odd)

        large_value = 1e8
        cost_matrix = np.full((len(even_cells), len(odd_cells)), large_value)
        even_to_index = {cell: i for i, cell in enumerate(even_cells)}
        odd_to_index = {cell: i for i, cell in enumerate(odd_cells)}

        for u, v in pairs:
            if u in even_to_index and v in odd_to_index:
                val = self.grid.cost((u, v))-min(self.grid.value[u],self.grid.value[v])
                cost_matrix[even_to_index[u], odd_to_index[v]] = val
            elif v in even_to_index and u in odd_to_index:
                val = val = self.grid.cost((u, v))-min(self.grid.value[u],self.grid.value[v])
                cost_matrix[even_to_index[v], odd_to_index[u]] = val

        row_ind, col_ind = linear_sum_assignment(cost_matrix)

        matched_pairs = []
        for i, j in zip(row_ind, col_ind):
            if cost_matrix[i, j] < large_value: 
                even = even_cells[i]
                odd = odd_cells[j]
                if (even, odd) in pairs or (odd, even) in pairs:
                    matched_pairs.append((even, odd))
        self.pairs = matched_pairs
        return matched_pairs

   