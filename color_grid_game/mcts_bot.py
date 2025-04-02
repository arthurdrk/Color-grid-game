import sys
import os
import heapq
import random
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from color_grid_game import *

class MCTS_Bot:
    """
    A bot that chooses a pair using Monte Carlo Tree Search (MCTS).
    """

    def __init__(self, grid : Grid, simulations_per_move: int = 20, epsilon: float = 0.1):
        """
        Initializes the MCTS Bot.

        Parameters
        ----------
        simulations_per_move : int
            Number of full game simulations per move.
        epsilon : float
            Exploration parameter for epsilon-greedy strategy.
        grid : Grid
            The game grid used to evaluate pair costs.
        """
        self.simulations_per_move = simulations_per_move
        self.epsilon = epsilon
        self.grid = grid

    def mcts_move(self) -> tuple[tuple[int, int], tuple[int, int]] | None:
        """
        Selects the best move using simplified Monte Carlo Tree Search (MCTS).
        For each possible pair of cells, runs multiple full-game simulations and
        returns the one with the best average score differential.

        Returns
        -------
        best_pair : tuple[tuple[int, int], tuple[int, int]] or None
            The best move to play (as a pair of cells), or None if no move is possible.
        """
        initial_pairs = self.grid.all_pairs()
        if not initial_pairs:
            return None

        best_pair = None
        best_score = float("inf")

        for pair in initial_pairs:
            total_diff = 0.0

            for _ in range(self.simulations_per_move):
                diff = self.simulate_from_pair(pair, initial_pairs)
                total_diff += diff

            avg_diff = total_diff / self.simulations_per_move

            if avg_diff < best_score:
                best_score = avg_diff
                best_pair = pair

        return best_pair


    def simulate_from_pair(self, initial_pair: tuple[tuple[int, int], tuple[int, int]], initial_pairs: list[tuple[tuple[int, int], tuple[int, int]]]) -> float:
        """
        Simulates a complete game starting from a given initial move,
        assuming both players play using an epsilon-greedy strategy.

        Parameters
        ----------
        initial_pair : tuple[tuple[int, int], tuple[int, int]]
            The initial pair played by the current player.
        initial_pairs : list of tuple[tuple[int, int], tuple[int, int]]
            All valid pairs at the start of the simulation.

        Returns
        -------
        score_diff : float
            The score differential (player_score - opponent_score) for the simulation.
        """

        # Init used cells with the initial move
        used = {initial_pair[0], initial_pair[1]}
        remaining_pairs = [
            p for p in initial_pairs if p[0] not in used and p[1] not in used
        ]

        player_score = self.grid.cost(initial_pair)
        opponent_score = 0
        current_player = 1  # opponent starts after our move

        while remaining_pairs:
            move = self.epsilon_greedy_from_pairs(remaining_pairs)
            if move is None:
                break

            cost = self.grid.cost(move)
            if current_player == 0:
                player_score += cost
            else:
                opponent_score += cost

            # Remove cells used in this move
            used.update(move)
            remaining_pairs = [
                p for p in remaining_pairs if p[0] not in used and p[1] not in used
            ]

            current_player = 1 - current_player  # alternate turns

        return player_score - opponent_score

    def epsilon_greedy_from_pairs(self, pairs: list[tuple[tuple[int, int], tuple[int, int]]]) -> tuple[tuple[int, int], tuple[int, int]] | None:
        """
        Selects a pair of cells to play using an epsilon-greedy strategy:
        with probability ε, selects randomly among the 5 lowest-cost pairs;
        otherwise, selects the best (lowest-cost) pair.

        Parameters
        ----------
        pairs : list of tuple[tuple[int, int], tuple[int, int]]
            List of valid pairs to choose from.

        Returns
        -------
        pair : tuple[tuple[int, int], tuple[int, int]] or None
            The selected pair, or None if the list is empty.
        """
        if not pairs:
            return None

        if random.random() < self.epsilon:
            # Random pick among top 5 lowest-cost pairs
            k = min(5, len(pairs))
            top_k_pairs = heapq.nsmallest(k, pairs, key=lambda p: self.grid.cost(p))
            return random.choice(top_k_pairs)

        return min(pairs, key=lambda p: self.grid.cost(p))


