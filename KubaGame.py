# Melissa J Johnson
# 06/09/2021
# CS 162 Final Project

# Write a class named KubaGame for playing a board game called Kuba.

import copy


class KubaGame:
    """ Class for playing a Python version of the board game Kuba. """

    def __init__(self, player_a, player_b):
        """
        Builds a KubaGame.

        The game is in an 'unstarted' state, meaning that either player can conduct
        the next move and from there on, the game will alternate turns between two players.

        The class refers to the players as "player_a" and "player_b." This naming is only to
        differentiate between the two players and does not have any implications as to which
        player comes first.

        :param player_a: tuple containing the data for player_a. The first element is the player's name
            and the second element is the player's color.
        :param player_b: tuple containing the data for player_b. The first element is the player's name
            and the second element is the player's color.

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

        # Internally we keep two boards: one that represents the current state
        # of the game and the one that represents the state of the game in
        # the previous turn. This allows us to prevent movements that would
        # return the board to the same state as in the previous turn, which
        # effectively implements the Ko Rule.

    def get_current_turn(self):
        """
        Returns the player's name whose turn it is to play the game.
        Can be None if the game has just been initialized.
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
        """
        Returns the marble at a specific position on the board.
        :param coordinates: the (row, col) coordinates of the position
            to return
        :return: the marble present at "coordinates" on the board.
        :raises : IndexError: if invalid coordinates are given.
        """
        row, col = coordinates

        if self._are_valid_coordinates(coordinates):
            return self._board[row][col]
        raise IndexError(f"Invalid board coordinates ({row}, {col})")

    def _validate_player_name_exists(self, player_name):
        """
        Checks if a provided string is a valid name for a player.
        :param player_name: the name to check
        :return: True if 'name' is a valid player name, False otherwise.
        """
        if player_name != self._player_a[0] or self._player_b[0]:
            return False

    def _are_valid_coordinates(self, coordinates):
        """
        Checks that the given coordinates are on the game board.
        :param coordinates: the (row, col) coordinates to check
        :returns: True if 'coordinates' are within the boundaries
            of the board, False otherwise.
        """
        row, col = coordinates
        return 0 <= row <= 6 and 0 <= col <= 6

    def make_move(self, player_name, coordinates, direction):
        """
        Attempts to perform a move by a player and modifies the state of
        the game accordingly.

        :param player_name: player making move
        :param coordinates: coordinates as tuple (row, column) of marble
            that is going to be pushed
        :param direction: L (left), R (right), F (forward), B (backward). This is
            the direction that the marbles will be pushed towards.
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

        # If there is already a winner, no moves are allowed.
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

        #### Below this line, we know the move is valid ####

        # We know the move is valid, so we can call it complete and update
        # the boards.
        self._previous_board = self._board
        self._board = board_copy

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

        # If the move was valid but the game did not end, return True
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
        white_marbles = 0
        black_marbles = 0
        red_marbles = 0

        for row in range(7):
            for col in range(7):
                cell_color = self._board[row][col]
                if cell_color == 'R':
                    red_marbles += 1
                elif cell_color == 'B':
                    black_marbles += 1
                elif cell_color == 'W':
                    white_marbles += 1

        return white_marbles, black_marbles, red_marbles

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
        """
        This method performs the actual shifting of marbles that happen
        when a move is performed.

        This method does not make any checks to make sure the move is valid.
        Its only role is to shift cells of the passed in board in the
        specified direction.

        Shifting the board might result in a marble falling off the board,
        so this method returns the content of the marble that went
        off the board (if there is one). Otherwise, it returns None.
        """
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
                if overwrite == 'X':
                    break

        if direction == 'R':
            to_move = board[row][col]
            overwrite = 'X'
            while col <= 6:
                board[row][col] = overwrite
                if col == 6:
                    pushed_off = to_move
                    break
                col += 1
                to_move, overwrite = board[row][col], to_move
                if overwrite == 'X':
                    break

        if direction == 'F':
            to_move = board[row][col]
            overwrite = 'X'
            while row >= 0:
                if row == 0:
                    pushed_off = to_move
                board[row][col] = overwrite
                row -= 1
                to_move, overwrite = board[row][col], to_move
                if overwrite == 'X':
                    break

        if direction == 'B':
            to_move = board[row][col]
            overwrite = 'X'
            while row <= 6:
                board[row][col] = overwrite
                if row == 6:
                    pushed_off = to_move
                    break
                row += 1
                to_move, overwrite = board[row][col], to_move
                if overwrite == 'X':
                    break

        return pushed_off


