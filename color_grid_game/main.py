import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from color_grid_game import *

def main():
    # Set up argument parser
    parser = argparse.ArgumentParser(description="Solve color grid game with specified rules.")
    parser.add_argument('--rules', choices=['original', 'new'], default='original', help='Choose the rule set: original or new')
    args = parser.parse_args()

    data_path: str = "./input/"
    grid_files = [f for f in os.listdir(data_path) if f.endswith(".in")]

    print("Solving all grids \n")
    for file_name in grid_files:
        full_file_path = os.path.join(data_path, file_name)
        print("Solving grid:", file_name)

        grid = Grid.grid_from_file(full_file_path, read_values=True)
        rules = "original rules" if args.rules == 'original' else "new rules"

        solver_blossom = SolverBlossom(grid, rules)
        solver_hungarian = SolverHungarian(grid, rules)

        start_blossom = time.time()
        solver_blossom.run()
        end_blossom = time.time()

        start_hungarian = time.time()
        solver_hungarian.run()
        end_hungarian = time.time()

        blossom_score = solver_blossom.score()
        hungarian_score = solver_hungarian.score()

        time_blossom = end_blossom - start_blossom
        time_hungarian = end_hungarian - start_hungarian

        print(f"  SolverBlossom {rules.capitalize()} score: {blossom_score},  Time : {time_blossom:.4f} seconds")
        print(f"  SolverHungarian {rules.capitalize()} score: {hungarian_score},  Time : {time_hungarian:.4f} seconds\n")

if __name__ == '__main__':
    main()
