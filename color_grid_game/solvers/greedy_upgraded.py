import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from color_grid_game import *

class SolverGreedy_upgraded(Solver):
    """
    Improvement of SolverGreedy that tries all possible starting points and keeps the pairing with the minimum score.
    """

    def run(self) -> list[tuple[tuple[int, int], tuple[int, int]]]:
        """
        Runs the greedy algorithm from all possible starting cells and selects the best pairing.

        Returns:
            list[tuple[tuple[int, int], tuple[int, int]]: List of pairs with the lowest score.

        Raises:
        -------
        ValueError: If any cell in pairs is invalid.
        """
        pairs = self.grid.all_pairs()
        pair_dict = defaultdict(list)
        for pair in pairs:
            pair_dict[pair[0]].append(pair)
            pair_dict[pair[1]].append(pair)

        best_score = float('inf')
        best_pairs = []

        # Iterate over all possible starting cells (k, l)
        for k in range(self.grid.n):
            for l in range(self.grid.m):
                used = set()
                current_pairs = []
                # Traverse grid in shifted order based on k and l
                for row_shift in range(self.grid.n):
                    for col_shift in range(self.grid.m):
                        i = (row_shift + k) % self.grid.n
                        j = (col_shift + l) % self.grid.m
                        current_cell = (i, j)
                        if current_cell not in used and not self.grid.is_forbidden(i, j):
                            used.add(current_cell)
                            # Find all possible pairs for current_cell not yet used
                            available_pairs = []
                            for pair in pair_dict.get(current_cell, []):
                                other = pair[0] if pair[1] == current_cell else pair[1]
                                if other not in used and not self.grid.is_forbidden(other[0], other[1]):
                                    available_pairs.append(pair)
                            if available_pairs:
                                best_pair = min(available_pairs, key=lambda p: self.grid.cost(p))
                                other_cell = best_pair[0] if best_pair[1] == current_cell else best_pair[1]
                                current_pairs.append((current_cell, other_cell))
                                used.add(other_cell)
                # Calculate score for current_pairs
                self.pairs = current_pairs
                score = self.score()
                # Update best if current score is better
                if score < best_score:
                    best_score = score
                    best_pairs = current_pairs.copy()
        self.pairs = best_pairs
        return best_pairs