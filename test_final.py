import unittest
import unittest.mock
from api import get_board_from_api
from parameterized import parameterized
from sudoku_interface import Interface
from sudoku import Sudoku4, Sudoku9


class Test_api(unittest.TestCase):

    def test_board_size_9(self):
        board = get_board_from_api(9)
        self.assertEqual(len(board), 9)
        for column in range(9):
            self.assertEqual(len(board[column]), 9)

    def test_board_size_4(self):
        board = get_board_from_api(4)
        self.assertEqual(len(board), 4)
        for column in range(4):
            self.assertEqual(len(board[column]), 4)

    @parameterized.expand([
        (-1,),
        (0,),
        (1,),
        (2,),
        (3,),
        (5,),
        (6,),
        (7,),
        (8,),
        (10,),
        ("10",),
        ("ten",),
        ("",),
        ("4.5",),
        ("cuatro",),
        (44,),
        (99,),
    ])
    def test_invalid_board_size_parameterized(self, value):
        board = get_board_from_api(value)
        self.assertEqual(board, "Invalid size")

##################################################################################################
##################################### Interface ##################################################
##################################################################################################


class Test_interface(unittest.TestCase):

    def setUp(self):
        self.board_4_start = [
            [" ", 3, 4, " "],
            [4, " ", " ", 2],
            [1, " ", " ", 3],
            [" ", 2, 1, " "]]
        self.board_4_end = [
            [2, 3, 4, 1],
            [4, 1, 3, 2],
            [1, 4, 2, 3],
            [3, 2, 1, " "]]
        self.board_9_start = [
            [5, 3, " ", " ", 7, " ", " ", " ", " "],
            [6, " ", " ", 1, 9, 5, " ", " ", " "],
            [" ", 9, 8, " ", " ", " ", " ", 6, " "],
            [8, " ", " ", " ", 6, " ", " ", " ", 3],
            [4, " ", " ", 8, " ", 3, " ", " ", 1],
            [7, " ", " ", " ", 2, " ", " ", " ", 6],
            [" ", 6, " ", " ", " ", " ", 2, 8, " "],
            [" ", " ", " ", 4, 1, 9, " ", " ", 5],
            [" ", " ", " ", " ", 8, " ", " ", 7, 9]]
        self.board_9_end = [
            [5, 3, 4, 6, 7, 8, 9, 1, 2],
            [6, 7, 2, 1, 9, 5, 3, 4, 8],
            [1, 9, 8, 3, 4, 2, 5, 6, 7],
            [8, 5, 9, 7, 6, 1, 4, 2, 3],
            [4, 2, 6, 8, 5, 3, 7, 9, 1],
            [7, 1, 3, 9, 2, 4, 8, 5, 6],
            [9, 6, 1, 5, 3, 7, 2, 8, 4],
            [2, 8, 7, 4, 1, 9, 6, 3, 5],
            [3, 4, 5, 2, 8, 6, " ", 7, 9]]
        self.game = Interface()

    @unittest.mock.patch("builtins.input", side_effect=["4", "n"])
    def test_sudoku4_start(self, mock):
        self.game.set_game()
        self.assertEqual(self.game.size, 4)
        self.assertEqual(len(self.game.play.board[0]), 4)
        self.assertEqual(self.game.play.__class__.__name__, "Sudoku4")

    @unittest.mock.patch("builtins.input", side_effect=["9", "n"])
    def test_sudoku9_start(self, mock):
        self.game.set_game()
        self.assertEqual(self.game.size, 9)
        self.assertEqual(len(self.game.play.board[0]), 9)
        self.assertEqual(self.game.play.__class__.__name__, "Sudoku9")

    @unittest.mock.patch("builtins.input", side_effect=["1", "2", "3"])
    def test_inputs(self, mock):
        self.game.user_inputs()
        self.assertEqual(self.game.number, "1")
        self.assertEqual(self.game.row, "2")
        self.assertEqual(self.game.column, "3")

    @unittest.mock.patch("builtins.input", side_effect=["4", "y"])
    def test_nice_board_true_4x4(self, mock):
        self.game.set_game()
        self.assertTrue(self.game.play.nice_board)

    @unittest.mock.patch("builtins.input", side_effect=["4", "n"])
    def test_nice_board_false_4x4(self, mock):
        self.game.set_game()
        self.assertFalse(self.game.play.nice_board)

    @unittest.mock.patch("builtins.input", side_effect=["9", "y"])
    def test_nice_board_true_9x9(self, mock):
        self.game.set_game()
        self.assertTrue(self.game.play.nice_board)

    @unittest.mock.patch("builtins.input", side_effect=["9", "n"])
    def test_nice_board_true_9x9(self, mock):
        self.game.set_game()
        self.assertFalse(self.game.play.nice_board)

    @unittest.mock.patch("builtins.input", side_effect=["4","n", "4", "4", "4"])
    def test_sudoku4_endgame(self, mock):
        self.game.set_game()
        self.game.play.set_board(self.board_4_end)
        self.assertEqual(self.game.size, 4)
        self.assertEqual(len(self.game.play.board[0]), 4)
        self.assertTrue(self.game.play.is_playing)
        self.game.start_playing()
        self.assertFalse(self.game.play.is_playing)

    @unittest.mock.patch("builtins.input", side_effect=["9","n", "1", "9", "7"])
    def test_sudoku9_endgame(self, mock):
        self.game.set_game()
        self.game.play.set_board(self.board_9_end)
        self.assertEqual(self.game.size, 9)
        self.assertEqual(len(self.game.play.board[0]), 9)
        self.assertTrue(self.game.play.is_playing)
        self.game.start_playing()
        self.assertFalse(self.game.play.is_playing)

##################################################################################################
##################################### Sudoku 9x9 #################################################
##################################################################################################


class Test_Sudoku9(unittest.TestCase):

    def setUp(self):
        self.board_start = [
            [5, 3, " ", " ", 7, " ", " ", " ", " "],
            [6, " ", " ", 1, 9, 5, " ", " ", " "],
            [" ", 9, 8, " ", " ", " ", " ", 6, " "],
            [8, " ", " ", " ", 6, " ", " ", " ", 3],
            [4, " ", " ", 8, " ", 3, " ", " ", 1],
            [7, " ", " ", " ", 2, " ", " ", " ", 6],
            [" ", 6, " ", " ", " ", " ", 2, 8, " "],
            [" ", " ", " ", 4, 1, 9, " ", " ", 5],
            [" ", " ", " ", " ", 8, " ", " ", 7, 9]]
        self.board_end = [
            [5, 3, 4, 6, 7, 8, 9, 1, 2],
            [6, 7, 2, 1, 9, 5, 3, 4, 8],
            [1, 9, 8, 3, 4, 2, 5, 6, 7],
            [8, 5, 9, 7, 6, 1, 4, 2, 3],
            [4, 2, 6, 8, 5, 3, 7, 9, 1],
            [7, 1, 3, 9, 2, 4, 8, 5, 6],
            [9, 6, 1, 5, 3, 7, 2, 8, 4],
            [2, 8, 7, 4, 1, 9, 6, 3, 5],
            [3, 4, 5, 2, 8, 6, " ", 7, 9]]
        self.juego = Sudoku9()

    def test_board_set(self):
        self.juego.set_board(self.board_start)
        self.assertEqual(self.juego.board, self.board_start)
        self.assertEqual(self.juego.original_numbers,
            [[0, 0], [0, 1], [0, 4], [1, 0], [1, 3], [1, 4],
            [1, 5], [2, 1], [2, 2], [2, 7], [3, 0], [3, 4],
            [3, 8], [4, 0], [4, 3], [4, 5], [4, 8], [5, 0],
            [5, 4], [5, 8], [6, 1], [6, 6], [6, 7], [7, 3],
            [7, 4], [7, 5], [7, 8], [8, 4], [8, 7], [8, 8]])
        self.assertTrue(self.juego.is_playing)

    @parameterized.expand([
        (0, 0),
        (0, 1),
        (0, 4),
        (1, 0),
        (5, 4),
        (5, 8),
        (6, 1),
        (6, 6),
        (6, 7),
        (7, 3),
        (7, 4),
        (7, 5),
        (7, 8),
        (8, 4),
        (8, 7),
        (8, 8),
    ])
    def test_check_if_original_is_original(self, row, column):
        # False means it is an original number
        self.juego.set_board(self.board_start)
        self.assertFalse(self.juego.check_if_original(row + 1, column + 1))

    @parameterized.expand([
        (0, 2),
        (0, 3),
        (0, 5),
        (1, 1),
        (5, 5),
        (5, 1),
        (6, 0),
        (6, 2),
        (6, 3),
        (7, 0),
        (7, 1),
        (7, 2),
        (7, 6),
        (8, 0),
        (8, 1),
        (8, 2),
    ])
    def test_check_if_original_not_original(self, row, column):
        # True means it is not an original number
        self.juego.set_board(self.board_start)
        self.assertTrue(self.juego.check_if_original(row + 1, column + 1))

    @parameterized.expand([
        (1, 1, [5, 3, " ", 6, " ", " ", " ", 9, 8]),
        (1, 5, [' ', 7, ' ', 1, 9, 5, ' ', ' ', ' ']),
        (1, 8, [' ', ' ', ' ', ' ', ' ', ' ', ' ', 6, ' ']),
        (4, 2, [8, ' ', ' ', 4, ' ', ' ', 7, ' ', ' ']),
        (4, 4, [' ', 6, ' ', 8, ' ', 3, ' ', 2, ' ']),
        (4, 9, [' ', ' ', 3, ' ', ' ', 1, ' ', ' ', 6]),
        (7, 3, [' ', 6, ' ', ' ', ' ', ' ', ' ', ' ', ' ']),
        (7, 6, [' ', ' ', ' ', 4, 1, 9, ' ', 8, ' ']),
        (7, 7, [2, 8, ' ', ' ', ' ', 5, ' ', 7, 9])
    ])
    def test_get_region(self, row, column, region):
        self.juego.set_board(self.board_start)
        self.assertEqual(self.juego.get_region(row - 1, column - 1), region)

    @parameterized.expand([
        (5, 1, 3),
        (4, 5, 3),
        (9, 8, 3),
        (8, 2, 3),
        (2, 7, 5),
        (8, 7, 5),
        (6, 7, 5),
        (1, 7, 5),
        (9, 9, 1)
    ])
    def test_verify_location_invalid(self, num, row, column):
        self.juego.set_board(self.board_start)
        self.assertFalse(self.juego.verify_location(num, row, column))

    @parameterized.expand([
        (4, 1, 3),
        (6, 1, 4),
        (8, 1, 6),
        (9, 1, 7),
        (1, 1, 8),
        (2, 1, 9),
        (7, 2, 2),
        (2, 2, 3),
        (3, 2, 7),
        (4, 2, 8),
        (8, 2, 9),
        (1, 3, 1),
        (3, 3, 4),
    ])
    def test_verify_location_valid(self, num, row, column):
        self.juego.set_board(self.board_start)
        self.assertTrue(self.juego.verify_location(num, row, column))

    @parameterized.expand([
        (5, 1),
        (6, 2),
        (9, 3),
        (8, 4),
        (4, 5),
        (7, 6),
        (6, 7),
        (4, 8),
        (8, 9)
    ])
    def test_verify_row_invalid(self, num, row):
        self.juego.set_board(self.board_start)
        self.assertFalse(self.juego.verify_row(num, row - 1))

    @parameterized.expand([
        (1, 1),
        (2, 2),
        (3, 3),
        (4, 4),
        (5, 5),
        (8, 6),
        (9, 7),
        (6, 8),
        (2, 9)
    ])
    def test_verify_row_valid(self, num, row):
        self.juego.set_board(self.board_start)
        self.assertTrue(self.juego.verify_row(num, row - 1))

    @parameterized.expand([
        (5, 1),
        (3, 2),
        (8, 3),
        (1, 4),
        (7, 5),
        (5, 6),
        (2, 7),
        (6, 8),
        (3, 9)
    ])
    def test_verify_column_invalid(self, num, column):
        self.juego.set_board(self.board_start)
        self.assertFalse(self.juego.verify_column(num, column - 1))

    @parameterized.expand([
        (1, 1),
        (2, 2),
        (3, 3),
        (5, 4),
        (4, 5),
        (6, 6),
        (7, 7),
        (9, 8),
        (8, 9)
    ])
    def test_verify_column_valid(self, num, column):
        self.juego.set_board(self.board_start)
        self.assertTrue(self.juego.verify_column(num, column - 1))

    @parameterized.expand([
        (5, 1, 1),
        (7, 2, 4),
        (6, 3, 7),
        (8, 4, 2),
        (6, 5, 5),
        (3, 6, 8),
        (6, 7, 3),
        (4, 8, 6),
        (2, 9, 9)
    ])
    def test_verify_region_invalid(self, num, row, column):
        self.juego.set_board(self.board_start)
        self.assertFalse(self.juego.verify_region(num, row - 1, column - 1))

    @parameterized.expand([
        (1, 1, 1),
        (2, 2, 4),
        (3, 3, 7),
        (5, 4, 2),
        (7, 5, 5),
        (8, 6, 8),
        (9, 7, 3),
        (2, 8, 6),
        (3, 9, 9)
    ])
    def test_verify_region_valid(self, num, row, column):
        self.juego.set_board(self.board_start)
        self.assertTrue(self.juego.verify_region(num, row - 1, column - 1))

    def test_set_column_board(self):
        self.juego.set_board(self.board_start)
        self.juego.set_column_board()
        self.assertEqual(self.juego.board_column, [[5, 6, ' ', 8, 4, 7, ' ', ' ', ' '], 
                                                    [3, ' ', 9, ' ', ' ', ' ', 6, ' ', ' '], 
                                                    [' ', ' ', 8, ' ', ' ', ' ', ' ', ' ', ' '], 
                                                    [' ', 1, ' ',' ', 8, ' ', ' ', 4, ' '], 
                                                    [7, 9, ' ', 6, ' ', 2, ' ', 1, 8], 
                                                    [' ', 5, ' ', ' ', 3, ' ', ' ', 9, ' '], 
                                                    [' ', ' ', ' ', ' ', ' ', ' ', 2, ' ', ' '], 
                                                    [' ', ' ', 6, ' ', ' ', ' ', 8, ' ', 7], 
                                                    [' ', ' ', ' ', 3, 1, 6, ' ', 5, 9]])

    def test_place_valid_number(self):
        self.juego.set_board(self.board_start)
        self.juego.play(1, 1, 3)
        self.assertTrue(self.juego.is_playing)
        self.assertEqual(self.juego.board, [
            [5, 3, 1, " ", 7, " ", " ", " ", " "],
            [6, " ", " ", 1, 9, 5, " ", " ", " "],
            [" ", 9, 8, " ", " ", " ", " ", 6, " "],
            [8, " ", " ", " ", 6, " ", " ", " ", 3],
            [4, " ", " ", 8, " ", 3, " ", " ", 1],
            [7, " ", " ", " ", 2, " ", " ", " ", 6],
            [" ", 6, " ", " ", " ", " ", 2, 8, " "],
            [" ", " ", " ", 4, 1, 9, " ", " ", 5],
            [" ", " ", " ", " ", 8, " ", " ", 7, 9]])

    def test_place_wrong_number_row(self):
        self.juego.set_board(self.board_start)
        self.juego.play(3, 1, 4)
        self.assertTrue(self.juego.is_playing)
        self.assertEqual(self.juego.error, "Number already in Row!")

    def test_place_wrong_number_column(self):
        self.juego.set_board(self.board_start)
        self.juego.play(3, 6, 2)
        self.assertTrue(self.juego.is_playing)
        self.assertEqual(self.juego.error, "Number already in Column!")

    def test_place_wrong_number_region(self):
        self.juego.set_board(self.board_start)
        self.juego.play(7, 5, 2)
        self.assertTrue(self.juego.is_playing)
        self.assertEqual(self.juego.error, "Number already in Region!")

    def test_replace_unoriginal_number(self):
        self.juego.set_board(self.board_start)
        self.juego.play(1, 1, 3)
        self.assertEqual(self.juego.board, [
            [5, 3, 1, " ", 7, " ", " ", " ", " "],
            [6, " ", " ", 1, 9, 5, " ", " ", " "],
            [" ", 9, 8, " ", " ", " ", " ", 6, " "],
            [8, " ", " ", " ", 6, " ", " ", " ", 3],
            [4, " ", " ", 8, " ", 3, " ", " ", 1],
            [7, " ", " ", " ", 2, " ", " ", " ", 6],
            [" ", 6, " ", " ", " ", " ", 2, 8, " "],
            [" ", " ", " ", 4, 1, 9, " ", " ", 5],
            [" ", " ", " ", " ", 8, " ", " ", 7, 9]])
        self.juego.play(2, 1, 3)
        self.assertTrue(self.juego.is_playing)
        self.assertEqual(self.juego.board, [
            [5, 3, 2, " ", 7, " ", " ", " ", " "],
            [6, " ", " ", 1, 9, 5, " ", " ", " "],
            [" ", 9, 8, " ", " ", " ", " ", 6, " "],
            [8, " ", " ", " ", 6, " ", " ", " ", 3],
            [4, " ", " ", 8, " ", 3, " ", " ", 1],
            [7, " ", " ", " ", 2, " ", " ", " ", 6],
            [" ", 6, " ", " ", " ", " ", 2, 8, " "],
            [" ", " ", " ", 4, 1, 9, " ", " ", 5],
            [" ", " ", " ", " ", 8, " ", " ", 7, 9]])

    @parameterized.expand([
        (1, 1),
        (1, 2),
        (1, 5),
        (2, 1),
        (2, 4),
        (2, 5),
        (2, 6),
        (3, 2),
        (3, 3),
        (3, 8),
        (4, 1),
        (4, 5),
        (4, 9),
        (5, 1),
        (5, 4),
    ])
    def test_try_to_replace_original_number(self, row, column):
        self.juego.set_board(self.board_start)
        self.juego.play(1, row, column)
        self.assertTrue(self.juego.is_playing)
        self.assertEqual(self.juego.board, self.board_start)
        self.assertEqual(self.juego.error, "Tried to replace an original number")

    def test_victory(self):
        self.juego.set_board(self.board_end)
        self.juego.play(1, 9, 7)
        self.assertFalse(self.juego.is_playing)
        self.assertEqual(self.juego.board, [
            [5, 3, 4, 6, 7, 8, 9, 1, 2],
            [6, 7, 2, 1, 9, 5, 3, 4, 8],
            [1, 9, 8, 3, 4, 2, 5, 6, 7],
            [8, 5, 9, 7, 6, 1, 4, 2, 3],
            [4, 2, 6, 8, 5, 3, 7, 9, 1],
            [7, 1, 3, 9, 2, 4, 8, 5, 6],
            [9, 6, 1, 5, 3, 7, 2, 8, 4],
            [2, 8, 7, 4, 1, 9, 6, 3, 5],
            [3, 4, 5, 2, 8, 6, 1, 7, 9]])

    @parameterized.expand([
        ("hola", "Number, row, or column are NOT valid"),
        (10, "Number is not between 1-9"),
        (0, "Number is not between 1-9"),
        (11, "Number is not between 1-9"),
        (33, "Number is not between 1-9"),
        ("", "Number, row, or column are NOT valid"),
        ("2.05", "Number, row, or column are NOT valid"),
        ("A", "Number, row, or column are NOT valid"),
        ("b", "Number, row, or column are NOT valid"),
    ])
    def test_parameterized_invalid_numbers(self, num, result):
        self.juego.set_board(self.board_start)
        self.juego.play(num, 1, 3)
        self.assertEqual(self.juego.error, result)

    @parameterized.expand([
        ("hola", "Number, row, or column are NOT valid"),
        (0, "Row or Column not between 1-9"),
        (22, "Row or Column not between 1-9"),
        ("", "Number, row, or column are NOT valid"),
        ("2.05", "Number, row, or column are NOT valid"),
        ("A", "Number, row, or column are NOT valid"),
        ("b", "Number, row, or column are NOT valid"),
    ])
    def test_parameterized_invalid_rows(self, row, result):
        self.juego.set_board(self.board_start)
        self.juego.play(1, row, 3)
        self.assertEqual(self.juego.error, result)

    @parameterized.expand([
        ("hola", "Number, row, or column are NOT valid"),
        (0, "Row or Column not between 1-9"),
        (55, "Row or Column not between 1-9"),
        ("", "Number, row, or column are NOT valid"),
        ("2.05", "Number, row, or column are NOT valid"),
        ("A", "Number, row, or column are NOT valid"),
        ("b", "Number, row, or column are NOT valid"),
    ])
    def test_parameterized_invalid_columns(self, column, result):
        self.juego.set_board(self.board_start)
        self.juego.play(1, 1, column)
        self.assertEqual(self.juego.error, result)

    @parameterized.expand([
        (4, 1, 3),
        (6, 1, 4),
        (8, 1, 6),
        (9, 1, 7),
        (1, 1, 8),
        (2, 1, 9),
        (7, 2, 2),
        (2, 2, 3),
        (3, 2, 7),
        (4, 2, 8),
        (8, 2, 9),
        (1, 3, 1),
        (3, 3, 4),
        (4, 3, 5),
        (2, 3, 6),
        (5, 3, 7),
        (7, 3, 9),
        (5, 4, 2),
        (9, 4, 3),
        (7, 4, 4),
        (1, 4, 6),
        (4, 4, 7),
        (2, 5, 2),
        (6, 5, 3),
        (5, 5, 5),
        (7, 5, 7),
        (9, 5, 8),
        (1, 6, 2),
        (3, 6, 3),
        (9, 6, 4),
        (4, 6, 6),
        (8, 6, 7),
        (9, 7, 1),
        (1, 7, 3),
        (5, 7, 4),
        (3, 7, 5),
        (7, 7, 6),
        (4, 7, 9),
        (2, 8, 1),
        (8, 8, 2),
        (7, 8, 3),
        (6, 8, 7),
        (3, 8, 8),
        (3, 9, 1),
        (4, 9, 2),
        (5, 9, 3),
        (2, 9, 4),
        (6, 9, 6),
        (1, 9, 7),
    ])
    def test_parameterized_valid_numbers_rows_columns(self, num, row, column):
        self.juego.set_board(self.board_start)
        self.juego.play(num, row, column)
        self.assertEqual(self.juego.error, "")

##################################################################################################
##################################### Sudoku 4x4 #################################################
##################################################################################################


class Test_Sudoku4(unittest.TestCase):
    def setUp(self):
        self.board_start = [
            [" ", 3, 4, " "],
            [4, " ", " ", 2],
            [1, " ", " ", " "],
            [" ", 2, 1, " "]]
        self.board_end = [
            [2, 3, 4, 1],
            [4, 1, 3, 2],
            [1, 4, 2, 3],
            [3, 2, 1, " "]]
        self.juego = Sudoku4()

    def test_board_set(self):
        self.juego.set_board(self.board_start)
        self.assertEqual(self.juego.board, self.board_start)
        self.assertEqual(self.juego.original_numbers,
            [[0, 1], [0, 2], [1, 0], [1, 3], [2, 0], [3, 1], [3, 2]])
        self.assertTrue(self.juego.is_playing)

    @parameterized.expand([
        (0, 1),
        (0, 2),
        (1, 0),
        (1, 3),
        (2, 0),
        (3, 1),
        (3, 2),
    ])
    def test_check_if_original_is_original(self, row, column):
        # False means it is an original number
        self.juego.set_board(self.board_start)
        self.assertFalse(self.juego.check_if_original(row + 1, column + 1))

    @parameterized.expand([
        (0, 0),
        (0, 3),
        (1, 1),
        (1, 2),
        (2, 1),
        (3, 0),
        (3, 3),
    ])
    def test_check_if_original_not_original(self, row, column):
        # True means it is not an original number
        self.juego.set_board(self.board_start)
        self.assertTrue(self.juego.check_if_original(row + 1, column + 1))

    def test_set_column_board(self):
        self.juego.set_board(self.board_start)
        self.juego.set_column_board()
        self.assertEqual(self.juego.board_column, [[' ', 4, 1, ' '], 
                                                    [3, ' ', ' ', 2], 
                                                    [4, ' ', ' ', 1], 
                                                    [' ', 2, ' ',' ']])

    @parameterized.expand([
        (1, 1, [" ", 3, 4, " "]),
        (2, 3, [4, " ", ' ', 2]),
        (3, 2, [1, ' ', ' ', 2]),
        (4, 4, [" ", ' ', 1, " "]),
    ])
    def test_get_region(self, row, column, region):
        self.juego.set_board(self.board_start)
        self.assertEqual(self.juego.get_region(row - 1, column - 1), region)

    @parameterized.expand([
        (4, 1, 1),
        (3, 2, 2),
        (1, 3, 3),
        (2, 4, 4),
    ])
    def test_verify_location_invalid(self, num, row, column):
        self.juego.set_board(self.board_start)
        self.assertFalse(self.juego.verify_location(num, row, column))

    @parameterized.expand([
        (2, 1, 1),
        (1, 1, 4),
        (1, 2, 2),
        (3, 2, 3),
        (4, 3, 2),
    ])
    def test_verify_location_valid(self, num, row, column):
        self.juego.set_board(self.board_start)
        self.assertTrue(self.juego.verify_location(num, row, column))

    @parameterized.expand([
        (3, 1),
        (4, 2),
        (1, 3),
        (2, 4),
    ])
    def test_verify_row_invalid(self, num, row):
        self.juego.set_board(self.board_start)
        self.assertFalse(self.juego.verify_row(num, row - 1))

    @parameterized.expand([
        (1, 1),
        (3, 2),
        (2, 3),
        (4, 4),
    ])
    def test_verify_row_valid(self, num, row):
        self.juego.set_board(self.board_start)
        self.assertTrue(self.juego.verify_row(num, row - 1))

    @parameterized.expand([
        (1, 1),
        (3, 2),
        (4, 3),
        (2, 4),
    ])
    def test_verify_column_invalid(self, num, column):
        self.juego.set_board(self.board_start)
        self.assertFalse(self.juego.verify_column(num, column - 1))

    @parameterized.expand([
        (2, 1),
        (1, 2),
        (3, 3),
        (4, 4),
    ])
    def test_verify_column_valid(self, num, column):
        self.juego.set_board(self.board_start)
        self.assertTrue(self.juego.verify_column(num, column - 1))

    @parameterized.expand([
        (3, 1, 1),
        (4, 2, 3),
        (2, 3, 2),
        (1, 4, 4),
    ])
    def test_verify_region_invalid(self, num, row, column):
        self.juego.set_board(self.board_start)
        self.assertFalse(self.juego.verify_region(num, row - 1, column - 1))

    @parameterized.expand([
        (1, 1, 1),
        (3, 2, 3),
        (4, 3, 2),
        (2, 4, 4),
    ])
    def test_verify_region_valid(self, num, row, column):
        self.juego.set_board(self.board_start)
        self.assertTrue(self.juego.verify_region(num, row - 1, column - 1))

    def test_place_valid_number(self):
        self.juego.set_board(self.board_start)
        self.juego.play(1, 1, 4)
        self.assertTrue(self.juego.is_playing)
        self.assertEqual(self.juego.board, [
            [" ", 3, 4, 1],
            [4, " ", " ", 2],
            [1, " ", " ", " "],
            [" ", 2, 1, " "]])

    def test_place_wrong_number_row(self):
        self.juego.set_board(self.board_start)
        self.juego.play(3, 1, 4)
        self.assertTrue(self.juego.is_playing)
        self.assertEqual(self.juego.error, "Number already in Row!")

    def test_place_wrong_number_column(self):
        self.juego.set_board(self.board_start)
        self.juego.play(4, 3, 3)
        self.assertTrue(self.juego.is_playing)
        self.assertEqual(self.juego.error, "Number already in Column!")

    def test_replace_unoriginal_number(self):
        self.juego.set_board(self.board_start)
        self.juego.play(3, 3, 4)
        self.assertEqual(self.juego.board, [
            [" ", 3, 4, " "],
            [4, " ", " ", 2],
            [1, " ", " ", 3],
            [" ", 2, 1, " "]])
        self.juego.play(4, 3, 4)
        self.assertTrue(self.juego.is_playing)
        self.assertEqual(self.juego.board, [
            [" ", 3, 4, " "],
            [4, " ", " ", 2],
            [1, " ", " ", 4],
            [" ", 2, 1, " "]])

    @parameterized.expand([
        (1, 2),
        (1, 3),
        (2, 1),
        (2, 4),
        (3, 1),
        (4, 2),
        (4, 3),
    ])
    def test_try_to_replace_original_number(self, row, column):
        self.juego.set_board(self.board_start)
        self.juego.play(1, row, column)
        self.assertTrue(self.juego.is_playing)
        self.assertEqual(self.juego.board, self.board_start)
        self.assertEqual(self.juego.error, "Tried to replace an original number")

    def test_victory(self):
        self.juego.set_board(self.board_end)
        self.juego.play(4, 4, 4)
        self.assertFalse(self.juego.is_playing)
        self.assertEqual(self.juego.board, [
            [2, 3, 4, 1],
            [4, 1, 3, 2],
            [1, 4, 2, 3],
            [3, 2, 1, 4]])

    @parameterized.expand([
        ("hola", "Number, row, or column are NOT valid"),
        (10, "Number is not between 1-4"),
        (0, "Number is not between 1-4"),
        (11, "Number is not between 1-4"),
        (33, "Number is not between 1-4"),
        ("", "Number, row, or column are NOT valid"),
        ("2.05", "Number, row, or column are NOT valid"),
        ("A", "Number, row, or column are NOT valid"),
        ("b", "Number, row, or column are NOT valid"),
    ])
    def test_parameterized_invalid_numbers(self, num, result):
        self.juego.set_board(self.board_start)
        self.juego.play(num, 1, 1)
        self.assertEqual(self.juego.error, result)

    @parameterized.expand([
        ("hola", "Number, row, or column are NOT valid"),
        (0, "Row or Column not between 1-4"),
        (22, "Row or Column not between 1-4"),
        (5, "Row or Column not between 1-4"),
        (7, "Row or Column not between 1-4"),
        (9, "Row or Column not between 1-4"),
        ("", "Number, row, or column are NOT valid"),
        ("2.05", "Number, row, or column are NOT valid"),
        ("A", "Number, row, or column are NOT valid"),
        ("b", "Number, row, or column are NOT valid"),
    ])
    def test_parameterized_invalid_rows(self, row, result):
        self.juego.set_board(self.board_start)
        self.juego.play(1, row, 1)
        self.assertEqual(self.juego.error, result)

    @parameterized.expand([
        ("hola", "Number, row, or column are NOT valid"),
        (0, "Row or Column not between 1-4"),
        (55, "Row or Column not between 1-4"),
        (5, "Row or Column not between 1-4"),
        (7, "Row or Column not between 1-4"),
        (9, "Row or Column not between 1-4"),
        ("", "Number, row, or column are NOT valid"),
        ("2.05", "Number, row, or column are NOT valid"),
        ("A", "Number, row, or column are NOT valid"),
        ("b", "Number, row, or column are NOT valid"),
    ])
    def test_parameterized_invalid_columns(self, column, result):
        self.juego.set_board(self.board_start)
        self.juego.play(1, 1, column)
        self.assertEqual(self.juego.error, result)

    @parameterized.expand([
        (2, 1, 1),
        (1, 1, 4),
        (1, 2, 2),
        (3, 2, 3),
        (4, 3, 2),
        (2, 3, 3),
        (3, 4, 1),
        (4, 4, 4),
    ])
    def test_parameterized_valid_numbers_rows_columns(self, num, row, column):
        self.juego.set_board(self.board_start)
        self.juego.play(num, row, column)
        self.assertEqual(self.juego.error, "")

##############################################################################################
###################################### Test Profe ############################################
##############################################################################################


class Test_Profe(unittest.TestCase):

    def setUp(self):
        self.board_start = [
            [5, 3, " ", " ", 7, " ", " ", " ", " "],
            [6, " ", " ", 1, 9, 5, " ", " ", " "],
            [" ", 9, 8, " ", " ", " ", " ", 6, " "],
            [8, " ", " ", " ", 6, " ", " ", " ", 3],
            [4, " ", " ", 8, " ", 3, " ", " ", 1],
            [7, " ", " ", " ", 2, " ", " ", " ", 6],
            [" ", 6, " ", " ", " ", " ", 2, 8, " "],
            [" ", " ", " ", 4, 1, 9, " ", " ", 5],
            [" ", " ", " ", " ", 8, " ", " ", 7, 9]]
        self.board_end = [
            [5, 3, 4, 6, 7, 8, 9, 1, 2],
            [6, 7, 2, 1, 9, 5, 3, 4, 8],
            [1, 9, 8, 3, 4, 2, 5, 6, 7],
            [8, 5, 9, 7, 6, 1, 4, 2, 3],
            [4, 2, 6, 8, 5, 3, 7, 9, 1],
            [7, 1, 3, 9, 2, 4, 8, 5, 6],
            [9, 6, 1, 5, 3, 7, 2, 8, 4],
            [2, 8, 7, 4, 1, 9, 6, 3, 5],
            [3, 4, 5, 2, 8, 6, " ", 7, 9]]
        self.game = Sudoku9()
        self.game.set_board(self.board_start)

    @parameterized.expand([
        (1, 1),
        (1, 2),
        (1, 5),
        (2, 1),
        (2, 4),
        (2, 5),
        (2, 6),
        (3, 2),
        (3, 3),
        (3, 8),
        (4, 1),
        (4, 5),
        (4, 9),
        (5, 1),
        (5, 4),
    ])
    def test_existing_numbers_are_not_modifiable(self, row, column):
        self.game.set_board(self.board_start)
        self.game.play(1, row, column)
        self.assertTrue(self.game.is_playing)
        self.assertEqual(self.game.board, self.board_start)
        self.assertEqual(self.game.error, "Tried to replace an original number")

    @parameterized.expand([
        ("a", "Number, row, or column are NOT valid"),
        ("b", "Number, row, or column are NOT valid"),
        ("c", "Number, row, or column are NOT valid"),
        ("d", "Number, row, or column are NOT valid"),
        ("e", "Number, row, or column are NOT valid"),
        ("f", "Number, row, or column are NOT valid"),
        ("g", "Number, row, or column are NOT valid"),
        ("h", "Number, row, or column are NOT valid"),
        ("i", "Number, row, or column are NOT valid"),
        ("hola", "Number, row, or column are NOT valid"),
        (0, "Row or Column not between 1-9"),
        (22, "Row or Column not between 1-9"),
        ("", "Number, row, or column are NOT valid"),
        ("2.05", "Number, row, or column are NOT valid"),
    ])
    def test_validate_insert_illegal_value_in_row(self, row, message):
        self.game.set_board(self.board_start)
        self.game.play(1, row, 3)
        self.assertEqual(self.game.error, message)

    @parameterized.expand([
        (9, 1, 7),
        (3, 2, 7),
        (5, 3, 7),
        (4, 4, 7),
        (7, 5, 7),
        (8, 6, 7),
        (4, 7, 9),
        (6, 8, 7),
        (1, 9, 7),
    ])
    def test_validate_insert_legal_value_in_row(self, number, row, column):
        self.game.play(number, row, column)
        self.assertEqual(self.game.error, "")

    @parameterized.expand([
        ("a", "Number, row, or column are NOT valid"),
        ("b", "Number, row, or column are NOT valid"),
        ("c", "Number, row, or column are NOT valid"),
        ("d", "Number, row, or column are NOT valid"),
        ("e", "Number, row, or column are NOT valid"),
        ("f", "Number, row, or column are NOT valid"),
        ("g", "Number, row, or column are NOT valid"),
        ("h", "Number, row, or column are NOT valid"),
        ("i", "Number, row, or column are NOT valid"),
        ("hola", "Number, row, or column are NOT valid"),
        (0, "Row or Column not between 1-9"),
        (22, "Row or Column not between 1-9"),
        ("", "Number, row, or column are NOT valid"),
        ("2.05", "Number, row, or column are NOT valid"),
    ])
    def test_validate_insert_illegal_value_in_column(self, column, message):
        self.game.set_board(self.board_start)
        self.game.play(1, 3, column)
        self.assertEqual(self.game.error, message)

    @parameterized.expand([
        (9, 1, 7),
        (3, 2, 7),
        (5, 3, 7),
        (4, 4, 7),
        (7, 5, 7),
        (8, 6, 7),
        (4, 7, 9),
        (6, 8, 7),
        (1, 9, 7),
    ])
    def test_validate_insert_legal_value_in_column(self, number, row, column):
        self.game.play(number, row, column)
        self.assertEqual(self.game.error, "")

    @parameterized.expand([
        (3, 3, 1),
        (5, 3, 4),
        (5, 3, 5),
        (6, 1, 7),
        (8, 6, 2),
        (4, 4, 2),
        (3, 6, 4),
        (1, 4, 7),
        (6, 8, 3),
        (9, 7, 4),
        (2, 8, 8),
        ])
    def test_validate_insert_illegal_value_in_region(self, value, row, column):
        self.game.play(value, row, column)
        self.assertEqual(self.game.error, "Number already in Region!")

    @parameterized.expand([
        (9, 1, 7),
        (3, 2, 7),
        (5, 3, 7),
        (4, 4, 7),
        (7, 5, 7),
        (8, 6, 7),
        (4, 7, 9),
        (6, 8, 7),
        (1, 9, 7),
    ])
    def test_validate_insert_legal_value_in_region(self, value, row, column):
        self.game.play(value, row, column)
        self.assertEqual(self.game.error, "")



    @parameterized.expand([
        (1, 1, [5, 3, " ", 6, " ", " ", " ", 9, 8]),
        (1, 5, [' ', 7, ' ', 1, 9, 5, ' ', ' ', ' ']),
        (1, 8, [' ', ' ', ' ', ' ', ' ', ' ', ' ', 6, ' ']),
        (4, 2, [8, ' ', ' ', 4, ' ', ' ', 7, ' ', ' ']),
        (4, 4, [' ', 6, ' ', 8, ' ', 3, ' ', 2, ' ']),
        (4, 9, [' ', ' ', 3, ' ', ' ', 1, ' ', ' ', 6]),
        (7, 3, [' ', 6, ' ', ' ', ' ', ' ', ' ', ' ', ' ']),
        (7, 6, [' ', ' ', ' ', 4, 1, 9, ' ', 8, ' ']),
        (7, 7, [2, 8, ' ', ' ', ' ', 5, ' ', 7, 9])
    ])
    def test_get_region(self, row, column, region):
        self.assertEqual(self.game.get_region(row - 1, column - 1), region)

    @parameterized.expand([
        (4, 1, 3),
        (6, 1, 4),
        (8, 1, 6),
        (9, 1, 7),
        (1, 1, 8),
        (2, 1, 9),
        (7, 2, 2),
        (2, 2, 3),
        (3, 2, 7),
        (4, 2, 8),
        (8, 2, 9),
        (1, 3, 1),
        (3, 3, 4),
        (4, 3, 5),
        (2, 3, 6),
        (5, 3, 7),
        (7, 3, 9),
        (5, 4, 2),
        (9, 4, 3),
        (7, 4, 4),
        (1, 4, 6),
        (4, 4, 7),
        (2, 5, 2),
        (6, 5, 3),
        (5, 5, 5),
        (7, 5, 7),
        (9, 5, 8),
        (1, 6, 2),
        (3, 6, 3),
        (9, 6, 4),
        (4, 6, 6),
        (8, 6, 7),
        (9, 7, 1),
        (1, 7, 3),
        (5, 7, 4),
        (3, 7, 5),
        (7, 7, 6),
        (4, 7, 9),
        (2, 8, 1),
        (8, 8, 2),
        (7, 8, 3),
        (6, 8, 7),
        (3, 8, 8),
        (3, 9, 1),
        (4, 9, 2),
        (5, 9, 3),
        (2, 9, 4),
        (6, 9, 6),
        (1, 9, 7),
    ])
    def test_place_number_legally(self, value, row, column):
        self.game.play(value, row, column)
        self.assertEqual(self.game.board[row - 1][column - 1], value)

    @parameterized.expand([
        ((8, 1), 9, "Number already in Row!"),
        ((4, 4), 4, "Number already in Column!"),
        ((6, 3), 2, "Number already in Row!"),
        ((1, 7), 6, "Number already in Region!"),
        ((3, 6), 3, "Number already in Column!"),
        ((8, 8), 2, "Number already in Region!"),
        ((1, 1), 1, "Tried to replace an original number"),
        ((4, 5), 2, "Tried to replace an original number"),
    ])
    def test_place_number_in_invalid_places(
            self, coordinates, value, message):

        row, column = coordinates
        self.game.play(value, row, column)
        self.assertEqual(self.game.error, message)

    def test_is_finished_for_an_unfinished_board(self):
        # Checks if still playing, True = Not win, False = Win
        self.assertTrue(self.game.win())

    def test_is_finished_for_a_finished_board(self):
        # Checks if still playing, True = Not win, False = Win
        self.game.set_board(self.board_end)
        self.game.play(1, 9, 7)
        self.assertFalse(self.game.win())

    def test_board(self):
        self.assertEqual("\n5 3   |  7   |     \n6     |1 9 5 |     \n  9 8 |      |  6  \n------+------+------\n8     |  6   |    3\n4     |8   3 |    1\n7     |  2   |    6\n------+------+------\n  6   |      |2 8  \n      |4 1 9 |    5\n      |  8   |  7 9"
            , self.game.board_print())


if __name__ == '__main__':
    unittest.main()
