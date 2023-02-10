import numpy as np
import copy
import math
import random

class AIPlayer:
    def __init__(self, player_number):
        self.player_number = player_number
        self.type = 'ai'
        self.player_string = 'Player {}:ai'.format(player_number)
        self.moves = set([])
        self.move = 0

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
        # raise NotImplementedError('Whoops I don\'t know what to do')
        
        self.move, score = self.abpruning(board, -math.inf, math.inf, 4, self.player_number)

        return self.move
    
    def abpruning(self, board, a, b, depth, player):
        if depth == 0 or self.is_terminal(board):
            if self.is_terminal(board):
                if self.check_win(board, self.player_number):
                    # print('win', board)
                    return (None, 100000000000000)
                elif self.check_win(board, 3 - self.player_number):
                    # print('lose', board)
                    return (None, -100000000000000)
                else: #board is filled or no more valid moves or draw
                    return (None, 0)
            else: #depth limit
                # print('depth limit', board)
                return (None, self.evaluation_function(board))
        if player == self.player_number:
            score = -math.inf
            col = 0
            while not self.check_move_valid(col, board) and col < board.shape[1]:
                col += 1
            for i in range(0, board.shape[1]):
                if a > b: #pruning
                        break
                if self.check_move_valid(i, board):
                    mem = copy.deepcopy(board)
                    self.make_move(i, mem, player)
                    p = 3 - player
                    if player == 1: #flip player
                        p = 2
                    else:
                        p = 1
                    # print(p)
                    new_score = self.abpruning(mem, a, b, depth-1, p)[-1]
                    if new_score > score:
                        col = i
                        score = new_score
                    a = max(a, score)
            return (col, score)
        else:
            score = math.inf
            col = 0
            while not self.check_move_valid(col, board) and col < board.shape[1]:
                col += 1
            for i in range(0, board.shape[1]):
                if a > b: #pruning
                    break
                if self.check_move_valid(i, board):
                    mem = copy.deepcopy(board)
                    self.make_move(i, mem, player)
                    if player == 1: #flip player
                        p = 2
                    else:
                        p = 1
                    # print(p)
                    new_score = self.abpruning(mem, a, b, depth-1, p)[-1]
                    if new_score < score:
                        col = i
                        score = new_score
                    b = min(b, score)
            return (col, score)
        
    
    def is_terminal(self, board):
        return self.check_win(board, self.player_number) or self.check_win(board, 3 - self.player_number) or not any([self.check_move_valid(i, board) for i in range(0, 7)])


    def expectimax(self, board, depth, player):
        if depth == 0 or self.is_terminal(board):
            if self.is_terminal(board):
                if self.check_win(board, self.player_number):
                    # print('win', board)
                    return (None, 10000000000000000000)
                elif self.check_win(board, 3 - self.player_number):
                    # print('lose', board)
                    return (None, -10000000000000000000)
                else: #board is filled or no more valid moves or draw
                    return (None, 0)
            else: #depth limit
                # print('depth limit', board)
                return (None, self.evaluation_function(board))
        if player == self.player_number:
            score = -math.inf
            col = 0
            while not self.check_move_valid(col, board) and col < board.shape[1]:
                col += 1
            for i in range(0, board.shape[1]):
                if self.check_move_valid(i, board):
                    mem = copy.deepcopy(board)
                    self.make_move(i, mem, player)
                    if player == 1: #flip player
                        p = 2
                    else:
                        p = 1
                    # print(p)
                    new_score = self.expectimax(mem, depth-1, p)[-1]
                    if new_score > score:
                        col = i
                        score = new_score
            return (col, score)
        else:
            score = 0
            col = 0
            while not self.check_move_valid(col, board) and col < board.shape[1]:
                col += 1
            for i in range(0, board.shape[1]):
                if self.check_move_valid(i, board):
                    mem = copy.deepcopy(board)
                    self.make_move(i, mem, player)
                    if player == 1: #flip player
                        p = 2
                    else:
                        p = 1
                    # print(p)
                    new_score = self.expectimax(mem, depth-1, p)[-1]
                    score += new_score / 7
            return (col, score)
    
    def check_move_valid(self, i, board):
        return board[0][i] == 0 and i < board.shape[1]
    
    def make_move(self, i, board, player):
        pos = 0
        while pos < board.shape[0] and board[pos][i] == 0:
            pos += 1
        pos -= 1
        if pos >= board.shape[0]:
            return
        board[pos][i] = player
        return
    
    
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
        
        # raise NotImplementedError('Whoops I don\'t know what to do')
        
        self.move, score = self.expectimax(board, 4, self.player_number)
                        
        return self.move
    
    def eval_fours(self, arr):
        score = 0
        if arr.count(self.player_number) == 4:
            score += 100
        elif arr.count(self.player_number) == 3 and arr.count(0) == 1:
            score += 8
        elif arr.count(self.player_number) == 2 and arr.count(0) == 2:  
            score += 3
        else:
            score += 0
            
        if arr.count(3 - self.player_number) == 3 and arr.count(0) == 1:
            score -= 40
            
        return score    
        
    def is_terminal(self, board):
        return self.check_win(board, self.player_number) or self.check_win(board, 3 - self.player_number) or not any([self.check_move_valid(i, board) for i in range(0, 7)])
    
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
        
        #forcing to work in centre of the grid
        carr = [int(i) for i in board[:, board.shape[1] // 2]]
        c_count = carr.count(self.player_number)
        score += c_count * 5

        #horizontal score
        for i in range(board.shape[0]):
            for j in range(0, board.shape[1] - 4):
                # print(j ,j + 4)
                # print(board.shape)
                score += self.eval_fours(list(board[i, j : j + 4]))

        #vertical
        for j in range(board.shape[1]):
            for j in range(0, board.shape[0] - 4):
                score += self.eval_fours(list(board[j : j + 4, i]))
                    
        #for diagonals \
        for i in range(0, board.shape[0] - 3):
            for j in range(0, board.shape[1] - 3):
                score += self.eval_fours(list([board[i][j], board[i+1][j+1], board[i+2][j+2], board[i+3][j+3]]))

        for i in range(0, board.shape[0] - 3):
            for j in range(board.shape[1] - 1, 3):
                score += self.eval_fours(list([board[i][j], board[i+1][j-1], board[i+2][j-2], board[i+3][j-3]]))
        
        return score

    def check_win(self, board, player):
        #for horizontal checks
        for i in range(0, board.shape[0]):
            for j in range(0, board.shape[1] - 3):
                if board[i][j] == board[i][j+1] == board[i][j+2] == board[i][j+3] == player:
                    return True
        
        #for diagonals \
        for i in range(0, board.shape[0] - 3):
            for j in range(0, board.shape[1] - 3):
                if board[i][j] == board[i+1][j+1] == board[i+2][j+2] == board[i+3][j+3] == player:
                    return True
                
        #for diagonals /
        for i in range(0, board.shape[0] - 3):
            for j in range(board.shape[1] - 1, 3, -1):
                if board[i][j] == board[i+1][j-1] == board[i+2][j-2] == board[i+3][j-3] == player:
                    return True
    
        #for verticals
        for i in range(0, board.shape[0] - 3):
            for j in range(0, board.shape[1]):
                if board[i][j] == board[i+1][j] == board[i+2][j] == board[i+3][j] == player:
                    return True
                
        return False
        

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

