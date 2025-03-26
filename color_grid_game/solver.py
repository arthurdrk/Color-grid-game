from color_grid_game import *

class Solver:
    """
    A solver class for finding optimal pairs in a grid.

    Attributes:
    -----------
    grid : Grid
        The grid to be solved.
    pairs : list[tuple[tuple[int, int], tuple[int, int]]]
        A list of pairs, each being a tuple ((i1, j1), (i2, j2)) representing paired cells.
    """

    def __init__(self, grid: Grid, rules="original rules"):
        """
        Initializes the solver with a grid.

        Parameters:
        -----------
        grid : Grid
            The grid to be solved.
        rules : str, optional
            The rules to apply for solving the grid. Default is "original rules".

        Raises:
        -------
        TypeError: If grid is not an instance of Grid.
        """
        self.grid = grid
        self.pairs = []
        self.rules = rules

    def score(self) -> int:
        """
        Computes the score of the list of pairs in self.pairs.

        The score is calculated as the sum of the values of unpaired cells
        excluding black cells, plus the sum of the cost of each pair of cells.

        Returns:
        --------
        int
            The computed score.

        Raises:
        -------
        ValueError: If any cell in pairs is invalid.
        """
        # Add all paired cells to the set and calculate the cost of each pair
        score = sum(self.grid.cost(pair) for pair in self.pairs)
        taken = set([cell for pair in self.pairs for cell in pair])
        score += sum(self.grid.value[i][j] for i in range(self.grid.n)
                     for j in range(self.grid.m)
                     if (i, j) not in taken and not self.grid.is_forbidden(i, j))
        return score