from grid import Grid
from solver import SolverGreedy, SolverFordFulkerson, SolverGeneral, SolverGreedy2
import os

# Directory containing the grid files
data_path = "./ensae-prog25/input/"
# List all files 
grid_files = [f for f in os.listdir(data_path) if f.endswith(".in")]


# grid = Grid.grid_from_file("./ensae-prog25/input/grid11.in", read_values=True)
# solver_general = SolverGeneral(grid)
# solver_general.run()
# general_score = solver_general.score()
# pairs = solver_general.pairs
# print(f"  SolverGeneral score: {general_score} \n")


print("Solving all grids \n")
for file_name in grid_files:
    
    full_file_path = os.path.join(data_path, file_name)
    print("Solving grid:", file_name)

    grid = Grid.grid_from_file(full_file_path, read_values=True)
    solver_general = SolverGeneral(grid)
    solver_general.run()
    general_score = solver_general.score()
    pairs = solver_general.pairs
    print(f"  SolverGeneral score: {general_score} \n")
    
