import pygame
from settings import *

class Gamescreen:
    def __init__(self):
        # Screen setup with additional space for status
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT + 100))  # Screen creation
        pygame.display.set_caption("Modern Omok")  # Set window title

        # Fonts
        self.font_large = pygame.font.SysFont(None, 40)  # Large font for status
        self.font_button = pygame.font.SysFont(None, 32)  # Font for buttons

        # Button definitions - adjusted positions
        self.button_y = HEIGHT + 50  # Button y-coordinate
        self.button_width = 180
        self.button_height = 40
        self.button_spacing = 30

        # Three buttons
        self.save_button = pygame.Rect((WIDTH - 3 * self.button_width - 2 * self.button_spacing) // 2,
                                       self.button_y, self.button_width, self.button_height)
        self.load_button = pygame.Rect(self.save_button.right + self.button_spacing,
                                       self.button_y, self.button_width, self.button_height)
        self.new_game_button = pygame.Rect(self.load_button.right + self.button_spacing,
                                           self.button_y, self.button_width, self.button_height)

    def draw_board(self):
        # Draw the Omok board
        board_surface = pygame.Surface((WIDTH - 2 * BOARD_PADDING, HEIGHT - 2 * BOARD_PADDING))
        board_surface.fill(BOARD_COLOR)

        # Simulate wood grain effect
        for i in range(0, board_surface.get_height(), 3):
            pygame.draw.line(board_surface, (220, 180, 133),
                             (0, i), (board_surface.get_width(), i))

        self.screen.blit(board_surface, (BOARD_PADDING, BOARD_PADDING))

        # Draw grid lines
        for i in range(BOARD_SIZE):
            # Vertical lines
            x = BOARD_PADDING + i * CELL_SIZE
            pygame.draw.line(self.screen, GRID_COLOR,
                             (x, BOARD_PADDING),
                             (x, HEIGHT - BOARD_PADDING), 1)
            # Horizontal lines
            y = BOARD_PADDING + i * CELL_SIZE
            pygame.draw.line(self.screen, GRID_COLOR,
                             (BOARD_PADDING, y),
                             (WIDTH - BOARD_PADDING, y), 1)

        # Enhanced star points
        star_points = [(3, 3), (3, 11), (11, 3), (11, 11), (7, 7)]
        for point in star_points:
            x = BOARD_PADDING + point[0] * CELL_SIZE
            y = BOARD_PADDING + point[1] * CELL_SIZE
            pygame.draw.circle(self.screen, GRID_COLOR, (x, y), 5)
            pygame.draw.circle(self.screen, (180, 146, 115), (x, y), 3)

    def draw_stones(self, board):
        # Draw the stones on the board
        for i in range(BOARD_SIZE):
            for j in range(BOARD_SIZE):
                if board[i][j] != 0:  # If there is a stone
                    x = BOARD_PADDING + j * CELL_SIZE
                    y = BOARD_PADDING + i * CELL_SIZE

                    # Enhanced shadow effect
                    shadow_offset = 3
                    pygame.draw.circle(self.screen, (100, 100, 100, 100),
                                       (x + shadow_offset, y + shadow_offset),
                                       CELL_SIZE // 2 - 4)

                    # Determine stone color
                    color = BLACK if board[i][j] == 1 else WHITE

                    # Main stone with gradient effect
                    pygame.draw.circle(self.screen, color, (x, y), CELL_SIZE // 2 - 4)

                    # Highlight effect on the stone
                    if board[i][j] == 1:  # Black stones
                        highlight_color = (80, 80, 80)
                        pygame.draw.circle(self.screen, highlight_color,
                                           (x - 4, y - 4), CELL_SIZE // 4, 2)
                    else:  # White stones
                        highlight_color = (220, 220, 220)
                        pygame.draw.circle(self.screen, highlight_color,
                                           (x - 4, y - 4), CELL_SIZE // 4, 2)

    def draw_button(self, text, rect, hover=False):
        # Button color with hover effect
        color = BUTTON_HOVER if hover else BUTTON_COLOR

        # Button shadow
        shadow_rect = rect.copy()
        shadow_rect.move_ip(2, 2)
        pygame.draw.rect(self.screen, (160, 126, 95, 128),
                         shadow_rect, border_radius=8)

        # Main button
        pygame.draw.rect(self.screen, color, rect, border_radius=8)
        pygame.draw.rect(self.screen, (160, 126, 95), rect, 2, border_radius=8)

        # Button text
        text_surf = self.font_button.render(text, True, TEXT_COLOR)
        text_rect = text_surf.get_rect(center=rect.center)
        self.screen.blit(text_surf, text_rect)

    def draw_status_bar(self, game_state, current_player, winner):
        # Status bar background
        status_bar_rect = pygame.Rect(0, HEIGHT, WIDTH, 100)
        pygame.draw.rect(self.screen, STATUS_BAR_COLOR, status_bar_rect)

        # Determine status text based on game state
        if game_state == "READY":
            status_text = "Click 'New Game' to start"
        elif game_state == "PLAYING":
            status_text = f"Current Player: {'Black' if current_player == 1 else 'White'}"
        else:  # "OVER"
            status_text = f"Game Over! {winner} wins!"

        # Draw status text
        status_surf = self.font_large.render(status_text, True, TEXT_COLOR)
        status_rect = status_surf.get_rect(center=(WIDTH // 2, HEIGHT + 25))
        self.screen.blit(status_surf, status_rect)

    def get_board_position(self, mouse_pos):
        x, y = mouse_pos
        if (BOARD_PADDING <= x <= WIDTH - BOARD_PADDING and
                BOARD_PADDING <= y <= HEIGHT - BOARD_PADDING):
            # Adjust click position to the nearest intersection
            col = round((x - BOARD_PADDING) / CELL_SIZE)
            row = round((y - BOARD_PADDING) / CELL_SIZE)
            if 0 <= row < BOARD_SIZE and 0 <= col < BOARD_SIZE:
                return row, col
        return None

    def update_screen(self, board,game_state, current_player, winner, hover_button):
        # Screen update
        self.screen.fill(BACKGROUND)
        self.draw_board()
        self.draw_stones(board)
        self.draw_status_bar(game_state, current_player, winner)

        # Draw buttons with hover effect
        self.draw_button("Save Game", self.save_button, hover_button == "save")
        self.draw_button("Load Game", self.load_button, hover_button == "load")
        self.draw_button("New Game", self.new_game_button, hover_button == "new")

        # Update the display
        pygame.display.flip()