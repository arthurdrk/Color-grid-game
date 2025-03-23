import numpy as np

def hungarian_algorithm(cost_matrix):
    cost = np.array(cost_matrix, dtype=np.float64)
    n, m = cost.shape
    u = np.zeros(n)
    v = np.zeros(m)
    row_ind = -np.ones(n, dtype=int)
    col_ind = -np.ones(m, dtype=int)
    
    for cur_row in range(n):
        pi = np.full(m, np.inf)
        pred = np.full(m, cur_row)
        visited = np.zeros(m, dtype=bool)
        j_min = -1
        
        while True:
            min_val = np.inf
            j_min = -1
            for j in range(m):
                if not visited[j] and pi[j] < min_val:
                    min_val = pi[j]
                    j_min = j
            if j_min == -1:
                break
            
            visited[j_min] = True
            i = col_ind[j_min]
            if i == -1:
                break
                
            for j in range(m):
                if not visited[j]:
                    slack = cost[i, j] - u[i] - v[j]
                    if pi[j] > slack + min_val:
                        pi[j] = slack + min_val
                        pred[j] = i
            
        if j_min != -1:
            i = pred[j_min]
            if row_ind[i] != -1:
                raise ValueError("Internal error: matching failed")
            
            while True:
                j = col_ind[j_min]
                col_ind[j_min] = i
                temp = row_ind[i]
                row_ind[i] = j_min
                i = temp
                if i == -1:
                    break
                j_min = j
            
            u[cur_row] += min_val
            for j in range(m):
                if visited[j]:
                    v[j] -= pi[j] - min_val
                    u[pred[j]] += pi[j] - min_val
    
    row_indices = np.array([i for i in range(n) if row_ind[i] != -1])
    col_indices = np.array([row_ind[i] for i in row_indices])
    return (row_indices, col_indices)