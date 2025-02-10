from grid import Grid
from solver import *


data_path = "C:/Users/arthr/Desktop/ENSAE 1A/S2/Projet-Prog/Projet-de-programmation-1A/input/"
file_name = data_path + "grid14.in"

grid = Grid.grid_from_file(file_name, read_values=True)



solver = SolverBiparti(grid)
solver.run()
print("The final score of SolverBiparti is:", solver.score())
print(solver.pairs)
grid.plot()