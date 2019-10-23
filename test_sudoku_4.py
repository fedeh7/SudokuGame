import unittest
from sudoku import Sudoku4
from parameterized import parameterized


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

    def test_valid_number(self):
        self.juego.set_board(self.board_start)
        self.juego.play(1, 1, 4)
        self.assertTrue(self.juego.is_playing)
        self.assertEqual(self.juego.board, [
            [" ", 3, 4, 1],
            [4, " ", " ", 2],
            [1, " ", " ", 3],
            [" ", 2, 1, " "]])

    def test_wrong_number(self):
        self.juego.set_board(self.board_start)
        self.juego.play(1, 1, 1)
        self.assertTrue(self.juego.is_playing)
        self.assertEqual(self.juego.board, [
            [1, 3, 4, " "],
            [4, " ", " ", 2],
            [1, " ", " ", 3],
            [" ", 2, 1, " "]])

    def test_replace_number(self):
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

    def test_invalid_replacement(self):
        self.juego.set_board(self.board_start)
        self.juego.play(1, 1, 2)
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

    def test_no_victory(self):
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
        ("", "Number, row, or column are NOT valid"),
        ("2.05", "Number, row, or column are NOT valid"),
    ])
    def test_parameterized_invalid_numbers(self, num, result):
        self.juego.set_board(self.board_start)
        self.juego.play(num, 1, 1)
        self.assertEqual(self.juego.error, result)

    @parameterized.expand([
        ("hola", "Number, row, or column are NOT valid"),
        (0, "Number, row, or column are NOT valid"),
        (22, "Number, row, or column are NOT valid"),
        ("", "Number, row, or column are NOT valid"),
    ])
    def test_parameterized_invalid_rows(self, row, result):
        self.juego.set_board(self.board_start)
        self.juego.play(1, row, 1)
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
