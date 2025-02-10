from grid import Grid
from solver import *

grid = Grid(2, 3)
print(grid)

data_path = "W:/Documents/1A ENSAE/Projet Prog/ensae-prog25/input/"

file_name = data_path + "grid01.in"
grid = Grid.grid_from_file(file_name)
print(grid)

file_name = data_path + "grid01.in"
grid = Grid.grid_from_file(file_name, read_values=True)
print(grid)
grid.plot()

solver = SolverEmpty(grid)
solver.run()
print("The final score of SolverEmpty is:", solver.score())
