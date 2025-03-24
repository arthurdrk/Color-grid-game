from grid import Grid

def move_to_play(grid: Grid):
    """
    Choose the best pair considering that the opponent is playing greedy and wants to choose the best pair possible
    with a prediction of one turn.

    Parameters:
    -----------
    grid : Grid
        The grid of the turn to be solved.

    Returns:
    --------
    pair : tuple[tuple[int, int], tuple[int, int]]
        The pair of cells to be played, or None if no choice is possible.

    Complexity: O((n*m)²) can be bettered to O(n*m).
    """

    pairs = list(set(sorted(grid.all_pairs())))
    res = None  # tuple[tuple[int, int], tuple[int, int]]
    best = float('inf')  # best score with this choice of pair

    if len(pairs) == 1:
        return pairs[0]
    else:
        for pair in pairs:
            grid_copy = Grid(grid.n, grid.m, grid.color, grid.value)
            grid_copy.color[pair[0][0]][pair[0][1]] = 4
            grid_copy.color[pair[1][0]][pair[1][1]] = 4

            # Assume the opponent plays greedy and find the best pair remaining without pair
            pairs2 = grid_copy.all_pairs()

            if not pairs2:
                # If there are no pairs left, skip this iteration
                continue

            player_choice = min(pairs2, key=lambda x: grid_copy.cost(x))
            score = grid_copy.cost(pair) - grid_copy.cost(player_choice)

            if score < best:
                best = score
                res = pair

        return res
