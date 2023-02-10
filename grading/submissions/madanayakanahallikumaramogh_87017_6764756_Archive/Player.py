import copy
import numpy as np
import random
import time

MAX_SCORE = 100000
MIN_SCORE = -100000

class AIPlayer:
    def __init__(self, player_number):
        self.player_number = player_number
        self.opposition_number = 2 if player_number==1 else 1
        self.type = 'ai'
        self.player_string = 'Player {}:ai'.format(player_number)

    def get_valid_locations(self, board):
        """
        returns list of column numbers with atleast one row space empty
        """
        valid_cols = []
        for col in range(board.shape[1]):
            if 0 in board[:,col]:
                valid_cols.append(col)
        return valid_cols

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

        def minimax(board, curr_depth, max_depth, alpha, beta, maximizing_player):
            valid_cols = self.get_valid_locations(board)
            if not valid_cols:
                return None, 0
            if curr_depth == max_depth:
                return None, self.evaluation_function(board)
            if maximizing_player:
                value = float('-inf')
                choice = random.choice(valid_cols)
                for col in valid_cols:
                    row = board.shape[0]-1
                    while board[row, col] != 0:
                        row -= 1
                    cp_board = copy.deepcopy(board)
                    cp_board[row, col] = self.player_number
                    new_score = minimax(cp_board, curr_depth+1, max_depth, alpha, beta, False)[-1]
                    if new_score > value:
                        value = new_score
                        choice = col
                    alpha = max(alpha, value)
                    if alpha >= beta:
                        break
                return choice, value
            else:
                value = float('inf')
                choice = random.choice(valid_cols)
                for col in valid_cols:
                    row = board.shape[0]-1
                    while board[row, col] != 0:
                        row -= 1
                    cp_board = copy.deepcopy(board)
                    cp_board[row, col] = self.opposition_number
                    new_score = minimax(cp_board, curr_depth+1, max_depth, alpha, beta, True)[-1]
                    if new_score < value:
                        value = new_score
                        choice = col
                    beta = min(beta, value)
                    if alpha >= beta:
                        break
                return choice, value
        
        choice, value = minimax(board, curr_depth=0, max_depth=4, alpha=float('-inf'), 
                        beta=float('inf'), maximizing_player=True)

        return choice

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
        def expectimax(board, curr_depth, max_depth, maximizing_player):
            valid_cols = self.get_valid_locations(board)
            if not valid_cols:
                return None, 0
            if curr_depth == max_depth:
                return None, self.evaluation_function(board)
            if maximizing_player:
                value = float('-inf')
                choice = random.choice(valid_cols)
                for col in valid_cols:
                    row = board.shape[0]-1
                    while board[row, col] != 0:
                        row -= 1
                    cp_board = copy.deepcopy(board)
                    cp_board[row, col] = self.player_number
                    new_score = expectimax(cp_board, curr_depth+1, max_depth, False)[-1]
                    if new_score > value:
                        value = new_score
                        choice = col
                return choice, value
            else:
                value = 0
                for col in valid_cols:
                    row = board.shape[0]-1
                    while board[row, col] != 0:
                        row -= 1
                    cp_board = copy.deepcopy(board)
                    cp_board[row, col] = self.opposition_number
                    value += expectimax(cp_board, curr_depth+1, max_depth, True)[-1]
                return None, value/len(valid_cols)
        
        choice, value = expectimax(board, curr_depth=0, max_depth=4, maximizing_player=True)

        return choice

    def score_position(self, board, row, col, delta_y, delta_x):
        """
        returns the score of a window from a given position (row, col).
        
        the window could either be horizontal or vertical or diagonal
        and the window is formed by delta_y and delta_x.

        the score is the MAX_SCORE or MIN_SCORE if the window  has all
        4 player numbers or opposition numbers accordingly. if not, the
        score is the number of player number in the window.
        """
        player_points = 0
        opp_points = 0

        opp_number = self.opposition_number
        player_number = self.player_number

        for i in range(4):
            if board[row, col] == opp_number:
                opp_points += 1
            elif board[row, col] == player_number:
                player_points += 1

            row += delta_y
            col += delta_x
        
        if opp_points == 4:
            return MIN_SCORE
        elif player_points == 4:
            return MAX_SCORE
        else:
            return player_points

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

        if there is a winning or losing sequence, it return the MAX_SCORE or
        MIN_SCORE accordingly.
        returns the sum of scores of all windows from all possible locations
        as the utility of the board in that state.
        """
        rows, cols = board.shape
        
        vertical_points = 0
        horizontal_points = 0
        diagonal_points1 = 0
        diagonal_points2 = 0

        for row in range(rows):
            for col in range(cols-3):
                score = self.score_position(board, row, col, 0, 1)
                if score in [MAX_SCORE, MIN_SCORE]:
                    return score
                horizontal_points += score

        for row in range(rows-3):
            for col in range(cols):
                score = self.score_position(board, row, col, 1, 0)
                if score in [MAX_SCORE, MIN_SCORE]:
                    return score
                vertical_points += score
                
        for row in range(rows-3):
            for col in range(cols-3):
                score = self.score_position(board, row, col, 1, 1)
                if score in [MAX_SCORE, MIN_SCORE]:
                    return score
                diagonal_points1 += score
        
        for row in range(3, rows):
            for col in range(cols-3):
                score = self.score_position(board, row, col, -1, 1)
                if score in [MAX_SCORE, MIN_SCORE]:
                    return score
                diagonal_points2 += score
        
        points = horizontal_points + vertical_points + diagonal_points1 + diagonal_points2
        return points


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
            if 0 in board[:,col]:
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

