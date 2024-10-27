import json
from datetime import datetime
from tkinter import Tk
from tkinter.filedialog import askopenfilename

# Save game state function
def save_game(board, current_player):
    # Create filename with current date and time
    filename = datetime.now().strftime("%Y-%m-%d-%H-%M-%S.json")
    game_state_data = {
        'board': board,
        'current_player': current_player
    }
    # Save game state data to JSON file
    with open(filename, 'w') as f:
        json.dump(game_state_data, f)
    print(f"Game saved as {filename}.")

# Load game function
def load_game(board, current_player, game_state):
    # Tkinter to select file
    Tk().withdraw()  # Hide Tkinter default window
    filename = askopenfilename(filetypes=[("JSON files", "*.json")])

    if filename:  # If file is selected
        try:
            # Load game state from JSON file
            with open(filename, 'r') as f:
                loaded_state = json.load(f)

            # Update board and current player
            board[:] = loaded_state['board']
            current_player = loaded_state['current_player']  
            game_state = "PLAYING" 
            print("Game loaded successfully.")
        except FileNotFoundError:
            print("Selected file not found.")
        except json.JSONDecodeError:
            print("Error decoding JSON file. Ensure the file format is correct.")
    else:
        print("No file selected.")

# Save winner function
def save_winner(winner):
    try:
        # Load existing winners
        with open('winners.json', 'r') as f:
            winners = json.load(f)
    except FileNotFoundError:
        winners = []

    # Add new winner
    winners.append({
        'winner': winner,
        'date': datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    })

    # Save updated winners
    with open('winners.json', 'w') as f:
        json.dump(winners, f)
    print("Winner saved.")