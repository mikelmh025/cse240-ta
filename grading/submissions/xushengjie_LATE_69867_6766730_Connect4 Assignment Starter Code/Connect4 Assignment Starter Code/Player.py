import numpy as np
import random
import math

class AIPlayer:
    def __init__(self, player_number):
        self.player_number = player_number
        self.type = 'ai'
        self.player_string = 'Player {}:ai'.format(player_number)
        self.WINDOW_LENGTH = 4
    
    def is_valid_location(self, board, col):
        return board[0][col] == 0

    def get_valid_locations(self, board):
        valid_locations = []
        for col in range(7):
            if self.is_valid_location(board, col):
                for row in range(5,0,-1):
                    # print('check:',row,col)
                    if board[row][col] == 0:
                        valid_locations.append([row,col])
                        break
        return valid_locations

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
        # print(board)
        piece = self.player_number
        opp_piece = (self.player_number *2)%3
        values = []
        # print('Next moves:',self.get_valid_locations(board))
        def alpha_beta_move( board, alpha, beta, depth, piece, opp_piece):
            for row, column in self.get_valid_locations(board):
                board[row][column] = piece
                alpha = max(alpha, minValue(board, alpha, beta, depth+1 , piece, opp_piece))
                # print(alpha)
                values.append([alpha,column])
                board[row][column] = 0
            output = max(values, key = lambda x: x[0]) 
            return output[1]

        def maxValue(board, alpha, beta, depth, piece, opp_piece):
            v = -math.inf
            locations = self.get_valid_locations(board)
            if depth == 6 or not locations:
                # print('depth:',depth)
                return self.evaluation_function(board)
            for row, column in locations:
                temp_board = board.copy()
                temp_board[row][column] = piece
                # print('depth:',depth) 
                v = max(v,minValue(temp_board, alpha, beta, depth+1, piece, opp_piece))
                if v>= beta: return v
                alpha = max(alpha, v)
                if alpha >= beta:
                    break
            return v

        def minValue(board, alpha, beta, depth, piece, opp_piece):
            v = math.inf
            locations = self.get_valid_locations(board)
            if depth == 6 or not locations:
                # print('depth:',depth)
                return self.evaluation_function(board)
            for row, column in locations:
                temp_board = board.copy()
                temp_board[row][column] = opp_piece
                v = min(v,maxValue(temp_board, alpha, beta, depth+1, piece, opp_piece))
                if v<= alpha: return v
                beta = min(beta, v)
                if beta <= alpha:
                    break
            return v

        return alpha_beta_move(board, -math.inf, math.inf, 0, piece, opp_piece) 
 
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
        # return 0
        piece = self.player_number
        opp_piece = (self.player_number *2)%3
        values = []
        
        def value(board, depth, piece, opp_piece):
            # if s is a max node：
            #     return maxValue(s) 
            # if s is an exp node：
            #     return expValue(s) 
            # if s is a terminal node：
            #     return self.evaluation_function(s) 
            a = -math.inf
            locations = self.get_valid_locations(board)
            for row, column in locations:
                board[row][column] = piece
                a = max(a, expValue(board,depth-1 , piece, opp_piece))
                values.append([a,column])
                board[row][column] = 0
            output = max(values, key = lambda x: x[0])
            return output[1]

        def maxValue(board, depth, piece, opp_piece):
            # values = [value(s’) for s’ in successors(s)] 
            # return max(values)
            v = []
            locations = self.get_valid_locations(board)
            if depth == 0 or not locations:
                return self.evaluation_function(board)
            for row, column in locations:
                temp_board = board.copy()
                temp_board[row][column] = piece 
                v.append(expValue(temp_board, depth-1, piece, opp_piece))
            return max(v)

        def expValue(board, depth, piece, opp_piece):
            # values = [value(s’) for s’ in successors(s)] 
            # weights = [probability(s, s’) for s’ in successors(s)]
            v = []
            # weights = []
            locations = self.get_valid_locations(board)
            if depth == 0 or not locations:
                return self.evaluation_function(board)
            for row, column in locations:
                temp_board = board.copy()
                temp_board[row][column] = piece 
                v.append(maxValue(temp_board, depth-1, piece, opp_piece))
            # for _ in v:
            #     weights.append(1/len(v))
            return sum(v)/len(v)

        return value(board, 3, piece, opp_piece)

    def evaluate_window(self, window, piece):
        score = 0
        opp_piece = (piece *2)%3
        if window.count(piece) == 4:
            score += 100
        elif window.count(piece) == 3 and window.count(0) == 1:
            score += 5
        elif window.count(piece) == 2 and window.count(0) == 2:
            score += 1
        elif window.count(piece) == 1 and window.count(0) == 2:
            score += 0.5

        if window.count(opp_piece) == 3 and window.count(0) == 1:
            score -= 20
        elif window.count(opp_piece) == 2 and window.count(0) == 2:
            score -= 1
        elif window.count(opp_piece) == 1 and window.count(0) == 2:
            score -= 0.5

        return score

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
        
        piece = self.player_number
        score = 0

        # ## Score center column
        # center_array = [int(i) for i in list(board[:, 6//2])]
        # center_count = center_array.count(piece)
        # score += center_count * 3

        ## Score Horizontal
        for r in range(6):
            row_array = [int(i) for i in list(board[r,:])]
            for c in range(7-3):
                window = row_array[c:c+self.WINDOW_LENGTH]
                score += self.evaluate_window(window, piece)

        ## Score Vertical
        for c in range(7):
            col_array = [int(i) for i in list(board[:,c])]
            for r in range(6-2):
                window = col_array[r:r+self.WINDOW_LENGTH]
                score += self.evaluate_window(window, piece)

        ## Score positive sloped diagonal
        for r in range(6-3):
            for c in range(6,3,-1):
                window = [board[r+i][c-i] for i in range(self.WINDOW_LENGTH)]
                score += self.evaluate_window(window, piece)

        for r in range(6-3):
            for c in range(4):
                window = [board[r+i][c+i] for i in range(self.WINDOW_LENGTH)]
                score += self.evaluate_window(window, piece)

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

