from src.helpers import display_board
from src.actions import action1, action2

def main():
    choice = int(input("Please type 1 for one player mode, or 2 for two player mode"))
    while choice not in (1, 2):
        choice = int(input("Please type 1 for one player mode, or 2 for two player mode"))
    if choice == 2:
        display_board()
        action2()
    elif choice == 1:
        display_board()
        action1()   


if __name__ == "__main__":
    main()