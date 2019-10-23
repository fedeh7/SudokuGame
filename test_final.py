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


class Test_interface(unittest.TestCase):

    def setUp(self):
        self.board_4_start = [
            ["", 3, 4, ""],
            [4, "", "", 2],
            [1, "", "", 3],
            ["", 2, 1, ""]]
        self.board_4_end = [
            [2, 3, 4, 1],
            [4, 1, 3, 2],
            [1, 4, 2, 3],
            [3, 2, 1, ""]]
        self.board_9_start = [
            [5, 3, "", "", 7, "", "", "", ""],
            [6, "", "", 1, 9, 5, "", "", ""],
            ["", 9, 8, "", "", "", "", 6, ""],
            [8, "", "", "", 6, "", "", "", 3],
            [4, "", "", 8, "", 3, "", "", 1],
            [7, "", "", "", 2, "", "", "", 6],
            ["", 6, "", "", "", "", 2, 8, ""],
            ["", "", "", 4, 1, 9, "", "", 5],
            ["", "", "", "", 8, "", "", 7, 9]]
        self.board_9_end = [
            [5, 3, 4, 6, 7, 8, 9, 1, 2],
            [6, 7, 2, 1, 9, 5, 3, 4, 8],
            [1, 9, 8, 3, 4, 2, 5, 6, 7],
            [8, 5, 9, 7, 6, 1, 4, 2, 3],
            [4, 2, 6, 8, 5, 3, 7, 9, 1],
            [7, 1, 3, 9, 2, 4, 8, 5, 6],
            [9, 6, 1, 5, 3, 7, 2, 8, 4],
            [2, 8, 7, 4, 1, 9, 6, 3, 5],
            [3, 4, 5, 2, 8, 6, "", 7, 9]]
        self.game = Interface()

    @unittest.mock.patch("builtins.input", side_effect=["4"])
    def test_sudoku4_start(self, mock):
        self.game.set_game()
        self.assertEqual(self.game.size, 4)
        self.assertEqual(len(self.game.play.board[0]), 4)
        self.assertEqual(self.game.play.__class__.__name__, "Sudoku4")

    @unittest.mock.patch("builtins.input", side_effect=["9"])
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

    @unittest.mock.patch("builtins.input", side_effect=["4", "4", "4", "4"])
    def test_sudoku4_endgame(self, mock):
        self.game.set_game()
        self.game.play.set_board(self.board_4_end)
        self.assertEqual(self.game.size, 4)
        self.assertEqual(len(self.game.play.board[0]), 4)
        self.assertTrue(self.game.play.is_playing)
        self.game.start_playing()
        self.assertFalse(self.game.play.is_playing)

    @unittest.mock.patch("builtins.input", side_effect=["9", "1", "9", "7"])
    def test_sudoku9_endgame(self, mock):
        self.game.set_game()
        self.game.play.set_board(self.board_9_end)
        self.assertEqual(self.game.size, 9)
        self.assertEqual(len(self.game.play.board[0]), 9)
        self.assertTrue(self.game.play.is_playing)
        self.game.start_playing()
        self.assertFalse(self.game.play.is_playing)


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

    def test_place_wrong_number(self):
        self.juego.set_board(self.board_start)
        self.juego.play(3, 1, 3)
        self.assertTrue(self.juego.is_playing)
        self.assertEqual(self.juego.board, [
            [5, 3, 3, " ", 7, " ", " ", " ", " "],
            [6, " ", " ", 1, 9, 5, " ", " ", " "],
            [" ", 9, 8, " ", " ", " ", " ", 6, " "],
            [8, " ", " ", " ", 6, " ", " ", " ", 3],
            [4, " ", " ", 8, " ", 3, " ", " ", 1],
            [7, " ", " ", " ", 2, " ", " ", " ", 6],
            [" ", 6, " ", " ", " ", " ", 2, 8, " "],
            [" ", " ", " ", 4, 1, 9, " ", " ", 5],
            [" ", " ", " ", " ", 8, " ", " ", 7, 9]])

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

    def test_no_victory_beacuse_of_regions(self):
        self.juego.set_board([
            [1, 2, 3, 4, 5, 6, 7, 8, 9],
            [9, 1, 2, 3, 4, 5, 6, 7, 8],
            [8, 9, 1, 2, 3, 4, 5, 6, 7],
            [7, 8, 9, 1, 2, 3, 4, 5, 6],
            [6, 7, 8, 9, 1, 2, 3, 4, 5],
            [5, 6, 7, 8, 9, 1, 2, 3, 4],
            [4, 5, 6, 7, 8, 9, 1, 2, 3],
            [3, 4, 5, 6, 7, 8, 9, 1, 2],
            [2, 3, 4, 5, 6, 7, 8, 9, " "]])
        self.juego.play(1, 9, 9)
        self.assertTrue(self.juego.is_playing)
        self.assertEqual(self.juego.board, [
            [1, 2, 3, 4, 5, 6, 7, 8, 9],
            [9, 1, 2, 3, 4, 5, 6, 7, 8],
            [8, 9, 1, 2, 3, 4, 5, 6, 7],
            [7, 8, 9, 1, 2, 3, 4, 5, 6],
            [6, 7, 8, 9, 1, 2, 3, 4, 5],
            [5, 6, 7, 8, 9, 1, 2, 3, 4],
            [4, 5, 6, 7, 8, 9, 1, 2, 3],
            [3, 4, 5, 6, 7, 8, 9, 1, 2],
            [2, 3, 4, 5, 6, 7, 8, 9, 1]])

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
        (0, "Number, row, or column are NOT valid"),
        (22, "Number, row, or column are NOT valid"),
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
        (0, "Number, row, or column are NOT valid"),
        (55, "Number, row, or column are NOT valid"),
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
        (1, 1, 3),
        (2, 1, 4),
        (3, 1, 6),
        (4, 1, 7),
        (5, 1, 8),
        (6, 1, 9),
        (7, 2, 2),
        (8, 2, 3),
        (9, 2, 7),
        (1, 2, 8),
        (2, 2, 9),
        (3, 3, 1),
        (4, 3, 4),
        (5, 3, 5),
        (6, 3, 6),
        (7, 3, 7),
        (8, 3, 9),
        (9, 4, 2),
        (1, 4, 3),
        (2, 4, 4),
        (3, 4, 6),
        (4, 4, 7),
        (5, 5, 2),
        (6, 5, 3),
        (7, 5, 5),
        (8, 5, 7),
        (9, 5, 8),
        (1, 6, 3),
        (2, 6, 2),
        (3, 6, 3),
        (4, 6, 4),
        (5, 6, 6),
        (6, 6, 7),
        (7, 7, 1),
        (8, 7, 3),
        (9, 7, 4),
        (1, 7, 5),
        (2, 7, 6),
        (3, 7, 9),
        (4, 8, 1),
        (5, 8, 2),
        (6, 8, 3),
        (7, 8, 7),
        (8, 8, 8),
        (9, 9, 1),
        (1, 9, 2),
        (2, 9, 3),
        (3, 9, 4),
        (4, 9, 6),
        (5, 9, 7),
    ])
    def test_parameterized_valid_numbers_rows_columns(self, num, row, column):
        self.juego.set_board(self.board_start)
        self.juego.play(num, row, column)
        self.assertEqual(self.juego.error, "")
            

class Test_Sudoku4(unittest.TestCase):
    def setUp(self):
        self.board_start = [
            [" ", 3, 4, " "],
            [4, " ", " ", 2],
            [1, " ", " ", 3],
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
            [[0, 1], [0, 2], [1, 0], [1, 3], [2, 0], [2, 3], [3, 1], [3, 2]])
        self.assertTrue(self.juego.is_playing)

    def test_place_valid_number(self):
        self.juego.set_board(self.board_start)
        self.juego.play(1, 1, 4)
        self.assertTrue(self.juego.is_playing)
        self.assertEqual(self.juego.board, [
            [" ", 3, 4, 1],
            [4, " ", " ", 2],
            [1, " ", " ", 3],
            [" ", 2, 1, " "]])

    def test_place_wrong_number(self):
        self.juego.set_board(self.board_start)
        self.juego.play(1, 1, 1)
        self.assertTrue(self.juego.is_playing)
        self.assertEqual(self.juego.board, [
            [1, 3, 4, " "],
            [4, " ", " ", 2],
            [1, " ", " ", 3],
            [" ", 2, 1, " "]])

    def test_replace_unoriginal_number(self):
        self.juego.set_board(self.board_start)
        self.juego.play(1, 1, 1)
        self.assertEqual(self.juego.board, [
            [1, 3, 4, " "],
            [4, " ", " ", 2],
            [1, " ", " ", 3],
            [" ", 2, 1, " "]])
        self.juego.play(2, 1, 1)
        self.assertTrue(self.juego.is_playing)
        self.assertEqual(self.juego.board, [
            [2, 3, 4, " "],
            [4, " ", " ", 2],
            [1, " ", " ", 3],
            [" ", 2, 1, " "]])

    @parameterized.expand([
        (1, 2),
        (1, 3),
        (2, 1),
        (2, 4),
        (3, 1),
        (3, 4),
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

    def test_no_victory_because_of_regions(self):
        self.juego.set_board([
            [1, 2, 3, 4],
            [4, 1, 2, 3],
            [3, 4, 1, 2],
            [2, 3, 4, " "]])
        self.juego.play(1, 4, 4)
        self.assertTrue(self.juego.is_playing)
        self.assertEqual(self.juego.board, [
            [1, 2, 3, 4],
            [4, 1, 2, 3],
            [3, 4, 1, 2],
            [2, 3, 4, 1]])

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
        (0, "Number, row, or column are NOT valid"),
        (22, "Number, row, or column are NOT valid"),
        (5, "Number, row, or column are NOT valid"),
        (7, "Number, row, or column are NOT valid"),
        (9, "Number, row, or column are NOT valid"),
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
        (0, "Number, row, or column are NOT valid"),
        (55, "Number, row, or column are NOT valid"),
        (5, "Number, row, or column are NOT valid"),
        (7, "Number, row, or column are NOT valid"),
        (9, "Number, row, or column are NOT valid"),
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
        (1, 1, 1),
        (2, 1, 4),
        (3, 2, 2),
        (4, 2, 3),
        (1, 3, 2),
        (2, 3, 3),
        (3, 4, 1),
        (4, 4, 4),
    ])
    def test_parameterized_valid_numbers_rows_columns(self, num, row, column):
        self.juego.set_board(self.board_start)
        self.juego.play(num, row, column)
        self.assertEqual(self.juego.error, "")


if __name__ == '__main__':
    unittest.main()
