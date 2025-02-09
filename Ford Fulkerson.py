def bfs(rGraph, source, sink, parent):
    """
    Effectue une recherche en largeur (BFS) sur le graphe résiduel pour trouver un chemin
    de la source au puits. Le tableau 'parent' est utilisé pour stocker le chemin.
    """
    visited = [False] * len(rGraph)
    queue = [source]
    visited[source] = True

    while queue:
        u = queue.pop(0)
        for v, capacity in enumerate(rGraph[u]):
            if not visited[v] and capacity > 0:
                queue.append(v)
                visited[v] = True
                parent[v] = u
                if v == sink:
                    return True  # Chemin trouvé
    return False  # Pas de chemin trouvé

def ford_fulkerson(graph, source, sink):
    """
    Implémente l'algorithme Ford-Fulkerson pour calculer le flot maximum entre 'source' et 'sink'.
    """
    # Créer un graphe résiduel initial en copiant le graphe original
    rGraph = [row[:] for row in graph]
    parent = [-1] * len(rGraph)  # Pour stocker le chemin trouvé par BFS
    max_flow = 0  # Initialisation du flot maximum

    # Tant qu'il existe un chemin de la source au puits dans le graphe résiduel
    while bfs(rGraph, source, sink, parent):
        # Trouver le flot maximum possible dans le chemin trouvé (flot d'augmentation)
        path_flow = float('inf')
        s = sink
        while s != source:
            path_flow = min(path_flow, rGraph[parent[s]][s])
            s = parent[s]

        # Ajouter le flot d'augmentation au flot total
        max_flow += path_flow

        # Mettre à jour le graphe résiduel en soustrayant le flot de chaque arête du chemin
        # et en ajoutant le flot dans le sens inverse
        v = sink
        while v != source:
            u = parent[v]
            rGraph[u][v] -= path_flow
            rGraph[v][u] += path_flow
            v = parent[v]

    return max_flow

if __name__ == '__main__':
    # Exemple de graphe représenté par une matrice d'adjacence
    # Le graphe ci-dessous est emprunté à l'exemple classique du flot maximum.
    graph = [
        [0, 16, 13, 0, 0, 0],
        [0, 0, 10, 12, 0, 0],
        [0, 4, 0, 0, 14, 0],
        [0, 0, 9, 0, 0, 20],
        [0, 0, 0, 7, 0, 4],
        [0, 0, 0, 0, 0, 0]
    ]
    source = 0  # Le nœud source
    sink = 5    # Le nœud puits

    print("Le flot maximum est :", ford_fulkerson(graph, source, sink))
