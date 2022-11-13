# Melissa J Johnson
# 05/09/2021
# CS162 Project 6d

# unit tests for row_puzzle.py

import unittest
from row_puzzle import row_puzzle


class RowPuzzleTester(unittest.TestCase):
    def test_another_row_puzzle_with_a_solution(self):
        self.assertTrue(row_puzzle([2, 4, 5, 3, 1, 3, 1, 4, 0]))

    def test_row_puzzle_with_another_puzzle_that_has_solution(self):
        self.assertTrue(row_puzzle([7, 2, 6, 5, 1, 4, 2, 3, 0]))

    def test_row_puzzle_handles_possible_infinite_loop_successfully(self):
        self.assertFalse(row_puzzle([1, 3, 2, 1, 3, 4, 0]))

    def test_row_puzzle_returns_true_with_additional_zero_in_puzzle_with_solution(self):
        self.assertTrue(row_puzzle([2, 4, 5, 3, 0, 3, 1, 4, 0]))

    def test_row_puzzle_with_two_elements_and_no_solution(self):
        self.assertFalse(row_puzzle([2, 0]))

    def test_row_puzzle_with_two_elements_and_has_solution(self):
        self.assertTrue(row_puzzle([1, 0]))



