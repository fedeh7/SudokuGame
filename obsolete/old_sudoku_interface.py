from sudoku import Sudoku9, Sudoku4
from api import get_board_from_api


def interface():
    number = row = column = selection = static = 0
    while selection != "4" and selection != "9":
        selection = input("What version do you want to play? input 4 or 9: ")
    while static != "y" and static != "n":
        static = input("Do you want to play with a static board?: ")
    if selection == "9":
        print("Starting Game")
        print("Rows and Colums go from 1 to 9, not from 0 to 8")
        game = Sudoku9()
        if static == "y":
            game.set_board([
                [5, 3, "", "", 7, "", "", "", ""],
                [6, "", "", 1, 9, 5, "", "", ""],
                ["", 9, 8, "", "", "", "", 6, ""],
                [8, "", "", "", 6, "", "", "", 3],
                [4, "", "", 8, "", 3, "", "", 1],
                [7, "", "", "", 2, "", "", "", 6],
                ["", 6, "", "", "", "", 2, 8, ""],
                ["", "", "", 4, 1, 9, "", "", 5],
                ["", "", "", "", 8, "", "", 7, 9]])
        elif static == "n":
            game.set_board(get_board_from_api(9))
        while game.is_playing:
            board = game.board_print()
            print(board)
            number = input("Wich number do you want to place?: ")
            row = input("Wich ROW: ")
            column = input("Wich COLUMN: ")
            game.play(number, row, column)

        print("Victory")

    elif selection == "4":
        print("Starting Game")
        print("Rows and Colums go from 1 to 4, not from 0 to 3")
        game = Sudoku4()
        if static == "y":
            game.set_board([
                ["", 3, 4, ""],
                [4, "", "", 2],
                [1, "", "", 3],
                ["", 2, 1, ""]])
        elif static == "n":
            game.set_board(get_board_from_api(4))
        while game.is_playing:
            board = game.board_print()
            print(board)
            number = input("Wich number do you want to place?: ")
            row = input("Wich ROW: ")
            column = input("Wich COLUMN: ")
            game.play(number, row, column)

        print("Victory")


interface()
