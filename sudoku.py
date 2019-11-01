
class SudokuBase():
    def __init__(self, length, quadrant):
        self.is_playing = True
        self.board = []
        self.error = ""
        self.original_numbers = []
        self.board_column = []
        self.nice_board = False
        self.board_display = ""
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
        self.board_display = ""
        count_row = count_column = 0
        for row in range(self.length):
            count_row += 1
            for column in range(self.length):
                count_column += 1
                count_column = self.board_print_add_vertical_separators(column, count_column)
                self.board_print_add_values(row, column)
            count_row = self.board_print_add_horizontal_separators(row, count_row)
            count_column = 0
        return self.board_display

    def board_print_add_horizontal_separators(self, row, count_row):
        if row < self.length - 1 and count_row == self.quadrant_length:
            count_row = 0
            if self.length == 4:
                self.board_display = self.board_display + "\n----+----"
            elif self.length == 9:
                self.board_display = self.board_display + "\n------+------+------"
        return count_row

    def board_print_add_vertical_separators(self, column, count_column):
        if column == 0:
            self.board_display = self.board_display + "\n"
        elif count_column == self.quadrant_length + 1:
            count_column = 1
            self.board_display = self.board_display + " |"
        else:
            self.board_display = self.board_display + " "
        return count_column

    def board_print_add_values(self, row, column):
        if self.nice_board:
            if [row, column] in self.original_numbers:
                self.board_display = self.board_display + "\033[1m\033[4m"
            self.board_display = self.board_display + f"{self.board[row][column]}"
            if [row, column] in self.original_numbers:
                self.board_display = self.board_display + "\033[0m"
        else:
            self.board_display = self.board_display + f"{self.board[row][column]}"

    def verify_board(self):

        self.board_column = []
        self.set_column_board()
        ocurrences_row = ocurrences_column = empty_row = empty_column = 0
        for number in range(1, (self.length + 1)):
            for row in range(self.length):
                ocurrences_row = ocurrences_column = empty_column = empty_row = 0
                ocurrences_row = self.board[row].count(int(number))
                ocurrences_column = self.board_column[row].count(int(number))
                empty_column = self.board_column[row].count(" ")
                empty_row = self.board[row].count(" ")
                if ocurrences_row > 1 or ocurrences_column > 1 or empty_column > 0 or empty_row > 0:
                    return False
        return True

    def verify_quadrant(self):
        region = []
        for row_region in range(0, self.length, self.quadrant_length):
            for column_region in range(0, self.length, self.quadrant_length):
                region = self.get_region(row_region, column_region)
                for number in range(1, self.length + 1):
                    if region.count(int(number)) > 1 or region.count(" ") > 0:
                        return False

        return True

    def set_column_board(self):
        self.board_column = []
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
            self.error = f"Row or Column not between 1-{self.length}"
            return False
        if number < 1 or number > self.length:
            self.error = f"Number is not between 1-{self.length}"
            return False
        else:
            return True

    def verify_location(self, number, row, column):
        number = int(number)
        row = int(row) - 1
        column = int(column) - 1
        if self.verify_row(number, row) and self.verify_column(number, column) and self.verify_region(number, row, column):
            return True
        else:
            return False

    def verify_row(self, number, row):
        if number in self.board[row]:
            self.error = "Number already in Row!"
            return False
        else:
            return True

    def verify_column(self, number, column):
        self.board_column = []
        self.set_column_board()
        if number in self.board_column[column]:
            self.error = "Number already in Column!"
            return False
        else:
            return True

    def verify_region(self, number, row, column):
        region = []
        region = self.get_region(row, column)
        if number in region:
            self.error = "Number already in Region!"
            return False
        else:
            return True

    def get_region(self, row, column):
        region = []
        region_found = False
        for board_row in range(0, self.length, self.quadrant_length):
            for board_column in range(0, self.length, self.quadrant_length):
                if region_found:
                    return region
                region = []
                for region_row in range(self.quadrant_length):
                    for region_column in range(self.quadrant_length):
                        region.append(self.board[region_row + board_row][region_column + board_column])
                        if not region_found:
                            if row == (region_row + board_row) and column == (region_column + board_column):
                                region_found = True
        return region

    def check_if_original(self, row, column):
        if [int(row) - 1, int(column) - 1] in self.original_numbers:
            self.error = "Tried to replace an original number"
            return False
        else:
            return True

    def play(self, number, row, column):
        # Intenta ingresar un numero
        self.error = ""
        if self.verify_number(number, row, column):
            if self.check_if_original(row, column):
                if self.verify_location(number, row, column):
                    self.apply(number, row, column)
                    self.is_playing = self.win()

    def apply(self, number, row, column):
        number = int(number)
        row = int(row) - 1
        column = int(column) - 1
        self.board[row][column] = number

    def win(self):
        # Verifica que se haya completado bien el sudoku
        if self.verify_board() is True and self.verify_quadrant() is True:
            # print("Congratulations!")
            return False
        else:
            return True


class Sudoku9(SudokuBase):
    def __init__(self):
        super().__init__(9, 3)


class Sudoku4(SudokuBase):
    def __init__(self):
        super().__init__(4, 2)