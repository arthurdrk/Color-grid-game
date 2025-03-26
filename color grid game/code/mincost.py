import heapq
from collections import defaultdict

def minimum_cost_perfect_matching(graph, costs):
    """
    Find a minimum-cost perfect matching in a bipartite graph.
    
    Args:
        graph: A dictionary where keys are nodes in X and values are lists of adjacent nodes in Y
        costs: A dictionary where keys are (x,y) tuples and values are the costs of the edges
    
    Returns:
        A dictionary representing the minimum-cost perfect matching where keys are nodes in X
        and values are the matched nodes in Y
    """
    X = set(graph.keys())
    Y = set()
    for neighbors in graph.values():
        Y.update(neighbors)
    
    if len(X) != len(Y):
        raise ValueError("The graph must have an equal number of nodes in X and Y for a perfect matching")
    
    # Initialize empty matching and prices
    M = {}  # Matching: X -> Y
    M_inverse = {}  # Inverse mapping: Y -> X
    p_x = {x: 0 for x in X}  # Prices for nodes in X
    
    # Initialize prices for nodes in Y (minimum cost of edges entering y)
    p_y = {}
    for y in Y:
        min_cost = float('inf')
        for x in X:
            if y in graph[x]:
                min_cost = min(min_cost, costs[(x, y)])
        p_y[y] = min_cost
    
    # Continue until we have a perfect matching
    while len(M) < len(X):
        # Build the residual graph for the current matching
        residual_graph = build_residual_graph(graph, M, M_inverse, X, Y)
        
        # Find shortest paths from s to all nodes using Dijkstra's algorithm
        dist, prev = dijkstra(residual_graph, 's', p_x, p_y, costs, M, M_inverse)
        
        # Find the minimum-cost path from s to t
        min_dist = float('inf')
        min_y = None
        for y in Y - set(M_inverse.keys()):  # Unmatched nodes in Y
            if y in dist and dist[y] < min_dist:
                min_dist = dist[y]
                min_y = y
        
        if min_y is None:
            raise ValueError("No augmenting path found. Perfect matching may not exist.")
            
        # Reconstruct the path
        path = []
        current = min_y
        while current != 's':
            path.insert(0, current)
            current = prev[current]
        path.insert(0, 's')  # Add source to the beginning
        
        # Augment the matching along the path (skipping s and t)
        true_path = [node for node in path if node != 's' and node != 't']
        augment_path(true_path, M, M_inverse)
        
        # Update prices
        for v in X | Y:
            if v in dist:
                if v in X:
                    p_x[v] = p_x[v] + dist[v]
                else:  # v in Y
                    p_y[v] = p_y[v] + dist[v]
    
    return M

def build_residual_graph(graph, M, M_inverse, X, Y):
    """Build the residual graph for the current matching."""
    residual = defaultdict(list)
    
    # Add edge from s to all unmatched nodes in X
    for x in X - set(M.keys()):
        residual['s'].append(x)
    
    # Add edges from X to Y (if not in matching) and from Y to X (if in matching)
    for x in X:
        if x in M:  # x is matched
            y = M[x]
            residual[y].append(x)  # Edge from Y to X (in matching)
        
        for y in graph[x]:
            if M.get(x) != y:  # Edge not in matching
                residual[x].append(y)  # Edge from X to Y (not in matching)
    
    # Add edge from all unmatched nodes in Y to t
    for y in Y - set(M_inverse.keys()):
        residual[y].append('t')
    
    return residual

def dijkstra(graph, start, p_x, p_y, costs, M, M_inverse):
    """
    Run Dijkstra's algorithm with reduced costs.
    Returns distances from start to all nodes and the predecessor map.
    """
    dist = {start: 0}
    prev = {}
    # Use a counter for tie-breaking to avoid comparing strings with strings
    counter = 0
    pq = [(0, counter, start)]
    
    while pq:
        d, _, u = heapq.heappop(pq)
        
        if d > dist.get(u, float('inf')):
            continue
        
        for v in graph[u]:
            # Skip if 't' because we don't need to compute paths beyond t
            if u == 't':
                continue
                
            # Calculate reduced cost
            if u == 's':
                reduced_cost = 0
            elif v == 't':
                reduced_cost = 0
            elif u in M_inverse:  # u is in Y, v is in X
                reduced_cost = p_y[u] - costs[(v, u)] - p_x[v]
            else:  # u is in X, v is in Y
                reduced_cost = p_x[u] + costs[(u, v)] - p_y[v]
            
            new_dist = dist[u] + reduced_cost
            
            if v not in dist or new_dist < dist[v]:
                dist[v] = new_dist
                prev[v] = u
                counter += 1
                heapq.heappush(pq, (new_dist, counter, v))  # Add counter for tie-breaking
    
    return dist, prev

def augment_path(path, M, M_inverse):
    """Augment the matching along the given path."""
    # Path alternates between X and Y
    for i in range(0, len(path) - 1, 2):
        x = path[i]
        y = path[i + 1]
        
        # If x was already matched, remove that match
        if x in M:
            old_y = M[x]
            del M_inverse[old_y]
            del M[x]
        
        # If y was already matched, remove that match
        if y in M_inverse:
            old_x = M_inverse[y]
            del M[old_x]
            del M_inverse[y]
        
        # Add the new match
        M[x] = y
        M_inverse[y] = x

# Example usage
def example():
    # Define a bipartite graph with X = {0, 1, 2} and Y = {'A', 'B', 'C'}
    graph = {
        0: ['A', 'B', 'C'],
        1: ['A', 'B'],
        2: ['A', 'C']
    }
    
    # Define costs for each edge
    costs = {
        (0, 'A'): 3,
        (0, 'B'): 1,
        (0, 'C'): 5,
        (1, 'A'): 2,
        (1, 'B'): 6,
        (2, 'A'): 4,
        (2, 'C'): 3
    }
    
    # Find minimum-cost perfect matching
    matching = minimum_cost_perfect_matching(graph, costs)
    
    # Calculate total cost
    total_cost = sum(costs[(x, matching[x])] for x in matching)
    print(matching)
    print("Minimum-cost perfect matching:")
    for x, y in matching.items():
        print(f"{x} -> {y} (cost: {costs[(x, y)]})")
    print(f"Total cost: {total_cost}")

if __name__ == "__main__":
    example()