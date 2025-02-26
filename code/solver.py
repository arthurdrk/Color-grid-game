from collections import deque
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
        """
        self.grid = grid
        self.pairs = []

    def score(self) -> int:
        """
        Computes the score of the list of pairs in self.pairs.

        The score is calculated as the sum of the values of unpaired cells,
        excluding black cells.

        Returns:
        --------
        int
            The computed score.
        """
        paired = set()
        res = 0
        for pair in self.pairs:
            paired.add(pair[0])
            paired.add(pair[1])

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
        """
        used = []  # Cells that have already been visited
        res = []
        pairs = self.grid.all_pairs()

        for i in range(self.grid.n):
            for j in range(self.grid.m):
                case = (i, j)
                if case not in used:
                    used.append(case)
                    try:
                        # Find the neighboring cell that minimizes the cost
                        k, l = min(
                            [el for el in pairs if (el[0] == case and el[1] not in used) or (el[0] not in used and el[1] == case)],
                            key=lambda x: self.grid.cost(x)
                        )
                        if k == case:
                            res.append((case, l))
                            used.append(l)
                        else:
                            res.append((case, k))
                            used.append(k)
                    except ValueError:
                        pass

        return res

class SolverBiparti(Solver):
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
        """
        graph = {}
        even_cells = set()
        odd_cells = set()

        # Add edges between cells (direction: from even to odd)
        for cell1, cell2 in self.grid.all_pairs():
            if sum(cell1) % 2 == 0:
                even = cell1
                odd = cell2
            else:
                even = cell2
                odd = cell1
            even_cells.add(even)
            odd_cells.add(odd)
            graph.setdefault(even, []).append(odd)

        # Add edges from source "s" to even cells
        for even in even_cells:
            graph.setdefault("s", []).append(even)
            graph.setdefault(even, [])

        # Add edges from odd cells to sink "t"
        for odd in odd_cells:
            graph.setdefault(odd, []).append("t")
        graph.setdefault("t", [])

        # Store sets of cells for later extraction of the matching
        self.even_cells = even_cells
        self.odd_cells = odd_cells

        # Calculate the maximum flow (thus the size of the maximum matching)
        matching = self.ford_fulkerson(graph)
        self.pairs = matching
        return matching

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
        """
        path = []
        current = t
        while current is not None:
            path.append(current)
            current = parents[current]
        path.reverse()
        return path

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
        """
        while True:
            path = self.bfs(graph, "s", "t")
            if path is None:
                break
            for i in range(len(path) - 1):
                u = path[i]
                v = path[i + 1]
                graph[u].remove(v)
                graph.setdefault(v, []).append(u)

        matching = []
        for odd in self.odd_cells:
            for u in graph.get(odd, []):
                if u in self.even_cells:
                    matching.append((u, odd))
        return matching
