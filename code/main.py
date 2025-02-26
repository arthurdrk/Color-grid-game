from grid import Grid
from solver import SolverGreedy, SolverFordFulkerson
import os

# Directory containing the grid files
data_path = "./input/"

# List all files in the directory
grid_files = [f for f in os.listdir(data_path)]

for file_name in grid_files:
    
    full_file_path = os.path.join(data_path, file_name)
    print("Solving grid:", file_name)

    grid = Grid.grid_from_file(full_file_path, read_values=False)

    # Run SolverFordFulkerson
    solver_ff = SolverFordFulkerson(grid)
    solver_ff.run()
    ff_score = solver_ff.score()

    # Run SolverGreedy
    solver_greedy = SolverGreedy(grid)
    solver_greedy.run()
    greedy_score = solver_greedy.score()

    # Print the results
    print(f"  SolverFordFulkerson score: {ff_score}")
    print(f"  SolverGreedy score: {greedy_score}")
    print()  # Add a blank line for readability
