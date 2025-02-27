import pygame
import sys
import os
from grid import Grid
from solver import Solver, SolverGreedy

# Initialisation de Pygame
pygame.init()

# Dimensions de la fenêtre
WINDOW_SIZE = 600
CELL_SIZE = WINDOW_SIZE // 3

# Couleurs
COLORS = {
    0: (255, 255, 255),  # Blanc cassé foncé
    1: (200, 0, 0),    # Rouge foncé
    2: (0, 0, 200),    # Bleu foncé
    3: (0, 200, 0),    # Vert foncé
    4: (0, 0, 0)      # Gris foncé
}

# Répertoire contenant les fichiers de grille
data_path = "./input/"

# Lister tous les fichiers dans le répertoire
grid_files = [f for f in os.listdir(data_path) if f.endswith(".in")]

# Fonction pour dessiner le titre
def draw_title(screen):
    font = pygame.font.Font(None, 72)
    text = font.render("ColorGrid", True, (0, 0, 0))
    screen.blit(text, (WINDOW_SIZE // 2 - text.get_width() // 2, 50))

# Fonction pour dessiner les options de grille
def draw_grid_options(screen):
    font = pygame.font.Font(None, 36)
    y_offset = 150
    for grid in grid_files:
        text = font.render(grid, True, (0, 0, 0))
        pygame.draw.rect(screen, (200, 200, 200), (WINDOW_SIZE // 2 - 100, y_offset, 200, 40))
        screen.blit(text, (WINDOW_SIZE // 2 - text.get_width() // 2, y_offset + 10))
        y_offset += 50

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
    screen.blit(text, (5, WINDOW_SIZE - 50))  # Décaler de 5 pixels vers la droite

# Fonction pour afficher le message de fin de jeu
def draw_end_screen(screen, message, color):
    font = pygame.font.Font(None, 72)
    text = font.render(message, True, color)
    screen.blit(text, (WINDOW_SIZE // 2 - text.get_width() // 2, WINDOW_SIZE // 2 - text.get_height() // 2))
    pygame.display.flip()
    pygame.time.wait(2000)  # Réduire le délai à 2 secondes

# Fonction pour afficher un message d'erreur
def draw_error_message(screen, message):
    font = pygame.font.Font(None, 48)  # Même taille que le score
    text = font.render(message, True, (255, 0, 0))
    screen.blit(text, (5, WINDOW_SIZE - 20))  # Décaler de 5 pixels vers la droite
    pygame.display.flip()
    pygame.time.wait(2000)

# Fonction pour dessiner le bouton Restart
def draw_restart_button(screen):
    font = pygame.font.Font(None, 36)
    text = font.render("Restart", True, (255, 255, 255))
    pygame.draw.rect(screen, (0, 0, 255), (WINDOW_SIZE - 110, WINDOW_SIZE + 10, 100, 40))
    screen.blit(text, (WINDOW_SIZE - 100, WINDOW_SIZE + 20))

# Fonction principale du jeu
def main():
    screen = pygame.display.set_mode((WINDOW_SIZE, WINDOW_SIZE + 70))  # Augmenter la taille de la fenêtre pour inclure le bouton
    pygame.display.set_caption("ColorGrid")

    selected_grid = None
    while selected_grid is None:
        screen.fill((255, 255, 255))
        draw_title(screen)
        draw_grid_options(screen)
        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                x, y = event.pos
                y_offset = 150
                for grid in grid_files:
                    if WINDOW_SIZE // 2 - 100 <= x <= WINDOW_SIZE // 2 + 100 and y_offset <= y <= y_offset + 40:
                        selected_grid = grid
                        break
                    y_offset += 50

    # Charger la grille sélectionnée
    grid = Grid.grid_from_file(os.path.join(data_path, selected_grid),read_values=True)
    solver = Solver(grid)
    solver_greedy = SolverGreedy(grid)
    solver_greedy.run()
    greedy_score = solver_greedy.score()

    selected_cells = []
    game_over = False

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                x, y = event.pos
                if y >= WINDOW_SIZE:  # Ignorer les clics en dessous de la grille
                    if WINDOW_SIZE - 110 <= x <= WINDOW_SIZE - 10 and WINDOW_SIZE + 10 <= y <= WINDOW_SIZE + 50:
                        # Réinitialiser les paires appariées
                        solver.pairs = []
                        selected_cells = []
                        game_over = False
                        continue
                i, j = y // CELL_SIZE, x // CELL_SIZE
                if grid.is_forbidden(i, j):
                    draw_error_message(screen, "You cannot pair these two cells")
                    selected_cells = []  # Réinitialiser la sélection
                elif (i, j) not in [cell for pair in solver.pairs for cell in pair]:
                    selected_cells.append((i, j))
                    if len(selected_cells) == 2:
                        # Vérifier si la paire est valide
                        if selected_cells[1] in grid.vois(selected_cells[0][0], selected_cells[0][1]):
                            color1, color2 = grid.color[selected_cells[0][0]][selected_cells[0][1]], grid.color[selected_cells[1][0]][selected_cells[1][1]]
                            if can_pair(color1, color2):
                                solver.pairs.append((selected_cells[0], selected_cells[1]))
                            else:
                                draw_error_message(screen, "You cannot pair these two cells")
                        else:
                            draw_error_message(screen, "You cannot pair these two cells")
                        selected_cells = []

        screen.fill((200, 200, 200))
        draw_grid(screen, grid, solver)
        draw_score(screen, solver)
        draw_restart_button(screen)
        pygame.display.flip()

        # Vérifier s'il reste des paires valides à sélectionner
        if not any(pair_is_valid(pair, solver.pairs, grid) for pair in grid.all_pairs()):
            if not game_over:
                game_over = True
                if solver.score() > greedy_score:
                    draw_end_screen(screen, "You lost!", (255, 0, 0))
                else:
                    draw_end_screen(screen, "You won!", (0, 255, 0))
                # Réinitialiser le jeu après 2 secondes
                solver.pairs = []
                selected_cells = []
                game_over = False

def can_pair(color1, color2):
    allowed = {
        0: {0, 1, 2, 3},  # white can pair with all except black
        1: {0, 1, 2},     # red can pair with white, blue, red
        2: {0, 1, 2},     # blue can pair with white, blue, red
        3: {0, 3}         # green can pair with white, green
    }
    return color2 in allowed.get(color1, set()) and color1 in allowed.get(color2, set())

def pair_is_valid(pair, existing_pairs, grid):
    # Vérifier si la paire est adjacente et respecte les règles de couleur
    (i1, j1), (i2, j2) = pair
    if grid.is_forbidden(i1, j1) or grid.is_forbidden(i2, j2):
        return False
    if (i1, j1) in [cell for pair in existing_pairs for cell in pair]:
        return False
    if (i2, j2) in [cell for pair in existing_pairs for cell in pair]:
        return False
    if can_pair(grid.color[i1][j1], grid.color[i2][j2]):
        return True
    return False

if __name__ == "__main__":
    main()
