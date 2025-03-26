from grid import Grid

def move_to_play(grid: Grid):
    """
    Choose the best pair by:
    1. Minimizing the current move's cost for the bot
    2. Maximizing the opponent's next move cost, assuming they choose the minimum cost pair

    Parameters:
    -----------
    grid : Grid
        The grid of the turn to be solved.

    Returns:
    --------
    pair : tuple[tuple[int, int], tuple[int, int]]
        The pair of cells to be played, or None if no choice is possible.

    Complexity: O(n*m * log(n*m))
    """
    pairs = grid.all_pairs()
    
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
        remaining_pairs = grid_copy.all_pairs()
        
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