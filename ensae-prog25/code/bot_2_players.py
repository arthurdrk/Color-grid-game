from grid import Grid


def move_to_play(grid: Grid):
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

    pairs = grid.all_pairs()  # O(n*m)
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
            score = 0 - grid.cost(pair)
        else:
            score = grid.cost(choice_adversaire) - grid.cost(pair)

        # We take the pair that minimizes the score
        if score < best_score:
            best_score = score
            best_pair_for_us = pair

    return best_pair_for_us

