import numpy as np
import math
import random
import time

ROW_COUNT = 6
COLUMN_COUNT = 7
WINDOW_LENGTH = 4
EMPTY = 0
INF = math.inf

class AIPlayer:
    def __init__(self, player_number):
        self.player_number = player_number
        self.type = 'ai'
        self.player_string = 'Player {}:ai'.format(player_number)
        self.explored = 0

    def get_valid_locations(self, board):
        valid_cols = []
        for col in range(board.shape[1]):
            if 0 in board[:,col]:
                valid_cols.append(col)
        return valid_cols

    def get_next_open_row(self, board, col):
        for row in range(board.shape[0]-1, -1, -1):
            if board[row, col] == 0:
                return row

    def winning_move(self, board, piece):
        """
            This function returns if the current move is the winning move
            PLAYER is an object of AIPlayer, RandomPlayer or HumanPlayer
        """
        #horizontal
        for c in range(COLUMN_COUNT-3):
            for r in range(ROW_COUNT):
                if board[r,c]==board[r,c+1]==board[r,c+2]==board[r,c+3]==piece:
                    return True
        #vertical
        for c in range(COLUMN_COUNT):
            for r in range(ROW_COUNT-3):
                if board[r,c]==board[r+1,c]==board[r+2,c]==board[r+3,c]==piece:
                    return True
        #diagnal
        for c in range(COLUMN_COUNT-3):
            for r in range(ROW_COUNT-3):
                if board[r,c]==board[r+1,c+1]==board[r+2,c+2]==board[r+3,c+3]==piece:
                    return True
        #negative diagnal
        for c in range(COLUMN_COUNT-3):
            for r in range(3, ROW_COUNT):
                if board[r,c]==board[r-1,c+1]==board[r-2,c+2]==board[r-3,c+3]==piece:
                    return True

    def evaluate_window(self,window):
        """
        This function will be used to calculate the score of the window
        4 same pieces in a row: score+100
        3 same pieces in a row: score+10
        2 same pieces in a row: score+4
        """
        piece = self.player_number #piece = 1 or 2
        opp_piece = 1 if piece == 2 else 2 
        score = 0
        if window.count(piece) == 4:
            score += 1000
        elif window.count(piece) == 3 and window.count(EMPTY) == 1:
            score += 10
        elif window.count(piece) == 2 and window.count(EMPTY) == 2:
            score += 4
        if window.count(opp_piece) == 3 and window.count(EMPTY) == 1:
            score -= 30 #opp_piece minimize the score
        return score


    def is_terminal_node(self, board):
        return self.winning_move(board, self.player_number) or self.winning_move(board, 1 if self.player_number==2 else 2) or len(self.get_valid_locations(board)) == 0

    def drop_piece(self, board, row, col, piece):
        board[row,col] = piece

    def minimax(self, board, ɑ, β ,depth, turn):
        is_terminal = self.is_terminal_node(board)
        valid_locations = self.get_valid_locations(board)
        my_turn = turn
        
        start_time = time.time()

        if depth == 0 or is_terminal:
            if is_terminal:      
                if self.winning_move(board, self.player_number):   
                    #print("my win", board)              
                    return None, 100000
                elif self.winning_move(board, 1 if self.player_number==2 else 2):
                    #print("my lose", board)
                    return None, -100000
                else:
                    return None, 0 
            else:
                #print("score is {}".format(self.evaluation_function(board)))
                return None, self.evaluation_function(board) 
        if my_turn:
            #print("max turn")
            value = -INF
            column = random.choice(valid_locations)
            for col in valid_locations:                             
                row = self.get_next_open_row(board, col)
                b_copy = board.copy()
                self.explored += 1
                if time.time() - start_time >= 10:
                    return column, value, self.explored
                self.drop_piece(b_copy, row, col, self.player_number)
                new_score = self.minimax(b_copy,ɑ, β , depth-1, False)[1]
                #print("my_turn, score is ", new_score, "\n" ,b_copy)
                if new_score > value:                
                    value = new_score
                    column = col
                ɑ = max(ɑ, value)
                if ɑ >= β:
                    break
            
            return column, value, self.explored
        else:
            #print("min turn")
            value = INF
            column = random.choice(valid_locations)
            for col in valid_locations:
                row = self.get_next_open_row(board, col)
                b_copy = board.copy()
                self.explored += 1
                if time.time() - start_time >= 10:
                    return column, value, self.explored
                self.drop_piece(b_copy, row, col, 1 if self.player_number==2 else 2)
                new_score = self.minimax(b_copy, ɑ, β ,depth-1, True)[1]
                #print("not my_turn, score is ", new_score, "\n" ,b_copy)
                # print("min score",new_score)
                if new_score < value:
                    value = new_score
                    column = col
                β = min(β, value)
                if ɑ >= β:
                    break
            
            return column, value, self.explored

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
        #print("I choose: ",self.minimax(board,-INF, INF, 2, True)[0])
        return self.minimax(board,-INF, INF, 2, True)[0]

    def expectimax(self, board, depth, turn):
        is_terminal = self.is_terminal_node(board)
        valid_locations = self.get_valid_locations(board)
        my_turn = turn
        if depth == 0 or is_terminal:
            if is_terminal:      
                if self.winning_move(board, self.player_number):           
                    return None, 100000
                elif self.winning_move(board, 1 if self.player_number==2 else 2):
                    return None, -100000
                else:
                    return None, 0 
            else:
                return None, self.evaluation_function(board) 

        if my_turn:
            #print("max turn")
            value = -INF
            column = random.choice(valid_locations)
            for col in valid_locations:
                row = self.get_next_open_row(board, col)
                b_copy = board.copy()
                self.drop_piece(b_copy, row, col, self.player_number)
                new_score = self.expectimax(b_copy, depth-1, False)[1]
                # print("my_turn",board)
                # print("max score",new_score)
                if new_score > value:                
                    value = new_score
                    column = col        
            return column, value 

        else:
            value = 0
            column = random.choice(valid_locations)
            row = self.get_next_open_row(board, column)
            b_copy = board.copy()
            self.drop_piece(b_copy, row, column, 1 if self.player_number==2 else 2)
            for col in valid_locations:           
                value += self.expectimax(b_copy, depth-1, True)[1]
            value /= len(valid_locations)
            return column, value 


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
        return self.expectimax(board, 2, True)[0]




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

        score = 0
        piece = self.player_number
        #score center
        center_array = [int(i) for i in list(board[:,COLUMN_COUNT//2])]
        center_count = center_array.count(piece)
        score += center_count

        #Horizontal
        for r in range(ROW_COUNT):
            row_array = [int(i) for i in list(board[r,:])]
            for c in range(COLUMN_COUNT-3):
                window = row_array[c:c+WINDOW_LENGTH]
                score += self.evaluate_window(window)

        #Vertical
        for c in range(COLUMN_COUNT):
            col_array = [int(i) for i in list(board[:,c])]
            for r in range(ROW_COUNT-3):
                window = col_array[r:r+WINDOW_LENGTH]
                score += self.evaluate_window(window)

        #Positive diagnal
        for r in range(ROW_COUNT-3):
            for c in range(COLUMN_COUNT-3):
                window = [board[r+i][c+i] for i in range(WINDOW_LENGTH)]
                score += self.evaluate_window(window)

        #Negative diagnal
        for r in range(ROW_COUNT-3):
            for c in range(COLUMN_COUNT-3):
                window = [board[r+3-i][c+i] for i in range(WINDOW_LENGTH)]
                score += self.evaluate_window(window)
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

