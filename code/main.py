from grid import Grid
from solver import *


data_path = "./input/"
file_name = data_path + "grid27.in"

grid = Grid.grid_from_file(file_name, read_values=False)

solver = SolverFordFulkerson(grid)
solver.run()
print("The final score of SolverFordFulkerson is:", solver.score())


solver = SolverGreedy(grid)
solver.run()
print("The final score of SolverGreedy is:", solver.score())