from grid import Grid
from solver import SolverGreedy, SolverFordFulkerson, SolverGeneral1, SolverGreedy2
import os
import time  # Import the time module

# Directory containing the grid files
data_path = "./ensae-prog25/input/"
# List all files 
grid_files = [f for f in os.listdir(data_path) if f.endswith(".in")]

print("Solving all grids \n")
for file_name in grid_files:
    full_file_path = os.path.join(data_path, file_name)
    print("Solving grid:", file_name)

    grid = Grid.grid_from_file(full_file_path, read_values=True)
    solver_general = SolverGeneral1(grid)
    
    # Start timing
    start_time = time.time()
    solver_general.run()
    # End timing
    end_time = time.time()
    elapsed_time = end_time - start_time  # Calculate elapsed time
    
    general_score = solver_general.score()
    # Print score and time with two decimal places
    print(f"  SolverGeneral score: {general_score}, Time: {elapsed_time:.2f} seconds\n")