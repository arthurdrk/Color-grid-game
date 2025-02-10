from collections import deque
from grid import Grid
    
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
        paired=set()
        res = 0
        for el in self.pairs:
            res += self.grid.cost(el)
            paired.add(el[0])
            paired.add(el[1])
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
        used = [] #les cases déjà visités
        res = []
        pairs = self.grid.all_pairs()
        for i in range(len(self.grid.n)):
            for j in range(len(self.grid.m)):
                case = (i, j)
            if case not in used:
                (k, l) = min([el for el in pairs if (el[0] == case and el[1] not in used) or (el[0] not in used and el[1] == case)], key=lambda x: self.grid.cost(x)) #pour chaque case du grid on l'associe à sa voisine légale qui minimise le cout
                if k == case:
                    res.append(case, l)
                    used.append(l)
                else:
                    res.append(case, k)
                    used.append(k)
        return res
        
    
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
        self.pairs = matching
        return matching
    
    
    def bfs(self, graph, s, t):
        queue = deque([s])
        # parents[v] mémorise le sommet précédent sur le chemin s->v
        parents = {s: None}
        
        while queue:
            u = queue.popleft()
            
            # On parcourt tous les voisins de u
            for v in graph.get(u, []):
                # Si on ne l’a pas déjà visité
                if v not in parents:
                    parents[v] = u
                    # Si on vient d’atteindre t, on reconstitue le chemin et on le renvoie
                    if v == t:
                        return self._reconstruct_path(parents, s, t)
                    # Sinon, on continue à l’explorer
                    queue.append(v)
        # Pas de chemin trouvé
        return None

    def _reconstruct_path(self, parents, s, t):
        """Reconstitue le chemin s->t à partir du dictionnaire parents."""
        path = []
        current = t
        while current is not None:
            path.append(current)
            current = parents[current]
        path.reverse()  # on l’a reconstruit à l’envers
        return path


    def ford_fulkerson(self, graph):
        """
        Calcule le flot maximum (matching maximum) dans le réseau biparti
        en utilisant un BFS pour trouver les chemins augmentants (Edmond–Karp).
        """
        while True:
            path = self.bfs(graph, "s", "t")
            if path is None:
                break  # plus de chemin augmentant
            
            # On a trouvé un chemin augmentant : on incrémente le flot de 1
            # et on met à jour le graphe résiduel (ajout de l'arête inverse).
            for i in range(len(path) - 1):
                u = path[i]
                v = path[i + 1]
                # on enlève l’arête u->v du graphe direct
                graph[u].remove(v)
                # on ajoute l’arête inverse v->u au graphe résiduel
                graph.setdefault(v, []).append(u)
        
        # Extraction du matching final en regardant dans le graphe résiduel
        matching = []
        for odd in self.odd_cells:
            for u in graph.get(odd, []):
                if u in self.even_cells:
                    matching.append((u, odd))
        return matching

  
  
