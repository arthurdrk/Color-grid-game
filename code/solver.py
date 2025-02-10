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
        Computes the score of the list of pairs in self.pairs
        """
        paired=[]
        res = 0
        for el in self.pairs:
            res += self.grid.cost(el)
            paired.append(el[0])
            paired.append(el[1])
        for i in range(self.grid.n):
            for j in range(self.grid.m):
                if (i, j) not in paired and not self.grid.is_forbidden(i, j):
                    res += self.grid.value[i][j]
        return res
        
        # Add the values of unpaired cells (excluding black cells)
        


class SolverEmpty(Solver):
    def run(self):
        pass

class SolverGreedy(Solver):
    def run(self):
        pass
    
class SolverBiparti(Solver):
    def run(self):
        # On suppose que self.grid.all_pairs() renvoie toutes les paires de cellules adjacentes.
        # On construit un graphe biparti avec :
        #   - les cellules paires (i+j pair) d'un côté,
        #   - les cellules impaires (i+j impair) de l'autre côté.
        # Ensuite, on ajoute une source "s" connectée à toutes les cellules paires
        # et un puits "t" auquel sont connectées toutes les cellules impaires.
        graph = {}
        even_cells = set()
        odd_cells = set()
        # Ajout des arêtes entre cellules (direction : de pair vers impair)
        for cell1, cell2 in self.grid.all_pairs():
            # Déterminer laquelle est paire (i+j pair) et laquelle est impaire.
            if sum(cell1) % 2 == 0:
                even = cell1
                odd  = cell2
            else:
                even = cell2
                odd  = cell1
            even_cells.add(even)
            odd_cells.add(odd)
            # Ajouter l'arête de la cellule paire vers la cellule impaire.
            graph.setdefault(even, []).append(odd)

        # Ajout des arêtes de la source "s" aux cellules paires
        for even in even_cells:
            graph.setdefault("s", []).append(even)
            # S'assurer que chaque cellule paire apparaisse dans le graphe.
            graph.setdefault(even, [])
            
        # Ajout des arêtes des cellules impaires vers le puits "t"
        for odd in odd_cells:
            graph.setdefault(odd, []).append("t")
            # La ligne suivante est inutile puisque odd est déjà dans graph
            # graph.setdefault(odd, [])
        graph.setdefault("t", [])

        # Stocker les ensembles de cellules pour une extraction ultérieure de l'appariement
        self.even_cells = even_cells
        self.odd_cells = odd_cells
        # Calculer le flot maximum (donc la taille de l'appariement maximum)
        matching = self.ford_fulkerson(graph)
        print(len(matching))
        return matching
    
    
    def dfs(self, graph, u, t, visited):
        """Recherche récursive d'un chemin de u à t dans le graphe."""
        if u == t:
            return [t]
        for v in graph.get(u, []):
            if v not in visited:
                visited.add(v)
                path = self.dfs(graph, v, t, visited)
                if path is not None:
                    return [u] + path
        return None

    def ford_fulkerson(self, graph):
        """
        Calcule le flot maximum dans le réseau d'appariement biparti
        en utilisant une recherche DFS pour trouver des chemins augmentants (algorithme Ford–Fulkerson).

        Renvoie:
            matching (list) : une liste de tuples (cellule_pair, cellule_impair) représentant l'appariement.
        """
        max_flow = 0
        # Recherche répétée d'un chemin augmentant de "s" à "t"
        while True:
            visited = {"s"}
            path = self.dfs(graph, "s", "t", visited)
            if path is None:
                break  # plus de chemin augmentant trouvé
            max_flow += 1
            # Pour des capacités unitaires, le goulot d'étranglement est toujours 1.
            # Mise à jour du graphe résiduel :
            # On retire l'arête utilisée dans le sens direct et on ajoute l'arête inverse.
            for i in range(len(path) - 1):
                u = path[i]
                v = path[i + 1]
                graph[u].remove(v)
                graph.setdefault(v, []).append(u)
        # Extraction de l'appariement :
        # Dans le graphe résiduel, une arête de "v" (cellule impaire) vers "u" (cellule paire)
        # signifie que la cellule paire u est appariée avec la cellule impaire v.
        matching = []
        for odd in self.odd_cells:
            for u in graph.get(odd, []):
                if u in self.even_cells:
                    matching.append((u, odd))
        self.pairs=matching
        return matching
  
  