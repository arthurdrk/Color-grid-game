import sys
import os
import numpy as np

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from color_grid_game import *

class SolverHungarian_general(Solver):
    """
    An alternative implementation of the Hungarian algorithm solver.
    """

    def run(self, rules="original rules") -> list[tuple[tuple[int, int], tuple[int, int]]]:
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
        if self.rules == "original rules":
            # Collect all unique cells from valid pairs
            pairs = self.grid.all_pairs()
            all_cells = set()
            for u, v in pairs:
                all_cells.add(u)
                all_cells.add(v)

            # Split into even/odd based on coordinate parity
            even_cells = [cell for cell in all_cells if (cell[0] + cell[1]) % 2 == 0]
            odd_cells = [cell for cell in all_cells if (cell[0] + cell[1]) % 2 == 1]

            # Create mappings for matrix indices
            even_to_idx = {cell: i for i, cell in enumerate(even_cells)}
            odd_to_idx = {cell: j for j, cell in enumerate(odd_cells)}

            # Build cost matrix with valid pairs only and pad to square
            even_count = len(even_cells)
            odd_count = len(odd_cells)
            max_dim = max(even_count, odd_count)
            cost_matrix = np.zeros((max_dim, max_dim))
            for u, v in pairs:
                # Ensure u is even and v is odd
                if (u[0] + u[1]) % 2 != 0:
                    u, v = v, u
                if u in even_to_idx and v in odd_to_idx:
                    cost = self.grid.cost((u, v))
                    weight = cost - self.grid.value[u[0]][u[1]] - self.grid.value[v[0]][v[1]]
                    cost_matrix[even_to_idx[u], odd_to_idx[v]] = weight

            # Apply Hungarian algorithm on the padded square matrix
            row_ind, col_ind = self.hungarian_algorithm(cost_matrix)

            # Rebuild pairs from matrix indices, filtering valid entries
            self.pairs = []
            for i, j in zip(row_ind, col_ind):
                if i < even_count and j < odd_count and cost_matrix[i][j] != 0:
                    self.pairs.append((even_cells[i], odd_cells[j]))

        elif rules == "new rules":
            pass


        # Apply Hungarian algorithm on the bipartite matrix
        row_ind, col_ind = self.hungarian_algorithm(cost_matrix)

        # Rebuild valid pairs from the result
        self.pairs = []
        for i, j in zip(row_ind, col_ind):
            if cost_matrix[i, j] < 0:
                u = even_cells[i]
                v = odd_cells[j]
                if ((u, v) in pairs) or ((v, u) in pairs):
                    self.pairs.append((u, v))
        return self.pairs


    @staticmethod
    def hungarian_algorithm(cost_matrix):
        """
        Solve the assignment problem using the Hungarian algorithm.

        Parameters
        ----------
        cost_matrix : array-like
            A 2D array representing the cost matrix.

        Returns
        -------
        tuple
            A tuple of arrays representing the row and column indices of the optimal assignment.

        Raises
        ------
        ValueError
            If the input is not a 2D array.
        """
        cost_matrix = np.asarray(cost_matrix)
        if len(cost_matrix.shape) != 2:
            raise ValueError("expected a matrix (2-d array), got a %r array"
                             % (cost_matrix.shape,))

        # The algorithm expects more columns than rows in the cost matrix.
        if cost_matrix.shape[1] < cost_matrix.shape[0]:
            cost_matrix = cost_matrix.T
            transposed = True
        else:
            transposed = False

        state = SPUtils._Hungary(cost_matrix)

        # No need to bother with assignments if one of the dimensions
        # of the cost matrix is zero-length.
        step = None if 0 in cost_matrix.shape else SPUtils._step1

        while step is not None:
            step = step(state)

        if transposed:
            marked = state.marked.T
        else:
            marked = state.marked
        return np.where(marked == 1)

    class _Hungary(object):
        """
        Internal class to manage the state of the Hungarian algorithm.
        """

        def __init__(self, cost_matrix):
            self.C = cost_matrix.copy()

            n, m = self.C.shape
            self.row_uncovered = np.ones(n, dtype=bool)
            self.col_uncovered = np.ones(m, dtype=bool)
            self.Z0_r = 0
            self.Z0_c = 0
            self.path = np.zeros((n + m, 2), dtype=int)
            self.marked = np.zeros((n, m), dtype=int)

        def _clear_covers(self):
            """Clear all covered matrix cells"""
            self.row_uncovered[:] = True
            self.col_uncovered[:] = True

    @staticmethod
    def _step1(state):
        """
        Step 1 of the Hungarian algorithm.
        """
        state.C -= state.C.min(axis=1)[:, np.newaxis]
        for i, j in zip(*np.where(state.C == 0)):
            if state.col_uncovered[j] and state.row_uncovered[i]:
                state.marked[i, j] = 1
                state.col_uncovered[j] = False
                state.row_uncovered[i] = False

        state._clear_covers()
        return SPUtils._step3

    @staticmethod
    def _step3(state):
        """
        Step 3 of the Hungarian algorithm.
        """
        marked = (state.marked == 1)
        state.col_uncovered[np.any(marked, axis=0)] = False

        if marked.sum() < state.C.shape[0]:
            return SPUtils._step4

    @staticmethod
    def _step4(state):
        """
        Step 4 of the Hungarian algorithm.
        """
        C = (state.C == 0).astype(int)
        covered_C = C * state.row_uncovered[:, np.newaxis]
        covered_C *= np.asarray(state.col_uncovered, dtype=int)
        n = state.C.shape[0]
        m = state.C.shape[1]

        while True:
            row, col = np.unravel_index(np.argmax(covered_C), (n, m))
            if covered_C[row, col] == 0:
                return SPUtils._step6
            else:
                state.marked[row, col] = 2
                star_col = np.argmax(state.marked[row] == 1)
                if state.marked[row, star_col] != 1:
                    state.Z0_r = row
                    state.Z0_c = col
                    return SPUtils._step5
                else:
                    col = star_col
                    state.row_uncovered[row] = False
                    state.col_uncovered[col] = True
                    covered_C[:, col] = C[:, col] * (
                        np.asarray(state.row_uncovered, dtype=int))
                    covered_C[row] = 0

    @staticmethod
    def _step5(state):
        """
        Step 5 of the Hungarian algorithm.
        """
        count = 0
        path = state.path
        path[count, 0] = state.Z0_r
        path[count, 1] = state.Z0_c

        while True:
            row = np.argmax(state.marked[:, path[count, 1]] == 1)
            if state.marked[row, path[count, 1]] != 1:
                break
            else:
                count += 1
                path[count, 0] = row
                path[count, 1] = path[count - 1, 1]

            col = np.argmax(state.marked[path[count, 0]] == 2)
            if state.marked[row, col] != 2:
                col = -1
            count += 1
            path[count, 0] = path[count - 1, 0]
            path[count, 1] = col

        for i in range(count + 1):
            if state.marked[path[i, 0], path[i, 1]] == 1:
                state.marked[path[i, 0], path[i, 1]] = 0
            else:
                state.marked[path[i, 0], path[i, 1]] = 1

        state._clear_covers()
        state.marked[state.marked == 2] = 0
        return SPUtils._step3

    @staticmethod
    def _step6(state):
        """
        Step 6 of the Hungarian algorithm.
        """
        if np.any(state.row_uncovered) and np.any(state.col_uncovered):
            minval = np.min(state.C[state.row_uncovered], axis=0)
            minval = np.min(minval[state.col_uncovered])
            state.C[~state.row_uncovered] += minval
            state.C[:, state.col_uncovered] -= minval
        return SPUtils._step4