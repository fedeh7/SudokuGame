from api import get_board_from_api
from sudoku import Sudoku9, Sudoku4


class Interface():

    def __init__(self):
        self.size = 9
        self.play = ""
        self.number = ""
        self.row = ""
        self.column = ""

    def get_size(self):
        size = ""
        while size not in ('4', '9'):
            size = input("\nWhat size do you want the board to be? Answer '4' or '9'\n").lower()
            if size not in ('4', '9'):
                print("Please answer with '4' or '9'\n")
        if size == "9":
            self.size = 9
            self.play = Sudoku9()
        elif size == "4":
            self.size = 4
            self.play = Sudoku4()

    def nice_board(self):
        nice = ""
        while nice not in ("y", "n"):
            nice = input("\nWould you like to play with a nicer board? (y, n)\n").lower()
            if nice not in ('y', 'n'):
                print("Please answer with 'y' or 'n'\n")
        if nice == "y":
            self.play.nice_board = True
        elif nice == "n":
            self.play.nice_board = False

    def set_game(self):
        self.get_size()
        self.play.set_board(get_board_from_api(self.size))
        self.nice_board()

    def start_playing(self):
        print("Game Starts!")
        while self.play.is_playing:
            print(self.play.board_print())
            self.user_inputs()
            self.play.play(self.number, self.row, self.column)
            if self.play.error != "":
                print("\n Error\n" + self.play.error)
        print(self.play.board_print())
        print("Congratulations! You Win!")

    def user_inputs(self):
        self.number = input("What number do you want to place? ")
        self.row = input("What row? ")
        self.column = input("What column? ")


if __name__ == "__main__":
    game = Interface()
    game.set_game()
    game.start_playing()
