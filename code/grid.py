"""
This is the grid module. It contains the Grid class and its associated methods.
"""
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.colors
class Grid():
    """
    A class representing the grid. 

    Attributes: 
    -----------
    n: int
        Number of lines in the grid
    m: int
        Number of columns in the grid
    color: list[list[int]]
        The color of each grid cell: value[i][j] is the value in the cell (i, j), i.e., in the i-th line and j-th column. 
        Note: lines are numbered 0..n-1 and columns are numbered 0..m-1.
    value: list[list[int]]
        The value of each grid cell: value[i][j] is the value in the cell (i, j), i.e., in the i-th line and j-th column. 
        Note: lines are numbered 0..n-1 and columns are numbered 0..m-1.
    colors_list: list[char]
        The mapping between the value of self.color[i][j] and the corresponding color
    """
    def __init__(self, n, m, color=[], value=[]):
        """
        Initializes the grid.

        Parameters: 
        -----------
        n: int
            Number of lines in the grid
        m: int
            Number of columns in the grid
        color: list[list[int]]
            The grid cells colors. Default is empty (then the grid is created with each cell having color 0, i.e., white).
        value: list[list[int]]
            The grid cells values. Default is empty (then the grid is created with each cell having value 1).
        
        The object created has an attribute colors_list: list[char], which is the mapping between the value of self.color[i][j] and the corresponding color
        """
        self.n = n
        self.m = m
        if not color:
            color = [[0 for j in range(m)] for i in range(n)]            
        self.color = color
        if not value:
            value = [[1 for j in range(m)] for i in range(n)]            
        self.value = value
        self.colors_list = ['w', 'r', 'b', 'g', 'k']

    def __str__(self): 
        """
        Prints the grid as text.
        """
        output = f"The grid is {self.n} x {self.m}. It has the following colors:\n"
        for i in range(self.n): 
            output += f"{[self.colors_list[self.color[i][j]] for j in range(self.m)]}\n"
        output += f"and the following values:\n"
        for i in range(self.n): 
            output += f"{self.value[i]}\n"
        return output

    def __repr__(self): 
        """
        Returns a representation of the grid with number of rows and columns.
        """
        return f"<grid.Grid: n={self.n}, m={self.m}>"

    def plot(self): 
        """
        Plots a visual representation of the grid.
        """
        plt.figure(figsize=(8, 8))    
        plt.imshow(self.color, cmap=matplotlib.colors.ListedColormap(self.colors_list), interpolation='nearest')
        for i in range(self.n):
            for j in range(self.m):
                color_idx = self.color[i][j]
                val=self.value[i][j]
                plt.text(j, i, str(val), ha='center', va='center', fontsize=14)
        plt.xticks([])
        plt.yticks([])
        plt.show()

    def is_forbidden(self, i, j):
        """
        Returns True is the cell (i, j) is black and False otherwise
        """
        return self.color[i][j] == 4

    def cost(self, pair):
        """
        Returns the cost of a pair

        Parameters:
        -----------
        pair: tuple[tuple[int]]
            A pair in the format ((i1, j1), (i2, j2))

        Output:
        -----------
        cost: int
            the cost of the pair defined as the absolute value of the difference between their values
        """
        return abs(self.value[pair[0][0]][pair[0][1]] - self.value[pair[1][0]][pair[1][1]])



    def all_pairs(self):
        res = []
        allowed = {
            0: {0, 1, 2, 3},  # blanc avec tout sauf noir
            1: {0, 1, 2},     # rouge avec blanc, bleu, rouge
            2: {0, 1, 2},     # bleu avec blanc, bleu, rouge
            3: {0, 3}         # vert avec blanc, vert
        }
        directions = [(0, 1), (1, 0)]

        for i in range(self.n):
            for j in range(self.m):
                if self.is_forbidden(i, j):
                    continue
                c1 = self.color[i][j]

                for dx, dy in directions:
                    k, l = i + dx, j + dy
                    if 0 <= k < self.n and 0 <= l < self.m:
                        if self.is_forbidden(k, l):
                            continue
                        c2 = self.color[k][l]
                        if c2 in allowed[c1] and c1 in allowed[c2]:
                            res.append(((i, j), (k, l)))
        return res

    
    def vois(self, i, j):
        """
        retourne la liste des voisins de la case (i, j)
        """
        res = []
        var = [(-1, 0), (+1, 0), (0, -1), (0, +1)]
        for ele in var:
            k, l = i+ele[0], j+ele[1]
            if k >= 0 and k <= self.n-1 and l >= 0 and l <= self.m-1:
                res.append((k,  l))
        return res


    @classmethod
    def grid_from_file(cls, file_name, read_values=False): 
        """
        Creates a grid object from class Grid, initialized with the information from the file file_name.
        
        Parameters: 
        -----------
        file_name: str
            Name of the file to load. The file must be of the format: 
            - first line contains "n m" 
            - next n lines contain m integers that represent the colors of the corresponding cell
            - next n lines [optional] contain m integers that represent the values of the corresponding cell
        read_values: bool
            Indicates whether to read values after having read the colors. Requires that the file has 2n+1 lines

        Output: 
        -------
        grid: Grid
            The grid
        """
        with open(file_name, "r") as file:
            n, m = map(int, file.readline().split())
            color = [[] for i_line in range(n)]
            for i_line in range(n):
                line_color = list(map(int, file.readline().split()))
                if len(line_color) != m: 
                    raise Exception("Format incorrect")
                for j in range(m):
                    if line_color[j] not in range(5):
                        raise Exception("Invalid color")
                color[i_line] = line_color

            if read_values:
                value = [[] for i_line in range(n)]
                for i_line in range(n):
                    line_value = list(map(int, file.readline().split()))
                    if len(line_value) != m: 
                        raise Exception("Format incorrect")
                    value[i_line] = line_value
            else:
                value = []

            grid = Grid(n, m, color, value)
        return grid


