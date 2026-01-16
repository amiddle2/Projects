from src.helpers import board

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


def check_almost_win():
    def check_almost_horizontal():
        for row in board:
            for col in range(4):
                if row[col] == row[col + 1] == row[col + 2] != "_":
                    return row, col, row[col]
        return False
    
    def check_almost_vertical():
        for col in range(7):
            for row in range(3):
                if (
                    board[row][col]
                    == board[row + 1][col]
                    == board[row + 2][col]
                    != "_"
                ):
                    return row, col, board[row][col]
        return False

    def check_almost_left_diagonal():
        for row in range(3):
            for col in range(4):
                if (
                    board[row][col]
                    == board[row + 1][col + 1]
                    == board[row + 2][col + 2]
                    != "_"
                ):
                    return row, col, board[row][col]
        return False   

    def check_almost_right_diagonal():
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
                    return row, col, board[row][col]
        return False 
    
    if x := check_almost_horizontal():
        return x, "x"
    if x := check_almost_vertical():
        return x, "y"
    if x := check_almost_left_diagonal():
        return x, "ld"
    if x := check_almost_right_diagonal():
        return x, "rd"
    return False