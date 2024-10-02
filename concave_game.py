import pygame
import sys
import json
from datetime import datetime

# 초기화
pygame.init()

# 상수
WIDTH, HEIGHT = 600, 600  # 15x15 보드에 맞게 크기 조정
BOARD_SIZE = 15
CELL_SIZE = WIDTH // BOARD_SIZE
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
BROWN = (139, 69, 19)
GRAY = (200, 200, 200)
LIGHT_GRAY = (220, 220, 220)

# 화면 설정
screen = pygame.display.set_mode((WIDTH, HEIGHT + 50))  # 버튼을 위한 추가 공간
pygame.display.set_caption("오목 게임")

# 게임 보드 초기화
board = [[0 for _ in range(BOARD_SIZE)] for _ in range(BOARD_SIZE)]
current_player = 1

# 게임 상태
game_state = "READY"  # "READY", "PLAYING", "OVER"

# 폰트 설정
font = pygame.font.Font(None, 36)

def draw_board():
    screen.fill(BROWN)
    for i in range(BOARD_SIZE):
        pygame.draw.line(screen, BLACK, (CELL_SIZE // 2, i * CELL_SIZE + CELL_SIZE // 2),
                         (WIDTH - CELL_SIZE // 2, i * CELL_SIZE + CELL_SIZE // 2))
        pygame.draw.line(screen, BLACK, (i * CELL_SIZE + CELL_SIZE // 2, CELL_SIZE // 2),
                         (i * CELL_SIZE + CELL_SIZE // 2, HEIGHT - CELL_SIZE // 2))

def draw_stones():
    for i in range(BOARD_SIZE):
        for j in range(BOARD_SIZE):
            if board[i][j] == 1:
                pygame.draw.circle(screen, BLACK, (j * CELL_SIZE + CELL_SIZE // 2, i * CELL_SIZE + CELL_SIZE // 2), CELL_SIZE // 2 - 2)
            elif board[i][j] == 2:
                pygame.draw.circle(screen, WHITE, (j * CELL_SIZE + CELL_SIZE // 2, i * CELL_SIZE + CELL_SIZE // 2), CELL_SIZE // 2 - 2)

def check_win(row, col):
    directions = [(0, 1), (1, 0), (1, 1), (1, -1)]
    for dr, dc in directions:
        count = 1
        for i in range(1, 5):
            r, c = row + dr * i, col + dc * i
            if 0 <= r < BOARD_SIZE and 0 <= c < BOARD_SIZE and board[r][c] == current_player:
                count += 1
            else:
                break
        for i in range(1, 5):
            r, c = row - dr * i, col - dc * i
            if 0 <= r < BOARD_SIZE and 0 <= c < BOARD_SIZE and board[r][c] == current_player:
                count += 1
            else:
                break
        if count >= 5:
            return True
    return False

def save_game():
    game_state = {
        'board': board,
        'current_player': current_player
    }
    with open('game_state.json', 'w') as f:
        json.dump(game_state, f)
    print("게임이 저장되었습니다.")

def load_game():
    global board, current_player, game_state
    try:
        with open('game_state.json', 'r') as f:
            loaded_state = json.load(f)
        board = loaded_state['board']
        current_player = loaded_state['current_player']
        game_state = "PLAYING"
        print("게임을 불러왔습니다.")
    except FileNotFoundError:
        print("저장된 게임을 찾을 수 없습니다.")

def save_winner(winner):
    try:
        with open('winners.json', 'r') as f:
            winners = json.load(f)
    except FileNotFoundError:
        winners = []
    
    winners.append({
        'winner': winner,
        'date': datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    })
    
    with open('winners.json', 'w') as f:
        json.dump(winners, f)

def draw_button(text, x, y, w, h, color, text_color):
    pygame.draw.rect(screen, color, (x, y, w, h))
    text_surf = font.render(text, True, text_color)
    text_rect = text_surf.get_rect(center=(x + w // 2, y + h // 2))
    screen.blit(text_surf, text_rect)

def is_button_clicked(mouse_pos, button_rect):
    return button_rect.collidepoint(mouse_pos)

# 버튼 정의
save_button = pygame.Rect(50, HEIGHT + 10, 150, 30)
load_button = pygame.Rect(225, HEIGHT + 10, 150, 30)
new_game_button = pygame.Rect(400, HEIGHT + 10, 150, 30)

# 메인 게임 루프
running = True
winner = None

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            mouse_pos = pygame.mouse.get_pos()
            if game_state == "PLAYING" and mouse_pos[1] < HEIGHT:
                col = mouse_pos[0] // CELL_SIZE
                row = mouse_pos[1] // CELL_SIZE
                
                if board[row][col] == 0:
                    board[row][col] = current_player
                    if check_win(row, col):
                        game_state = "OVER"
                        winner = "흑" if current_player == 1 else "백"
                        print(f"{winner}돌 승리!")
                        save_winner(winner)
                    else:
                        current_player = 3 - current_player  # Switch player (1 -> 2 or 2 -> 1)
            else:
                if is_button_clicked(mouse_pos, save_button):
                    save_game()
                elif is_button_clicked(mouse_pos, load_button):
                    load_game()
                elif is_button_clicked(mouse_pos, new_game_button):
                    board = [[0 for _ in range(BOARD_SIZE)] for _ in range(BOARD_SIZE)]
                    current_player = 1
                    game_state = "PLAYING"
                    winner = None
                    print("새 게임을 시작합니다.")

    # 화면 그리기
    screen.fill(BROWN)
    draw_board()
    draw_stones()

    # 버튼 그리기 (항상 그리도록 수정)
    draw_button("저장", *save_button, GRAY, BLACK)
    draw_button("불러오기", *load_button, GRAY, BLACK)
    draw_button("새 게임", *new_game_button, GRAY, BLACK)

    # 게임 상태 텍스트 표시
    if game_state == "READY":
        status_text = "게임을 시작하려면 '새 게임'을 클릭하세요"
    elif game_state == "PLAYING":
        status_text = f"현재 플레이어: {'흑' if current_player == 1 else '백'}"
    else:  # "OVER"
        status_text = f"게임 종료! {winner}돌 승리!"
    
    status_surf = font.render(status_text, True, BLACK)
    status_rect = status_surf.get_rect(center=(WIDTH // 2, HEIGHT + 25))
    screen.blit(status_surf, status_rect)

    pygame.display.flip()

pygame.quit()
sys.exit()