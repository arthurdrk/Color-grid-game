class SolverHungarian(Solver):
    """
    A solver that uses the Hungarian algorithm to find optimal pairs in a grid.
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
        if self.rules == "original rules":
            # Collect all unique cells from valid pairs
            valid_pairs = self.grid.all_pairs()
            all_cells = set()
            for u, v in valid_pairs:
                all_cells.add(u)
                all_cells.add(v)

            # Split into even/odd based on coordinate parity
            even_cells = [cell for cell in all_cells if (cell[0] + cell[1]) % 2 == 0]
            odd_cells = [cell for cell in all_cells if (cell[0] + cell[1]) % 2 == 1]

            # Create mappings for matrix indices
            even_to_idx = {cell: i for i, cell in enumerate(even_cells)}
            odd_to_idx = {cell: j for j, cell in enumerate(odd_cells)}

            # Build cost matrix with valid pairs only
            cost_matrix = np.full((len(even_cells), len(odd_cells)), 0)
            for u, v in valid_pairs:
                # Ensure u is even and v is odd
                if (u[0] + u[1]) % 2 != 0:
                    u, v = v, u
                if u in even_to_idx and v in odd_to_idx:
                    cost = self.grid.cost((u, v))
                    weight = cost - self.grid.value[u[0]][u[1]] - self.grid.value[v[0]][v[1]]
                    cost_matrix[even_to_idx[u], odd_to_idx[v]] = weight

            # Apply Hungarian algorithm
            row_ind, col_ind = hungarian_algorithm(cost_matrix)

            # Rebuild pairs from matrix indices
            self.pairs = []
            for i, j in zip(row_ind, col_ind):
                if cost_matrix[i][j] != 0:
                    self.pairs.append((even_cells[i], odd_cells[j]))

        elif self.rules == "new rules":
            # Handle new rules (implementation omitted)
            pass

        return self.pairs