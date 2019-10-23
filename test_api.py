import unittest
from api import get_board_from_api
from parameterized import parameterized


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
        (1,),
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


if __name__ == '__main__':
    unittest.main()
