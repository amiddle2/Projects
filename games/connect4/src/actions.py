from src.helpers import find_empty_slot, display_board, change_player, board, current_player, turn_count
from src.win_checks import check_win, check_almost_win
import random

def ai_logic(turn_count):
    print("Opponent's turn")
    # Two goals: block opposing wins, set up ai wins
    choices = {0, 1, 2, 3, 4, 5, 6}
    for choice in choices:
        if all(board[x][choice] != "_" for x in range(6)):
            choices.remove(choice)
    

    scores = {choice: 0 for choice in choices}

    # Blocking logic and winning logic, add scores to columns with the ability to either win or block wins
    if not check_almost_win():
        output = random.choice(list(choices))
    else:
        win_val, win_type, player = check_almost_win()
        row, col = win_val
        match win_type:
            # Horizontal and vertical cases have three checks: make sure the column to be scored is on the board, the ideal spot is empty, and the column to be scored hasn't been removed for being full
            case "x":
                if col != 0 and board[row][col - 1] == "_" and col - 1 in choices:
                    scores[col - 1] = 2 if player == "O" else 1
                if col < 4 and board[row][col + 3] == "_" and col + 3 in choices:
                    scores[col + 3] = 2 if player == "O" else 1
            case "y":
                if row != board[0] and board[row - 1][col] == "_" and col in choices:
                    scores[col] = 2 if player == "O" else 1
            case "ld":
                if col != 0 and row != board[0]: # Left column and top row are valid
                    if board[row - 1][col - 1] == "_" and board[row][col - 1] != "_": # Spot for play is blank and has support
                        scores[col - 1] = 2 if player == "O" else 1
                if col < 4 and row < 3: # Right column and bottom row are valid
                    if row == 2: # Placement needs support
                        if board[row + 1][col + 1] == "_" and board[row + 2][col + 1] != "_": # Spot for play is blank and has support
                            scores[col + 1] = 2 if player == "O" else 1
                    else: # Row does not need support
                        if board[row + 1][col + 1] == "_":
                            scores[col + 1] = 2 if player == "O" else 1
            case "rd":
                if col != 6 and row != board[0]: # Right column and top row are valid
                    if board[row - 1][col + 1] == "_" and board[row][col + 1] != "_": # Spot for play is blank and has support
                        scores[col + 1] = 2 if player == "O" else 1
                if col > 2 and row < 3: # Left column and bottom row are valid
                    if row == 2: # Placement needs support
                        if board[row + 1][col - 1] == "_" and board[row + 2][col - 1] != "_": # Spot for play is blank and has support
                            scores[col + 1] = 2 if player == "O" else 1
                    else: # Row does not need support
                        if board[row + 1][col - 1] == "_":
                            scores[col - 1] = 2 if player == "O" else 1

    max_weight = 0  
    output = 0 
    for column, weight in scores.items():
        if weight > max_weight:
            max_weight = weight
            output = column
    row_index = find_empty_slot(output)
    board[row_index][column] = "O"
    display_board()
    turn_count += 1
    if turn_count >= 7:
        if check_win():
            print("You lose")
            return
    action1()

def action1():
    global turn_count
    column = int(input(
        f"Choose which column to put your piece into (1-7)"
    ))
    if not isinstance(column, int) or column > 7 or column < 1:
        print("Warning! - Input must be a number 1-7")
        action1()
    row_index = find_empty_slot(column)
    if not row_index:
        action1()
    board[row_index][column - 1] = "X"
    display_board()
    turn_count += 1
    if turn_count >= 7:
        if check_win():
            print("You win!")
            return
    ai_logic(turn_count)



def action2():
    global turn_count, current_player
    column = input(
        f"{current_player}, Choose which column to put your piece into (1-7)"
    )
    while not column.isdigit():
        column = input(
            f"{current_player}, Choose which column to put your piece into (1-7)"
        )
    column = int(column)
       

    if not isinstance(column, int) or column > 7 or column < 1:
        print("Warning! - Input must be a number 1-7")
        action2()
    row_index = find_empty_slot(column=column)
    if not row_index:
        action2()
    board[row_index][column - 1] = current_player
    display_board()
    turn_count += 1
    if turn_count >= 7:
        if check_win():
            print(f"{current_player} has won!")
            return
    current_player = change_player(current_player)
    action2()