# Name: Rohan Ghosalkar
# SID: 2005624
# Class : CSE240
# References added at the end

import numpy as np
import math
import copy
DEPTH = 4
window_length = 4
EMPTY = 0
total_rows = 6
total_columns = 7

class AIPlayer:
    def __init__(self, player_number):
        self.player_number = player_number
        self.type = 'ai'
        self.player_string = 'Player {}:ai'.format(player_number)

    def get_alpha_beta_move(self, board):

        player_num = self.player_number
        opponent_num = (player_num*2)%3
        values = []

        def alpha_beta_move(board, alpha, beta, depth, player_num, opponent_num):
            for row, column in self.possible_moves(board):
                board[row][column] = player_num
                alpha = max(alpha, min_value(board, alpha, beta, depth + 1 , player_num, opponent_num))
                values.append([alpha,column])
                board[row][column] = 0
                
            output = max(values, key = lambda x: x[0]) 
            return output[1]

        def min_value(board, alpha, beta, depth, player_num, opponent_num):
            actions = self.possible_moves(board)
            if depth >= DEPTH or not actions:
                return self.evaluation_function(board)
            for row, column in actions:
                board[row][column] = opponent_num 
                ret = max_value(board, alpha, beta, depth+1, player_num, opponent_num)
                beta = min(beta, ret)
                board[row][column] = 0
                if beta <= alpha:
                    return beta 
            return beta

        def max_value(board, alpha, beta, depth, player_num, opponent_num):
            actions = self.possible_moves(board)
            if depth == DEPTH or not actions:
                return self.evaluation_function(board)
            for row, column in actions:
                board[row][column] = player_num 
                result = min_value(board, alpha, beta, depth+1, player_num, opponent_num)
                alpha = max(alpha, result)
                board[row][column] = 0
                if alpha >= beta:
                    return alpha
            return alpha

        return alpha_beta_move(board, -math.inf, math.inf, 0, player_num, opponent_num) 

 #       raise NotImplementedError('Whoops I don\'t know what to do')


    def possible_moves(self, board):   #We are calculating all the possible moves the payer can make


        possible_moves = []
        for column in range(total_columns):
            for row in range(total_rows):
                if board[row][column] == 0:
                    possible_moves.append([row, column])
                    break

        return possible_moves


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

        player_num = self.player_number
        opponent_num = (player_num*2)%3
        values = []

        def value(board, depth, player_num, opponent_num):
            a = -math.inf
            actions = self.possible_moves(board)
            for row, column in actions:
                board[row][column] = player_num
                a = max(a, exp_val(board,depth-1 , player_num, opponent_num))
                values.append([a,column])
                board[row][column] = 0
            output = max(values, key = lambda x: x[0])
            return output[1]


        def max_val(board, depth, player_num, opponent_num):
            maxval = -math.inf
            actions = self.possible_moves(board)
            if depth == 0 or not actions: 
                return self.evaluation_function(board)
            for row, column in actions:
                board[row][column] = player_num 
                val = exp_val(board, depth - 1, player_num, opponent_num)
                maxval = max(maxval, val)
            return maxval


        def exp_val(board, depth, player_num, opponent_num): 
            exp_value = 0
            actions = self.possible_moves(board)
            if depth == 0 or not actions: 
                return self.evaluation_function(board)
            for row, column in actions:
                board[row][column] = opponent_num 
                val = max_val(board , depth-1, player_num, opponent_num)
                exp_value += val
            p = 1/len(actions)
            return exp_value*p


        return value(board, DEPTH, player_num, opponent_num)

 #       raise NotImplementedError('Whoops I don\'t know what to do')


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

        player_num = self.player_number
        opponent_num = (player_num*2)%3
        values = []      
       
        score = 0

        def evaluate_window(window, player_num):
            w_score = 0
            if window.count(player_num) == 4:
                w_score += 100
            elif window.count(player_num) == 3 and window.count(EMPTY) == 1:
                w_score += 5
            elif window.count(player_num) == 2 and window.count(EMPTY) == 2:
                w_score += 2

            if window.count(opponent_num) == 3 and window.count(EMPTY) == 1:
                w_score -= 4
            elif window.count(opponent_num) == 2 and window.count(EMPTY) == 2:
                w_score -= 5
            elif window.count(opponent_num) == 4:
                w_score -= 500
            return w_score 

        center_array = [int(i) for i in list(board[:, total_columns//2])]
        center_count = center_array.count(player_num)
        score += center_count * 3
        
        #Horizontal check
        for r in range(total_rows):
            row_array = [int(i) for i in list(board[r,:])]
            for c in range(total_columns-3):
                window = row_array[c:c+window_length]
                score += evaluate_window(window, player_num)

        #Vertical check
        for c in range(total_columns):
            col_array = [int(i) for i in list(board[:,c])]
            for r in range(total_rows-3):
                window = col_array[r:r+window_length]
                score += evaluate_window(window, player_num)

        #Positive sloped diagonal check
        for r in range(total_rows-3):
            for c in range(total_columns-3):
                window = [board[r+i][c+i] for i in range(window_length)]
                score += evaluate_window(window, player_num)

        #Negative sloped diagonal check
        for r in range(total_rows-3):
            for c in range(total_columns-3):
                window = [board[r+3-i][c+i] for i in range(window_length)]
                score += evaluate_window(window, player_num)      
        #print("eval done")

        return score


        return 0


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

# References : https://medium.com/analytics-vidhya/artificial-intelligence-at-play-connect-four-minimax-algorithm-explained-3b5fc32e4a4f
# References : https://github.com/KeithGalli/Connect4-Python/blob/master/connect4_with_ai.py
# References : https://github.com/gita-vahdatinia/ConnectFour/blob/master/Player.py


