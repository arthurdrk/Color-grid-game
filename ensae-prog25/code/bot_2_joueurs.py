from grid import Grid

def calcul_coup(grid : Grid):
        """

        choose the best pair considering that the opponent is playing greedy and want to choose the best pair possible with a prediction of one turn
        
        Parameters:
        -----------
        grid : Grid
            The grid of the turn to be solved 

        returns:
        --------
        pair : tuple[tuple[int, int], tuple[int, int]]
            The pair of cells to be played
        or None if no choice is possible   

        complexity : ?
        """ 

        pairs = grid.all_pairs()
        res = [] #tuple[tuple[int, int], tuple[int, int]]
        best = float('inf') #best score with this choice of pair
        for pair in pairs:
                grid_copy = Grid(grid.n, grid.m, grid.color, grid.value)
                grid_copy.color[pair[0][0]][pair[0][1]] = 4
                grid_copy.color[pair[1][0]][pair[1][1]] = 4
                # we now assume the opponenet plays greedy and find the best pair remaining without pair
                pairs2 = grid_copy.all_pairs()
                try:
                        choice = min(pairs2, key=lambda x: grid_copy.cost(x))
                except ValueError:
                        try:
                               res = min(pairs, key=lambda x: grid.cost(x))
                        except ValueError:
                                return None
                
                score = grid_copy.cost(choice)-grid_copy.cost(pair)
                if score > best:
                    best = score
                    res = pair
        return res
                        
                

        
