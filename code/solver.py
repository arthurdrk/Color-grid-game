
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
    def run(self):
        # Supposons que self.grid.all_pairs() renvoie toutes les paires de cellules adjacentes.
        # On veut construire un graphe biparti : cellules paires à gauche, cellules impaires à droite.
        # Puis, ajouter une source "s" reliée à toutes les cellules paires et un puits "t" relié à toutes les cellules impaires.
        self.graph = {}
        even_cells = set()
        odd_cells = set()
        
        # Ajout des arêtes entre cellules (direction : de pair vers impair)
        for cell1, cell2 in self.grid.all_pairs():
            # Déterminer laquelle est paire (i+j pair) et laquelle est impaire.
            if cell1.sum() % 2 == 0:
                even = cell1
                odd  = cell2
            else:
                even = cell2
                odd  = cell1
            even_cells.add(even)
            odd_cells.add(odd)
            # Ajouter l'arête de la cellule paire vers la cellule impaire.
            self.graph.setdefault(even, []).append(odd)
        
        # Ajout des arêtes de la source "s" aux cellules paires,
        # et des cellules impaires vers le puits "t".
        for even in even_cells:
            self.graph.setdefault("s", []).append(even)
            # S'assurer que chaque cellule paire apparaisse dans le graphe même si elle n'a pas d'arêtes sortantes.
            self.graph.setdefault(even, [])
        for odd in odd_cells:
            self.graph.setdefault(odd, []).append("t")
            self.graph.setdefault(odd, [])
        self.graph.setdefault("t", [])
        
        # Conserver les ensembles de cellules paires et impaires pour la récupération ultérieure de l'appariement.
        self.even_cells = even_cells
        self.odd_cells = odd_cells

    def ford_fulkerson(self):
        """
        Calcule le flot maximum dans self.graph (le réseau d'appariement biparti)
        en utilisant une recherche DFS pour trouver des chemins augmentants (algorithme Ford–Fulkerson).

        Renvoie:
            max_flow (int) : la valeur du flot maximum, c'est-à-dire la taille de l'appariement maximum.
            appariements (list) : une liste de tuples (cellule_pair, cellule_impair) représentant l'appariement.
        """
        def dfs(u, t, visited):
            if u == t:
                return [t]
            for v in self.graph.get(u, []):
                if v not in visited:
                    visited.add(v)
                    path = dfs(v, t, visited)
                    if path is not None:
                        return [u] + path
            return None

        max_flow = 0
        # Recherche répétée d'un chemin augmentant de "s" à "t"
        while True:
            visited = set(["s"])
            path = dfs("s", "t", visited)
            if path is None:
                break  # plus de chemin augmentant trouvé
            max_flow += 1
            # Pour des capacités unitaires, le goulot d'étranglement est toujours 1.
            # Mise à jour du graphe résiduel :
            # pour chaque arête du chemin, on retire l'arête dans le sens direct
            # et on ajoute l'arête inverse.
            for i in range(len(path) - 1):
                u = path[i]
                v = path[i + 1]
                self.graph[u].remove(v)
                self.graph.setdefault(v, []).append(u)
        # Récupérer l'appariement à partir du graphe résiduel.
        # Dans ce réseau, une arête de "v" (cellule impaire) vers "u" (cellule paire)
        # indique que la cellule paire u est appariée avec la cellule impaire v.
        appariements = []
        for odd in self.odd_cells:
            for u in self.graph.get(odd, []):
                # On ne considère que les voisins qui sont des cellules paires.
                if u in self.even_cells:
                    appariements.append((u, odd))
                    break  # chaque cellule impaire est appariée à au plus une cellule paire
        
        return max_flow, appariements

    
        

