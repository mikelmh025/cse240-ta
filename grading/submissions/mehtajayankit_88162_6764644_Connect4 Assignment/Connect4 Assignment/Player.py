import numpy as np
import math

import random


max_depth = 4

row_count = 6
col_count = 7

empty = 0
window_len = 4


class AIPlayer:
    def __init__(self, player_number):
        self.player_number = player_number
        self.type = 'ai'
        self.player_string = 'Player {}:ai'.format(player_number)
    

    def valid_moves(self, board):

        # Check for all valid columns

        valid_moves = []
        for i in range(row_count):
            for j in range(row_count):

                if board[i][j] == 0:
                    valid_moves.append([i,j])
                    break


        return valid_moves


    def get_alpha_beta_move(self, board):


        piece = self.player_number
        opp_piece = (self.player_number*2)%3
        values = []
        #count = 0


        def move(board, alpha, beta, depth, piece, opp_piece):


            # if count == 0:
            #     count += 1
            #     return 3 

            #print(f'depth: {depth}')
            #print(f'valid moves: {self.valid_moves(board)}')

            # if [3,0] in self.valid_moves(board):
            #     return 3

            for row, col in self.valid_moves(board):
                board[row][col] = piece
                alpha = max(alpha, min_val(board, alpha, beta, depth + 1, piece, opp_piece))
                #print(f'alpha: {alpha}')
                values.append([alpha, col])
                board[row][col] = 0
                

            #print(f'values: {values}')
            path = max(values, key = lambda x: x[0])
            #print(f'path: {path}')


            #print(f'path: {path[1]}')
            
            return path[1]

            #return random.randint(0, 6)


        def min_val(board, alpha, beta, depth, piece, opp_piece):

            valid_moves = self.valid_moves(board)
            #print(f'depth in beta: {depth}')
            
            if depth >= max_depth or not valid_moves:
                return self.evaluation_function(board)

            for row, col in valid_moves:
                #c = np.random.choice(col)
                #print(f'c: {c}')
                board[row][col] = opp_piece
                local_max = max_value(board, alpha, beta, depth+1, piece, opp_piece)
                beta = min(beta, local_max)
                board[row][col] = 0

                if beta <= alpha:
                    #print(f'beta: {beta}')
                    return beta

            #print(f'beta: {beta}')
            return beta


        def max_value(board, alpha, beta, depth, piece, opp_piece):

            valid_moves = self.valid_moves(board)
            #print(f'depth in alpha: {depth}')


            if depth == max_depth or not valid_moves:
                return self.evaluation_function(board)

            for row, col in valid_moves:
                board[row][col] = opp_piece
                local_min = min_val(board, alpha, beta, depth+1, piece, opp_piece)
                alpha = max(alpha, local_min)
                board[row][col] = 0

                if alpha >= beta:
                    #print(f'alpha: {alpha}')
                    return alpha

            #print(f'alpha: {alpha}')
            return alpha




        return move(board, -math.inf, math.inf, 0, piece, opp_piece)

        
    
    def get_expectimax_move(self, board):
        
        piece = self.player_number
        opp_piece = (self.player_number*2) % 3
        values = []

        def val(board, depth, piece, opp_piece):

            local_max = -math.inf
            valid_moves = self.valid_moves(board)
            for row, col in valid_moves:

                board[row][col] = piece
                local_max = max(local_max, expected_val(board, depth-1, piece, opp_piece))
                values.append([local_max, col])
                board[row][col] = 0

            path = max(values, key = lambda x: x[0])
            return path[1]


        def max_val(board, depth, piece, opp_piece):
            
            local_max = -math.inf
            valid_moves = self.valid_moves(board)

            if depth == 0 or not valid_moves:
                return self.evaluation_function(board)

            for r,c in valid_moves:
                board[r][c] = piece
                exp_val = expected_val(board, depth-1, piece, opp_piece)
                local_max = max(local_max, exp_val)

            return local_max

        def expected_val(board, depth, piece, opp_piece):

            exp_val = 0
            valid_moves = self.valid_moves(board)

            if depth == 0 or not valid_moves: return self.evaluation_function(board)

            for r,c in valid_moves:
                board[r][c] = opp_piece
                local_max = max_val(board, depth-1, piece, opp_piece)
                exp_val += local_max

            p = 1/len(valid_moves)

            return exp_val*p




        return val(board, 3, piece, opp_piece)



        



    def evaluation_function(self, board):
        
        piece = self.player_number
        opp_piece = (self.player_number*2)%3
        score = 0

        def evaluate_window(window, piece):

            sc = 0
            #Player score evaluation
            if window.count(piece) == 4:
                sc += 10000000

            elif window.count(piece) == 3 and window.count(empty) == 1:
                sc += 20000
            
            elif window.count(piece) == 2 and window.count(empty) == 2:
                sc += 1000

            # Opponent score evaluation    
            if window.count(opp_piece) == 3 and window.count(empty) == 1:
                sc -= 20000
            
            elif window.count(opp_piece) == 2 and window.count(empty) == 2:
                sc -= 1000
            
            elif window.count(opp_piece) == 4:
                sc -= 10000000 

            

            return sc


        #Horizontal Check
        for r in range(row_count):
            row_range = [int(i) for i in list(board[r,:])]
            for c in range(col_count-3):
                win = row_range[c:c+window_len]
                score += evaluate_window(win, piece)

        #Vertical Check
        for c in range(col_count):
            col_range = [int(i) for i in list(board[:,c])]
            for r in range(row_count-3):
                win = col_range[r:r+window_len]
                score += evaluate_window(win, piece)

        #Positive Sloped Diagonal Check
        for r in range(row_count-3):
            for c in range(col_count-3):
                win = [board[r+i][c+i] for i in range(window_len)]
                score += evaluate_window(win, piece)

        #Negative Sloped Diagonal Check
        for r in range(row_count-3):
            for c in range(col_count-3):
                win = [board[r+3-i][c+i] for i in range(window_len)]
                score += evaluate_window(win, piece)

        #print(f'eval score: {score}')
        return score
    

class RandomPlayer:
    def __init__(self, player_number):
        self.player_number = player_number
        self.type = 'random'
        self.player_string = 'Player {}:random'.format(player_number)

    def get_move(self, board):
        

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
        

        valid_cols = []
        for i, col in enumerate(board.T):
            if 0 in col:
                valid_cols.append(i)

        move = int(input('Enter your move: '))

        while move not in valid_cols:
            print('Column full, choose from:{}'.format(valid_cols))
            move = int(input('Enter your move: '))

        return move

