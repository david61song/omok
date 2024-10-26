import json
from datetime import datetime
from tkinter import Tk
from tkinter.filedialog import askopenfilename

# 게임 상태 저장 함수
def save_game(board, current_player):
    # 현재 시간을 기반으로 파일 이름 생성
    filename = datetime.now().strftime("%Y-%m-%d-%H-%M-%S.json")
    game_state_data = {
        'board': board,
        'current_player': current_player
    }
    # JSON 파일로 저장
    with open(filename, 'w') as f:
        json.dump(game_state_data, f)
    print(f"Game saved as {filename}.")

# 게임 불러오기 함수
def load_game(board, current_player, game_state):
    # Tkinter로 파일 선택 창 띄우기
    Tk().withdraw()  # Tkinter 기본 창 숨기기
    filename = askopenfilename(filetypes=[("JSON files", "*.json")])

    if filename:  # 파일이 선택되었을 때만 불러오기 진행
        try:
            # JSON 파일에서 게임 상태 불러오기
            with open(filename, 'r') as f:
                loaded_state = json.load(f)

            # 불러온 게임 상태를 현재 상태에 반영
            board[:] = loaded_state['board']
            current_player[0] = loaded_state['current_player']  # 리스트로 값 업데이트
            game_state[0] = "PLAYING"  # 게임 상태도 리스트로 업데이트
            print("Game loaded successfully.")
        except FileNotFoundError:
            print("Selected file not found.")
        except json.JSONDecodeError:
            print("Error decoding JSON file. Ensure the file format is correct.")
    else:
        print("No file selected.")

# 승리 기록 저장 함수
def save_winner(winner):
    try:
        # 기존 승리 기록 불러오기
        with open('winners.json', 'r') as f:
            winners = json.load(f)
    except FileNotFoundError:
        winners = []

    # 새로운 승리 기록 추가
    winners.append({
        'winner': winner,
        'date': datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    })

    # 업데이트된 기록 저장
    with open('winners.json', 'w') as f:
        json.dump(winners, f)
    print("Winner saved.")