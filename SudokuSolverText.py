import random
import numpy as np


def print_board(matrix):
    """
    Prints the Sudoku board

    :param matrix: a 2D array for ints
    :return: None
    """

    for r in range(len(matrix)):
        for c in range(len(matrix[r])):
            if c == 2 or c == 5:
                print("[" + str(matrix[r][c]) + "]", end=" | ")
            else:
                print("[" + str(matrix[r][c]) + "]", end=" ")
        print()
        if r == 2 or r == 5:
            for i in range(20):
                print("-", end=" ")
            print()


def generate_numbers(matrix):
    """
    Generates random numbers to fill the board

    :param matrix: a 2D array of ints; board to be filled
    :return: None
    """

    num_of_nums = random.randint(5, 20)
    print("# of numbers to be generated: " + str(num_of_nums))
    chance = 25
    while num_of_nums > 0:
        for r in range(len(matrix)):
            for c in range(len(matrix[r])):
                if random.randint(1, 101) < chance and num_of_nums > 0:
                    temp_bool = add_number(r, c, random.randint(1, 9), matrix)
                    while not temp_bool:
                        temp_bool = add_number(r, c, random.randint(1, 9), matrix)
                    num_of_nums -= 1


def add_number(row, col, num, matrix):
    """
    Adds the parameter number to the board

    :param row: row to be checked
    :param col: column to be checked
    :param num: number to be added
    :param matrix: a 2D array of ints
    :return: True if the number was added; False if otherwise
    """

    if row < 0 or row >= 9:
        print("Invalid row #")
    elif col < 0 or col >= 9:
        print("Invalid col #")
    else:
        start_row = row // 3 * 3
        start_col = col // 3 * 3

        if search_box(start_row, start_col, num, matrix) and \
                search_row_peers(row, num, matrix) and \
                search_col_peers(col, num, matrix):
            matrix[row][col] = num
            return True
        else:
            return False


def find_empty(matrix):
    """
    Finds an empty space in the board

    :param matrix: a 2D array of ints
    :return: the row and column of the empty space, None if there is no empty space
    """

    for r in range(len(matrix)):
        for c in range(len(matrix[r])):
            if matrix[r][c] == 0:
                return r, c
    return None


def search_box(start_row, start_col, num, matrix):
    """
    Helper method of add_number()
    Searches the box to check if the parameter number is already there

    :param start_row: starting row of the box
    :param start_col: starting column of the box
    :param num: number being checked for
    :param matrix: a 2D array of ints
    :return: True if the number is not in the box; False if otherwise
    """

    if start_row < 0 or start_row >= 9:
        print("Invalid row #")
    elif start_col < 0 or start_col >= 9:
        print("Invalid col #")
    else:
        for r in range(start_row, start_row + 3):
            for c in range(start_col, start_col + 3):
                if matrix[r][c] == num:
                    return False
        return True


def search_row_peers(row, num, matrix):
    """
    Searches the row to check if the parameter number is already there

    :param row: row to be iterated through
    :param num: number to be checked for
    :param matrix: a 2D array of ints
    :return: True if the number is not in the row; False if otherwise
    """

    for c in range(len(matrix)):
        if matrix[row][c] == num and c != row:
            return False
    return True


def search_col_peers(col, num, matrix):
    """
    Searches the column to check if the parameter number is already there

    :param col: column to be iterated through
    :param num: number to be checked for
    :param matrix: a 2D array of ints
    :return: True if the number is not in the column; False if otherwise
    """

    for r in range(len(matrix[0])):
        if matrix[r][col] == num and r != col:
            return False
    return True


def solve(matrix):
    """
    Solves the board through recursive backtracking

    :param matrix: a 2D array of ints; board to be solved
    :return: True if the solution is valid, False if otherwise
    """

    space = find_empty(matrix)
    if space:
        row, col = space
    else:
        return True

    for i in range(1, 10):
        if add_number(row, col, i, matrix):
            if solve(matrix):
                return True

            matrix[row][col] = 0

    return False


# Initializing the board
board = np.zeros((9, 9), dtype=int)
print_board(board)
print()

# Generates the numbers on the board
generate_numbers(board)
print_board(board)
print()

# Solves the board
solve(board)
print_board(board)
