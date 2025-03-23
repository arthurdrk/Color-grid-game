import os
import time
from grid import Grid
from solver import SolverGreedy, SolverBlossom, SolverGreedy_upgraded

# Directory containing the grid files
data_path = "./ensae-prog25/input/"
# List all files
grid_files = [f for f in os.listdir(data_path) if f.endswith(".in")]

print("Solving all grids \n")
for file_name in grid_files:
    full_file_path = os.path.join(data_path, file_name)
    print("Solving grid:", file_name)

    grid = Grid.grid_from_file(full_file_path, read_values=True)
    solver_blossom = SolverBlossom(grid)
    solver_greedy = SolverGreedy(grid)
    solver_greedy_upgraded = SolverGreedy_upgraded(grid)
    # Start the timer
    start_blossom = time.time()
    solver_blossom.run()
    end_blossom = time.time()

    start_greedy = time.time()
    solver_greedy.run()
    end_greedy = time.time()

    start_greedy_upgraded = time.time()
    solver_greedy_upgraded.run()
    end_greedy_upgraded = time.time()

    blossom_score = solver_blossom.score()
    greedy_score = solver_greedy.score()
    greedy_upgraded_score = solver_greedy_upgraded.score()

    time_blossom = end_blossom - start_blossom
    time_greedy = end_greedy - start_greedy
    time_greedy_upgraded = end_greedy_upgraded - start_greedy_upgraded

    print(f"  SolverBlossom score: {blossom_score}")
    print(f"  Time Blossom: {time_blossom:.4f} seconds")
    print(f"  SolverGreedy score: {greedy_score}")
    print(f"  Time Greedy: {time_greedy:.4f} seconds")
    print(f"  SolverGreedyUpgraded score: {greedy_upgraded_score}")
    print(f"  Time GreedyUpgraded: {time_greedy_upgraded:.4f} seconds\n")
