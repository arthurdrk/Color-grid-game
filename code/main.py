from grid import Grid
from solver import *


data_path = "C:/Users/arthr/Desktop/ENSAE 1A/S2/Projet-Prog/Projet-de-programmation-1A/input/"
file_name = data_path + "grid28.in"

grid = Grid.grid_from_file(file_name, read_values=False)



solver = SolverBiparti(grid)
solver.run()
print("The final score of SolverBiparti is:", solver.score())
print(solver.pairs)
print(len(solver.pairs))
grid.plot() 