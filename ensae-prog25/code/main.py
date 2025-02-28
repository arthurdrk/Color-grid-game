from grid import Grid
from solver import SolverGreedy, SolverFordFulkerson, SolverGeneral
import os

# Directory containing the grid files
data_path = "./input/"

# List all files in the directory
grid_files = [f for f in os.listdir(data_path) if f.endswith(".in")]

print("Solving all grids (with all values equal to 1)\n")
for file_name in grid_files:
    
    full_file_path = os.path.join(data_path, file_name)
    print("Solving grid:", file_name)

    grid = Grid.grid_from_file(full_file_path, read_values=True)

    solver_ff = SolverFordFulkerson(grid)
    solver_ff.run()
    ff_score = solver_ff.score()
    
    solver_greedy = SolverGreedy(grid)
    solver_greedy.run()
    greedy_score = solver_greedy.score()

    solver_general = SolverGeneral(grid)
    solver_general.run()
    general_score = solver_general.score()
    
    print(f"  SolverGeneral score: {general_score}")
    print(f"  SolverFordFulkerson score: {ff_score}")
    print(f"  SolverGreedy score: {greedy_score}\n")
    
