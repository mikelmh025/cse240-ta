import copy
import numpy as np
import random
import time
import math

MAX_SCORE = 10000
MIN_SCORE = -10000

class AIPlayer:
    def __init__(self, player_number):
        self.player_number = player_number
        self.opponent_number = (self.player_number*2)%3
        self.type = 'ai'
        self.player_string = 'Player {}:ai'.format(player_number)

    def get_valid_cols(self, board):
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

        def minimax(board, curr_depth, max_depth, alpha, beta, max_player):
            valid_cols = self.get_valid_cols(board)
            if not valid_cols:
                return None, 0
            if curr_depth == max_depth:
                return None, self.evaluation_function(board)
            if max_player:
                local_max = -math.inf
                choice = random.choice(valid_cols)
                #print(curr_depth)
                for col in valid_cols:
                    row = board.shape[0]-1
                    while board[row, col] != 0:
                        row -= 1
                    board_new = copy.deepcopy(board)
                    board_new[row, col] = self.player_number
                    new_score = minimax(board_new, curr_depth+1, max_depth, alpha, beta, False)[-1]
                    if new_score > local_max:
                        local_max = new_score
                        choice = col
                    alpha = max(alpha, local_max)
                    if alpha >= beta:
                        break
                return choice, local_max
            else:
                local_max = math.inf
                choice = random.choice(valid_cols)
                #print(curr_depth)
                for col in valid_cols:
                    row = board.shape[0]-1
                    while board[row, col] != 0:
                        row -= 1
                    board_new = copy.deepcopy(board)
                    board_new[row, col] = self.opponent_number
                    new_score = minimax(board_new, curr_depth+1, max_depth, alpha, beta, True)[-1]
                    if new_score < local_max:
                        local_max = new_score
                        choice = col
                    beta = min(beta, local_max)
                    if alpha >= beta:
                        break
                return choice, local_max
        
        start = time.time()
        choice = minimax(board, curr_depth=0, max_depth=6, alpha=-math.inf, beta=math.inf, max_player=True)[0]
        end = time.time()
        print(end - start)
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
        def expectimax(board, curr_depth, max_depth, max_player):
            valid_cols = self.get_valid_cols(board)
            if not valid_cols:
                return None, 0
            if curr_depth == max_depth:
                return None, self.evaluation_function(board)
            if max_player:
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
                    cp_board[row, col] = self.opponent_number
                    value += expectimax(cp_board, curr_depth+1, max_depth, True)[-1]
                return None, value/len(valid_cols)
        
        choice = expectimax(board, curr_depth=0, max_depth=4, max_player=True)[0]

        return choice

    def position_score(self, board, row, col, y, x):
        player_points = 0
        opponent_points = 0

        opp_number = self.opponent_number
        player_number = self.player_number

        for i in range(4):
            if board[row, col] == opp_number:
                opponent_points += 1
            elif board[row, col] == player_number:
                player_points += 1

            row += y
            col += x
        
        if opponent_points == 4:
            return MIN_SCORE
        elif player_points == 4:
            return MAX_SCORE
        else:
            return player_points

    def evaluation_function(self, board):
        rows, cols = board.shape
        
        vertical_points = 0
        horizontal_points = 0
        diagonal_points1 = 0
        diagonal_points2 = 0

        # horizontal score for win
        for row in range(rows):
            for col in range(cols-3):
                score = self.position_score(board, row, col, 0, 1)
                if score in [MAX_SCORE, MIN_SCORE]:
                    return score
                horizontal_points += score
        # vertical score for win
        for row in range(rows-3):
            for col in range(cols):
                score = self.position_score(board, row, col, 1, 0)
                if score in [MAX_SCORE, MIN_SCORE]:
                    return score
                vertical_points += score
        # diagonal score for win        
        for row in range(rows-3):
            for col in range(cols-3):
                score = self.position_score(board, row, col, 1, 1)
                if score in [MAX_SCORE, MIN_SCORE]:
                    return score
                diagonal_points1 += score
        # diagonal score for win
        for row in range(3, rows):
            for col in range(cols-3):
                score = self.position_score(board, row, col, -1, 1)
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

