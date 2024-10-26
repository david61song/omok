import pygame
import sys
from gamescreen import *
from load_util import save_game, load_game, save_winner

# Game initialization
board = [[0 for _ in range(BOARD_SIZE)] for _ in range(BOARD_SIZE)]  # Empty board
current_player = [1]  # 현재 플레이어를 리스트로 저장하여 값 변경 가능
game_state = ["READY"]  # 게임 상태를 리스트로 저장하여 값 변경 가능

# Create an instance of Gamescreen
pygame.init()
gamescreen = Gamescreen()

# Main game loop
running = True
winner = None
hover_button = None

def check_win(row, col):
    # Check for winning condition in directions (horizontal, vertical, diagonal)
    directions = [(0, 1), (1, 0), (1, 1), (1, -1)]
    for dr, dc in directions:
        count = 1
        # Check in one direction
        for i in range(1, 5):
            r, c = row + dr * i, col + dc * i
            if 0 <= r < BOARD_SIZE and 0 <= c < BOARD_SIZE and board[r][c] == current_player[0]:
                count += 1
            else:
                break
        # Check in the opposite direction
        for i in range(1, 5):
            r, c = row - dr * i, col - dc * i
            if 0 <= r < BOARD_SIZE and 0 <= c < BOARD_SIZE and board[r][c] == current_player[0]:
                count += 1
            else:
                break
        # If 5 or more stones are connected, return True
        if count >= 5:
            return True
    return False

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        elif event.type == pygame.MOUSEBUTTONDOWN:
            mouse_pos = pygame.mouse.get_pos()

            # If the game is in progress and the click is on the board area
            if game_state[0] == "PLAYING" and mouse_pos[1] < HEIGHT:
                board_pos = gamescreen.get_board_position(mouse_pos)
                if board_pos:
                    row, col = board_pos
                    if board[row][col] == 0:  # If the cell is empty
                        board[row][col] = current_player[0]  # Place the stone

                        # Check for win
                        if check_win(row, col):
                            game_state[0] = "OVER"
                            winner = "Black" if current_player[0] == 1 else "White"
                            save_winner(winner)
                        else:
                            # Switch to the next player
                            current_player[0] = 3 - current_player[0]

            # Handle button clicks
            else:
                if gamescreen.save_button.collidepoint(mouse_pos):
                    save_game(board, current_player[0])
                elif gamescreen.load_button.collidepoint(mouse_pos):
                    load_game(board, current_player, game_state)
                    winner = None  # Reset winner since we're loading a game
                elif gamescreen.new_game_button.collidepoint(mouse_pos):
                    # Start a new game
                    board = [[0 for _ in range(BOARD_SIZE)] for _ in range(BOARD_SIZE)]
                    current_player[0] = 1
                    game_state[0] = "PLAYING"
                    winner = None

        # Mouse movement for hover effect on buttons
        elif event.type == pygame.MOUSEMOTION:
            mouse_pos = pygame.mouse.get_pos()
            if gamescreen.save_button.collidepoint(mouse_pos):
                hover_button = "save"
            elif gamescreen.load_button.collidepoint(mouse_pos):
                hover_button = "load"
            elif gamescreen.new_game_button.collidepoint(mouse_pos):
                hover_button = "new"
            else:
                hover_button = None

    # Screen update
    gamescreen.screen.fill(BACKGROUND)
    gamescreen.draw_board()
    gamescreen.draw_stones(board)
    gamescreen.draw_status_bar(game_state[0], current_player[0], winner)

    # Draw buttons with hover effect
    gamescreen.draw_button("Save Game", gamescreen.save_button, hover_button == "save")
    gamescreen.draw_button("Load Game", gamescreen.load_button, hover_button == "load")
    gamescreen.draw_button("New Game", gamescreen.new_game_button, hover_button == "new")

    # Update the display
    pygame.display.flip()

# Quit the game
pygame.quit()
sys.exit()