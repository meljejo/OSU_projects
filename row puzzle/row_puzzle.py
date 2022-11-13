# Melissa J Johnson
# 05/09/2021
# Project 6d

# Write a recursive function to solve a puzzle which consists of a row of squares that contain non-negative integers
# with a zero in rightmost square (other squares can contain zero). The goal of the game is to move the token from its
# starting position (leftmost square) and get to the end of the row (which contains a zero).
# The token can move left or right equal to the value in its current square, but cannot move off either end of the row.

def row_puzzle(row):
    # Row puzzle is a classic backtracking problem and
    # is solved recursively by trying each possible (and valid)
    # movement on each step. The function only returns True when we reach the last
    # element of the row. If we have backtracked all the way that means no solution
    # could be found and will return False.

    # The helper function, _row_puzzle_helper is what implements this algorithm.
    # _row_puzzle_helper gets the parameters needed to properly solve the problem.
    return _row_puzzle_helper(row, 0, set())


def _row_puzzle_helper(row, row_index, visited):
    """
    Recursive helper for row_puzzle function.
    :param row: puzzle
    :param row_index: index in the row that is visited next. The index can be out-of-bounds, in which
                      case the function will return False.
    :param visited: A set of integers that keeps track of the indices that have been visited so far. This is required
                    to avoid entering loops in the recursion. If we were to land on the same index twice it would
                    mean that we have reached the same point again and that would cause infinite recursion.
    """

    # If the last position of the row is reached, it means row_puzzle has a solution. The value of the position
    # is disregarded since it's assumed to be zero for this type of puzzle.
    if row_index == len(row) - 1:
        return True

    # If the row_index is out-of-bounds, return False
    if row_index >= len(row) or row_index < 0:
        return False

    # If the index has already been visited, this is another dead end. Trying to continue
    # this way would cause inifinite recursion.
    if row_index in visited:
        return False

    row_value = row[row_index]

    # If we land on a 0 that is not the last element of the row,
    # this path is a dead end.
    if row_value == 0:
        return False

    # If the above conditions didn't return False, continue by recursively traversing
    # the left and ride sides. If either branch returns True, then there's a solution,
    # otherwise there is no solution.

    # Before calling the recursive function, we need to add the current index to the
    # visited set, to avoid ending up in an infinite loop.

    visited.add(row_index)
    result = _row_puzzle_helper(row, row_index + row_value, visited) or _row_puzzle_helper(row, row_index - row_value, visited)

    return result
