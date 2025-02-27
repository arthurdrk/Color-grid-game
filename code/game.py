import pygame
import sys
from grid import Grid
from solver import Solver

# Initialisation de Pygame
pygame.init()

# Dimensions de la fenêtre
WINDOW_SIZE = 600
CELL_SIZE = WINDOW_SIZE // 3

# Couleurs
COLORS = {
    0: (255, 255, 255),  # Blanc
    1: (255, 0, 0),      # Rouge
    2: (0, 0, 255),      # Bleu
    3: (0, 255, 0),      # Vert
    4: (0, 0, 0)         # Noir
}

# Chargement de la grille
grid = Grid(2, 3,
            color=[[0, 1, 2], [1, 4, 3]],
            value=[[5, 11, 1], [8, 0, 3]])

solver = Solver(grid)

# Fonction pour dessiner la grille
def draw_grid(screen, grid, solver):
    for i in range(grid.n):
        for j in range(grid.m):
            color = COLORS[grid.color[i][j]]
            pygame.draw.rect(screen, color, (j * CELL_SIZE, i * CELL_SIZE, CELL_SIZE, CELL_SIZE))
            pygame.draw.rect(screen, (0, 0, 0), (j * CELL_SIZE, i * CELL_SIZE, CELL_SIZE, CELL_SIZE), 1)
            font = pygame.font.Font(None, 36)
            text = font.render(str(grid.value[i][j]), True, (0, 0, 0))
            screen.blit(text, (j * CELL_SIZE + CELL_SIZE // 2 - text.get_width() // 2, i * CELL_SIZE + CELL_SIZE // 2 - text.get_height() // 2))

    # Dessiner les lignes entre les paires appariées
    for pair in solver.pairs:
        start = (pair[0][1] * CELL_SIZE + CELL_SIZE // 2, pair[0][0] * CELL_SIZE + CELL_SIZE // 2)
        end = (pair[1][1] * CELL_SIZE + CELL_SIZE // 2, pair[1][0] * CELL_SIZE + CELL_SIZE // 2)
        pygame.draw.line(screen, (255, 255, 0), start, end, 2)

# Fonction pour afficher le score
def draw_score(screen, solver):
    font = pygame.font.Font(None, 48)
    text = font.render(f"Score: {solver.score()}", True, (0, 0, 0))
    screen.blit(text, (10, 10))

# Fonction principale du jeu
def main():
    screen = pygame.display.set_mode((WINDOW_SIZE, WINDOW_SIZE))
    pygame.display.set_caption("Jeu de Grille")

    selected_cells = []

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                x, y = event.pos
                i, j = y // CELL_SIZE, x // CELL_SIZE
                if not grid.is_forbidden(i, j):
                    selected_cells.append((i, j))
                    if len(selected_cells) == 2:
                        solver.pairs.append((selected_cells[0], selected_cells[1]))
                        selected_cells = []

        screen.fill((200, 200, 200))
        draw_grid(screen, grid, solver)
        draw_score(screen, solver)
        pygame.display.flip()

if __name__ == "__main__":
    main()
