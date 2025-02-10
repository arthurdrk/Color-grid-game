
class Solver:
    """
    A solver class. 

    Attributes: 
    -----------
    grid: Grid
        The grid
    pairs: list[tuple[tuple[int]]]
        A list of pairs, each being a tuple ((i1, j1), (i2, j2))
    """

    def __init__(self, grid):
        """
        Initializes the solver.

        Parameters: 
        -----------
        grid: Grid
            The grid
        """
        self.grid = grid
        self.pairs = list()

    def score(self):
        """
        Computes the of the list of pairs in self.pairs
        """
        return "Method not implemented yet"

class SolverEmpty(Solver):
    def run(self):
        pass

class SolverGreedy(Solver):
    def run(self):
        pass

class SolverBiparti(Solver):
    def __init__(self):
        self.pairs = list()
        U = []
        V = []
        graph = {}
        for i in range(self.grid.n):
            for j in range(self.grid.m):
                if (i + j) % 2 == 0:
                    U.append((i, j))
                else:
                    V.append((i, j))
                graph[(i, j)] = []
                for di, dj in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
                    voisin_i, voisin_j = i + di, j + dj
                    if 0 <= voisin_i < self.n and 0 <= voisin_j < self.m:
                        graph[(i, j)].append((voisin_i, voisin_j))
        self.graph=graph
        self.U=U
        self.V=V

    
    def ford_fulkerson(self):
        """
        Ford-Fulkerson
        """
 
        self.pairs = []
        matchU = {u: None for u in self.U}
        matchV = {v: None for v in self.V}

        def dfs(u, visited):
            """Parcours en profondeur pour trouver un chemin augmentant."""
            for v in self.graph[u]:
                if v not in visited:
                    visited.add(v)
                    # Si v n'est pas encore apparié ou si on peut réassigner son partenaire
                    if matchV[v] is None or dfs(matchV[v], visited):
                        matchU[u] = v
                        matchV[v] = u
                        return True
            return False
        
        # Parcourir chaque nœud de U pour essayer de trouver un chemin augmentant
        for u in self.U:
            dfs(u, set())

        # Construire la liste des paires à partir des matchings
        self.pairs = [(u, v) for u, v in matchU.items() if v is not None]

        


