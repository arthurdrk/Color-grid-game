<img width="200" alt="image" src="https://github.com/user-attachments/assets/536d54e2-bfd8-40b4-919e-80e28ae60b50" />

## Description

ColorGrid is a programming project developed as part of the first-year curriculum at ENSAE Paris. The game involves a grid-based matching problem with specific rules and constraints.
Documentation can be found here : (https://arthurdrk.github.io/Color-grid-game/)

## Problem Description
<img width="400" alt="image" src="https://github.com/user-attachments/assets/4428a98a-1e09-4fa4-97fb-8e00bd2b01b0" />



Consider an `n × m` grid, where `n ≥ 1` and `m ≥ 2` are integers representing the number of rows and columns, respectively. Each cell in the grid has coordinates `(i, j)` where `i ∈ {0, ..., n-1}` is the row index and `j ∈ {0, ..., m-1}` is the column index. Each cell has two attributes:

- **Color `c(i, j)`**: An integer in `{0, 1, 2, 3, 4}` corresponding to a color:
  - 0: White (`'w'`)
  - 1: Red (`'r'`)
  - 2: Blue (`'b'`)
  - 3: Green (`'g'`)
  - 4: Black (`'k'`)

- **Value `v(i, j)`**: A positive integer.

### Objective

The goal is to select pairs of adjacent cells with the following constraints:

- Cells must be adjacent either horizontally or vertically.
- Black cells cannot be paired.
- White cells can be paired with any other color except black.
- Blue cells can be paired with blue, red, or white cells.
- Red cells can be paired with blue, red, or white cells.
- Green cells can only be paired with green or white cells.

Each cell can only be part of one pair. The objective is to minimize the score calculated as the sum of the absolute differences in values of the paired cells plus the sum of the values of unpaired cells (excluding black cells).

## How to play

1. Clone the repository:
   ```bash
   git clone https://github.com/arthurdrk/Color-grid-game.git
   cd Color-grid-game
   ```

2. In VSCode, use the File menu to open the 'ensae-prog25' folder within the cloned repository.

3. Install the required packages:
   ```bash
   pip install -r requirements.txt
   ```

4. Run the game.py script:
   ```bash
   python code/run_game.py
   ```
   
## License

This project is licensed under the MIT License.
