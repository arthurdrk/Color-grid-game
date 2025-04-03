import sys
import os
import pygame

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from color_grid_game import *

pygame.init()

class UIManager:
    """
    Manages the user interface elements and interactions for the game.

    Attributes
    ----------
    screen : pygame.Surface
        The screen surface where the game is rendered.
    colors : dict
        Dictionary mapping color indices to RGB tuples.
    colors_title : dict
        Dictionary mapping title color indices to RGB tuples.
    volume_theme : float
        Volume level for the theme music.
    volume : float
        Volume level for sound effects.
    game_theme : pygame.mixer.Sound
        Sound object for the game theme music.
    win_sound : pygame.mixer.Sound
        Sound object for the win sound effect.
    lose_sound : pygame.mixer.Sound
        Sound object for the lose sound effect.
    sound_on_img : pygame.Surface
        Image surface for the sound on icon.
    sound_off_img : pygame.Surface
        Image surface for the sound off icon.
    color_index : int
        Index for cycling through title colors.
    color_timer : int
        Timer for changing title colors.
    color_interval : int
        Interval for changing title colors.

    Methods
    -------
    draw_volume_button(window_size, pressed)
        Draws the volume button on the screen.
    toggle_volume()
        Toggles the volume between on and off.
    draw_return_button(window_size, pressed)
        Draws the return button on the screen.
    draw_title(window_size)
        Draws the title on the screen with cycling colors.
    draw_grid_options(window_size, scroll, scroll_bar_rect, scroll_bar_height, grid_files, grid_colors, pressed_index)
        Draws the grid options on the screen.
    draw_rule_choice(window_size, pressed_button)
        Draws the rule choice options on the screen.
    darken_color(color, factor=0.7)
        Darkens a color by a given factor.
    draw_grid(grid, solver, cell_size, selected_cells, game_mode, player_pairs, top_margin, new_rules)
        Draws the game grid on the screen.
    darken_pair_cells(pair, grid, cell_size, top_margin)
        Darkens the cells of a pair without drawing the line.
    draw_pair_line(pair, color, cell_size, top_margin)
        Draws the line between the centers of two cells.
    draw_pair_frame(pair, color, cell_size, top_margin)
        Draws a frame around a pair of cells.
    draw_score(solver, window_size, cell_size, player1_score, player2_score, game_mode, player_timers, current_player)
        Draws the score on the screen.
    draw_turn_indicator(current_player, window_size, top_margin, game_mode)
        Draws the turn indicator on the screen.
    draw_end_screen(message, color, window_size)
        Draws the end screen on the screen.
    draw_error_message(message, window_size, mode, cell_size)
        Draws an error message on the screen.
    draw_restart_button(window_size, pressed, mode)
        Draws the restart button on the screen.
    draw_solution_button(window_size, pressed)
        Draws the solution button on the screen.
    draw_menu_button(window_size, pressed)
        Draws the menu button on the screen.
    draw_rules_button(window_size, pressed)
        Draws the rules button on the screen.
    draw_player_choice(window_size, pressed_button)
        Draws the player choice options on the screen.
    draw_rules(window_size, scroll, scroll_bar_rect, scroll_bar_height)
        Draws the rules on the screen.
    """

    def __init__(self, screen, colors, colors_title):
        """
        Initializes the UIManager with screen and color settings.

        Parameters
        ----------
        screen : pygame.Surface
            The screen surface where the game is rendered.
        colors : dict
            Dictionary mapping color indices to RGB tuples.
        colors_title : dict
            Dictionary mapping title color indices to RGB tuples.
        """
        self.screen = screen
        self.colors = colors
        self.colors_title = colors_title
        self.volume_theme = 0.005
        self.volume = 0.02

        self.game_theme = pygame.mixer.Sound("./medias/game theme.mp3")
        self.win_sound = pygame.mixer.Sound("./medias/win.mp3")
        self.lose_sound = pygame.mixer.Sound("./medias/lose.mp3")
        self.sound_on_img = pygame.transform.scale(
            pygame.image.load("./medias/sound on.png").convert_alpha(),
            (30, 30)
        )
        self.sound_off_img = pygame.transform.scale(
            pygame.image.load("./medias/sound off.png").convert_alpha(),
            (30, 30)
        )

        self.game_theme.set_volume(self.volume_theme)
        self.win_sound.set_volume(self.volume)
        self.lose_sound.set_volume(self.volume)
        self.game_theme.play(loops=-1)

        self.color_index = 0
        self.color_timer = 0
        self.color_interval = 500

    def draw_volume_button(self, window_size, pressed):
        """
        Draws the volume button on the screen.

        Parameters
        ----------
        window_size : tuple
            The size of the window (width, height).
        pressed : bool
            Whether the button is pressed.
        """
        button_rect = pygame.Rect(window_size[0] - 95, window_size[1] - 70, 50, 40)
        color = (30, 30, 30) if pressed else (50, 50, 50)
        pygame.draw.rect(self.screen, color, button_rect)

        img = self.sound_off_img if self.volume == 0 else self.sound_on_img
        img_rect = img.get_rect(center=button_rect.center)
        self.screen.blit(img, img_rect)

    def toggle_volume(self):
        """
        Toggles the volume between on and off.
        """
        if self.volume == 0:
            self.volume = 0.02
            self.volume_theme = 0.005
            self.game_theme.set_volume(self.volume_theme)
            self.win_sound.set_volume(self.volume)
            self.lose_sound.set_volume(self.volume)
        else:
            self.volume = 0
            self.game_theme.set_volume(self.volume)
            self.win_sound.set_volume(self.volume)
            self.lose_sound.set_volume(self.volume)

    def draw_return_button(self, window_size, pressed):
        """
        Draws the return button on the screen.

        Parameters
        ----------
        window_size : tuple
            The size of the window (width, height).
        pressed : bool
            Whether the button is pressed.
        """
        font = pygame.font.Font(None, 36)
        text = font.render("Return", True, (255, 255, 255))
        button_rect = pygame.Rect(50, window_size[1] - 70, 100, 40)
        text_rect = text.get_rect(center=button_rect.center)
        color = (30, 30, 30) if pressed else (50, 50, 50)
        pygame.draw.rect(self.screen, color, button_rect)
        self.screen.blit(text, text_rect.topleft)

    def draw_title(self, window_size):
        """
        Draws the title on the screen with cycling colors.

        Parameters
        ----------
        window_size : tuple
            The size of the window (width, height).
        """
        font = pygame.font.Font(None, 72)
        title = "ColorGrid"

        current_time = pygame.time.get_ticks()
        if current_time - self.color_timer > self.color_interval:
            self.color_index = (self.color_index + 1) % len(self.colors_title)
            self.color_timer = current_time

        colors = [self.colors_title[(self.color_index + i) % len(self.colors_title)] for i in range(len(title))]

        total_width = sum(font.size(char)[0] for char in title)
        start_x = (window_size[0] - total_width) // 2

        current_x = start_x
        for i, char in enumerate(title):
            text = font.render(char, True, colors[i])
            self.screen.blit(text, (current_x, 20))
            current_x += text.get_width()

    def draw_grid_options(self, window_size, scroll, scroll_bar_rect, scroll_bar_height, grid_files, grid_colors, pressed_index):
        """
        Draws the grid options on the screen.

        Parameters
        ----------
        window_size : tuple
            The size of the window (width, height).
        scroll : int
            The current scroll position.
        scroll_bar_rect : pygame.Rect
            The rectangle for the scroll bar.
        scroll_bar_height : int
            The height of the scroll bar.
        grid_files : list
            List of grid files.
        grid_colors : list
            List of colors for the grid files.
        pressed_index : int
            The index of the pressed grid option.
        """
        font = pygame.font.Font(None, 36)
        y_offset = 100
        max_scroll = max(0, len(grid_files) * 50 - (window_size[1] - 170))
        scroll = max(0, min(scroll, max_scroll))

        pygame.draw.rect(self.screen, (255, 255, 255), (50, 100, window_size[0] - 120, window_size[1] - 170))

        for i, (filename, _) in enumerate(grid_files):
            if y_offset + 50 - scroll > window_size[1] - 70:
                break

            btn_color = self.darken_color(grid_colors[i]) if i == pressed_index else grid_colors[i]
            brightness = (btn_color[0] * 299 + btn_color[1] * 587 + btn_color[2] * 114) // 1000
            text_color = (0, 0, 0) if brightness > 128 else (255, 255, 255)

            formatted_name = f"Grid {filename[4:-3]}" if filename.startswith("grid") and filename.endswith(".in") else filename

            btn_rect = pygame.Rect(window_size[0] // 2 - 100, y_offset - scroll, 200, 40)
            pygame.draw.rect(self.screen, btn_color, btn_rect)
            text_surface = font.render(formatted_name, True, text_color)
            text_rect = text_surface.get_rect(center=btn_rect.center)
            self.screen.blit(text_surface, text_rect)
            y_offset += 50

        pygame.draw.rect(self.screen, (150, 150, 150), scroll_bar_rect.inflate(0, scroll_bar_height - scroll_bar_rect.height))

    def draw_rule_choice(self, window_size, pressed_button):
        """
        Draws the rule choice options on the screen.

        Parameters
        ----------
        window_size : tuple
            The size of the window (width, height).
        pressed_button : str
            The currently pressed button ('classic' or 'new').
        """
        font = pygame.font.Font(None, 50)

        classic_rect = pygame.Rect(window_size[0] // 2 - 140, 200, 300, 60)
        color_choice = (30, 30, 30) if pressed_button == 'classic' else (50, 50, 50)
        pygame.draw.rect(self.screen, color_choice, classic_rect)
        text = font.render("Classic Rules", True, (255, 255, 255))
        text_rect = text.get_rect(center=classic_rect.center)
        self.screen.blit(text, text_rect)

        new_rect = pygame.Rect(window_size[0] // 2 - 140, 300, 300, 60)
        color_choice = (30, 30, 30) if pressed_button == 'new' else (50, 50, 50)
        pygame.draw.rect(self.screen, color_choice, new_rect)
        text = font.render("No Adjacency", True, (255, 255, 255))
        text_rect = text.get_rect(center=new_rect.center)
        self.screen.blit(text, text_rect)

        current_time = pygame.time.get_ticks()
        if current_time - self.color_timer > self.color_interval:
            self.color_index = (self.color_index + 1) % len(self.colors_title)
            self.color_timer = current_time

        title_font = pygame.font.Font(None, 72)
        title = "Rules Choice"
        title_colors = [self.colors_title[(self.color_index + i) % len(self.colors_title)] for i in range(len(title))]
        total_width = sum(title_font.size(char)[0] for char in title)
        start_x = (window_size[0] - total_width) // 2
        current_x = start_x
        for i, char in enumerate(title):
            text = title_font.render(char, True, title_colors[i])
            self.screen.blit(text, (current_x, 20))
            current_x += text.get_width()

    def darken_color(self, color, factor=0.7):
        """
        Darkens a color by a given factor.

        Parameters
        ----------
        color : tuple
            The RGB color to darken.
        factor : float, optional
            The factor by which to darken the color.

        Returns
        -------
        tuple
            The darkened RGB color.
        """
        return (int(color[0] * factor), int(color[1] * factor), int(color[2] * factor))

    def draw_grid(self, grid, solver, cell_size, selected_cells, game_mode, player_pairs, top_margin, new_rules):
        """
        Draws the game grid on the screen.

        Parameters
        ----------
        grid : Grid
            The game grid.
        solver : Solver
            The solver for the game.
        cell_size : int
            The size of each cell.
        selected_cells : list
            List of selected cells.
        game_mode : str
            The game mode ('one', 'two', or 'bot').
        player_pairs : list
            List of player pairs.
        top_margin : int
            The top margin for the grid.
        new_rules : bool
            Whether the new rules are being used.
        """
        for i in range(grid.n):
            for j in range(grid.m):
                color = self.colors[grid.color[i][j]]
                if (i, j) in selected_cells:
                    color = self.darken_color(color)
                pygame.draw.rect(self.screen, color, (j * cell_size, i * cell_size + top_margin, cell_size, cell_size))
                pygame.draw.rect(self.screen, (0, 0, 0), (j * cell_size, i * cell_size + top_margin, cell_size, cell_size), 1)
                font = pygame.font.Font(None, 36)
                text = font.render(str(grid.value[i][j]), True, (0, 0, 0))
                self.screen.blit(text, (j * cell_size + cell_size//2 - text.get_width()//2, i * cell_size + top_margin + cell_size//2 - text.get_height()//2))
        if new_rules:
            if game_mode == 'one':
                for pair in solver.pairs:
                    self.darken_pair_cells(pair, grid, cell_size, top_margin)
            else:
                for pair in player_pairs[0]:
                    self.darken_pair_cells(pair, grid, cell_size, top_margin)
                for pair in player_pairs[1]:
                    self.darken_pair_cells(pair, grid, cell_size, top_margin)
        if new_rules:
            if game_mode == 'one':
                for pair in solver.pairs:
                    self.draw_pair_line(pair, self.colors[5], cell_size, top_margin)
            else:
                for pair in player_pairs[0]:
                    self.draw_pair_line(pair, self.colors[5], cell_size, top_margin)
                for pair in player_pairs[1]:
                    self.draw_pair_line(pair, (148, 0, 211), cell_size, top_margin)

        else:
            if game_mode == 'one':
                for pair in solver.pairs:
                    self.darken_pair_cells(pair, grid, cell_size, top_margin)
                    self.draw_pair_frame(pair, self.colors[5], cell_size, top_margin)
            else:
                if player_pairs:
                    for pair in player_pairs[0]:
                        self.darken_pair_cells(pair, grid, cell_size, top_margin)
                        self.draw_pair_frame(pair, self.colors[5], cell_size, top_margin)
                    for pair in player_pairs[1]:
                        self.darken_pair_cells(pair, grid, cell_size, top_margin)
                        self.draw_pair_frame(pair, (148, 0, 211), cell_size, top_margin)

    def darken_pair_cells(self, pair, grid, cell_size, top_margin):
        """
        Darkens the cells of a pair without drawing the line.

        Parameters
        ----------
        pair : tuple
            The pair of cells to darken.
        grid : Grid
            The game grid.
        cell_size : int
            The size of each cell.
        top_margin : int
            The top margin for the grid.
        """
        (i1, j1), (i2, j2) = pair

        # Original colors
        original_color1 = self.colors[grid.color[i1][j1]]
        original_color2 = self.colors[grid.color[i2][j2]]

        # Darkened colors
        darkened_color1 = (
            int(original_color1[0] * 0.3),
            int(original_color1[1] * 0.3),
            int(original_color1[2] * 0.3)
        )
        darkened_color2 = (
            int(original_color2[0] * 0.3),
            int(original_color2[1] * 0.3),
            int(original_color2[2] * 0.3)
        )

        # Draw darkened cells
        pygame.draw.rect(self.screen, darkened_color1, (j1 * cell_size, i1 * cell_size + top_margin, cell_size, cell_size))
        pygame.draw.rect(self.screen, darkened_color2, (j2 * cell_size, i2 * cell_size + top_margin, cell_size, cell_size))

        # Cell borders
        pygame.draw.rect(self.screen, (0, 0, 0), (j1 * cell_size, i1 * cell_size + top_margin, cell_size, cell_size), 1)
        pygame.draw.rect(self.screen, (0, 0, 0), (j2 * cell_size, i2 * cell_size + top_margin, cell_size, cell_size), 1)

        # Display values
        font = pygame.font.Font(None, 36)
        text1 = font.render(str(grid.value[i1][j1]), True, (0, 0, 0))
        text2 = font.render(str(grid.value[i2][j2]), True, (0, 0, 0))
        self.screen.blit(text1, (j1 * cell_size + cell_size//2 - text1.get_width()//2, i1 * cell_size + top_margin + cell_size//2 - text1.get_height()//2))
        self.screen.blit(text2, (j2 * cell_size + cell_size//2 - text2.get_width()//2, i2 * cell_size + top_margin + cell_size//2 - text2.get_height()//2))

    def draw_pair_line(self, pair, color, cell_size, top_margin):
        """
        Draws the line between the centers of two cells.

        Parameters
        ----------
        pair : tuple
            The pair of cells to connect.
        color : tuple
            The color of the line.
        cell_size : int
            The size of each cell.
        top_margin : int
            The top margin for the grid.
        """
        (i1, j1), (i2, j2) = pair
        center1 = (j1 * cell_size + cell_size//2, i1 * cell_size + top_margin + cell_size//2)
        center2 = (j2 * cell_size + cell_size//2, i2 * cell_size + top_margin + cell_size//2)
        pygame.draw.line(self.screen, color, center1, center2, 4)

    def draw_pair_frame(self, pair, color, cell_size, top_margin):
        """
        Draws a frame around a pair of cells.

        Parameters
        ----------
        pair : tuple
            The pair of cells to frame.
        color : tuple
            The color to use for the frame.
        cell_size : int
            The size of each cell.
        top_margin : int
            The top margin for the grid.
        """
        (i1, j1), (i2, j2) = pair
        min_i = min(i1, i2)
        max_i = max(i1, i2)
        min_j = min(j1, j2)
        max_j = max(j1, j2)

        frame_inset = 4
        frame_x = min_j * cell_size + frame_inset
        frame_y = min_i * cell_size + top_margin + frame_inset
        frame_width = (max_j - min_j + 1) * cell_size - 2 * frame_inset
        frame_height = (max_i - min_i + 1) * cell_size - 2 * frame_inset

        pygame.draw.rect(self.screen, color, (frame_x, frame_y, frame_width, frame_height), 4)

    def draw_score(self, solver, window_size, cell_size, player1_score, player2_score, game_mode, player_timers, current_player, player1_bot_type, player2_bot_type):
        """
        Draws the score on the screen.

        Parameters
        ----------
        solver : Solver
            The solver for the game.
        window_size : tuple
            The size of the window (width, height).
        cell_size : int
            The size of each cell.
        player1_score : int
            The score of player 1.
        player2_score : int
            The score of player 2.
        game_mode : str
            The game mode ('one', 'two', or 'bot').
        player_timers : list
            List of player timers.
        current_player : int
            The current player (1 or 2).
        """
        font = pygame.font.Font(None, 38)

        def format_time(seconds):
            if seconds < 0:
                seconds = 0
            minutes = int(seconds // 60)
            seconds_part = int(seconds % 60)
            return f"{minutes:02}:{seconds_part:02}"

        if game_mode == 'one':
            time_str = format_time(player_timers[0])
            text = font.render(f"Score: {solver.score()} | Timer: {time_str}", True, (0, 0, 0))
            self.screen.blit(text, (5, window_size[1] - cell_size - 45))
        else:
            time1 = format_time(player_timers[0])
            time2 = format_time(player_timers[1])

            # Déterminer les noms des joueurs selon le mode de jeu
            if game_mode == 'botvs':
                bot_name1 = "Deep Blue" if player1_bot_type == 'mcts' else "Stockfish"
                bot_name2 = "Stockfish" if player2_bot_type == 'minimax' else "Deep Blue"
            else:
                bot_name1 = "Player 1"
                bot_name2 = "Player 2" if game_mode == 'two' else "Stockfish" if game_mode == 'bot' else "Deep Blue"

            # Afficher le score du premier joueur/bot
            color = self.darken_color(self.colors[5]) if current_player != 1 else self.colors[5]
            text = font.render(f"{bot_name1}: {player1_score} | Timer: {time1}", True, color)
            self.screen.blit(text, (5, window_size[1] - cell_size - 45))

            # Afficher le score du second joueur/bot
            color = self.darken_color((148, 0, 211)) if current_player != 2 else (148, 0, 211)
            text = font.render(f"{bot_name2}: {player2_score} | Timer: {time2}", True, color)
            self.screen.blit(text, (5, window_size[1] - cell_size - 15))

    def draw_turn_indicator(self, current_player, window_size, top_margin, game_mode, player1_bot_type, player2_bot_type):
        """
        Draws the turn indicator on the screen.

        Parameters
        ----------
        current_player : int
            The current player (1 or 2).
        window_size : tuple
            The size of the window (width, height).
        top_margin : int
            The top margin for the grid.
        game_mode : str
            The game mode ('one', 'two', or 'bot').
        """
        font = pygame.font.Font(None, 46)
        if game_mode == 'two':
            color = self.colors[5] if current_player == 1 else (148, 0, 211)
            text = font.render(f"Player {current_player} to play", True, color)
        elif game_mode == 'bot':
            color = self.colors[5] if current_player == 1 else (148, 0, 211)
            text = font.render("Player to play" if current_player == 1 else "Stockfish to play", True, color)
        elif game_mode == 'deepblue':
            color = self.colors[5] if current_player == 1 else (148, 0, 211)
            text = font.render("Player to play" if current_player == 1 else "DeepBlueto play", True, color)
        elif game_mode == 'botvs':
            bot_name1 = "Deep Blue" if player1_bot_type == 'mcts' else "Stockfish"
            bot_name2 = "Stockfish" if player2_bot_type == 'minimax' else "Deep Blue"
            color = self.colors[5] if current_player == 1 else (148, 0, 211)
            text = font.render(f"{bot_name1 if current_player == 1 else bot_name2} to play", True, color)
        else:  # one
            text = font.render("Your turn", True, self.colors[5])
        x_position = (window_size[0] - text.get_width()) // 2
        self.screen.blit(text, (x_position, top_margin // 2 - 20))

    def draw_end_screen(self, message, color, window_size):
        """
        Draws the end screen on the screen.

        Parameters
        ----------
        message : str
            The message to display.
        color : tuple
            The color to use for the message.
        window_size : tuple
            The size of the window (width, height).
        """
        pygame.time.delay(200)
        overlay = pygame.Surface(window_size, pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 190))
        self.screen.blit(overlay, (0, 0))

        font = pygame.font.Font(None, 72)
        text = font.render(message, True, color)
        text_rect = text.get_rect(center=(window_size[0] // 2, window_size[1] // 2))

        border_surface = pygame.Surface((text_rect.width + 4, text_rect.height + 4), pygame.SRCALPHA)
        self.screen.blit(border_surface, (text_rect.x - 2, text_rect.y - 2))

        self.screen.blit(text, text_rect)
        pygame.display.flip()
        pygame.time.wait(4000)

    def draw_error_message(self, message, window_size, mode, cell_size):
        """
        Draws an error message on the screen.

        Parameters
        ----------
        message : str
            The error message to display.
        window_size : tuple
            The size of the window (width, height).
        mode : str
            The game mode ('one', 'two', or 'bot').
        cell_size : int
            The size of each cell.
        """
        font = pygame.font.Font(None, 38)
        text = font.render(message, True, (200, 0, 0))
        y_position = window_size[1] - cell_size - 15 if mode == "one" else window_size[1] - cell_size + 15
        self.screen.blit(text, (5, y_position))
        pygame.display.flip()
        pygame.time.wait(700)

    def draw_restart_button(self, window_size, pressed, mode):
        """
        Draws the restart button on the screen.

        Parameters
        ----------
        window_size : tuple
            The size of the window (width, height).
        pressed : bool
            Whether the button is pressed.
        mode : str
            The game mode ('one', 'two', or 'bot').
        """
        font = pygame.font.Font(None, 36)
        text = font.render("Restart", True, (255, 255, 255))
        button_rect = pygame.Rect(window_size[0] - 330, window_size[1] - 70, 100, 40) if mode == "one" else pygame.Rect(window_size[0] - 220, window_size[1] - 70, 100, 40)
        text_rect = text.get_rect(center=button_rect.center)
        color = (30, 30, 30) if pressed else (50, 50, 50)
        pygame.draw.rect(self.screen, color, button_rect)
        self.screen.blit(text, text_rect.topleft)

    def draw_solution_button(self, window_size, pressed):
        """
        Draws the solution button on the screen.

        Parameters
        ----------
        window_size : tuple
            The size of the window (width, height).
        pressed : bool
            Whether the button is pressed.
        """
        font = pygame.font.Font(None, 36)
        text = font.render("Solution", True, (255, 255, 255))
        button_rect = pygame.Rect(window_size[0] - 225, window_size[1] - 70, 110, 40)
        text_rect = text.get_rect(center=button_rect.center)
        color = (0, 150, 0) if pressed else (0, 200, 0)
        pygame.draw.rect(self.screen, color, button_rect)
        self.screen.blit(text, text_rect.topleft)

    def draw_menu_button(self, window_size, pressed):
        """
        Draws the menu button on the screen.

        Parameters
        ----------
        window_size : tuple
            The size of the window (width, height).
        pressed : bool
            Whether the button is pressed.
        """
        font = pygame.font.Font(None, 36)
        text = font.render("Menu", True, (255, 255, 255))
        button_rect = pygame.Rect(window_size[0] - 110, window_size[1] - 70, 100, 40)
        text_rect = text.get_rect(center=button_rect.center)
        color = (30, 30, 30) if pressed else (50, 50, 50)
        pygame.draw.rect(self.screen, color, button_rect)
        self.screen.blit(text, text_rect.topleft)

    def draw_rules_button(self, window_size, pressed):
        """
        Draws the rules button on the screen.

        Parameters
        ----------
        window_size : tuple
            The size of the window (width, height).
        pressed : bool
            Whether the button is pressed.
        """
        font = pygame.font.Font(None, 36)
        text = font.render("Rules", True, (255, 255, 255))
        button_rect = pygame.Rect(window_size[0] - 200, window_size[1] - 70, 100, 40)
        text_rect = text.get_rect(center=button_rect.center)
        color = (30, 30, 30) if pressed else (50, 50, 50)
        pygame.draw.rect(self.screen, color, button_rect)
        self.screen.blit(text, text_rect.topleft)

    def draw_player_choice(self, window_size, pressed_button):
        """
        Draws the player choice options on the screen.

        Parameters
        ----------
        window_size : tuple
            The size of the window (width, height).
        pressed_button : str
            The currently pressed button.
        """
        font = pygame.font.Font(None, 50)

        # Bouton "One Player"
        one_rect = pygame.Rect(window_size[0] // 2 - 185, 150, 390, 60)
        color_choice = (30, 30, 30) if pressed_button == 'one' else (50, 50, 50)
        pygame.draw.rect(self.screen, color_choice, one_rect)
        text = font.render("One Player", True, (255, 255, 255))
        text_rect = text.get_rect(center=one_rect.center)
        self.screen.blit(text, text_rect)

        # Bouton "Two Players"
        two_rect = pygame.Rect(window_size[0] // 2 - 185, 225, 390, 60)
        color_choice = (30, 30, 30) if pressed_button == 'two' else (50, 50, 50)
        pygame.draw.rect(self.screen, color_choice, two_rect)
        text = font.render("Two Players", True, (255, 255, 255))
        text_rect = text.get_rect(center=two_rect.center)
        self.screen.blit(text, text_rect)

        # Bouton "Versus Stockfish"
        bot_rect = pygame.Rect(window_size[0] // 2 - 185, 300, 390, 60)
        color_choice = (30, 30, 30) if pressed_button == 'bot' else (50, 50, 50)
        pygame.draw.rect(self.screen, color_choice, bot_rect)
        text = font.render("Versus Stockfish", True, (255, 255, 255))
        text_rect = text.get_rect(center=bot_rect.center)
        self.screen.blit(text, text_rect)

        # Bouton "VS Deep Blue"
        deepblue_rect = pygame.Rect(window_size[0] // 2 - 185, 375, 390, 60)
        color_choice = (30, 30, 30) if pressed_button == 'deepblue' else (50, 50, 50)
        pygame.draw.rect(self.screen, color_choice, deepblue_rect)
        text = font.render("Versus DeepBlue", True, (255, 255, 255))
        text_rect = text.get_rect(center=deepblue_rect.center)
        self.screen.blit(text, text_rect)

        # Bouton "Stockfish VS DeepBlue"
        botvs_rect = pygame.Rect(window_size[0] // 2 - 185, 450, 390, 60)  # Taille ajustée pour centrer
        color_choice = (30, 30, 30) if pressed_button == 'botvs' else (50, 50, 50)
        pygame.draw.rect(self.screen, color_choice, botvs_rect)
        text = font.render("Stockfish VS DeepBlue", True, (255, 255, 255))
        text_rect = text.get_rect(center=botvs_rect.center)
        self.screen.blit(text, text_rect)



    def draw_rules(self, window_size, scroll, scroll_bar_rect, scroll_bar_height):
        """
        Draws the rules on the screen.

        Parameters
        ----------
        window_size : tuple
            The size of the window (width, height).
        scroll : int
            The current scroll position.
        scroll_bar_rect : pygame.Rect
            The rectangle for the scroll bar.
        scroll_bar_height : int
            The height of the scroll bar.
        """
        font = pygame.font.Font(None, 72)
        font_title = pygame.font.Font(None, 72)
        font_content = pygame.font.Font(None, 24)
        rules = [
            "Consider a grid of size n × m where n ≥ 1 and m ≥ 2 are integers representing the number",
            "of rows and columns respectively. Cells have coordinates (i,j) where:",
            "i in {0,...,n−1} (row index), j in {0,...,m−1} (column index).",
            "",
            "Each cell has 2 attributes:",
            "   — Color c(i,j) in {0 (white), 1 (red), 2 (blue), 3 (green), 4 (black)}",
            "   — Value v(i,j) in N* (positive integer)",
            "",
            "Pairing rules:",
            "   1. Adjacent cells only (horizontal/vertical)",
            "   2. Color constraints:",
            "       - Black (4) cannot be paired",
            "       - White (0) pairs with any except black",
            "       - Blue (2)/Red (1) pair with white/blue/red",
            "       - Green (3) pairs only with white/green",
            "   3. Each cell can only be in one pair",
            "",
            "Score calculation:",
            "   Score = ∑|v(i1,j1) − v(i2,j2)| for all pairs + ∑v for unpaired cells",
            "",
            "Objective: Find pairing with minimal score"
        ]

        self.screen.fill((255, 255, 255))

        title = "Game Rules"
        title_colors = [
            (0, 0, 0), (200, 0, 0), (0, 0, 200), (0, 200, 0), (0, 0, 0),
            (200, 0, 0), (0, 0, 200), (0, 200, 0), (200, 0, 0), (0, 0, 200)
        ]

        current_time = pygame.time.get_ticks()
        if current_time - self.color_timer > self.color_interval:
            self.color_index = (self.color_index + 1) % len(title_colors)
            self.color_timer = current_time

        colors = [title_colors[(self.color_index + i) % len(title_colors)] for i in range(len(title))]

        total_width = sum(font_title.size(char)[0] for char in title)
        start_x = (window_size[0] - total_width) // 2

        current_x = start_x
        for i, char in enumerate(title):
            text = font_title.render(char, True, colors[i])
            self.screen.blit(text, (current_x, 20))
            current_x += text.get_width()

        content_clip_top = 92
        content_clip_bottom = window_size[1] - 70
        content_clip_rect = pygame.Rect(0, content_clip_top, window_size[0], content_clip_bottom - content_clip_top)
        self.screen.set_clip(content_clip_rect)
        y_offset = 92

        for line in rules:
            formatted_line = ''.join(line)
            text_color = (200, 0, 0) if line.startswith("Objective:") else (0, 0, 0)
            text_surface = font_content.render(formatted_line, True, text_color)
            current_y = y_offset - scroll
            self.screen.blit(text_surface, (20, current_y))
            y_offset += 30

        self.screen.set_clip(None)
        pygame.draw.rect(self.screen, (150, 150, 150), scroll_bar_rect)
        self.draw_menu_button(window_size, False)
        pygame.display.flip()

class GridManager:
    """
    Manages the grid files and their difficulties.

    Attributes
    ----------
    data_path : str
        The path to the directory containing the grid files.
    grid_files : list
        List of grid files.
    difficulties : list
        List of difficulties for the grid files.
    min_d : int
        The minimum difficulty.
    max_d : int
        The maximum difficulty.
    range_d : int
        The range of difficulties.
    grid_colors : list
        List of colors for the grid files.
    """

    def __init__(self, data_path):
        """
        Initializes the GridManager with the data path.

        Parameters
        ----------
        data_path : str
            The path to the directory containing the grid files.
        """
        self.data_path = data_path
        self.grid_files = []
        self.difficulties = []
        self.grid_colors = []

        for f in os.listdir(data_path):
            if f.endswith(".in"):
                difficulty = self.extract_difficulty(f)
                self.grid_files.append((f, difficulty))
                self.difficulties.append(difficulty)

        self.min_d = min(self.difficulties) if self.difficulties else 0
        self.max_d = max(self.difficulties) if self.difficulties else 1
        self.range_d = self.max_d - self.min_d if self.max_d != self.min_d else 1
        self.grid_colors = [self.get_difficulty_color(d) for d in self.difficulties]

    def extract_difficulty(self, filename):
        """
        Extracts the difficulty from the filename.

        Parameters
        ----------
        filename : str
            The filename to extract the difficulty from.

        Returns
        -------
        int
            The extracted difficulty.
        """
        base = filename[4:-3]
        parts = base.split('_')
        try:
            return int(parts[-1])
        except (IndexError, ValueError):
            return 0

    def get_difficulty_color(self, difficulty):
        """
        Gets the color for a given difficulty.

        Parameters
        ----------
        difficulty : int
            The difficulty to get the color for.

        Returns
        -------
        tuple
            The RGB color for the difficulty.
        """
        normalized = (difficulty - self.min_d) / self.range_d if self.range_d != 0 else 0.5
        normalized = max(0.0, min(normalized, 1.0))

        stops = [
            (0.0, (255, 255, 255)),
            (0.2, (0, 200, 0)),
            (0.4, (220, 220, 0)),
            (0.6, (255, 165, 0)),
            (0.8, (200, 0, 0)),
            (1.0, (0, 0, 0))
        ]

        for i in range(len(stops) - 1):
            start_pos, start_color = stops[i]
            end_pos, end_color = stops[i + 1]
            if start_pos <= normalized <= end_pos:
                t = (normalized - start_pos) / (end_pos - start_pos)
                return (
                    int(start_color[0] + t * (end_color[0] - start_color[0])),
                    int(start_color[1] + t * (end_color[1] - start_color[1])),
                    int(start_color[2] + t * (end_color[2] - start_color[2]))
                )
        return stops[-1][1]

    def load_grid(self, selected_grid):
        """
        Loads a grid from a file.

        Parameters
        ----------
        selected_grid : str
            The filename of the grid to load.

        Returns
        -------
        Grid
            The loaded grid.
        """
        return Grid.grid_from_file(os.path.join(self.data_path, selected_grid), read_values=True)

class SolverManager:
    """
    Manages the solver for the game.

    Attributes
    ----------
    solver : Solver
        The solver for the game.
    solver_general : Solver_Hungarian or Solver_Blossom
        The general solver for the game.
    general_score : int
        The score of the general solver.
    """

    def __init__(self, grid, rules):
        """
        Initializes the SolverManager with the grid and rules.

        Parameters
        ----------
        grid : Grid
            The game grid.
        rules : str
            The rules to use for the solver.
        """
        self.solver = Solver(grid)
        if rules == "original rules":
            self.solver_general = Solver_Hungarian(grid, rules)
        elif rules == "new rules":
            self.solver_general = Solver_Blossom(grid, rules)
        else:
            raise ValueError("Unknown rules specified")

        self.solver_general.run()
        self.general_score = self.solver_general.score()

    def can_pair(self, color1, color2):
        """
        Checks if two colors can be paired.

        Parameters
        ----------
        color1 : int
            The first color.
        color2 : int
            The second color.

        Returns
        -------
        bool
            Whether the colors can be paired.
        """
        allowed = {
            0: {0, 1, 2, 3},
            1: {0, 1, 2},
            2: {0, 1, 2},
            3: {0, 3}
        }
        return color2 in allowed.get(color1, set()) and color1 in allowed.get(color2, set())

    def pair_is_valid(self, pair, existing_pairs, grid, player_pairs, rules):
        """
        Checks if a pair is valid.

        Parameters
        ----------
        pair : tuple
            The pair to check.
        existing_pairs : list
            List of existing pairs.
        grid : Grid
            The game grid.
        player_pairs : list
            List of player pairs.
        rules : str
            The rules to use for the solver.

        Returns
        -------
        bool
            Whether the pair is valid.
        """
        (i1, j1), (i2, j2) = pair
        if grid.is_forbidden(i1, j1) or grid.is_forbidden(i2, j2):
            return False
        if (i1, j1) == (i2, j2):
            return False
        if (i1, j1) in [cell for pair in existing_pairs for cell in pair]:
            return False
        if (i2, j2) in [cell for pair in existing_pairs for cell in pair]:
            return False
        if (i1, j1) in [cell for pair in player_pairs[0] for cell in pair] or (i2, j2) in [cell for pair in player_pairs[0] for cell in pair]:
            return False
        if (i1, j1) in [cell for pair in player_pairs[1] for cell in pair] or (i2, j2) in [cell for pair in player_pairs[1] for cell in pair]:
            return False

        if rules == "original rules":
            if self.can_pair(grid.color[i1][j1], grid.color[i2][j2]):
                return True
        elif rules == "new rules":
            if grid.color[i1][j1] == 0 or grid.color[i2][j2] == 0:
                return True
            elif self.can_pair(grid.color[i1][j1], grid.color[i2][j2]):
                return True

        return False

    def calculate_player_score(self, player_pairs, grid):
        """
        Calculates the score for a player.

        Parameters
        ----------
        player_pairs : list
            List of player pairs.
        grid : Grid
            The game grid.

        Returns
        -------
        int
            The calculated score.
        """
        paired_cells = set(cell for pair in player_pairs for cell in pair)
        score = sum(abs(grid.value[i1][j1] - grid.value[i2][j2]) for (i1, j1), (i2, j2) in player_pairs)
        score += sum(grid.value[i][j] for i in range(grid.n) for j in range(grid.m) if (i, j) not in paired_cells and grid.color[i][j] != 4)
        return score

    def calculate_two_player_score(self, player_pairs, grid):
        """
        Calculates the score for two players.

        Parameters
        ----------
        player_pairs : list
            List of player pairs.
        grid : Grid
            The game grid.

        Returns
        -------
        int
            The calculated score.
        """
        score = sum(grid.cost((u,v)) for u, v in player_pairs)
        return score

class Game:
    """
    Manages the game state and flow.

    Attributes
    ----------
    colors : dict
        Dictionary mapping color indices to RGB tuples.
    colors_title : dict
        Dictionary mapping title color indices to RGB tuples.
    screen : pygame.Surface
        The screen surface where the game is rendered.
    ui_manager : UIManager
        The UI manager for the game.
    grid_manager : GridManager
        The grid manager for the game.
    selected_grid : str
        The selected grid filename.
    scroll : int
        The current scroll position.
    scroll_bar_dragging : bool
        Whether the scroll bar is being dragged.
    mouse_y_offset : int
        The mouse y offset for scrolling.
    selected_cells : list
        List of selected cells.
    game_over : bool
        Whether the game is over.
    show_solution : bool
        Whether to show the solution.
    pressed_button : str
        The currently pressed button.
    pressed_grid_index : int
        The index of the pressed grid option.
    rules_scroll : int
        The current scroll position for the rules.
    rules_scroll_bar_dragging : bool
        Whether the rules scroll bar is being dragged.
    rules_mouse_y_offset : int
        The mouse y offset for rules scrolling.
    player_mode : str
        The game mode ('one', 'two', or 'bot').
    current_player : int
        The current player (1 or 2).
    player_pairs : list
        List of player pairs.
    player_scores : list
        List of player scores.
    volume_button_pressed_time : int
        The time the volume button was pressed.
    player_initial_times : list
        List of initial times for the players.
    player_time_used : list
        List of time used by the players.
    start_times : list
        List of start times for the players.
    player_timers : list
        List of player timers.
    timer_paused : bool
        Whether the timer is paused.
    """

    def __init__(self):
        """
        Initializes the Game with default settings.
        """
        self.colors = {
            0: (255, 255, 255),
            1: (199, 14, 14),
            2: (21, 143, 225),
            3: (80, 193, 45),
            4: (0, 0, 0),
            5: (255, 145, 0),
            6: (148, 0, 211)  # Color for DeepBlue
        }
        self.colors_title = {
            0: (0, 0, 0),
            1: (200, 0, 0),
            2: (0, 0, 200),
            3: (0, 200, 0)
        }
        self.screen = pygame.display.set_mode((600, 600), pygame.RESIZABLE)
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
        self.rules_scroll = 0
        self.rules_scroll_bar_dragging = False
        self.rules_mouse_y_offset = 0
        self.player_mode = None
        self.current_player = 1
        self.player_pairs = [[], []]
        self.player_scores = [0, 0]
        self.volume_button_pressed_time = None
        self.player_initial_times = [0.0, 0.0]
        self.player_time_used = [0.0, 0.0]
        self.start_times = [0, 0]
        self.player_timers = [0.0, 0.0]
        self.timer_paused = False
        self.starting_bot = None
        self.player1_bot_type = None
        self.player2_bot_type = None

    def create_grid_copy(self, grid, player_pairs):
        grid_copy = Grid(grid.n, grid.m,
                         [row.copy() for row in grid.color],
                         [row.copy() for row in grid.value])
        for pair_list in player_pairs:
            for pair in pair_list:
                for (i, j) in pair:
                    grid_copy.color[i][j] = 4
        return grid_copy

    def update_timer_display(self, grid, solver_manager, cell_size, window_size, top_margin):
        """Met à jour l'affichage du timer pendant le délai des bots."""

        self.screen.fill((220, 220, 220))
        new_rules = (self.selected_rules == "new rules")
        self.screen.fill((220, 220, 220))
        new_rules = (self.selected_rules == "new rules")

        # Redessiner tous les éléments d'interface
        self.ui_manager.draw_grid(grid, solver_manager.solver, cell_size, self.selected_cells,
                                  self.player_mode, self.player_pairs, top_margin, new_rules)

        # Dessiner les boutons
        if self.player_mode == 'botvs':
            self.ui_manager.draw_restart_button(window_size, False, self.player_mode)
        self.ui_manager.draw_menu_button(window_size, False)

        # Calcul des temps restants
        remaining_p1 = self.player_initial_times[0] - self.player_time_used[0]
        remaining_p2 = self.player_initial_times[1] - self.player_time_used[1]
        if self.current_player == 1 and not self.timer_paused:
            remaining_p1 -= (pygame.time.get_ticks() - self.start_times[0]) / 1000.0
        elif self.current_player == 2 and not self.timer_paused:
            remaining_p2 -= (pygame.time.get_ticks() - self.start_times[1]) / 1000.0

        # Affichage des scores
        self.ui_manager.draw_score(
            solver_manager.solver,
            window_size,
            cell_size,
            self.player_scores[0],
            self.player_scores[1],
            self.player_mode,
            [max(0, remaining_p1), max(0, remaining_p2)],
            self.current_player,
            self.player1_bot_type,
            self.player2_bot_type
        )

        pygame.display.flip()

    def main(self):
        """
        The main game loop.
        """
        while self.selected_grid is None:
            self.screen.fill((255, 255, 255))
            window_size = self.screen.get_size()
            visible_height = window_size[1] - 170
            total_content_height = len(self.grid_manager.grid_files) * 50
            max_scroll = max(0, total_content_height - visible_height)

            scroll_bar_height = max(20, int((visible_height / total_content_height) * visible_height)) if max_scroll > 0 else visible_height
            scroll_percentage = self.scroll / max_scroll if max_scroll > 0 else 0
            scroll_bar_y = 100 + (scroll_percentage * (visible_height - scroll_bar_height))
            scroll_bar_rect = pygame.Rect(window_size[0] - 20, int(scroll_bar_y), 20, scroll_bar_height)

            self.ui_manager.draw_grid_options(window_size, self.scroll, scroll_bar_rect, scroll_bar_height,
                                              self.grid_manager.grid_files, self.grid_manager.grid_colors, self.pressed_grid_index)
            pygame.draw.rect(self.screen, (255, 255, 255), (0, 0, window_size[0], 100))
            self.ui_manager.draw_title(window_size)
            self.ui_manager.draw_rules_button(window_size, self.pressed_button == 'rules')
            self.ui_manager.draw_volume_button(window_size, self.pressed_button == 'volume')
            current_time = pygame.time.get_ticks()
            if (self.volume_button_pressed_time is not None and current_time - self.volume_button_pressed_time >= 150):
                self.pressed_button = None
                self.volume_button_pressed_time = None
            pygame.display.flip()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    if event.button == 1:
                        x, y = event.pos
                        volume_rect = pygame.Rect(window_size[0] - 95, window_size[1] - 70, 50, 40)
                        if volume_rect.collidepoint(x, y):
                            self.pressed_button = 'volume'
                            self.volume_button_pressed_time = pygame.time.get_ticks()
                            self.ui_manager.toggle_volume()
                        elif scroll_bar_rect.collidepoint(x, y) and max_scroll > 0:
                            self.scroll_bar_dragging = True
                            self.mouse_y_offset = y - scroll_bar_rect.y
                        else:
                            self.pressed_grid_index = -1
                            for i in range(len(self.grid_manager.grid_files)):
                                btn_y = 100 + i * 50 - self.scroll
                                if btn_y < 100 or btn_y + 40 > window_size[1] - 70:
                                    continue
                                btn_rect = pygame.Rect(window_size[0] // 2 - 100, btn_y, 200, 40)
                                if btn_rect.collidepoint(x, y):
                                    self.pressed_grid_index = i
                                    break
                            rules_rect = pygame.Rect(window_size[0] - 200, window_size[1] - 70, 100, 40)
                            if rules_rect.collidepoint(x, y):
                                self.pressed_button = 'rules'
                elif event.type == pygame.MOUSEBUTTONUP:
                    if event.button == 1 and self.pressed_grid_index != -1:
                        x, y = event.pos
                        volume_rect = pygame.Rect(window_size[0] - 20, window_size[1] - 70, 50, 40)
                        if volume_rect.collidepoint(x, y):
                            self.pressed_button = 'volume'
                            self.volume_button_pressed_time = pygame.time.get_ticks()
                            self.ui_manager.toggle_volume()
                        visible_y = y + self.scroll - 100
                        released_index = visible_y // 50

                        if 0 <= released_index < len(self.grid_manager.grid_files) and released_index == self.pressed_grid_index:
                            self.ui_manager.draw_grid_options(window_size, self.scroll, scroll_bar_rect,
                                                              scroll_bar_height, self.grid_manager.grid_files,
                                                              self.grid_manager.grid_colors, self.pressed_grid_index)
                            pygame.display.flip()
                            pygame.time.delay(100)
                            self.selected_grid = self.grid_manager.grid_files[self.pressed_grid_index][0]

                    self.scroll_bar_dragging = False
                    self.pressed_grid_index = -1

                    if self.pressed_button == 'rules':
                        self.screen = pygame.display.set_mode((800, 600))
                        self.show_rules()
                        self.pressed_button = None

                elif event.type == pygame.MOUSEMOTION:
                    if self.scroll_bar_dragging and max_scroll > 0:
                        mouse_y = event.pos[1] - self.mouse_y_offset
                        new_y = max(100, min(mouse_y, 100 + visible_height - scroll_bar_height))
                        self.scroll = ((new_y - 100) / (visible_height - scroll_bar_height)) * max_scroll
                        self.scroll = max(0, min(self.scroll, max_scroll))
                elif event.type == pygame.MOUSEWHEEL:
                    self.scroll -= event.y * 50
                    self.scroll = max(0, min(self.scroll, max_scroll))
                elif event.type == pygame.VIDEORESIZE:
                    self.screen = pygame.display.set_mode((event.w, event.h), pygame.RESIZABLE)

        self.player_mode = None
        while self.player_mode is None:
            self.screen.fill((255, 255, 255))
            window_size = self.screen.get_size()
            self.ui_manager.draw_title(window_size)
            self.ui_manager.draw_player_choice(window_size, self.pressed_button)
            self.ui_manager.draw_return_button(window_size, self.pressed_button == 'return')
            pygame.display.flip()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    if event.button == 1:
                        x, y = event.pos
                        one_rect = pygame.Rect(window_size[0] // 2 - 185, 150, 390, 60)
                        two_rect = pygame.Rect(window_size[0] // 2 - 185, 225, 390, 60)
                        bot_rect = pygame.Rect(window_size[0] // 2 - 185, 300, 390, 60)
                        deepblue_rect = pygame.Rect(window_size[0] // 2 - 185, 375, 390, 60)
                        botvs_rect = pygame.Rect(window_size[0] // 2 - 185, 450, 390, 60)
                        return_rect = pygame.Rect(50, window_size[1] - 70, 100, 40)
                        if one_rect.collidepoint(x, y):
                            self.pressed_button = 'one'
                        elif two_rect.collidepoint(x, y):
                            self.pressed_button = 'two'
                        elif bot_rect.collidepoint(x, y):
                            self.pressed_button = 'bot'
                        elif deepblue_rect.collidepoint(x, y):
                            self.pressed_button = 'deepblue'
                        elif botvs_rect.collidepoint(x, y):
                            self.pressed_button = 'botvs'
                        elif return_rect.collidepoint(x, y):
                            self.pressed_button = 'return'

                elif event.type == pygame.MOUSEBUTTONUP:
                    if event.button == 1 and self.pressed_button:
                        x, y = event.pos
                        one_rect = pygame.Rect(window_size[0] // 2 - 140, 150, 300, 60)
                        two_rect = pygame.Rect(window_size[0] // 2 - 140, 225, 300, 60)
                        bot_rect = pygame.Rect(window_size[0] // 2 - 140, 300, 300, 60)
                        deepblue_rect = pygame.Rect(window_size[0] // 2 - 140, 375, 300, 60)
                        botvs_rect = pygame.Rect(window_size[0] // 2 - 140, 450, 390, 60)
                        return_rect = pygame.Rect(50, window_size[1] - 70, 100, 40)
                        if one_rect.collidepoint(x, y) and self.pressed_button == 'one':
                            pygame.time.wait(150)
                            self.player_mode = 'one'
                        elif two_rect.collidepoint(x, y) and self.pressed_button == 'two':
                            pygame.time.wait(150)
                            self.player_mode = 'two'
                        elif bot_rect.collidepoint(x, y) and self.pressed_button == 'bot':
                            pygame.time.wait(150)
                            self.player_mode = 'bot'
                        elif deepblue_rect.collidepoint(x, y) and self.pressed_button == 'deepblue':
                            pygame.time.wait(150)
                            self.player_mode = 'deepblue'
                        elif botvs_rect.collidepoint(x, y) and self.pressed_button == 'botvs':
                            pygame.time.wait(150)
                            self.player_mode = 'botvs'
                        elif return_rect.collidepoint(x, y) and self.pressed_button == 'return':
                            self.reset_game_state()
                            return
                        self.pressed_button = None

                elif event.type == pygame.VIDEORESIZE:
                    self.screen = pygame.display.set_mode((event.w, event.h), pygame.RESIZABLE)

        if self.player_mode == 'botvs':
            self.starting_bot = None
            while self.starting_bot is None:
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        pygame.quit()
                        sys.exit()
                    elif event.type == pygame.VIDEORESIZE:
                        # Mettre à jour la taille de la fenêtre
                        self.screen = pygame.display.set_mode((event.w, event.h), pygame.RESIZABLE)
                    elif event.type == pygame.MOUSEBUTTONDOWN:
                        if event.button == 1:
                            x, y = event.pos
                            window_size = self.screen.get_size()
                            db_rect = pygame.Rect(window_size[0]//2 - 150, 200, 300, 60)
                            sf_rect = pygame.Rect(window_size[0]//2 - 150, 300, 300, 60)
                            if db_rect.collidepoint(x, y):
                                self.pressed_button = 'db'
                            elif sf_rect.collidepoint(x, y):
                                self.pressed_button = 'sf'
                    elif event.type == pygame.MOUSEBUTTONUP:
                        if event.button == 1 and self.pressed_button:
                            x, y = event.pos
                            window_size = self.screen.get_size()
                            db_rect = pygame.Rect(window_size[0]//2 - 150, 200, 300, 60)
                            sf_rect = pygame.Rect(window_size[0]//2 - 150, 300, 300, 60)
                            if db_rect.collidepoint(x, y) and self.pressed_button == 'db':
                                self.starting_bot = 'deepblue'
                            elif sf_rect.collidepoint(x, y) and self.pressed_button == 'sf':
                                self.starting_bot = 'stockfish'
                            self.pressed_button = None

                self.screen.fill((255, 255, 255))
                window_size = self.screen.get_size()
                font = pygame.font.Font(None, 50)

                # Centrer les boutons horizontalement
                db_rect = pygame.Rect(window_size[0]//2 - 150, 200, 300, 60)
                sf_rect = pygame.Rect(window_size[0]//2 - 150, 300, 300, 60)

                color_db = (30, 30, 30) if self.pressed_button == 'db' else (50, 50, 50)
                color_sf = (30, 30, 30) if self.pressed_button == 'sf' else (50, 50, 50)

                pygame.draw.rect(self.screen, color_db, db_rect)
                text = font.render("DeepBlue starts", True, (255, 255, 255))
                text_rect = text.get_rect(center=db_rect.center)
                self.screen.blit(text, text_rect)

                pygame.draw.rect(self.screen, color_sf, sf_rect)
                text = font.render("Stockfish starts", True, (255, 255, 255))
                text_rect = text.get_rect(center=sf_rect.center)
                self.screen.blit(text, text_rect)
                pygame.display.flip()

                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        pygame.quit()
                        sys.exit()
                    elif event.type == pygame.MOUSEBUTTONDOWN:
                        if event.button == 1:
                            x, y = event.pos
                            if db_rect.collidepoint(x, y):
                                self.pressed_button = 'db'
                            elif sf_rect.collidepoint(x, y):
                                self.pressed_button = 'sf'
                    elif event.type == pygame.MOUSEBUTTONUP:
                        if event.button == 1 and self.pressed_button:
                            x, y = event.pos
                            if db_rect.collidepoint(x, y) and self.pressed_button == 'db':
                                self.starting_bot = 'deepblue'
                            elif sf_rect.collidepoint(x, y) and self.pressed_button == 'sf':
                                self.starting_bot = 'stockfish'
                            self.pressed_button = None

        self.selected_rules = "original rules"
        rules_selected = False
        while not rules_selected:
            self.screen.fill((255, 255, 255))
            window_size = self.screen.get_size()
            self.ui_manager.draw_rule_choice(window_size, self.pressed_button)
            self.ui_manager.draw_return_button(window_size, self.pressed_button == 'return')
            pygame.display.flip()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    if event.button == 1:
                        x, y = event.pos
                        classic_rect = pygame.Rect(window_size[0] // 2 - 140, 200, 300, 60)
                        new_rect = pygame.Rect(window_size[0] // 2 - 140, 300, 300, 60)
                        return_rect = pygame.Rect(50, window_size[1] - 70, 100, 40)
                        if classic_rect.collidepoint(x, y):
                            self.pressed_button = 'classic'
                        elif new_rect.collidepoint(x, y):
                            self.pressed_button = 'new'
                        elif return_rect.collidepoint(x, y):
                            self.pressed_button = 'return'
                elif event.type == pygame.MOUSEBUTTONUP:
                    if event.button == 1 and self.pressed_button:
                        x, y = event.pos
                        classic_rect = pygame.Rect(window_size[0] // 2 - 140, 200, 300, 60)
                        new_rect = pygame.Rect(window_size[0] // 2 - 140, 300, 300, 60)
                        return_rect = pygame.Rect(50, window_size[1] - 70, 100, 40)
                        if classic_rect.collidepoint(x, y) and self.pressed_button == 'classic':
                            self.selected_rules = "original rules"
                            rules_selected = True
                        elif new_rect.collidepoint(x, y) and self.pressed_button == 'new':
                            self.selected_rules = "new rules"
                            rules_selected = True
                        elif return_rect.collidepoint(x, y) and self.pressed_button == 'return':
                            self.reset_game_state()
                            return
                        self.pressed_button = None

        grid = self.grid_manager.load_grid(self.selected_grid)
        solver_manager = SolverManager(grid, self.selected_rules)
        general_score = solver_manager.general_score

        if self.player_mode == 'one':
            self.player1_bot_type = None
            self.player2_bot_type = None
        elif self.player_mode == 'two':
            self.player1_bot_type = None
            self.player2_bot_type = None
        elif self.player_mode == 'bot':
            self.player1_bot_type = None
            self.player2_bot_type = 'minimax'
        elif self.player_mode == 'deepblue':
            self.player1_bot_type = None
            self.player2_bot_type = 'mcts'
        elif self.player_mode == 'botvs':
            if self.starting_bot == 'deepblue':
                self.player1_bot_type = 'mcts'
                self.player2_bot_type = 'minimax'
            else:
                self.player1_bot_type = 'minimax'
                self.player2_bot_type = 'mcts'

        if self.selected_grid.startswith("grid0"):
            self.player_initial_times = [60.0, 60.0]
        elif self.selected_grid.startswith("grid1"):
            self.player_initial_times = [3 * 60.0, 3 * 60.0]
        elif self.selected_grid.startswith("grid2"):
            self.player_initial_times = [10 * 60.0, 10 * 60.0]

        self.player_timers = self.player_initial_times.copy()
        self.player_time_used = [0.0, 0.0]
        self.start_times = [pygame.time.get_ticks(), 0]

        cell_size = 60
        top_margin = 50 if self.player_mode in ['two', 'bot'] else 0
        window_height = grid.n * cell_size + 110 + top_margin
        window_width = max(600, grid.m * cell_size)
        window_size = (window_width, window_height)
        self.screen = pygame.display.set_mode(window_size, pygame.RESIZABLE)
        self.selected_cells = []
        self.game_over = False
        self.show_solution = False
        self.pressed_button = None

        while True:
            current_time = pygame.time.get_ticks()
            if not self.game_over:
                if self.current_player == 1 and self.player1_bot_type is not None:
                    grid_copy = self.create_grid_copy(grid, self.player_pairs)
                    if self.player1_bot_type == 'mcts':
                        bot = MCTS_Bot(grid_copy, simulations_per_move=20, epsilon=0.1)
                        bot_pair = bot.mcts_move()
                    elif self.player1_bot_type == 'minimax':
                        bot_pair = Minimax_Bot.move_to_play(grid_copy, self.selected_rules)
                    if bot_pair is not None:
                        valid = solver_manager.pair_is_valid(bot_pair, [], grid, self.player_pairs, self.selected_rules)
                        if valid:
                            start_wait = pygame.time.get_ticks()
                            while pygame.time.get_ticks() - start_wait < 1500:
                                for event in pygame.event.get():
                                    if event.type == pygame.QUIT:
                                        pygame.quit()
                                        sys.exit()
                                self.update_timer_display(grid, solver_manager, cell_size, window_size, top_margin)
                                pygame.time.wait(10)
                            bot_end_time = pygame.time.get_ticks()
                            elapsed_bot = (bot_end_time - self.start_times[0]) / 1000.0
                            self.player_time_used[0] += elapsed_bot
                            self.player_pairs[0].append(bot_pair)
                            self.player_scores[0] = solver_manager.calculate_two_player_score(self.player_pairs[0], grid)
                            self.current_player = 2
                            self.start_times[1] = pygame.time.get_ticks()
                        else:
                            self.game_over = True
                    else:
                        self.game_over = True
                elif self.current_player == 2 and self.player2_bot_type is not None:
                    grid_copy = self.create_grid_copy(grid, self.player_pairs)
                    if self.player2_bot_type == 'mcts':
                        bot = MCTS_Bot(grid_copy, simulations_per_move=20, epsilon=0.1)
                        bot_pair = bot.mcts_move()
                    elif self.player2_bot_type == 'minimax':
                        bot_pair = Minimax_Bot.move_to_play(grid_copy, self.selected_rules)
                    if bot_pair is not None:
                        valid = solver_manager.pair_is_valid(bot_pair, [], grid, self.player_pairs, self.selected_rules)
                        if valid:
                            start_wait = pygame.time.get_ticks()
                            while pygame.time.get_ticks() - start_wait < 1500:
                                for event in pygame.event.get():
                                    if event.type == pygame.QUIT:
                                        pygame.quit()
                                        sys.exit()
                                self.update_timer_display(grid, solver_manager, cell_size, window_size, top_margin)
                                pygame.time.wait(10)
                            bot_end_time = pygame.time.get_ticks()
                            elapsed_bot = (bot_end_time - self.start_times[1]) / 1000.0
                            self.player_time_used[1] += elapsed_bot

                            self.player_pairs[1].append(bot_pair)
                            self.player_scores[1] = solver_manager.calculate_two_player_score(self.player_pairs[1], grid)
                            self.current_player = 1
                            self.start_times[0] = pygame.time.get_ticks()
                        else:
                            self.game_over = True
                    else:
                        self.game_over = True

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

                elif event.type == pygame.MOUSEBUTTONDOWN:
                    x, y = event.pos
                    if y >= grid.n * cell_size + top_margin:
                        reset_rect = pygame.Rect(window_size[0] - 330, window_size[1] - 70, 100, 40) if self.player_mode == 'botvs' else pygame.Rect(window_size[0] - 225, window_size[1] - 70, 110, 40) if self.player_mode in ['two', 'bot'] else pygame.Rect(window_size[0] - 330, window_size[1] - 70, 100, 40)
                        solution_rect = pygame.Rect(window_size[0] - 225, window_size[1] - 70, 110, 40) if self.player_mode == 'one' else None
                        menu_rect = pygame.Rect(window_size[0] - 110, window_size[1] - 70, 100, 40)

                        if reset_rect.collidepoint(x, y):
                            self.pressed_button = 'reset'
                            self.timer_paused = False
                        elif solution_rect and solution_rect.collidepoint(x, y):
                            self.pressed_button = 'solution'
                            if not self.timer_paused:
                                elapsed = (current_time - self.start_times[0]) / 1000.0
                                self.player_time_used[0] += elapsed
                                self.timer_paused = True
                        elif menu_rect.collidepoint(x, y):
                            self.pressed_button = 'menu'
                        elif y >= window_size[1] - 40 and x <= 220:
                            self.pressed_button = None
                    else:
                        i, j = (y - top_margin) // cell_size, x // cell_size
                        if 0 <= i < grid.n and 0 <= j < grid.m:
                            if grid.is_forbidden(i, j):
                                self.ui_manager.draw_error_message("Invalid pair!", window_size, self.player_mode, cell_size)
                                self.selected_cells = []
                            elif (i, j) in [cell for pair in solver_manager.solver.pairs for cell in pair]:
                                for pair in solver_manager.solver.pairs:
                                    if (i, j) in pair:
                                        solver_manager.solver.pairs.remove(pair)
                                        break
                            elif (i, j) not in [cell for pair in solver_manager.solver.pairs for cell in pair]:
                                self.selected_cells.append((i, j))
                                if len(self.selected_cells) == 2:
                                    (i1, j1), (i2, j2) = self.selected_cells
                                    color1 = grid.color[i1][j1]
                                    color2 = grid.color[i2][j2]
                                    are_adjacent = (i2, j2) in grid.vois(i1, j1)
                                    valid_non_adjacent = (self.selected_rules == "new rules"
                                                        and (color1 == 0 or color2 == 0)
                                                        and color1 != 4 and color2 != 4)
                                    if are_adjacent or valid_non_adjacent:
                                        color1 = grid.color[self.selected_cells[0][0]][self.selected_cells[0][1]]
                                        color2 = grid.color[self.selected_cells[1][0]][self.selected_cells[1][1]]
                                        if solver_manager.can_pair(color1, color2):
                                            if self.player_mode == 'one':
                                                solver_manager.solver.pairs.append((self.selected_cells[0], self.selected_cells[1]))
                                            elif self.player_mode == 'bot':
                                                valid = solver_manager.pair_is_valid((self.selected_cells[0], self.selected_cells[1]), [], grid, self.player_pairs, self.selected_rules)
                                                if valid:
                                                    elapsed = (pygame.time.get_ticks() - self.start_times[0]) / 1000.0
                                                    self.player_time_used[0] += elapsed
                                                    self.player_pairs[0].append((self.selected_cells[0], self.selected_cells[1]))
                                                    self.player_scores[0] = solver_manager.calculate_two_player_score(self.player_pairs[0], grid)
                                                    self.current_player = 2
                                                    self.start_times[1] = pygame.time.get_ticks()
                                                else:
                                                    self.ui_manager.draw_error_message("Invalid pair!", window_size, self.player_mode, cell_size)
                                            else:
                                                if solver_manager.pair_is_valid((self.selected_cells[0], self.selected_cells[1]), solver_manager.solver.pairs, grid, self.player_pairs, self.selected_rules):
                                                    elapsed = (pygame.time.get_ticks() - self.start_times[self.current_player - 1]) / 1000.0
                                                    self.player_time_used[self.current_player - 1] += elapsed
                                                    self.player_pairs[self.current_player - 1].append((self.selected_cells[0], self.selected_cells[1]))
                                                    self.player_scores[self.current_player - 1] = solver_manager.calculate_two_player_score(self.player_pairs[self.current_player - 1], grid)
                                                    self.current_player = 3 - self.current_player
                                                    self.start_times[self.current_player - 1] = pygame.time.get_ticks()
                                                else:
                                                    self.ui_manager.draw_error_message("Invalid pair!", window_size, self.player_mode, cell_size)
                                        else:
                                            self.ui_manager.draw_error_message("Invalid pair!", window_size, self.player_mode, cell_size)
                                    else:
                                        self.ui_manager.draw_error_message("Invalid pair!", window_size, self.player_mode, cell_size)
                                    self.selected_cells = []
                            self.pressed_button = None

                elif event.type == pygame.MOUSEBUTTONUP:
                    x, y = event.pos
                    if self.pressed_button:
                        button_rect = None
                        if self.pressed_button == 'reset':
                            button_rect = pygame.Rect(window_size[0] - 330, window_size[1] - 70, 100, 40) if self.player_mode == 'botvs' else pygame.Rect(window_size[0] - 225, window_size[1] - 70, 110, 40) if self.player_mode in ['two', 'bot'] else pygame.Rect(window_size[0] - 330, window_size[1] - 70, 100, 40)
                        elif self.pressed_button == 'solution' and self.player_mode == 'one':
                            button_rect = pygame.Rect(window_size[0] - 225, window_size[1] - 70, 110, 40)
                        elif self.pressed_button == 'menu':
                            button_rect = pygame.Rect(window_size[0] - 110, window_size[1] - 70, 100, 40)
                            self.reset_game_state()
                            pygame.time.wait(150)
                        elif self.pressed_button == 'return':
                            button_rect = pygame.Rect(50, window_size[1] - 70, 100, 40)
                            self.reset_game_state()
                            return

                        if button_rect and button_rect.collidepoint(x, y):
                            if self.pressed_button == 'menu':
                                self.reset_game_state()
                                pygame.time.delay(150)

                            if self.pressed_button == 'reset':
                                solver_manager.solver.pairs = []
                                self.selected_cells = []
                                self.game_over = False
                                self.show_solution = False
                                self.player_pairs = [[], []]
                                self.current_player = 1
                                self.player_scores = [0, 0]
                                if self.selected_grid.startswith("grid0"):
                                    self.player_initial_times = [60.0, 60.0]
                                elif self.selected_grid.startswith("grid1"):
                                    self.player_initial_times = [3 * 60.0, 3 * 60.0]
                                elif self.selected_grid.startswith("grid2"):
                                    self.player_initial_times = [10 * 60.0, 10 * 60.0]
                                self.player_timers = self.player_initial_times.copy()
                                self.player_time_used = [0.0, 0.0]
                                self.start_times = [pygame.time.get_ticks(), 0]
                            elif self.pressed_button == 'solution':
                                solver_manager.solver.pairs = solver_manager.solver_general.pairs
                                self.show_solution = True
                            elif self.pressed_button == 'menu':
                                self.reset_game_state()
                                pygame.time.wait(150)
                            elif self.pressed_button == 'return':
                                self.reset_game_state()
                                return

                        self.pressed_button = None

                elif event.type == pygame.VIDEORESIZE:
                    self.screen = pygame.display.set_mode((event.w, event.h), pygame.RESIZABLE)
                    window_size = (event.w, event.h)
                    cell_size = min(window_size[0] // grid.m, window_size[1] // (grid.n + 2))
                    top_margin = 50 if self.player_mode in ['two', 'bot', 'botvs'] else 0
                    self.ui_manager.draw_grid(grid, solver_manager.solver, cell_size, self.selected_cells, self.player_mode, self.player_pairs, top_margin)
                    self.ui_manager.draw_score(
                        solver_manager.solver,
                        window_size,
                        cell_size,
                        self.player_scores[0],
                        self.player_scores[1],
                        self.player_mode,
                        [remaining_p1, remaining_p2],
                        self.current_player,
                        self.player1_bot_type,
                        self.player2_bot_type
                    )

                    if self.player_mode == 'two':
                        self.ui_manager.draw_turn_indicator(self.current_player, window_size, top_margin, 'two', self.player1_bot_type, self.player2_bot_type)
                        self.ui_manager.draw_restart_button(window_size, self.pressed_button == 'reset', self.player_mode)
                    if self.player_mode == 'bot':
                        self.ui_manager.draw_turn_indicator(self.current_player, window_size, top_margin, 'bot', self.player1_bot_type, self.player2_bot_type)
                        self.ui_manager.draw_restart_button(window_size, self.pressed_button == 'reset', self.player_mode)
                    if self.player_mode == 'one':
                        self.ui_manager.draw_solution_button(window_size, self.pressed_button == 'solution')
                        self.ui_manager.draw_restart_button(window_size, self.pressed_button == 'reset', self.player_mode)
                    if self.player_mode == 'botvs':
                        self.ui_manager.draw_restart_button(window_size, self.pressed_button == 'reset', self.player_mode)
                    self.ui_manager.draw_menu_button(window_size, self.pressed_button == 'menu')

            def calculate_remaining(player_index):
                if self.current_player != player_index + 1 or self.timer_paused:
                    return max(0.0, self.player_initial_times[player_index] - self.player_time_used[player_index])
                else:
                    if self.start_times[player_index] == 0:
                        return max(0.0, self.player_initial_times[player_index] - self.player_time_used[player_index])
                    current_time = pygame.time.get_ticks()
                    elapsed = (current_time - self.start_times[player_index]) / 1000.0
                    remaining = self.player_initial_times[player_index] - (self.player_time_used[player_index] + elapsed)
                    return max(0.0, remaining)

            current_time = pygame.time.get_ticks()
            remaining_p1 = calculate_remaining(0)
            remaining_p2 = calculate_remaining(1)

            if not self.game_over:
                if remaining_p1 <= 0:
                    self.game_over = True
                    self.ui_manager.win_sound.play()
                    self.ui_manager.draw_end_screen("Player 2 has won!", (148, 0, 211), window_size)
                elif remaining_p2 <= 0:
                    self.game_over = True
                    self.ui_manager.win_sound.play()
                    self.ui_manager.draw_end_screen("Player 1 has won!", self.colors[5], window_size)

            self.screen.fill((220, 220, 220))
            new_rules = (self.selected_rules == "new rules")
            self.ui_manager.draw_grid(grid, solver_manager.solver, cell_size, self.selected_cells, self.player_mode, self.player_pairs, top_margin, new_rules)
            self.ui_manager.draw_score(
                solver_manager.solver,
                window_size,
                cell_size,
                self.player_scores[0],
                self.player_scores[1],
                self.player_mode,
                [remaining_p1, remaining_p2],
                self.current_player,
                self.player1_bot_type,
                self.player2_bot_type
            )

            if self.player_mode == 'two':
                self.ui_manager.draw_turn_indicator(self.current_player, window_size, top_margin, 'two', self.player1_bot_type, self.player2_bot_type)
                self.ui_manager.draw_restart_button(window_size, self.pressed_button == 'reset', self.player_mode)
            if self.player_mode == 'bot':
                self.ui_manager.draw_turn_indicator(self.current_player, window_size, top_margin, 'bot', self.player1_bot_type, self.player2_bot_type)
                self.ui_manager.draw_restart_button(window_size, self.pressed_button == 'reset', self.player_mode)
            if self.player_mode == 'one':
                self.ui_manager.draw_solution_button(window_size, self.pressed_button == 'solution')
                self.ui_manager.draw_restart_button(window_size, self.pressed_button == 'reset', self.player_mode)
            if self.player_mode == 'botvs':
                self.ui_manager.draw_restart_button(window_size, self.pressed_button == 'reset', self.player_mode)
            self.ui_manager.draw_menu_button(window_size, self.pressed_button == 'menu')
            pygame.display.flip()

            if not self.show_solution and not any(
            solver_manager.pair_is_valid(pair, solver_manager.solver.pairs, grid, self.player_pairs, self.selected_rules)
            for pair in grid.all_pairs(self.selected_rules)):
                if not self.game_over:
                    current_time = pygame.time.get_ticks()
                    elapsed = (current_time - self.start_times[self.current_player - 1]) / 1000.0
                    self.player_time_used[self.current_player - 1] += elapsed
                    self.start_times[self.current_player - 1] = 0

                    self.game_over = True
                    if self.player_mode == 'one':
                        if solver_manager.solver.score() <= general_score:
                            self.ui_manager.win_sound.play()
                            self.ui_manager.draw_end_screen("You won!", (0, 200, 0), window_size)
                        else:
                            self.ui_manager.lose_sound.play()
                            self.ui_manager.draw_end_screen("You lost!", (200, 0, 0), window_size)
                        self.player_timers = self.player_initial_times.copy()
                        self.player_time_used = [0.0, 0.0]
                        self.start_times = [pygame.time.get_ticks(), 0]
                        solver_manager.solver.pairs = []
                        self.selected_cells = []
                        self.game_over = False

                    if self.player_mode == 'two':
                        if self.player_scores[0] < self.player_scores[1]:
                            self.ui_manager.win_sound.play()
                            self.ui_manager.draw_end_screen("Player 1 has won!", self.colors[5], window_size)
                        elif self.player_scores[1] < self.player_scores[0]:
                            self.ui_manager.win_sound.play()
                            self.ui_manager.draw_end_screen("Player 2 has won!", (148, 0, 211), window_size)
                        else:
                            remaining_p1 = self.player_initial_times[0] - self.player_time_used[0]
                            remaining_p2 = self.player_initial_times[1] - self.player_time_used[1]
                            if remaining_p1 > remaining_p2:
                                self.ui_manager.win_sound.play()
                                self.ui_manager.draw_end_screen("Player 1 Wins (Time)!", self.colors[5], window_size)
                            elif remaining_p2 > remaining_p1:
                                self.ui_manager.win_sound.play()
                                self.ui_manager.draw_end_screen("Player 2 Wins (Time)!", (148, 0, 211), window_size)
                            else:
                                self.ui_manager.lose_sound.play()
                                self.ui_manager.draw_end_screen("It's a Tie!", (0, 255, 255), window_size)
                        self.player_timers = self.player_initial_times.copy()
                        self.player_time_used = [0.0, 0.0]
                        self.start_times = [pygame.time.get_ticks(), 0]
                        self.player_pairs = [[], []]
                        self.player_scores = [0, 0]
                        self.current_player = 1
                        self.game_over = False

                    if self.player_mode == 'bot':
                        if self.player_scores[0] > self.player_scores[1]:
                            self.ui_manager.lose_sound.play()
                            self.ui_manager.draw_end_screen("Stockfish Wins!", (148, 0, 211), window_size)
                        elif self.player_scores[1] > self.player_scores[0]:
                            self.ui_manager.win_sound.play()
                            self.ui_manager.draw_end_screen("You Won!", self.colors[5], window_size)
                        else:
                            remaining_player = self.player_initial_times[0] - self.player_time_used[0]
                            remaining_bot = self.player_initial_times[1] - self.player_time_used[1]
                            if remaining_player > remaining_bot:
                                self.ui_manager.win_sound.play()
                                self.ui_manager.draw_end_screen("You Win (Time)!", self.colors[5], window_size)
                            elif remaining_bot > remaining_player:
                                self.ui_manager.lose_sound.play()
                                self.ui_manager.draw_end_screen("Stockfish Wins (Time)!", (148, 0, 211), window_size)
                            else:
                                self.ui_manager.lose_sound.play()
                                self.ui_manager.draw_end_screen("It's a Tie!", (0, 255, 255), window_size)
                        self.player_timers = self.player_initial_times.copy()
                        self.player_time_used = [0.0, 0.0]
                        self.start_times = [pygame.time.get_ticks(), 0]
                        self.player_pairs = [[], []]
                        self.player_scores = [0, 0]
                        self.current_player = 1
                        self.game_over = False

                    if self.player_mode == 'botvs':
                        if self.player_scores[0] < self.player_scores[1]:
                            self.ui_manager.win_sound.play()
                            self.ui_manager.draw_end_screen("Stockfish Wins!", (148, 0, 211), window_size)
                        elif self.player_scores[1] < self.player_scores[0]:
                            self.ui_manager.win_sound.play()
                            self.ui_manager.draw_end_screen("DeepBlue Wins!", self.colors[6], window_size)
                        else:
                            remaining_stockfish = self.player_initial_times[0] - self.player_time_used[0]
                            remaining_deepblue = self.player_initial_times[1] - self.player_time_used[1]
                            if remaining_stockfish < remaining_deepblue:
                                self.ui_manager.win_sound.play()
                                self.ui_manager.draw_end_screen("Stockfish Wins (Time)!", (148, 0, 211), window_size)
                            elif remaining_deepblue < remaining_stockfish:
                                self.ui_manager.win_sound.play()
                                self.ui_manager.draw_end_screen("DeepBlue Wins (Time)!", self.colors[6], window_size)
                            else:
                                self.ui_manager.lose_sound.play()
                                self.ui_manager.draw_end_screen("It's a Tie!", (0, 255, 255), window_size)
                        self.player_timers = self.player_initial_times.copy()
                        self.player_time_used = [0.0, 0.0]
                        self.start_times = [pygame.time.get_ticks(), 0]
                        self.player_pairs = [[], []]
                        self.player_scores = [0, 0]
                        self.current_player = 1
                        self.game_over = False

    def show_rules(self):
        """
        Displays the rules screen.
        """
        window_size = (800, 600)
        visible_height = window_size[1] - 170
        line_height = 30
        total_lines = 22
        total_content_height = total_lines * line_height
        max_scroll = max(0, total_content_height - visible_height)
        scroll_bar_height = max(20, int((visible_height / total_content_height) * visible_height)) if max_scroll > 0 else visible_height

        while True:
            current_time = pygame.time.get_ticks()
            scroll_percentage = self.rules_scroll / max_scroll if max_scroll > 0 else 0
            scroll_bar_y = 100 + (scroll_percentage * (visible_height - scroll_bar_height))
            scroll_bar_rect = pygame.Rect(780, int(scroll_bar_y), 20, scroll_bar_height)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

                elif event.type == pygame.MOUSEBUTTONDOWN:
                    if event.button == 1:
                        x, y = event.pos
                        if scroll_bar_rect.collidepoint(x, y) and max_scroll > 0:
                            self.rules_scroll_bar_dragging = True
                            self.rules_mouse_y_offset = y - scroll_bar_rect.y
                        else:
                            menu_rect = pygame.Rect(window_size[0] - 110, window_size[1] - 70, 100, 40)
                            if menu_rect.collidepoint(x, y):
                                self.pressed_button = 'menu'

                elif event.type == pygame.MOUSEBUTTONUP:
                    if self.pressed_button == 'menu':
                        self.reset_game_state()
                        x, y = event.pos
                        menu_rect = pygame.Rect(window_size[0] - 110, window_size[1] - 70, 100, 40)
                        if menu_rect.collidepoint(x, y):
                            self.ui_manager.draw_menu_button(window_size, True)
                            pygame.display.update(menu_rect)
                            pygame.time.delay(100)
                            self.reset_game_state()
                    self.pressed_button = None
                    self.rules_scroll_bar_dragging = False

                elif event.type == pygame.MOUSEMOTION:
                    if self.rules_scroll_bar_dragging and max_scroll > 0:
                        mouse_y = event.pos[1] - self.rules_mouse_y_offset
                        new_y = max(100, min(mouse_y, 100 + visible_height - scroll_bar_height))
                        self.rules_scroll = ((new_y - 100) / (visible_height - scroll_bar_height)) * max_scroll
                        self.rules_scroll = max(0, min(self.rules_scroll, max_scroll))

                elif event.type == pygame.MOUSEWHEEL:
                    self.rules_scroll -= event.y * 30
                    self.rules_scroll = max(0, min(self.rules_scroll, max_scroll))

                elif event.type == pygame.VIDEORESIZE:
                    self.screen = pygame.display.set_mode((event.w, event.h), pygame.RESIZABLE)
                    window_size = (event.w, event.h)
                    visible_height = window_size[1] - 170
                    total_content_height = total_lines * line_height
                    max_scroll = max(0, total_content_height - visible_height)
                    scroll_bar_height = max(20, int((visible_height / total_content_height) * visible_height)) if max_scroll > 0 else visible_height
                    scroll_percentage = self.rules_scroll / max_scroll if max_scroll > 0 else 0
                    scroll_bar_y = 100 + (scroll_percentage * (visible_height - scroll_bar_height))
                    scroll_bar_rect = pygame.Rect(780, int(scroll_bar_y), 20, scroll_bar_height)

            self.screen.fill((255, 255, 255))
            self.ui_manager.draw_rules(window_size, self.rules_scroll, scroll_bar_rect, scroll_bar_height)
            self.ui_manager.draw_menu_button(window_size, self.pressed_button == 'menu')
            pygame.display.flip()

    def reset_game_state(self):
        """
        Resets the game state to the initial settings.
        """
        self.selected_grid = None
        self.scroll = 0
        self.scroll_bar_dragging = False
        self.mouse_y_offset = 0
        self.selected_cells = []
        self.game_over = False
        self.show_solution = False
        self.pressed_button = None
        self.pressed_grid_index = -1
        self.rules_scroll = 0
        self.rules_scroll_bar_dragging = False
        self.rules_mouse_y_offset = 0
        self.player_scores = [0, 0]
        self.player_pairs = [[], []]
        self.current_player = 1
        self.screen = pygame.display.set_mode((600, 600))

        if self.selected_grid:
            if self.selected_grid.startswith("grid0"):
                self.player_initial_times = [60.0, 60.0]
            elif self.selected_grid.startswith("grid1"):
                self.player_initial_times = [3 * 60.0, 3 * 60.0]
            elif self.selected_grid.startswith("grid2"):
                self.player_initial_times = [10 * 60.0, 10 * 60.0]

        self.player_timers = self.player_initial_times.copy()
        self.player_time_used = [0.0, 0.0]
        self.start_times = [0, 0]
        self.timer_paused = False
        self.main()

if __name__ == "__main__":
    game = Game()
    game.main()