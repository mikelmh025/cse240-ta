import math
import random
from copy import deepcopy

import numpy as np

MAX_DEPTH_LIMIT = 2
PLAYER1_PIECE = 1
PLAYER2_PIECE = 2
ROW_COUNT = 6
COLUMN_COUNT = 7
WINDOW_LENGTH = 4


class AIPlayer:
    def __init__(self, player_number):
        self.player_number = player_number
        self.type = 'ai'
        self.player_string = 'Player {}:ai'.format(player_number)

    def check_game_over(self, board):
        player_num = self.player_number
        # Check horizontal locations for win
        for c in range(COLUMN_COUNT - 3):
            for r in range(ROW_COUNT):
                if board[r][c] == player_num and board[r][c + 1] == player_num and board[r][c + 2] == player_num and \
                        board[r][c + 3] == player_num:
                    return True

        # Check vertical locations for win
        for c in range(COLUMN_COUNT):
            for r in range(ROW_COUNT - 3):
                if board[r][c] == player_num and board[r + 1][c] == player_num and board[r + 2][c] == player_num and \
                        board[r + 3][c] == player_num:
                    return True

        # Check positively sloped diagonals
        for c in range(COLUMN_COUNT - 3):
            for r in range(ROW_COUNT - 3):
                if board[r][c] == player_num and board[r + 1][c + 1] == player_num and board[r + 2][
                    c + 2] == player_num and \
                        board[r + 3][c + 3] == player_num:
                    return True

        # Check negatively sloped diagonals
        for c in range(COLUMN_COUNT - 3):
            for r in range(3, ROW_COUNT):
                if board[r][c] == player_num and board[r - 1][c + 1] == player_num and board[r - 2][
                    c + 2] == player_num and \
                        board[r - 3][c + 3] == player_num:
                    return True

        return False

    def get_valid_actions(self, board):
        """
        Get (row, col) where next move can be validly placed
        The problem is to choose valid columns only
        But along with the we will also extract the first possible valid row in the column
        as a valid move spot
        """
        valid_action_spaces = []
        for col in range(len(board[0])):
            row = 5
            while board[row][col] != 0 and row > 0:
                row = row - 1
            if board[row][col] == 0:
                valid_action_spaces.append((row, col))
        return valid_action_spaces

    def get_board_copy_with_new_action(self, board, action, number):
        # list of all possible locations in board where move can be made
        board_copy = deepcopy(board)
        row, col = action[0], action[1]
        board_copy[row][col] = number
        return board_copy

    def min_value(self, board, alpha, beta, depth):
        current_player_num = self.player_number
        opponent_num = PLAYER2_PIECE if self.player_number == PLAYER1_PIECE else PLAYER1_PIECE
        if self.check_game_over(board) or depth >= MAX_DEPTH_LIMIT:
            ret = (self.evaluation_function(board, current_player_num), random.choice(range(7)))
            return ret
        val_to_compare = math.inf
        actions = self.get_valid_actions(board)
        valid_columns_board = list(map(lambda x: x[1], actions))
        column = random.choice(valid_columns_board)
        for action in actions:
            action_val = \
                self.max_value(self.get_board_copy_with_new_action(board, action, opponent_num), alpha, beta,
                               depth + 1)[0]
            if action_val < val_to_compare:
                column = action[1]
            val_to_compare = min(val_to_compare, action_val)
            if val_to_compare < alpha:
                return val_to_compare, column
            beta = min(beta, val_to_compare)
        return val_to_compare, column

    def max_value(self, board, alpha, beta, depth):
        current_player_num = self.player_number
        if self.check_game_over(board) or depth >= MAX_DEPTH_LIMIT:
            # Return some dummy column at terminal level. The column will be chosen correctly at higher levels of recursion
            ret = (self.evaluation_function(board, current_player_num), random.choice(range(7)))
            return ret
        val_to_compare = -math.inf
        actions = self.get_valid_actions(board)
        valid_columns_board = list(map(lambda x: x[1], actions))
        column = random.choice(valid_columns_board)
        for action in actions:
            action_val = \
                self.min_value(self.get_board_copy_with_new_action(board, action, current_player_num), alpha, beta,
                               depth + 1)[0]
            if action_val > val_to_compare:
                column = action[1]
            val_to_compare = max(val_to_compare, action_val)
            if val_to_compare > beta:
                return val_to_compare, column
            alpha = max(alpha, val_to_compare)
        return val_to_compare, column

    def get_alpha_beta_move(self, board):
        """
        Given the current state of the board, return the next move based on
        the alpha-beta pruning algorithm

        This will play against either itself or a human player

        INPUTS:
        board - a numpy array containing the state of the board using the
                following encoding:
                - the board maintains its same two dimensions
                    - row 0 is the top of the board and so is
                      the last row filled
                - spaces that are unoccupied are marked as 0
                - spaces that are occupied by player 1 have a 1 in them
                - spaces that are occupied by player 2 have a 2 in them

        RETURNS:
        The 0 based index of the column that represents the next move
        """
        alpha = -math.inf
        beta = math.inf
        depth = 0
        move = self.max_value(board, alpha, beta, depth)
        return move[1]

    def expectimax_maxValue(self, board, alpha, beta, depth):
        current_player_num = self.player_number
        if self.check_game_over(board) or depth == 0:
            # Return some dummy column at terminal level. The column will be chosen correctly at higher levels of recursion
            ret = (random.choice(range(7)), self.evaluation_function(board, current_player_num))
            return ret
        val_to_compare = -math.inf
        actions = self.get_valid_actions(board)
        valid_columns_board = list(map(lambda x: x[1], actions))
        column = random.choice(valid_columns_board)

        for action in actions:
            action_val = self.expectimax_expValue(self.get_board_copy_with_new_action(board, action, current_player_num), alpha, beta, depth-1)[1]

            if action_val > val_to_compare:
                val_to_compare = action_val
                column = action[1]

            alpha = max(alpha, val_to_compare)
            if alpha >= beta:
                break

        return column, val_to_compare

    def expectimax_expValue(self, board, alpha, beta, depth):
        current_player_num = self.player_number
        opponent_num = PLAYER2_PIECE if self.player_number == PLAYER1_PIECE else PLAYER1_PIECE
        if self.check_game_over(board) or depth >= MAX_DEPTH_LIMIT:
            ret = (random.choice(range(7)), self.evaluation_function(board, current_player_num))
            return ret
        val_to_compare = 0
        actions = self.get_valid_actions(board)
        valid_columns_board = list(map(lambda x: x[1], actions))
        column = random.choice(valid_columns_board)

        for action in actions:
            action_val = self.expectimax_maxValue(self.get_board_copy_with_new_action(board, action, opponent_num), alpha, beta, depth-1)[1]

            if action_val <= val_to_compare:
                val_to_compare = action_val
                column = action[1]

            beta = math.floor(val_to_compare / len(actions))
            if alpha >= beta:
                break

        return column, val_to_compare

    def get_expectimax_move(self, board):
        """
        Given the current state of the board, return the next move based on
        the expectimax algorithm.

        This will play against the random player, who chooses any valid move
        with equal probability

        INPUTS:
        board - a numpy array containing the state of the board using the
                following encoding:
                - the board maintains its same two dimensions
                    - row 0 is the top of the board and so is
                      the last row filled
                - spaces that are unoccupied are marked as 0
                - spaces that are occupied by player 1 have a 1 in them
                - spaces that are occupied by player 2 have a 2 in them

        RETURNS:
        The 0 based index of the column that represents the next move
        """
        alpha = -math.inf
        beta = 0
        depth = 4
        col, expectimax_score = self.expectimax_maxValue(board, alpha, beta, depth)
        return col

    def evaluation_function(self, board, player_num):
        """
        Given the current stat of the board, return the scalar value that
        represents the evaluation function for the current player
        Board dimension: 6x7
        INPUTS:
        board - a numpy array containing the state of the board using the
                following encoding:
                - the board maintains its same two dimensions
                    - row 0 is the top of the board and so is
                      the last row filled
                - spaces that are unoccupied are marked as 0
                - spaces that are occupied by player 1 have a 1 in them
                - spaces that are occupied by player 2 have a 2 in them

        RETURNS:
        The utility value for the current board
        """
        score = 0

        center_array = [int(i) for i in list(board[:, COLUMN_COUNT // 2])]
        center_count = center_array.count(player_num)
        score += center_count * 3

        # Score based on horizontal expansion
        for r in range(ROW_COUNT):
            row_arr = [int(i) for i in list(board[r, :])]
            # Look at window sizes of 4 in each row. The start of these window size of 4 ends at column -3.
            for c in range(
                    COLUMN_COUNT - 3):  # subtract 3 because we want to look at current pos to current pos + 4
                window = row_arr[c:c + WINDOW_LENGTH]
                score += self.evaluate_window(window, player_num)

        # Score Vertical
        for c in range(COLUMN_COUNT):
            col_array = [int(i) for i in list(board[:, c])]
            for r in range(ROW_COUNT - 3):
                window = col_array[r:r + WINDOW_LENGTH]
                score += self.evaluate_window(window, player_num)

        # Score positive sloped diagonal
        for r in range(ROW_COUNT - 3):
            for c in range(COLUMN_COUNT - 3):
                window = [board[r + i][c + i] for i in range(WINDOW_LENGTH)]
                score += self.evaluate_window(window, player_num)

        # Score negative sloped diagonal
        for r in range(ROW_COUNT - 3):
            for c in range(COLUMN_COUNT - 3):
                window = [board[r + 3 - i][c + i] for i in range(WINDOW_LENGTH)]
                score += self.evaluate_window(window, player_num)

        return score

    def evaluate_window(self, window, player_num):
        """
        Receives a window of size 4 form the game board. Depending on number of points captured by a player
        in the window an appropriate score is updated. Here we will follow the following heuristics:

            1. If all 4 circles are conquered, then its a victory => Max score of 100 is awarded
            2. If 3 circles are conquered and there is one empty space, an award of 5 is given
            3. If 2 circles are conquered and 2 are empty, a score of 2 is given
            4. If 3 circles are occupied by opponent piece and an empty square is present, a score penalty of -8 is given
        """
        window_score = 0
        if player_num == PLAYER1_PIECE:
            opponent = PLAYER2_PIECE
        else:
            opponent = PLAYER1_PIECE
        if window.count(player_num) == 4:
            window_score += 100
        elif window.count(player_num) == 3 and window.count(0) == 1:
            window_score += 5
        elif window.count(player_num) == 2 and window.count(0) == 2:
            window_score += 2

        if window.count(opponent) == 3 and window.count(0) == 1:
            window_score -= 8

        return window_score


class RandomPlayer:
    def __init__(self, player_number):
        self.player_number = player_number
        self.type = 'random'
        self.player_string = 'Player {}:random'.format(player_number)

    def get_move(self, board):
        """
        Given the current board state select a random column from the available
        valid moves.

        INPUTS:
        board - a numpy array containing the state of the board using the
                following encoding:
                - the board maintains its same two dimensions
                    - row 0 is the top of the board and so is
                      the last row filled
                - spaces that are unoccupied are marked as 0
                - spaces that are occupied by player 1 have a 1 in them
                - spaces that are occupied by player 2 have a 2 in them

        RETURNS:
        The 0 based index of the column that represents the next move
        """
        valid_cols = []
        for col in range(board.shape[1]):
            if 0 in board[:, col]:
                valid_cols.append(col)

        return np.random.choice(valid_cols)


class HumanPlayer:
    def __init__(self, player_number):
        self.player_number = player_number
        self.type = 'human'
        self.player_string = 'Player {}:human'.format(player_number)

    def get_move(self, board):
        """
        Given the current board state returns the human input for next move

        INPUTS:
        board - a numpy array containing the state of the board using the
                following encoding:
                - the board maintains its same two dimensions
                    - row 0 is the top of the board and so is
                      the last row filled
                - spaces that are unoccupied are marked as 0
                - spaces that are occupied by player 1 have a 1 in them
                - spaces that are occupied by player 2 have a 2 in them

        RETURNS:
        The 0 based index of the column that represents the next move
        """

        valid_cols = []
        for i, col in enumerate(board.T):
            if 0 in col:
                valid_cols.append(i)

        move = int(input('Enter your move: '))

        while move not in valid_cols:
            print('Column full, choose from:{}'.format(valid_cols))
            move = int(input('Enter your move: '))

        return move
