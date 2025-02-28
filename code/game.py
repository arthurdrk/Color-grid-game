import pygame
import sys
import os
from grid import Grid
from solver import Solver, SolverGeneral

pygame.init()

class UIManager:
    def __init__(self, screen, colors, colors_title):
        self.screen = screen
        self.colors = colors
        self.colors_title = colors_title

    def draw_title(self, window_size):
        font = pygame.font.Font(None, 72)
        title = "ColorGrid"
        colors = [self.colors_title[i % len(self.colors_title)] for i in range(len(title))]

        total_width = sum(font.size(char)[0] for char in title)
        start_x = (window_size[0] - total_width) // 2

        current_x = start_x
        for i, char in enumerate(title):
            text = font.render(char, True, colors[i])
            self.screen.blit(text, (current_x, 20))
            current_x += text.get_width()

    def draw_grid_options(self, window_size, scroll, scroll_bar_rect, scroll_bar_height, grid_files, pressed_index=-1):
        font = pygame.font.Font(None, 36)
        y_offset = 100
        max_scroll = max(0, len(grid_files) * 50 - (window_size[1] - 170))
        scroll = max(0, min(scroll, max_scroll))

        pygame.draw.rect(self.screen, (255, 255, 255), (50, 100, window_size[0] - 120, window_size[1] - 170))

        for i, grid in enumerate(grid_files):
            if y_offset + 50 - scroll > window_size[1] - 70:
                break

            btn_color = (150, 150, 150) if i == pressed_index else (200, 200, 200)
            
            if grid.startswith("grid") and grid.endswith(".in"):
                numbers = grid[4:-3]
                formatted_name = f"Grid {numbers}"
            else:
                formatted_name = grid

            text = font.render(formatted_name, True, (0, 0, 0))
            btn_rect = pygame.Rect(window_size[0]//2 - 100, y_offset - scroll, 200, 40)
            pygame.draw.rect(self.screen, btn_color, btn_rect)
            self.screen.blit(text, (window_size[0]//2 - text.get_width()//2, y_offset - scroll + 10))
            y_offset += 50

        pygame.draw.rect(self.screen, (150, 150, 150), scroll_bar_rect.inflate(0, scroll_bar_height - scroll_bar_rect.height))

    def draw_grid(self, grid, solver, cell_size):
        for i in range(grid.n):
            for j in range(grid.m):
                color = self.colors[grid.color[i][j]]
                pygame.draw.rect(self.screen, color, (j * cell_size, i * cell_size, cell_size, cell_size))
                pygame.draw.rect(self.screen, (0, 0, 0), (j * cell_size, i * cell_size, cell_size, cell_size), 1)
                font = pygame.font.Font(None, 36)
                text = font.render(str(grid.value[i][j]), True, (0, 0, 0))
                self.screen.blit(text, (j * cell_size + cell_size//2 - text.get_width()//2, i * cell_size + cell_size//2 - text.get_height()//2))

        for pair in solver.pairs:
            start = (pair[0][1] * cell_size + cell_size//2, pair[0][0] * cell_size + cell_size//2)
            end = (pair[1][1] * cell_size + cell_size//2, pair[1][0] * cell_size + cell_size//2)
            pygame.draw.line(self.screen, self.colors[5], start, end, 4)

    def draw_score(self, solver, window_size, cell_size):
        font = pygame.font.Font(None, 48)
        text = font.render(f"Score: {solver.score()}", True, (0, 0, 0))
        self.screen.blit(text, (5, window_size[1] - cell_size - 80))

    def draw_end_screen(self, message, color, window_size):
        font = pygame.font.Font(None, 72)
        text = font.render(message, True, color)
        y_position = window_size[1] - 120
        x_position = (window_size[0] - text.get_width()) // 2
        self.screen.blit(text, (x_position, y_position))
        pygame.display.flip()
        pygame.time.wait(2000)

    def draw_error_message(self, message, window_size):
        font = pygame.font.Font(None, 48)
        text = font.render(message, True, (255, 0, 0))
        y_position = window_size[1] - 110
        self.screen.blit(text, (5, y_position))
        pygame.display.flip()
        pygame.time.wait(2000)

    def draw_restart_button(self, window_size, pressed):
        font = pygame.font.Font(None, 36)
        text = font.render("Restart", True, (255, 255, 255))
        button_rect = pygame.Rect(window_size[0] - 330, window_size[1] - 70, 100, 40)
        text_rect = text.get_rect(center=button_rect.center)
        color = (30, 30, 30) if pressed else (50, 50, 50)
        pygame.draw.rect(self.screen, color, button_rect)
        self.screen.blit(text, text_rect.topleft)

    def draw_solution_button(self, window_size, pressed):
        font = pygame.font.Font(None, 36)
        text = font.render("Solution", True, (255, 255, 255))
        button_rect = pygame.Rect(window_size[0] - 225, window_size[1] - 70, 110, 40)
        text_rect = text.get_rect(center=button_rect.center)
        color = (0, 150, 0) if pressed else (0, 200, 0)
        pygame.draw.rect(self.screen, color, button_rect)
        self.screen.blit(text, text_rect.topleft)

    def draw_menu_button(self, window_size, pressed):
        font = pygame.font.Font(None, 36)
        text = font.render("Menu", True, (255, 255, 255))
        button_rect = pygame.Rect(window_size[0] - 110, window_size[1] - 70, 100, 40)
        text_rect = text.get_rect(center=button_rect.center)
        color = (30, 30, 30) if pressed else (50, 50, 50)
        pygame.draw.rect(self.screen, color, button_rect)
        self.screen.blit(text, text_rect.topleft)

class GridManager:
    def __init__(self, data_path):
        self.data_path = data_path
        self.grid_files = [f for f in os.listdir(self.data_path) if f.endswith(".in")]

    def load_grid(self, selected_grid):
        return Grid.grid_from_file(os.path.join(self.data_path, selected_grid), read_values=True)

class SolverManager:
    def __init__(self, grid):
        self.solver = Solver(grid)
        self.solver_general = SolverGeneral(grid)
        self.solver_general.run()
        self.general_score = self.solver_general.score()

    def can_pair(self, color1, color2):
        allowed = {
            0: {0, 1, 2, 3},
            1: {0, 1, 2},
            2: {0, 1, 2},
            3: {0, 3}
        }
        return color2 in allowed.get(color1, set()) and color1 in allowed.get(color2, set())

    def pair_is_valid(self, pair, existing_pairs, grid):
        (i1, j1), (i2, j2) = pair
        if grid.is_forbidden(i1, j1) or grid.is_forbidden(i2, j2):
            return False
        if (i1, j1) in [cell for pair in existing_pairs for cell in pair]:
            return False
        if (i2, j2) in [cell for pair in existing_pairs for cell in pair]:
            return False
        if self.can_pair(grid.color[i1][j1], grid.color[i2][j2]):
            return True
        return False

class Game:
    def __init__(self):
        self.colors = {
            0: (255, 255, 255),
            1: (200, 0, 0),
            2: (0, 0, 200),
            3: (0, 200, 0),
            4: (0, 0, 0),
            5: (220, 220, 0)
        }
        self.colors_title = {
            0: (0, 0, 0),
            1: (200, 0, 0),
            2: (0, 0, 200),
            3: (0, 200, 0)
        }
        self.screen = pygame.display.set_mode((600, 600))
        pygame.display.set_caption("ColorGrid")
        self.ui_manager = UIManager(self.screen, self.colors, self.colors_title)
        self.grid_manager = GridManager("./input/")
        self.selected_grid = None
        self.scroll = 0
        self.scroll_bar_dragging = False
        self.mouse_y_offset = 0
        self.selected_cells = []
        self.game_over = False
        self.show_solution = False
        self.pressed_button = None
        self.pressed_grid_index = -1

    def main(self):
        while self.selected_grid is None:
            self.screen.fill((255, 255, 255))
            window_size = (600, 600)
            visible_height = window_size[1] - 170
            total_content_height = len(self.grid_manager.grid_files) * 50
            max_scroll = max(0, total_content_height - visible_height)

            scroll_bar_height = max(20, int((visible_height / total_content_height) * visible_height)) if max_scroll > 0 else visible_height
            scroll_percentage = self.scroll / max_scroll if max_scroll > 0 else 0
            scroll_bar_y = 100 + (scroll_percentage * (visible_height - scroll_bar_height))
            scroll_bar_rect = pygame.Rect(580, int(scroll_bar_y), 20, scroll_bar_height)

            self.ui_manager.draw_grid_options(window_size, self.scroll, scroll_bar_rect, scroll_bar_height, 
                                            self.grid_manager.grid_files, self.pressed_grid_index)
            pygame.draw.rect(self.screen, (255, 255, 255), (0, 0, 600, 100))
            self.ui_manager.draw_title(window_size)
            pygame.display.flip()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    if event.button == 1:
                        x, y = event.pos
                        if scroll_bar_rect.collidepoint(x, y) and max_scroll > 0:
                            self.scroll_bar_dragging = True
                            self.mouse_y_offset = y - scroll_bar_rect.y
                        else:
                            visible_y = y + self.scroll - 100
                            self.pressed_grid_index = visible_y // 50
                elif event.type == pygame.MOUSEBUTTONUP:
                    if event.button == 1 and self.pressed_grid_index != -1:
                        x, y = event.pos
                        visible_y = y + self.scroll - 100
                        released_index = visible_y // 50
                        
                        if 0 <= released_index < len(self.grid_manager.grid_files) and released_index == self.pressed_grid_index:
                            self.ui_manager.draw_grid_options(window_size, self.scroll, scroll_bar_rect, 
                                                            scroll_bar_height, self.grid_manager.grid_files, 
                                                            self.pressed_grid_index)
                            pygame.display.flip()
                            pygame.time.delay(100)
                            self.selected_grid = self.grid_manager.grid_files[self.pressed_grid_index]
                            
                    self.scroll_bar_dragging = False
                    self.pressed_grid_index = -1
                elif event.type == pygame.MOUSEMOTION:
                    if self.scroll_bar_dragging and max_scroll > 0:
                        mouse_y = event.pos[1] - self.mouse_y_offset
                        new_y = max(100, min(mouse_y, 100 + visible_height - scroll_bar_height))
                        self.scroll = ((new_y - 100) / (visible_height - scroll_bar_height)) * max_scroll
                        self.scroll = max(0, min(self.scroll, max_scroll))
                elif event.type == pygame.MOUSEWHEEL:
                    self.scroll -= event.y * 50
                    self.scroll = max(0, min(self.scroll, max_scroll))

        grid = self.grid_manager.load_grid(self.selected_grid)
        solver_manager = SolverManager(grid)
        general_score = solver_manager.general_score

        cell_size = 60
        window_size = (max(600, grid.m * cell_size), grid.n * cell_size + 150)
        self.screen = pygame.display.set_mode(window_size)

        self.selected_cells = []
        self.game_over = False
        self.show_solution = False
        self.pressed_button = None

        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    x, y = event.pos
                    if y >= grid.n * cell_size:
                        restart_rect = pygame.Rect(window_size[0] - 330, window_size[1] - 70, 100, 40)
                        solution_rect = pygame.Rect(window_size[0] - 225, window_size[1] - 70, 110, 40)
                        menu_rect = pygame.Rect(window_size[0] - 110, window_size[1] - 70, 100, 40)
                        
                        if restart_rect.collidepoint(x, y):
                            self.pressed_button = 'restart'
                        elif solution_rect.collidepoint(x, y):
                            self.pressed_button = 'solution'
                        elif menu_rect.collidepoint(x, y):
                            self.pressed_button = 'menu'
                        else:
                            self.pressed_button = None
                    else:
                        self.pressed_button = None
                elif event.type == pygame.MOUSEBUTTONUP:
                    x, y = event.pos
                    if self.pressed_button:
                        button_rect = None
                        if self.pressed_button == 'restart':
                            button_rect = pygame.Rect(window_size[0] - 330, window_size[1] - 70, 100, 40)
                        elif self.pressed_button == 'solution':
                            button_rect = pygame.Rect(window_size[0] - 225, window_size[1] - 70, 110, 40)
                        elif self.pressed_button == 'menu':
                            button_rect = pygame.Rect(window_size[0] - 110, window_size[1] - 70, 100, 40)
                        
                        if button_rect and button_rect.collidepoint(x, y):
                            if self.pressed_button == 'restart':
                                self.ui_manager.draw_restart_button(window_size, True)
                            elif self.pressed_button == 'solution':
                                self.ui_manager.draw_solution_button(window_size, True)
                            elif self.pressed_button == 'menu':
                                self.ui_manager.draw_menu_button(window_size, True)
                            pygame.display.update(button_rect)
                            
                            if self.pressed_button == 'menu':
                                pygame.time.delay(100)
                            
                            if self.pressed_button == 'restart':
                                solver_manager.solver.pairs = []
                                self.selected_cells = []
                                self.game_over = False
                                self.show_solution = False
                            elif self.pressed_button == 'solution':
                                solver_manager.solver.pairs = solver_manager.solver_general.pairs
                                self.show_solution = True
                            elif self.pressed_button == 'menu':
                                self.reset_game_state()
                        
                        self.pressed_button = None

            self.screen.fill((200, 200, 200))
            self.ui_manager.draw_grid(grid, solver_manager.solver, cell_size)
            self.ui_manager.draw_score(solver_manager.solver, window_size, cell_size)
            
            self.ui_manager.draw_restart_button(window_size, self.pressed_button == 'restart')
            self.ui_manager.draw_solution_button(window_size, self.pressed_button == 'solution')
            self.ui_manager.draw_menu_button(window_size, self.pressed_button == 'menu')
            
            pygame.display.flip()

            if not self.show_solution and not any(solver_manager.pair_is_valid(pair, solver_manager.solver.pairs, grid) for pair in grid.all_pairs()):
                if not self.game_over:
                    self.game_over = True
                    if solver_manager.solver.score() <= general_score:
                        self.ui_manager.draw_end_screen("You won!", (0, 200, 0), window_size)
                    else:
                        self.ui_manager.draw_end_screen("You lost!", (200, 0, 0), window_size)
                    solver_manager.solver.pairs = []
                    self.selected_cells = []
                    self.game_over = False

    def reset_game_state(self):
        self.selected_grid = None
        self.scroll = 0
        self.scroll_bar_dragging = False
        self.mouse_y_offset = 0
        self.selected_cells = []
        self.game_over = False
        self.show_solution = False
        self.pressed_button = None
        self.pressed_grid_index = -1
        self.screen = pygame.display.set_mode((600, 600))
        self.main()

if __name__ == "__main__":
    game = Game()
    game.main()