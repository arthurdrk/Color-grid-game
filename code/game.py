import pygame
import sys
import os
from grid import Grid
from solver import Solver, SolverGeneral

# Initialisation de Pygame
pygame.init()

# Couleurs
COLORS = {
    0: (255, 255, 255),    # Blanc
    1: (200, 0, 0),        # Rouge foncé
    2: (0, 0, 200),        # Bleu foncé
    3: (0, 200, 0),        # Vert foncé
    4: (0, 0, 0),          # Noir
    5: (220, 220, 0)       # Jaune foncé
}
COLORS_title = {
    0: (0, 0, 0),    # Noir
    1: (200, 0, 0),  # Rouge foncé
    2: (0, 0, 200),  # Bleu foncé
    3: (0, 200, 0)   # Vert foncé
}

# Répertoire contenant les fichiers de grille
data_path = "./input/"

# Lister tous les fichiers dans le répertoire
grid_files = [f for f in os.listdir(data_path) if f.endswith(".in")]

# Fonction pour dessiner le titre avec des couleurs alternées
def draw_title(screen, window_size):
    font = pygame.font.Font(None, 72)
    title = "ColorGrid"
    colors = [COLORS_title[i % len(COLORS_title)] for i in range(len(title))]  # Alterner les couleurs

    # Calculer la position initiale pour centrer le titre
    total_width = sum(font.size(char)[0] for char in title)
    start_x = (window_size[0] - total_width) // 2

    # Dessiner chaque lettre avec une couleur différente
    current_x = start_x
    for i, char in enumerate(title):
        text = font.render(char, True, colors[i])
        screen.blit(text, (current_x, 20))
        current_x += text.get_width()  # Mettre à jour la position x pour la lettre suivante

# Fonction pour dessiner les options de grille avec défilement
def draw_grid_options(screen, window_size, scroll, scroll_bar_rect, scroll_bar_height):
    font = pygame.font.Font(None, 36)
    y_offset = 100  # Commencer en dessous du titre
    max_scroll = max(0, len(grid_files) * 50 - (window_size[1] - 170))
    scroll = max(0, min(scroll, max_scroll))

    # Dessiner un rectangle pour la zone de défilement
    pygame.draw.rect(screen, (255, 255, 255), (50, 100, window_size[0] - 120, window_size[1] - 170))

    for i, grid in enumerate(grid_files):
        if y_offset + 50 - scroll > window_size[1] - 70:
            break

        # Reformater le nom du fichier
        if grid.startswith("grid") and grid.endswith(".in"):
            # Enlever "grid" au début et ".in" à la fin
            numbers = grid[4:-3]
            formatted_name = f"Grid {numbers}"
        else:
            formatted_name = grid  # Garder le nom d'origine si le format ne correspond pas

        text = font.render(formatted_name, True, (0, 0, 0))
        pygame.draw.rect(screen, (200, 200, 200), (window_size[0] // 2 - 100, y_offset - scroll, 200, 40))
        screen.blit(text, (window_size[0] // 2 - text.get_width() // 2, y_offset - scroll + 10))
        y_offset += 50

    # Dessiner la barre de défilement
    pygame.draw.rect(screen, (150, 150, 150), scroll_bar_rect.inflate(0, scroll_bar_height - scroll_bar_rect.height))

# Fonction pour dessiner la grille
def draw_grid(screen, grid, solver, cell_size):
    for i in range(grid.n):
        for j in range(grid.m):
            color = COLORS[grid.color[i][j]]
            pygame.draw.rect(screen, color, (j * cell_size, i * cell_size, cell_size, cell_size))
            pygame.draw.rect(screen, (0, 0, 0), (j * cell_size, i * cell_size, cell_size, cell_size), 1)
            font = pygame.font.Font(None, 36)
            text = font.render(str(grid.value[i][j]), True, (0, 0, 0))
            screen.blit(text, (j * cell_size + cell_size // 2 - text.get_width() // 2, i * cell_size + cell_size // 2 - text.get_height() // 2))

    # Dessiner les lignes entre les paires appariées
    for pair in solver.pairs:
        start = (pair[0][1] * cell_size + cell_size // 2, pair[0][0] * cell_size + cell_size // 2)
        end = (pair[1][1] * cell_size + cell_size // 2, pair[1][0] * cell_size + cell_size // 2)
        pygame.draw.line(screen, COLORS[5], start, end, 4)  # Utiliser COLORS[5] pour jaune foncé et épaisseur 4

# Fonction pour afficher le score
def draw_score(screen, solver, window_size, cell_size):
    font = pygame.font.Font(None, 48)
    text = font.render(f"Score: {solver.score()}", True, (0, 0, 0))
    screen.blit(text, (5, window_size[1] - cell_size - 80))  # Sous la grille

# Fonction pour afficher le message de fin de jeu
def draw_end_screen(screen, message, color, window_size):
    font = pygame.font.Font(None, 72)
    text = font.render(message, True, color)

    # Position verticale fixe, comme pour le message d'erreur
    y_position = window_size[1] - 120

    # Position horizontale centrée
    x_position = (window_size[0] - text.get_width()) // 2

    screen.blit(text, (x_position, y_position))
    pygame.display.flip()
    pygame.time.wait(2000)  # Réduire le délai à 2 secondes

# Fonction pour afficher un message d'erreur
def draw_error_message(screen, message, window_size):
    font = pygame.font.Font(None, 48)  # Même taille que le score
    text = font.render(message, True, (255, 0, 0))
    # Ajuster la position verticale pour s'assurer que le texte reste dans la fenêtre
    y_position = window_size[1] - 110  # Au-dessus des boutons
    screen.blit(text, (5, y_position))  # Décaler de 5 pixels vers la droite
    pygame.display.flip()
    pygame.time.wait(2000)

# Fonction pour dessiner le bouton Restart
def draw_restart_button(screen, window_size):
    font = pygame.font.Font(None, 36)
    text = font.render("Restart", True, (255, 255, 255))

    # Calculer la position centrée pour le texte
    button_rect = pygame.Rect(window_size[0] - 330, window_size[1] - 70, 100, 40)
    text_rect = text.get_rect(center=button_rect.center)

    pygame.draw.rect(screen, (50, 50, 50), button_rect)  # Gris foncé
    screen.blit(text, text_rect.topleft)

# Fonction pour dessiner le bouton Solution
def draw_solution_button(screen, window_size):
    font = pygame.font.Font(None, 36)
    text = font.render("Solution", True, (255, 255, 255))

    # Calculer la position centrée pour le texte
    button_rect = pygame.Rect(window_size[0] - 225, window_size[1] - 70, 110, 40)  # Augmenter la largeur
    text_rect = text.get_rect(center=button_rect.center)

    pygame.draw.rect(screen, (0, 200, 0), button_rect)  # Vert
    screen.blit(text, text_rect.topleft)

# Fonction pour dessiner le bouton Menu
def draw_menu_button(screen, window_size):
    font = pygame.font.Font(None, 36)
    text = font.render("Menu", True, (255, 255, 255))

    # Calculer la position centrée pour le texte
    button_rect = pygame.Rect(window_size[0] - 110, window_size[1] - 70, 100, 40)
    text_rect = text.get_rect(center=button_rect.center)

    pygame.draw.rect(screen, (50, 50, 50), button_rect)  # Gris foncé
    screen.blit(text, text_rect.topleft)

# Fonction principale du jeu
def main():
    screen = pygame.display.set_mode((600, 600))
    pygame.display.set_caption("ColorGrid")

    selected_grid = None
    scroll = 0
    scroll_bar_dragging = False
    mouse_y_offset = 0

    while selected_grid is None:
        screen.fill((255, 255, 255))
        window_size = (600, 600)
        visible_height = window_size[1] - 170  # Hauteur visible de la liste
        total_content_height = len(grid_files) * 50  # Hauteur totale du contenu
        max_scroll = max(0, total_content_height - visible_height)

        # Calcul de la hauteur de la barre de défilement
        if max_scroll > 0:
            scroll_bar_height = max(20, int((visible_height / total_content_height) * visible_height))
        else:
            scroll_bar_height = visible_height

        # Calcul de la position Y de la barre de défilement
        if max_scroll > 0:
            scroll_percentage = scroll / max_scroll
            scroll_bar_y = 100 + (scroll_percentage * (visible_height - scroll_bar_height))
        else:
            scroll_bar_y = 100

        scroll_bar_rect = pygame.Rect(580, int(scroll_bar_y), 20, scroll_bar_height)

        # Dessin des éléments
        draw_grid_options(screen, window_size, scroll, scroll_bar_rect, scroll_bar_height)
        pygame.draw.rect(screen, (255, 255, 255), (0, 0, 600, 100))
        draw_title(screen, window_size)
        pygame.display.flip()

        # Gestion des événements
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    x, y = event.pos
                    # Clic sur la barre de défilement
                    if scroll_bar_rect.collidepoint(x, y) and max_scroll > 0:
                        scroll_bar_dragging = True
                        mouse_y_offset = y - scroll_bar_rect.y
                    # Clic sur un fichier
                    else:
                        y_offset = 100
                        for i, grid in enumerate(grid_files):
                            item_y = y_offset - scroll + i*50
                            if 50 <= item_y <= window_size[1]-70:
                                if (window_size[0]//2 - 100 <= x <= window_size[0]//2 + 100 and
                                    100 <= y - (item_y - 100) <= 140):
                                    selected_grid = grid
                                    break
            elif event.type == pygame.MOUSEBUTTONUP:
                scroll_bar_dragging = False
            elif event.type == pygame.MOUSEMOTION:
                if scroll_bar_dragging and max_scroll > 0:
                    mouse_y = event.pos[1] - mouse_y_offset
                    new_y = max(100, min(mouse_y, 100 + visible_height - scroll_bar_height))
                    scroll = ((new_y - 100) / (visible_height - scroll_bar_height)) * max_scroll
                    scroll = max(0, min(scroll, max_scroll))
            elif event.type == pygame.MOUSEWHEEL:
                scroll -= event.y * 50  # Sensibilité de la molette
                scroll = max(0, min(scroll, max_scroll))

    # Charger la grille sélectionnée
    grid = Grid.grid_from_file(os.path.join(data_path, selected_grid), read_values=True)
    solver = Solver(grid)
    solver_general = SolverGeneral(grid)
    solver_general.run()
    general_score = solver_general.score()

    # Calculer la taille de la fenêtre en fonction de la grille
    cell_size = 60
    window_size = (max(600, grid.m * cell_size), grid.n * cell_size + 150)
    screen = pygame.display.set_mode(window_size)

    selected_cells = []
    game_over = False
    show_solution = False

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                x, y = event.pos
                if y >= grid.n * cell_size:  # Ignorer les clics en dessous de la grille
                    if window_size[0] - 330 <= x <= window_size[0] - 230 and window_size[1] - 70 <= y <= window_size[1] - 30:
                        # Réinitialiser les paires appariées
                        solver.pairs = []
                        selected_cells = []
                        game_over = False
                        show_solution = False
                        continue
                    elif window_size[0] - 270 <= x <= window_size[0] - 120 and window_size[1] - 70 <= y <= window_size[1] - 30:
                        # Afficher la solution optimale
                        solver.pairs = solver_general.pairs
                        show_solution = True
                        continue
                    elif window_size[0] - 110 <= x <= window_size[0] - 10 and window_size[1] - 70 <= y <= window_size[1] - 30:
                        # Retourner au menu
                        main()
                        return
                if not show_solution:
                    i, j = y // cell_size, x // cell_size
                    if grid.is_forbidden(i, j):
                        draw_error_message(screen, "You cannot pair these two cells", window_size)
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
                                    draw_error_message(screen, "You cannot pair these two cells", window_size)
                            else:
                                draw_error_message(screen, "You cannot pair these two cells", window_size)
                            selected_cells = []

        screen.fill((200, 200, 200))
        draw_grid(screen, grid, solver, cell_size)
        draw_score(screen, solver, window_size, cell_size)
        draw_restart_button(screen, window_size)
        draw_solution_button(screen, window_size)
        draw_menu_button(screen, window_size)
        pygame.display.flip()

        # Vérifier s'il reste des paires valides à sélectionner
        if not show_solution and not any(pair_is_valid(pair, solver.pairs, grid) for pair in grid.all_pairs()):
            if not game_over:
                game_over = True
                if solver.score() > general_score:
                    draw_end_screen(screen, "You lost!", (200, 0, 0), window_size)
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
