import requests


def get_board_from_api(size):

    if size != 9 and size != 4:
        return "Invalid size"

    board = []
    for rows in range(size):
        board.append([])
        for columns in range(size):
            board[rows].append(" ")

    resp = requests.get(
        f"http://www.cs.utep.edu/cheon/ws/sudoku/new/?level=1&size={size}"
        )

    table = resp.json()["squares"]
    for number in range(len(table)):
        board[table[number]["x"]][table[number]["y"]] = "\033[1m\033[4m" + str(table[number]["value"]) + "\033[0m"

    return board


get_board_from_api(4)
