# Melissa J Johnson
# 06/02/2021
# CS 162 Final Project

# Write a class named KubaGame for playing a board game called Kuba.

import copy


class KubaGame:
    """ Class for playing a Python version of the board game Kuba. """

    def __init__(self, player_a, player_b):
        """
        Constructor for KubaGame. Initializes game board.
        :param player_a: takes tuple as parameter: (player, players_marble_color)
        :param player_b: (player, players_marble_color)

        The current_turn is None at the start of the game.
        The game_state is set to None (and will change when there is a win)
        The board is initialized by hardcoding the gameboard to it's starting state.
        """
        self._player_a = (player_a[0], player_a[1])
        self._player_b = (player_b[0], player_b[1])
        self._player_a_red = 0
        self._player_b_red = 0
        self._winner = None
        self._current_turn = None

        self._board = [['W', 'W', 'X', 'X', 'X', 'B', 'B'],
                       ['W', 'W', 'X', 'R', 'X', 'B', 'B'],
                       ['X', 'X', 'R', 'R', 'R', 'X', 'X'],
                       ['X', 'R', 'R', 'R', 'R', 'R', 'X'],
                       ['X', 'X', 'R', 'R', 'R', 'X', 'X'],
                       ['B', 'B', 'X', 'R', 'X', 'W', 'W'],
                       ['B', 'B', 'X', 'X', 'X', 'W', 'W']]

        self._previous_board = self._board

    def get_current_turn(self):
        """
        Returns the player's name whose turn it is to play the game.
        It should return None if the game hasn't started.
        """
        if self._current_turn is None:
            return None
        elif self._current_turn == self._player_a:
            # self._current_turn = self._player_a
            return self._player_a[0]
        elif self._current_turn == self._player_b:
            # self._current_turn = self._player_b
            return self._player_b[0]

    def get_marble(self, coordinates):
        row, col = coordinates

        if not self._are_valid_coordinates(coordinates):
            return self._board[row][col]
        raise IndexError(f"Invalid board coordinates ({row}, {col})")

    def _validate_player_name_exists(self, player_name):
        """
        Method to validate if the player's name exists.
        If the name does not exist, the method will return False.
        """
        if player_name != self._player_a[0] or self._player_b[0]:
            return False

    def _are_valid_coordinates(self, coordinates):
        """ Checks that the given coordinates are on the game board. """
        row, col = coordinates
        return 0 <= row <= 6 and 0 <= col <= 6

    def make_move(self, player_name, coordinates, direction):
        """
        Makes a move in Kuba (once several checks pass).
        :param player_name: player making move
        :param coordinates: coordinates as tuple (row, column) of marble that is going to be pushed
        :param direction: L (left), R (right), F (forward), B (backward)
        :return: True if move is successful, returns False if move is invalid
        """

        # Check that the player_name is valid.
        if self._validate_player_name_exists(player_name):
            return False

        # If the game has not been started, then set player to current_turn
        if self.get_current_turn() is None:
            if player_name == self._player_a[0]:
                self._current_turn = self._player_a
            if player_name == self._player_b[0]:
                self._current_turn = self._player_b

        # If move is being made after the game has been won return False
        if self.get_winner():
            return False

        # If it's not the correct players turn
        if player_name != self.get_current_turn()[0:]:
            return False

        # If coordinates provided are not valid
        if not self._are_valid_coordinates(coordinates):
            return False

        # If the player is pushing the wrong color, return False
        if self._board[coordinates[0]][coordinates[1]] != self._current_turn[1]:
            return False

        # If there isn't empty space for move
        if not self._is_there_empty_space_for_move(coordinates, direction):
            return False

        # We make a deepcopy of the board so we can simulate the move and check
        # if it violates the Ko Rule or if the player is pushing off their own color.
        board_copy = copy.deepcopy(self._board)

        # pushed_off holds the marbles that are pushed off during a turn
        pushed_off = self._shift_board_for_move(board_copy, coordinates, direction)

        # If player is pushing off their own color, return False.
        if pushed_off == self._current_turn[1]:
            return False

        # If the copy of the board is the same as the previous board, return False
        if board_copy == self._previous_board:
            # Ko rule has been triggered
            return False

        self._previous_board = self._board
        self._board = board_copy

        #### Below this line, we know the move is valid ####

        # Move is valid, so update self._board (instead of the copy)
        self._shift_board_for_move(self._board, coordinates, direction)

        # Update marble count
        if pushed_off is not None and pushed_off == 'R':
            if player_name == self._player_a[0]:
                self._player_a_red += 1
            if player_name == self._player_b[0]:
                self._player_b_red += 1

        # Move was valid, so now update current_turn
        if player_name == self._player_a[0]:
            self._current_turn = self._player_b
        else:
            self._current_turn = self._player_a

        # If player_a has 7 red marbles
        if self._player_a_red == 7:
            self._winner = self._player_a[0]
            return True

        if self._player_b_red == 7:
            self._winner = self._player_b[0]
            return True

        # Check if player_b has marbles remaining and player_a has no marbles remaining
        if self.get_marble_count()[0] == 0 and self.get_marble_count()[1] > 0:
            self._winner = self._player_b[1]
            return True

        # Check if player_a has marbles remaining and player_b has no marbles remaining
        if self.get_marble_count()[1] == 0 and self.get_marble_count()[0] > 0:
            self._winner = self._player_a[0]
            return True

    def get_winner(self):
        """
        This method returns the name of the winning player.
        :return: return's name of winning player if there is one, otherwise returns None
        """
        return self._winner


    def get_captured(self, player_name):
        """
         Method that takes the player's name as a parameter
         and returns how many red marbles they have captured.
         """
        if player_name == self._player_a[0]:
            return self._player_a_red
        if player_name == self._player_b[0]:
            return self._player_b_red


    def get_marble_count(self):
        """
        Counts the numbers of white, black, and red marbles remaining on the board.
        :return: Returns number of marbles in a tuple (W, B, R) which is White, Black, Red
        """
        white_marbles = sum(element == 'W' for element in self._count_marbles(self._board))
        black_marbles = sum(element == 'B' for element in self._count_marbles(self._board))
        red_marbles = sum(element == 'R' for element in self._count_marbles(self._board))
        return white_marbles, black_marbles, red_marbles

    def _count_marbles(self, board):
        for sublist in board:
            for element in sublist:
                yield element

    def _is_there_empty_space_for_move(self, coordinates, direction):
        # Checks if there's "empty" space to perform a move starting
        # at coordinates "coordinates", in the specified direction. In order
        # to perform a move, the space in the opposite direction of the move direction
        # needs to be empty.

        row, col = coordinates

        if direction == 'L':
            if col == 6:
                return True
            else:
                if self._board[row][col + 1] != 'X':
                    return False

        if direction == 'R':
            if col == 0:
                return True
            else:
                if self._board[row][col - 1] != 'X':
                    return False

        if direction == 'F':
            if row == 6:
                return True
            else:
                if self._board[row + 1][col] != 'X':
                    return False

        if direction == 'B':
            if row == 0:
                return True
            else:
                if self._board[row - 1][col] != 'X':
                    return False

        return True

    def _shift_board_for_move(self, board, coordinates, direction):
        # Shifts the cells of "board" from the specified "coordinates"
        # in the specified "direction".
        #
        # This method also returns the contents of the cell that has
        # been pushed off.
        row, col = coordinates
        pushed_off = None

        if direction == 'L':
            to_move = board[row][col]
            overwrite = 'X'
            while col >= 0:
                if col == 0:
                    pushed_off = to_move
                board[row][col] = overwrite
                col -= 1
                to_move, overwrite = board[row][col], to_move
                # check if you're at the edge of the board, if so, store the pushed off marble
                if overwrite == 'X':
                    break

        if direction == 'R':
            to_move = board[row][col]
            overwrite = 'X'
            while col <= 6:
                board[row][col] = overwrite
                # Check if you're at the edge of the board, and if so, assign pushed_off
                if col == 6:
                    pushed_off = to_move
                    break
                col += 1
                to_move, overwrite = board[row][col], to_move
                if overwrite == 'X':
                    break

        if direction == 'F':
            # The value to be moved is stored as to_move with the current coordinates.
            # Each value is sequentially moved until an 'X' is reached
            to_move = board[row][col]
            overwrite = 'X'
            while row >= 0:
                if row == 0:
                    pushed_off = to_move
                board[row][col] = overwrite
                row -= 1
                to_move, overwrite = board[row][col], to_move
                # check if you're at the edge of the board, if so, store the pushed off marble
                if overwrite == 'X':
                    break

        if direction == 'B':
            to_move = board[row][col]
            overwrite = 'X'
            while row <= 6:
                board[row][col] = overwrite
                # check if you're at the edge of the board, if so, store the pushed off marble
                if row == 6:
                    pushed_off = to_move
                    break
                row += 1
                to_move, overwrite = board[row][col], to_move
                if overwrite == 'X':
                    break

        return pushed_off

    def print_game(self):
        print("\n")
        for i in range(len(self._board)):
            grid = ""
            for j in range(len(self._board[i])):
                grid += str(self._board[i][j]) + "  "
            print(grid)


