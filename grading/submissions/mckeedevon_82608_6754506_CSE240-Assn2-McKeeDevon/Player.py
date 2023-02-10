import numpy as np
import tkinter as tk
import tkinter.simpledialog as sd
import random as rd

from numpy.core.overrides import verify_matching_signatures

# --- Helpers ---

def get_move_board(board, move, player_number):
    bc = np.copy(board)
    for i in range(len(bc) - 1, -1, -1):
        if bc[i][move] == 0:
            bc[i][move] = player_number
            return bc
    return None

def get_moves(board, player_number):
    return list(filter(lambda i: i is not None, [get_move_board(board, m, player_number) for m in range(len(board[0]))]))

def get_moves_index(board, player_number):
    return list(filter(lambda i: i[1] is not None, [(m, get_move_board(board, m, player_number)) for m in range(len(board[0]))]))

# --- ------- ---

class AIPlayer:
    def __init__(self, player_number):
        self.player_number = player_number
        self.type = 'ai'
        self.player_string = 'Player {}:ai'.format(player_number)
        # Max depth for alpha-beta and expectimax traversal before nodes are evaluated
        # as terminals
        self.MAX_DEPTH = 3
        # Weight for how negatively other player progress should be considered,
        # higher values of DEFENSIVENESS cause heuristic outcomes where other player 
        # makes progress much worse. Base value is 1.0, but AI tends to play very passively
        # with it at lower values.
        self.DEFENSIVENESS = 4.0

    def ab_visit(self, m_type, board, depth=0, alpha=float('-inf'), beta=float('inf')):
        if m_type == 'MAX':
            moves = get_moves(board, self.player_number)
            v = float('-inf')
            for m in moves:
                m_val = self.ab_visit('MIN', m, depth + 1, alpha, beta) if depth < self.MAX_DEPTH else self.evaluation_function(m)
                v = max(v, m_val)
                if v >= beta:
                    return v
                alpha = max(alpha, v)
            return v
        else:
            moves = get_moves(board, 1 if self.player_number == 2 else 2)
            v = float('inf')
            for m in moves:
                m_val = self.ab_visit('MAX', m, depth + 1, alpha, beta) if depth < self.MAX_DEPTH else self.evaluation_function(m)
                v = min(v, m_val)
                if v <= alpha:
                    return v
                beta = min(beta, v)
            return v

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
        valid_moves = get_moves_index(board, self.player_number) ###
        max_m_val = float('-inf')
        max_index = -1
        for i, m in valid_moves:
            m_val = self.ab_visit('MIN', m)
            if m_val > max_m_val:
                max_m_val = m_val
                max_index = i
        return max_index

    def em_visit(self, m_type, board, depth=0):
        if m_type == 'MAX':
            moves = get_moves(board, self.player_number)
            v = float('-inf')
            for m in moves:
                m_val = self.em_visit('EXP', m, depth + 1) if depth < self.MAX_DEPTH else self.evaluation_function(m)
                v = max(v, m_val)
            return v
        else:
            moves = get_moves(board, 1 if self.player_number == 2 else 2)
            p_random = 1 / len(moves)
            v = 0
            for m in moves:
                m_val = self.em_visit('MAX', m, depth + 1) if depth < self.MAX_DEPTH else self.evaluation_function(m)
                v += p_random * m_val
            return v

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
        
        valid_moves = get_moves_index(board, self.player_number)
        max_m_val = float('-inf')
        max_index = -1
        for i, m in valid_moves:
            m_val = self.em_visit('EXP', m)
            if m_val > max_m_val:
                max_m_val = m_val
                max_index = i
        return max_index

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
        h = len(board)
        w = len(board[0])
        other_player = 1 if self.player_number == 2 else 2

        # Calculating horizontals
        horiz_val = 0
        for i in range(h):
            last = -1
            last_ct = 0
            for j in range(w):
                if board[i][j] == last:
                    last_ct += 1
                else:
                    if last_ct > 0:
                        if last == self.player_number:
                            horiz_val += pow(last_ct, 2)
                        elif last == other_player:
                            horiz_val -= self.DEFENSIVENESS * pow(last_ct, 2)
                    last = board[i][j]
                    last_ct = 1
            if last_ct > 0:
                if last == self.player_number:
                    horiz_val += pow(last_ct, 2)
                elif last == other_player:
                    horiz_val -= self.DEFENSIVENESS * pow(last_ct, 2)

        # Calculating verticals
        vert_val = 0
        for j in range(w):
            last = -1
            last_ct = 0
            for i in range(h):
                if board[i][j] == last:
                    last_ct += 1
                else:
                    if last_ct > 0:
                        if last == self.player_number:
                            vert_val += pow(last_ct, 2)
                        elif last == other_player:
                            vert_val -= self.DEFENSIVENESS * pow(last_ct, 2)
                    last = board[i][j]
                    last_ct = 1
            if last_ct > 0:
                if last == self.player_number:
                    vert_val += pow(last_ct, 2)
                elif last == other_player:
                    vert_val -= self.DEFENSIVENESS * pow(last_ct, 2)

        # Calculating diagonals
        diag_val = 0
        for k in range(w * 2):
            last = -1
            last_ct = 0
            for j in range(k):
                i = k - j
                if i < h and j < w:
                    if board[i][j] == last:
                        last_ct += 1
                    else:
                        if last_ct > 0:
                            if last == self.player_number:
                                diag_val += pow(last_ct, 2)
                            elif last == other_player:
                                diag_val -= self.DEFENSIVENESS * pow(last_ct, 2)
                        last = board[i][j]
                        last_ct = 1
            if last_ct > 0:
                if last == self.player_number:
                    diag_val += pow(last_ct, 2)
                elif last == other_player:
                    diag_val -= self.DEFENSIVENESS * pow(last_ct, 2)
        # Rotating board to calculate reverse diagonals cause I'm lazy
        rot_board = np.rot90(board)
        rot_h = len(rot_board)
        rot_w = len(rot_board[0])
        for k in range(rot_w * 2):
            last = -1
            last_ct = 0
            for j in range(k):
                i = k - j
                if i < rot_h and j < rot_w:
                    if rot_board[i][j] == last:
                        last_ct += 1
                    else:
                        if last_ct > 0:
                            if last == self.player_number:
                                diag_val += pow(last_ct, 2)
                            elif last == other_player:
                                diag_val -= self.DEFENSIVENESS * pow(last_ct, 2)
                        last = rot_board[i][j]
                        last_ct = 1
            if last_ct > 0:
                if last == self.player_number:
                    diag_val += pow(last_ct, 2)
                elif last == other_player:
                    diag_val -= self.DEFENSIVENESS * pow(last_ct, 2)

        return horiz_val + vert_val + diag_val


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

        #move = int(input('Enter your move: '))
        move = sd.askinteger("Next Move", "Enter your move")

        while move not in valid_cols:
            print('Column full, choose from:{}'.format(valid_cols))
            #move = int(input('Enter your move: '))
            move = sd.askinteger("Next Move", "Enter your move")

        return move

