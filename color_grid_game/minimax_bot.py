import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from color_grid_game import *

class minimax_bot:
    """
    A bot that plays using the min-max strategy.

    Methods
    -------
    move_to_play(grid: Grid)
        Choose the best pair by minimizing the current move's cost for the bot
        and maximizing the opponent's next move cost.
    """

    @staticmethod
    def move_to_play2(grid: Grid, rules: str) -> tuple[tuple[int, int], tuple[int, int]] | None:
        """
        Choose the best pair by:
        1. Minimizing the current move's cost for the bot.
        2. Maximizing the opponent's next move cost, assuming they choose the minimum cost pair.

        Parameters
        ----------
        grid : Grid
            The grid of the turn to be solved.

        Returns
        -------
        pair : tuple[tuple[int, int], tuple[int, int]] or None
            The pair of cells to be played, or None if no choice is possible.

        Complexity
        ----------
        O(n*m * log(n*m))
        """
        pairs = grid.all_pairs(rules)

        # If no pairs are available, return None
        if not pairs:
            return None

        # If only one pair is available, return it
        if len(pairs) == 1:
            return pairs[0]

        best_pair = None
        best_score = float('inf')

        for pair in pairs:
            # Create a copy of the grid to simulate the move
            grid_copy = Grid(grid.n, grid.m, [row.copy() for row in grid.color], [row.copy() for row in grid.value])

            # Mark the current pair's cells as forbidden (black)
            grid_copy.color[pair[0][0]][pair[0][1]] = 4
            grid_copy.color[pair[1][0]][pair[1][1]] = 4

            # Get remaining pairs after this move
            remaining_pairs = grid_copy.all_pairs(rules)

            # If no pairs remain after this move, skip it
            if not remaining_pairs:
                continue

            # Find the opponent's best (minimum cost) move
            opponent_best_pair = min(remaining_pairs, key=lambda x: grid_copy.cost(x))

            # Calculate the score:
            # - Minimize our current move's cost
            # - Maximize the opponent's best move's cost
            current_move_cost = grid.cost(pair)
            opponent_best_move_cost = grid_copy.cost(opponent_best_pair)

            # Score combines our move cost and opponent's potential move cost
            # Lower score is better (penalizes both our move cost and opponent's potential low-cost move)
            score = current_move_cost - opponent_best_move_cost

            # Update best pair if this score is better
            if score < best_score:
                best_score = score
                best_pair = pair

        # If no suitable pair found, return the first pair or None
        return best_pair if best_pair is not None else pairs[0]


    def move_to_play(grid: Grid, rules: str):
        """
        Choose the best pair considering that the opponent is playing greedy and
        will choose the best possible pair with a one-turn prediction.
    
        Parameters:
        -----------
        grid : Grid
            The grid of the turn to be solved.
    
        Returns:
        --------
        pair : tuple[tuple[int, int], tuple[int, int]]
            The pair of cells to be played,
            or None if no choice is possible.
    
        Complexity : O(n*m * log(n*m))
        """ 
    
        pairs = grid.all_pairs(rules)  # O(n*m)
        if not pairs:
            return None
    
        # 1) We sort all pairs by cost (from smallest to largest)
        pairs_sorted = sorted(pairs, key=lambda p: grid.cost(p))  # O(n*m * log(n*m))
    
        best_score = float('inf')
        best_pair_for_us = None
    
        # We iterate over all possible pairs (O(n*m) iterations)
        for pair in pairs:
            # We "block" the two cells in this pair
            used_cells = {pair[0], pair[1]}  
    
            # 2) Find the best possible pair for the opponent
            #    by going through pairs_sorted
            choice_adversaire = None
            for candidate in pairs_sorted:  # In practice, we skip quickly if adjacency is limited
                c0, c1 = candidate
                if c0 not in used_cells and c1 not in used_cells:
                    # This pair is free in the modified grid
                    choice_adversaire = candidate
                    break
            # If we didn't find any free pair => the opponent can't play
            # We can set cost=0 or "no impact from the opponent"
            
            if choice_adversaire is None:
                # The opponent does not play
                score = grid.cost(pair)
            else:
                score =  grid.cost(pair) - grid.cost(choice_adversaire)
    
            # We take the pair that minimizes the score
            if score < best_score:
                best_score = score
                best_pair_for_us = pair
    
        return best_pair_for_us
