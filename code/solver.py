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
        used = set() # Cells that have already been visited
        res = []
        pairs = self.grid.all_pairs()

        # Create a dictionary to quickly access pairs by cell
        from collections import defaultdict

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
        """
        queue = deque([s])
        parents = {s: None}

        while queue:
            u = queue.popleft()
            for v in graph[u]:
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
        """
        while True:
            path = self.bfs(graph, "s", "t")
            if path is None:
                break
            for u, v in zip(path, path[1:]):
                graph[u].remove(v)
                graph[v].append(u)

        return [(u, odd) for odd in self.odd_cells for u in graph[odd] if u in self.even_cells]
