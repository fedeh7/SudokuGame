
class SudokuBase():
    def __init__(self, length, quadrant):
        self.is_playing = True
        self.board = []
        self.error = ""
        self.original_numbers = []
        self.board_column = []
        self.length = length
        self.quadrant_length = quadrant

    def set_board(self, table):

        self.board = table
        self.set_Originals()

    def set_Originals(self):

        # Guardar coordenadas de numeros inmutables

        self.original_numbers = []

        for row in range(self.length):
            for column in range(self.length):
                if self.board[row][column] != " ":
                    self.original_numbers.append([row, column])

    def board_print(self):
        table = ""
        count_row = count_column = 0
        for row in range(self.length):
            count_row += 1
            for column in range(self.length):
                count_column += 1
                if column == 0:
                    table = table + f"\n{self.board[row][column]}"
                elif count_column == self.quadrant_length + 1:
                    count_column = 1
                    table = table + f" |{self.board[row][column]}"
                else:
                    table = table + f" {self.board[row][column]}"
            if row < self.length - 1:
                if count_row == self.quadrant_length:
                    count_row = 0
                    if self.length == 4:
                        table = table + "\n----+----"
                    elif self.length == 9:
                        table = table + "\n------+------+------"
            count_column = 0
        return table

    def verify_board(self):

        self.board_column = []
        self.set_column_board()
        ocurrences_row = ocurrences_column = empty_row = empty_column = number = 0
        for number in range(1, (self.length + 1)):
            for row in range(self.length):
                ocurrences_row = ocurrences_column = empty_column = empty_row = 0
                ocurrences_row = self.board[row].count(number)
                ocurrences_column = self.board_column[row].count(number)
                empty_column = self.board_column[row].count(" ")
                empty_row = self.board[row].count(" ")
                if ocurrences_row > 1 or ocurrences_column > 1 or empty_column > 0 or empty_row > 0:
                    return False
        return True

    def verify_quadrant(self):
        verifier_list = []
        pos_row = pos_column = 0

        for iteration in range(self.length):
            verifier_list = []
            for row in range(pos_row, self.quadrant_length + pos_row):
                for column in range(pos_column, self.quadrant_length + pos_column):
                    verifier_list.append(self.board[row][column])

            for number in range(1, self.length + 1):
                if verifier_list.count(number) > 1:
                    return False

            pos_column = pos_column + self.quadrant_length
            if pos_column >= self.length:
                pos_column = 0
                pos_row = pos_row + self.quadrant_length
        return True

    def set_column_board(self):
        column_numbers = []
        for column in range(self.length):
            column_numbers = []

            for row in range(self.length):
                column_numbers.append(self.board[row][column])

            self.board_column.append(column_numbers)

    def verify_number(self, number, row, column):
        try:
            number = int(number)
            row = int(row)
            column = int(column)
        except Exception:
            self.error = "Number, row, or column are NOT valid"
            return False
        if column > self.length or row > self.length or column < 1 or row < 1:
            
        if number < 1 or number > self.length:
            self.error = f"Number is not between 1-{self.length}"
            return False
        return True

    

    def play(self, number, row, column):
        # Intenta ingresar un numero
        self.error = ""
        if self.verify_number(number, row, column):
            self.apply(number, row, column)
            self.win()

    def apply(self, number, row, column):
        number = int(number)
        row = int(row) - 1
        column = int(column) - 1
        self.board[row][column] = number

    def win(self):
        # Verifica que se haya completado bien el sudoku
        if self.verify_board() is True and self.verify_quadrant() is True:
            # print("Congratulations!")
            self.is_playing = False
        else:
            return


class Sudoku9(SudokuBase):
    def __init__(self):
        super().__init__(9, 3)


class Sudoku4(SudokuBase):
    def __init__(self):
        super().__init__(4, 2)