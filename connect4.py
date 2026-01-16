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


def check_win():
    def check_horizontal_win():
        for row in board:
            for i in range(4):
                if row[i] == row[i + 1] == row[i + 2] == row[i + 3] != "_":
                    return True
        return False

    def check_vertical_win():
        for column in range(7):
            for row in range(3):
                if (
                    board[row][column]
                    == board[row + 1][column]
                    == board[row + 2][column]
                    == board[row + 3][column]
                    != "_"
                ):
                    return True
        return False

    def check_left_diagonal_win():
        for row in range(3):
            for col in range(4):
                if (
                    board[row][col]
                    == board[row + 1][col + 1]
                    == board[row + 2][col + 2]
                    == board[row + 3][col + 3]
                    != "_"
                ):
                    return True
        return False

    def check_right_diagonal_win():
        for row in range(3):
            for col in range(1, 5):
                col *= -1
                if (
                    board[row][col]
                    == board[row + 1][col - 1]
                    == board[row + 2][col - 2]
                    == board[row + 3][col - 3]
                    != "_"
                ):
                    return True
        return False

    if check_horizontal_win():
        return True
    if check_vertical_win():
        return True
    if check_left_diagonal_win():
        return True
    if check_right_diagonal_win():
        return True
    return False


def find_empty_slot(column: int):
    index = column - 1
    
    for i in range(1, 7):
        i *= -1
        if board[i][index] == "_":
            output = i
            return output
    print("Selected column is full! Please choose another")
    return False


def action():
    global turn_count, current_player
    column = int(input(
        f"{current_player}, Choose which column to put your piece into (1-7)"
    ))
    if not isinstance(column, int) or column > 7 or column < 1:
        print("Warning! - Input must be a number 1-7")
        action()
    row_index = find_empty_slot(column=column)
    if not row_index:
        action()
    board[row_index][column - 1] = current_player
    display_board()
    turn_count += 1
    if turn_count >= 7:
        if check_win():
            print(f"{current_player} has won!")
            return
    current_player = change_player(current_player)
    action()


if __name__ == "__main__":
    display_board()
    action()
