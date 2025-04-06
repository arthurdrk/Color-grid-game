import sys
import os
import numpy as np

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))
from color_grid_game import *

class Solver_Hungarian(Solver):
    """
    An alternative implementation of the Hungarian algorithm solver.
    """

    def run(self):
        """
        Builds a bipartite cost matrix using only cells present in valid pairs.
        Applies the Hungarian algorithm to find optimal pairs.

        Returns
        -------
        list of tuple
            A list of pairs of cells, each represented as a tuple of tuples.

        Raises
        ------
        ValueError
            If the cost matrix is empty or if pairs are invalid.
        """
        pairs = self.grid.all_pairs(self.rules)  # O(P) where P is the number of pairs
        all_cells = list(set(cell for pair in pairs for cell in pair)) 

        if self.rules == "original rules":
            even_cells = []
            odd_cells = []
            for cell in all_cells:  
                if (cell[0] + cell[1]) % 2 == 0:
                    even_cells.append(cell)
                else:
                    odd_cells.append(cell)

            # Create mappings for matrix indices
            even_to_idx = {cell: i for i, cell in enumerate(even_cells)}  
            odd_to_idx = {cell: j for j, cell in enumerate(odd_cells)}  

            # Build cost matrix with valid pairs only and pad to square
            even_count = len(even_cells)
            odd_count = len(odd_cells)
            max_dim = max(even_count, odd_count)
            cost_matrix = np.zeros((max_dim, max_dim))

            for u, v in pairs:

                if (u[0] + u[1]) % 2 != 0:
                    u, v = v, u
                if u in even_to_idx and v in odd_to_idx:
                    cost = self.grid.cost((u, v)) 
                    weight = cost - self.grid.value[u[0]][u[1]] - self.grid.value[v[0]][v[1]]  
                    cost_matrix[even_to_idx[u], odd_to_idx[v]] = weight 

            # Apply Hungarian algorithm on the padded square matrix
            row_ind, col_ind = self.hungarian_algorithm(cost_matrix)  # O(max_dim^3)

            # Rebuild pairs from matrix indices, filtering valid entries
            self.pairs = []
            for i, j in zip(row_ind, col_ind):  # O(max_dim)
                if i < even_count and j < odd_count and cost_matrix[i][j] != 0:
                    self.pairs.append((even_cells[i], odd_cells[j]))  

        elif self.rules == "new rules":
            num_cells = len(all_cells) 
            cost_matrix = np.zeros((num_cells, num_cells))  

            # Create a mapping from cell to matrix index
            cell_to_idx = {cell: i for i, cell in enumerate(all_cells)}

            for u, v in pairs: 
                if u in cell_to_idx and v in cell_to_idx:
                    cost = self.grid.cost((u, v)) 
                    weight = cost - self.grid.value[u[0]][u[1]] - self.grid.value[v[0]][v[1]] 
                    cost_matrix[cell_to_idx[u], cell_to_idx[v]] = weight

            # Apply Hungarian algorithm on the square matrix
            row_ind, col_ind = self.hungarian_algorithm(cost_matrix)  # O(C^3)

            # Rebuild pairs from matrix indices, filtering valid entries
            self.pairs = []
            for i, j in zip(row_ind, col_ind):
                if cost_matrix[i][j] != 0:
                    self.pairs.append((all_cells[i], all_cells[j]))

        return self.pairs

    def hungarian_algorithm(self, cost):
        """
        Solve the linear sum assignment problem using the Hungarian algorithm.

        Parameters
        ----------
        cost : np.ndarray
            The cost matrix of the bipartite graph.

        Returns
        -------
        row_ind : np.ndarray
            An array of row indices giving the optimal assignment.
        col_ind : np.ndarray
            An array of corresponding column indices giving the optimal assignment.
        """
        n = cost.shape[0] 
        u = np.zeros(n, dtype=float)
        v = np.zeros(n, dtype=float) 

        # Initialize arrays to keep track of paths and assignments
        path = np.full(n, -1, dtype=int)
        col_to_row = np.full(n, -1, dtype=int) 
        row_to_col = np.full(n, -1, dtype=int) 

        def find_augmenting_path(current_row):
            """
            Find an augmenting path in the bipartite graph starting from the given row.
            """
            # Initialize arrays to keep track of visited nodes and shortest path costs
            visited_rows = np.full(n, False, dtype=bool)
            visited_columns = np.full(n, False, dtype=bool) 
            shortest_path_costs = np.full(n, np.inf)  

            # Initialize the remaining columns to be considered
            remaining = np.arange(n)[::-1] 
            num_remaining = n  
            min_value = 0 
            sink = -1 

            while sink == -1:  # O(n^2)
                index = -1  
                lowest = np.inf 
                visited_rows[current_row] = True 

                # Iterate over remaining columns to find the shortest path
                for it in range(num_remaining):  # O(n)
                    j = remaining[it]
                    # Calculate the reduced cost for the current row and column
                    r = min_value + cost[current_row, j] - u[current_row] - v[j]

                    # Update the shortest path costs and path
                    if r < shortest_path_costs[j]:
                        path[j] = current_row
                        shortest_path_costs[j] = r

                    # Track the column with the lowest shortest path cost
                    if (shortest_path_costs[j] < lowest) or (shortest_path_costs[j] == lowest and row_to_col[j] == -1):  # O(1)
                        index = it
                        lowest = shortest_path_costs[j]

                # Update min_value to the lowest shortest path cost found
                min_value = lowest
                  
                # Select the column with the lowest shortest path cost
                j = remaining[index]

                # If the selected column is unassigned, it becomes the sink
                if row_to_col[j] == -1:
                    sink = j  
                else:
                    # Otherwise, move to the row assigned to this column
                    current_row = row_to_col[j]  

                # Mark the column as visited
                visited_columns[j] = True  
                num_remaining -= 1  
                # Swap the current column with the last remaining column
                remaining[index] = remaining[num_remaining] 

            return sink, min_value, visited_rows, visited_columns, shortest_path_costs 

        # Iterate over each row to find the optimal assignment
        for current_row in range(n):  # O(n)
            sink, min_value, visited_rows, visited_columns, shortest_path_costs = find_augmenting_path(current_row)  # O(n^2)

            # Update the dual variables u and v
            u[current_row] += min_value  
            mask = visited_rows & (np.arange(n) != current_row)  # O(n)
            u += mask * (min_value - shortest_path_costs[col_to_row])  # O(n)

            mask = visited_columns
            v += mask * (shortest_path_costs - min_value)  # O(n)

            # Update the assignment based on the augmenting path
            while True:  # O(n)
                i = path[sink] 
                row_to_col[sink] = i  
                col_to_row[i], sink = sink, col_to_row[i] 
                if i == current_row: 
                    break

        # Return the optimal assignment
        return np.arange(n), col_to_row  # O(n)

# Overall Complexity:
# The overall time complexity is dominated by the Hungarian algorithm, which is O(n^3).
# The space complexity is O(n^2) due to the storage of the cost matrix and additional arrays.
