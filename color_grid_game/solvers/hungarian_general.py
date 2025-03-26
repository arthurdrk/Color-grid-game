from color_grid_game import *

class SolverHungarian_general(Solver):
    """
    An alternative implementation of the Hungarian algorithm solver.
    """

    def run(self):
        """
        Builds a bipartite cost matrix using only cells present in valid pairs.
        Applies the Hungarian algorithm to find optimal pairs.

        Returns:
        --------
        list[tuple[tuple[int, int], tuple[int, int]]]
            A list of pairs of cells.

        Raises:
        -------
        ValueError: If the cost matrix is empty or if pairs are invalid.
        """
        pairs = self.grid.all_pairs(self.rules)
        # Split cells into even and odd partitions based on coordinates
        even_cells = []
        odd_cells = []
        for cell in {cell for pair in pairs for cell in pair}:
            if (cell[0] + cell[1]) % 2 == 0:
                even_cells.append(cell)
            else:
                odd_cells.append(cell)

        # Create bipartite cost matrix (even rows, odd columns)
        cost_matrix = np.full((len(even_cells), len(odd_cells)), 0)
        even_to_idx = {cell: i for i, cell in enumerate(even_cells)}
        odd_to_idx = {cell: j for j, cell in enumerate(odd_cells)}

        for u, v in pairs:
            if (u[0] + u[1]) % 2 != 0:
                u, v = v, u  # Ensure u is even, v is odd
            if u in even_to_idx and v in odd_to_idx:
                cost = self.grid.cost((u, v))
                value_u = self.grid.value[u[0]][u[1]]
                value_v = self.grid.value[v[0]][v[1]]
                weight = cost - value_u - value_v
                cost_matrix[even_to_idx[u], odd_to_idx[v]] = weight

        # Apply Hungarian algorithm on the bipartite matrix
        row_ind, col_ind = hungarian_algorithm(cost_matrix)

        # Rebuild valid pairs from the result
        self.pairs = []
        for i, j in zip(row_ind, col_ind):
            if cost_matrix[i, j] < 0:
                u = even_cells[i]
                v = odd_cells[j]
                if ((u, v) in pairs) or ((v, u) in pairs):
                    self.pairs.append((u, v))
        return self.pairs
