import numpy as np

def hungarian_algorithm(cost_matrix):
    """
    Solves the linear assignment problem using the Hungarian algorithm.
    Args:
        cost_matrix: 2D numpy array (n x m) where n is rows, m is columns
    Returns:
        row_ind, col_ind: Arrays of row and column indices for the optimal assignment
    """
    # Convert to numpy array and make a copy
    cost = np.array(cost_matrix, dtype=float)
    n, m = cost.shape
    
    # If rectangular, pad with zeros to make it square
    if n != m:
        max_dim = max(n, m)
        padded = np.full((max_dim, max_dim), np.inf)
        padded[:n, :m] = cost
        cost = padded
        n = max_dim
    
    # Step 1: Subtract row minima
    for i in range(n):
        cost[i] -= np.min(cost[i])
    
    # Step 2: Subtract column minima
    for j in range(n):
        cost[:, j] -= np.min(cost[:, j])
    
    # Initialize labels and assignments
    row_covered = np.zeros(n, dtype=bool)
    col_covered = np.zeros(n, dtype=bool)
    assignments = np.full(n, -1, dtype=int)
    starred = np.zeros((n, n), dtype=bool)  # starred zeros
    primed = np.zeros((n, n), dtype=bool)  # primed zeros
    
    def find_uncovered_zero():
        for i in range(n):
            if not row_covered[i]:
                for j in range(n):
                    if not col_covered[j] and cost[i, j] == 0:
                        return i, j
        return -1, -1
    
    def find_star_in_row(row):
        for j in range(n):
            if starred[row, j]:
                return j
        return -1
    
    def find_star_in_col(col):
        for i in range(n):
            if starred[i, col]:
                return i
        return -1
    
    # Step 3: Cover columns with starred zeros
    while True:
        # Reset coverage
        row_covered.fill(False)
        col_covered.fill(False)
        primed.fill(False)
        
        # Initial starring of zeros
        for i in range(n):
            for j in range(n):
                if cost[i, j] == 0 and not col_covered[j]:
                    starred[i, j] = True
                    col_covered[j] = True
                    break
        
        # Count covered columns
        covered_cols = np.sum(col_covered)
        if covered_cols == n:
            break
        
        # Step 4: Main loop
        while True:
            # Find an uncovered zero
            row, col = find_uncovered_zero()
            if row == -1:  # No uncovered zero found
                # Step 6: Adjust the matrix
                min_val = np.inf
                for i in range(n):
                    if not row_covered[i]:
                        for j in range(n):
                            if not col_covered[j]:
                                min_val = min(min_val, cost[i, j])
                
                # Handle infinite min_val case
                if np.isinf(min_val):
                    break
                
                for i in range(n):
                    for j in range(n):
                        if row_covered[i]:
                            cost[i, j] += min_val
                        if not col_covered[j]:
                            cost[i, j] -= min_val
                continue
            
            # Prime the zero
            primed[row, col] = True
            
            # Check for starred zero in the row
            star_col = find_star_in_row(row)
            if star_col == -1:
                # Step 5: Augment path
                path = [(row, col)]
                while True:
                    star_row = find_star_in_col(path[-1][1])
                    if star_row == -1:
                        break
                    path.append((star_row, path[-1][1]))
                    prime_row, prime_col = next((i, j) for i in range(n) 
                                              for j in range(n) 
                                              if primed[i, j] and find_star_in_row(i) == path[-1][1])
                    path.append((prime_row, prime_col))
                
                # Update starring
                for r, c in path:
                    if starred[r, c]:
                        starred[r, c] = False
                    else:
                        starred[r, c] = True
                break
            else:
                # Step 4: Cover row, uncover column
                row_covered[row] = True
                col_covered[star_col] = False
    
    # Extract assignments
    row_ind = []
    col_ind = []
    for i in range(n):
        for j in range(n):
            if starred[i, j] and i < cost_matrix.shape[0] and j < cost_matrix.shape[1]:
                row_ind.append(i)
                col_ind.append(j)
    
    return np.array(row_ind), np.array(col_ind)