from collections import deque, defaultdict
from grid import Grid

class Solver:
    """
    A solver class for finding pairs in a grid.

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
        res = 0 # The score

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

1. Complexity of SolverGreedy:
   - Time Complexity: O(n * m)
     The `run` method iterates over each cell in the grid, checking its neighbors to find the best pair.
     The dominant term is iterating over all cells, which is O(n * m).
   - Space Complexity: O(n * m)
     The space complexity is O(n * m) due to storing the pairs and the results.

Optimality:
   - The greedy algorithm pairs cells based on minimizing the immediate cost without considering the global optimum.
   - This approach can lead to suboptimal solutions, especially in grids where local decisions affect the overall outcome significantly.
   - Consider the following 3x3 grid:

     Colors:
     [
       [0, 1, 0],  # Row 1: White, Red, White
       [1, 2, 1],  # Row 2: Red, Blue, Red
       [0, 1, 0]   # Row 3: White, Red, White
     ]

     Values:
     [
       [1, 2, 1],  # Row 1
       [2, 3, 2],  # Row 2
       [1, 2, 1]   # Row 3
     ]
     - The greedy algorithm might pair (0, 0) with (0, 1) due to immediate cost minimization, missing the optimal global configuration.
     - Optimal Solution: Pair (0, 0) with (1, 0), (0, 1) with (0, 2), (1, 1) with (1, 2), and (2, 0) with (2, 1), achieving a lower total cost.

Possible solution (brute force) and complexity:
   - A possible solution (brute force) would be to consider all possible pairings and selecting the one with the minimum score.
     - Time Complexity: O(2^(n * m))
       -> In the worst case, each cell could potentially be paired with any of its neighbors, leading to an exponential number of configurations.
     - Space Complexity: O(2^(n * m))
       Due to the need to store all possible configurations of pairs.

Other possible solutions:
   - Bipartite Matching (e.g., Ford-Fulkerson):
     This approach can find an optimal matching in polynomial time, specifically O(E * V), where E is the number of edges and V is the number of vertices in the bipartite graph representation of the grid.
     It provides a more global perspective compared to the greedy algorithm and can handle complex configurations better.
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
        used = set() # Cells that have already been visited
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
        self.pairs=res
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
        self.pairs=self.ford_fulkerson(graph)
        return self.pairs

    def bfs(self, graph: dict, s: str, t: str) -> list:
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
        list
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
                        return self.reconstruct_path(parents, s, t)
                    queue.append(v)

        return None

    def reconstruct_path(self, parents: dict, s: str, t: str) -> list:
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
        list
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

    def ford_fulkerson(self, graph: dict) -> list[tuple[tuple[int, int], tuple[int, int]]]:
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
            path = self.bfs(graph, "s", "t")
            if path is None:
                break
            for u, v in zip(path, path[1:]):
                graph[u].remove(v)
                graph[v].append(u)

        return [(u, odd) for odd in self.odd_cells for u in graph[odd] if u in self.even_cells]

class Edge:
    def __init__(self, to, rev, capacity, cost):
        self.to = to
        self.rev = rev
        self.capacity = capacity
        self.cost = cost

class MinCostFlow:
    def __init__(self, N):
        self.N = N
        self.graph = [[] for _ in range(N)]
        self.potential = [0] * N  # for Bellman-Ford

    def add_edge(self, fr, to, capacity, cost):
        forward = Edge(to, len(self.graph[to]), capacity, cost)
        backward = Edge(fr, len(self.graph[fr]), 0, -cost)
        self.graph[fr].append(forward)
        self.graph[to].append(backward)

    def flow(self, s, t, maxf):
        res = 0
        prevv = [0] * self.N
        preve = [0] * self.N
        INF = float('inf')

        while maxf > 0:
            dist = [INF] * self.N
            inqueue = [False] * self.N
            dist[s] = 0
            q = deque()
            q.append(s)
            inqueue[s] = True
            while q:
                v = q.popleft()
                inqueue[v] = False
                for i, e in enumerate(self.graph[v]):
                    if e.capacity > 0 and dist[e.to] > dist[v] + e.cost + self.potential[v] - self.potential[e.to]:
                        dist[e.to] = dist[v] + e.cost + self.potential[v] - self.potential[e.to]
                        prevv[e.to] = v
                        preve[e.to] = i
                        if not inqueue[e.to]:
                            q.append(e.to)
                            inqueue[e.to] = True
            if dist[t] == INF:
                break
            for v in range(self.N):
                if dist[v] < INF:
                    self.potential[v] += dist[v]
            d = maxf
            v = t
            while v != s:
                d = min(d, self.graph[prevv[v]][preve[v]].capacity)
                v = prevv[v]
            if d == 0:
                break
            maxf -= d
            res += d * self.potential[t]
            v = t
            while v != s:
                e = self.graph[prevv[v]][preve[v]]
                e.capacity -= d
                self.graph[v][e.rev].capacity += d
                v = prevv[v]
        return res

class SolverGeneral(Solver):
    def run(self) -> list[tuple[tuple[int, int], tuple[int, int]]]:
        pairs = self.grid.all_pairs()
        if not pairs:
            self.pairs = []
            return []

        even_cells = set()
        odd_cells = set()
        for i in range(self.grid.n):
            for j in range(self.grid.m):
                if self.grid.is_forbidden(i, j):
                    continue
                if (i + j) % 2 == 0:
                    even_cells.add((i, j))
                else:
                    odd_cells.add((i, j))

        nodes = {}
        node_id = 0
        nodes['s'] = node_id
        node_id += 1
        nodes['t'] = node_id
        node_id += 1
        for cell in even_cells:
            nodes[cell] = node_id
            node_id += 1
        for cell in odd_cells:
            nodes[cell] = node_id
            node_id += 1

        mcf = MinCostFlow(node_id)

        for cell in even_cells:
            mcf.add_edge(nodes['s'], nodes[cell], 1, 0)

        allowed_pairs = set()
        for u, v in pairs:
            if (u[0] + u[1]) % 2 == 0:
                even, odd = u, v
            else:
                even, odd = v, u
            if even in even_cells and odd in odd_cells:
                allowed_pairs.add((even, odd))

        for even, odd in allowed_pairs:
            weight = 2 * min(self.grid.value[even[0]][even[1]], self.grid.value[odd[0]][odd[1]])
            mcf.add_edge(nodes[even], nodes[odd], 1, -weight)

        for cell in odd_cells:
            mcf.add_edge(nodes[cell], nodes['t'], 1, 0)

        max_possible = min(len(even_cells), len(odd_cells))
        mcf.flow(nodes['s'], nodes['t'], max_possible)

        matched_pairs = []
        for cell in even_cells:
            cell_id = nodes[cell]
            for edge in mcf.graph[cell_id]:
                if edge.capacity == 0 and edge.to != nodes['s'] and edge.to in nodes.values():
                    for odd_cell in odd_cells:
                        if nodes[odd_cell] == edge.to:
                            matched_pairs.append((cell, odd_cell))
                            break

        self.pairs = matched_pairs
        return matched_pairs