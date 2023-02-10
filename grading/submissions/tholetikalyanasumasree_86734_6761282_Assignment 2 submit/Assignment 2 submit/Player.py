# Kalyana Suma Sree Tholeti
# SID: 2005436

import numpy as np

DEPTH = 6
WINDOW_SIZE = 4
ROWS, COLUMNS = 6, 7


class AIPlayer:
    def __init__(self, player_number):
        self.player_number = player_number
        self.type = 'ai'
        self.player_string = 'Player {}:ai'.format(player_number)

    @staticmethod
    def get_possible_moves(board):
        moves = []
        for c in range(COLUMNS):
            for r in range(ROWS):
                if board[r][c] != 0:
                    continue
                else:
                    moves.append([r, c])
                    break
        return moves

    def make_ab_move(self, board, alpha, beta, depth, player1, player2):
        alpha_columns_list = []
        for row, column in self.get_possible_moves(board):
            board[row][column] = player1
            alpha = max(alpha, self.min_max_value(board, alpha, beta, depth + 1, player1, player2, "min"))
            alpha_columns_list.append([alpha, column])
            board[row][column] = 0
        return max(alpha_columns_list, key=lambda z: z[0])[1]

    def min_max_value(self, board, alpha, beta, depth, player1, player2, min_max):
        moves = self.get_possible_moves(board)
        if (min_max == "min" and (depth >= DEPTH or not moves)) or (min_max == "max" and (depth == DEPTH or not moves)):
            return self.evaluation_function(board)
        for row, column in moves:
            board[row][column] = player2 if min_max == "min" else player1
            next_move = "min" if min_max == "max" else "max"
            ret = self.min_max_value(board, alpha, beta, depth + 1, player1, player2, next_move)
            val = min(beta, ret) if min_max == "min" else max(alpha, ret)
            if min_max == "min":
                beta = val
            else:
                alpha = val
            board[row][column] = 0
            if beta <= alpha:
                return beta if min_max == "min" else alpha
        return beta if min_max == "min" else alpha

    def get_alpha_beta_move(self, board):
        player1 = self.player_number
        player2 = 2 if self.player_number == 1 else 1
        return self.make_ab_move(board, float("-inf"), float("inf"), 0, player1, player2)

    def get_expectimax_move(self, board):
        player1 = self.player_number
        player2 = 2 if self.player_number == 1 else 1

        def make_move(depth):
            a = float("-inf")
            moves = self.get_possible_moves(board)
            alpha_cols_list = []
            for r, c in moves:
                board[r][c] = player1
                a = max(a, exp_val(depth - 1))
                alpha_cols_list.append([a, c])
                board[r][c] = 0
            return max(alpha_cols_list, key=lambda z: z[0])[1]

        def max_val(depth):
            max_ = float("-inf")
            actions = self.get_possible_moves(board)
            if depth == 0 or not actions:
                return self.evaluation_function(board)
            for row, column in actions:
                board[row][column] = player1
                max_ = max(max_, exp_val(depth - 1))
            return max_

        def exp_val(depth):
            exp_value = 0
            actions = self.get_possible_moves(board)
            if depth == 0 or not actions:
                return self.evaluation_function(board)
            for row, column in actions:
                board[row][column] = player2
                val = max_val(depth - 1)
                exp_value += val
            p = 1 / len(actions)
            return exp_value * p

        return make_move(3)

    @staticmethod
    def get_current_score(win, current_player, other_player):
        current_score = 0
        player_score = win.count(current_player)
        other_player_score = win.count(other_player)
        zero_score = win.count(0)
        if player_score == 3 and zero_score == 1:
            current_score += 100
        elif player_score == 2 and zero_score == 2:
            current_score += 10
        elif player_score == 4:
            current_score += 1000

        if other_player_score == 3 and zero_score == 1:
            current_score -= 10
        elif other_player_score == 2 and zero_score == 2:
            current_score -= 1
        elif other_player_score == 4:
            current_score -= 100

        return current_score

    def evaluation_function(self, board):
        """
        Given the current stat of the board, return the scalar value that 
        represents the evaluation function for the current player
       
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
        player1 = self.player_number
        player2 = 2 if self.player_number == 1 else 1
        score = 0

        for r in range(ROWS - 3):
            for c in range(COLUMNS - 3):
                current_window = [board[r + i][c + i] for i in range(WINDOW_SIZE)]
                score += self.get_current_score(current_window, player1, player2)

        for r in range(ROWS - 3):
            for c in range(COLUMNS - 3):
                current_window = [board[r + 3 - i][c + i] for i in range(WINDOW_SIZE)]
                score += self.get_current_score(current_window, player1, player2)

        for r in range(ROWS):
            row_array = [int(i) for i in list(board[r, :])]
            for c in range(COLUMNS - 3):
                current_window = row_array[c:c + WINDOW_SIZE]
                score += self.get_current_score(current_window, player1, player2)

        for c in range(COLUMNS):
            col_array = [int(i) for i in list(board[:, c])]
            for r in range(ROWS - 3):
                current_window = col_array[r:r + WINDOW_SIZE]
                score += self.get_current_score(current_window, player1, player2)

        return score


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
