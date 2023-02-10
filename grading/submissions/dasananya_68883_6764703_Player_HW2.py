#Ananya Das
#Student ID: 1926603

import numpy as np
import math
import copy

DEPTH = 6
EXP_DEPTH = 3
window_length = 4
EMPTY = 0
row_count = 6
column_count = 7

class AIPlayer:
    def __init__(self, player_number):
        self.player_number = player_number
        self.type = 'ai'
        self.player_string = 'Player {}:ai'.format(player_number)

    def actions(self, board):
        #check for valid columns that a player can add
        action = []
        for column in range(column_count):
            for row in range(row_count):
                if board[row][column] == 0:
                    action.append([row, column])
                    break
        #print(action)
        return action


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
        piece = self.player_number
        opp_piece = (self.player_number *2)%3
        values = []
        def alpha_beta_move( board, alpha, beta, depth, piece, opp_piece):
            for row, column in self.actions(board):
                board[row][column] = piece
                alpha = max(alpha, min_value(board, alpha, beta, depth + 1 , piece, opp_piece))
                values.append([alpha,column])
                board[row][column] = 0
                
            output = max(values, key = lambda x: x[0]) 
            #print(values)
            #print(output)
            return output[1]
        def min_value(board, alpha, beta, depth, piece, opp_piece):
            actions = self.actions(board)
            if depth >= DEPTH or not actions:
                return self.evaluation_function(board)
            for row, column in actions:
                board[row][column] = opp_piece 
                ret = max_value(board, alpha, beta, depth+1, piece, opp_piece)
                beta = min(beta, ret)
                board[row][column] = 0
                if beta <= alpha:
                    return beta 
            return beta
        def max_value(board, alpha, beta, depth, piece, opp_piece):
            actions = self.actions(board)
            if depth == DEPTH or not actions:
                return self.evaluation_function(board)
            for row, column in actions:
                board[row][column] = piece 
                result = min_value(board, alpha, beta, depth+1, piece, opp_piece)
                alpha = max(alpha, result)
                board[row][column] = 0
                if alpha >= beta:
                    return alpha
            return alpha
        return alpha_beta_move(board, -math.inf, math.inf, 0, piece, opp_piece) 
        # raise NotImplementedError('Whoops I don\'t know what to do')

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
        #expectimax implemented considering maximizer
        piece = self.player_number
        opp_piece = (self.player_number *2)%3
        values = []
        def value(board, depth, piece, opp_piece):
            a = -math.inf
            actions = self.actions(board)
            for row, column in actions:
                board[row][column] = piece
                a = max(a, exp_val(board,depth-1 , piece, opp_piece))
                values.append([a,column])
                board[row][column] = 0
            output = max(values, key = lambda x: x[0])
            #print(values)
            #print(output)
            return output[1]
        def max_val(board, depth, piece, opp_piece):
            maxval = -math.inf
            actions = self.actions(board)
            if depth == 0 or not actions: 
                return self.evaluation_function(board)
            for row, column in actions:
                board[row][column] = piece 
                val = exp_val(board, depth - 1, piece, opp_piece)
                maxval = max(maxval, val)
            #print(maxval)
            return maxval
        def exp_val(board, depth, piece, opp_piece): 
            exp_value = 0
            actions = self.actions(board)
            if depth == 0 or not actions: 
                return self.evaluation_function(board)
            for row, column in actions:
                board[row][column] = opp_piece 
                val = max_val(board , depth-1, piece, opp_piece)
                exp_value += val
            p = 1/len(actions)
            #print(p)
            #print(exp_value*p)
            return exp_value*p
        return value(board, EXP_DEPTH, piece, opp_piece)
        # raise NotImplementedError('Whoops I don\'t know what to do')

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
        #Evaluation function based on a window calculating the score based on vertical, horizontal and diagonal similar components
        piece = self.player_number
        opp_piece = (self.player_number *2)%3
        score = 0
        def evaluate_window(window, piece):
            w_score = 0
            if window.count(piece) == 4:
                w_score += 5000
            elif window.count(piece) == 3 and window.count(EMPTY) == 1:
                w_score += 500
            elif window.count(piece) == 2 and window.count(EMPTY) == 2:
                w_score += 50

            if window.count(opp_piece) == 3 and window.count(EMPTY) == 1:
                w_score -= 50
            elif window.count(opp_piece) == 2 and window.count(EMPTY) == 2:
                w_score -= 5
            elif window.count(opp_piece) == 4:
                w_score -= 500
            return w_score 
        
        #Horizontal check
        for r in range(row_count):
            row_array = [int(i) for i in list(board[r,:])]
            for c in range(column_count-3):
                window = row_array[c:c+window_length]
                score += evaluate_window(window, piece)
        #Vertical check
        for c in range(column_count):
            col_array = [int(i) for i in list(board[:,c])]
            for r in range(row_count-3):
                window = col_array[r:r+window_length]
                score += evaluate_window(window, piece)
        #Positive sloped diagonal check
        for r in range(row_count-3):
            for c in range(column_count-3):
                window = [board[r+i][c+i] for i in range(window_length)]
                score += evaluate_window(window, piece)
        #Negative sloped diagonal check
        for r in range(row_count-3):
            for c in range(column_count-3):
                window = [board[r+3-i][c+i] for i in range(window_length)]
                score += evaluate_window(window, piece)      
        #print("eval done")
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

