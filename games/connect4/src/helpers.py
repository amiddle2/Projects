board = [
    ["_", "_", "_", "_", "_", "_", "_"],
    ["_", "_", "_", "_", "_", "_", "_"],
    ["_", "_", "_", "_", "_", "_", "_"],
    ["_", "_", "_", "_", "_", "_", "_"],
    ["_", "_", "_", "_", "_", "_", "_"],
    ["_", "_", "_", "_", "_", "_", "_"],
]

current_player = "X"
turn_count = 0

def display_board():
    for row in board:
        print(*row)


def change_player(current_player):
    current_player = "X" if current_player == "O" else "O"
    return current_player

def find_empty_slot(column: int):
    index = column - 1
    
    for i in range(1, 7):
        i *= -1
        if board[i][index] == "_":
            output = i
            return output
    print("Selected column is full! Please choose another")
    return False