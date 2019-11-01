import unittest
from sudoku import Sudoku9
from parameterized import parameterized


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
        self.juego = ""
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

    def test_valid_number(self):
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

    def test_wrong_number(self):
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

    def test_replace_number(self):
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

    def test_try_to_replace_original_number(self):
        self.juego.set_board(self.board_start)
        self.juego.play(1, 1, 2)
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
        ("", "Number, row, or column are NOT valid"),
        ("2.05", "Number, row, or column are NOT valid"),
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
    ])
    def test_parameterized_invalid_columns(self, column, result):
        self.juego.set_board(self.board_start)
        self.juego.play(1, 1, column)
        self.assertEqual(self.juego.error, result)


if __name__ == '__main__':
    unittest.main()
