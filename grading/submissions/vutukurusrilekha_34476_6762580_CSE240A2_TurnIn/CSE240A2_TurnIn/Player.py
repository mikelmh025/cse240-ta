import numpy as np
from random import random
max_depth = 1
class AIPlayer:
    def __init__(self, player_number):
        self.player_number = player_number
        self.type = 'ai'
        self.player_string = 'Player {}:ai'.format(player_number)
    
    def opponent_num(self):
        if self.player_number == 1:
            return 2
        else:
            return 1
    """
    Given the current state of the board, return the scalar value that 
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
    def evaluation_function(self, board):
        
        def check_hori(b): # should return the max num of tokens in a row (0 to 4)
            #print("in check_hori")
            max_vals_in_row = 0
            to_str = lambda a: ''.join(a.astype(str))
            for row in b:
                row_to_string = to_str(row)
                temp_max_vals_in_row = max_vals_in_row + 1
                while(temp_max_vals_in_row<=4):
                    template = '{0}'*(temp_max_vals_in_row)
                    compare = template.format(self.player_number)
                    if compare in row_to_string:
                        max_vals_in_row = temp_max_vals_in_row
                    if max_vals_in_row == 4: # dont need to look through entire board if there is a 4 in a row
                        return max_vals_in_row
                    temp_max_vals_in_row+=1
            return max_vals_in_row

        def check_vert(b):
            return check_hori(b.T)

        def check_diag(b):
            max_vals_in_row = 0
            to_str = lambda a: ''.join(a.astype(str))
            for in_row in range(max_vals_in_row,5):
                template = '{0}'*in_row
                compare = template.format(self.player_number)
                for op in [None, np.fliplr]:
                    op_board = op(b) if op else b
                    root_diag = np.diagonal(op_board, offset=0).astype(np.int)
                    if compare in to_str(root_diag):
                        max_vals_in_row = in_row
                        if max_vals_in_row==4:
                            return 4
                    for i in range(1, b.shape[1]-3):
                        for offset in [i, -i]:
                            diag = np.diagonal(op_board, offset=offset)
                            diag = to_str(diag.astype(np.int))
                            if compare in diag:
                                max_vals_in_row = in_row
                                if max_vals_in_row==4:
                                    return 4
            return max_vals_in_row

        temp_utility = []
        temp_utility.append(check_hori(board) * 25)
        temp_utility.append(check_vert(board) * 25)
        temp_utility.append(check_diag(board) * 25)
        #print(board)
        #print("utilities", temp_utility)
        return max(temp_utility)
    
    def next_free_space(self, b, col): # find the row that has the lowest free space
        for i in range(len(b)-1, -1 , -1):
            if b[i][col]==0:
                return i
        return -1
    
    def alpha_beta_val(self, depth, isCurrPlayer, alpha, beta, b):
        def depth_reached(isMaxPlayer, b):
            #print("in depth reached")
            if isMaxPlayer:
                v = np.NINF
                best_col = 7
                for col in range(0,7): # find the best val
                    tempBoard = b.copy()
                    next_row = self.next_free_space(tempBoard, col)
                    if next_row != -1: # col is not full
                        tempBoard[next_row][col] = self.player_number
                        tempBoardValue = self.evaluation_function(tempBoard)
                        if (tempBoardValue>v):
                            v = tempBoardValue
                            best_col = col
                return v, best_col
            else:
                v = np.inf
                min_col = 7
                for col in range(0,7): # find the best val
                    tempBoard = b.copy()
                    next_row = self.next_free_space(tempBoard, col)
                    if next_row != -1: # col is not full
                        tempBoard[next_row][col] = self.opponent_num()
                        tempBoardValue = self.evaluation_function(tempBoard)
                        if (tempBoardValue<v):
                            v = tempBoardValue
                            min_col = col
                return v, min_col
        #print("depth: ", depth)
        #print("player: ", self.player_string)
        if depth>= max_depth: # max depth reached
            return depth_reached(isCurrPlayer, b)
        if isCurrPlayer: # maximizer player
            best_col = 7
            v = np.NINF
            for next_col in range(0,7): # for each successor of state (curr player's possible moves)
                tempBoard = b.copy()
                next_row = self.next_free_space(tempBoard, next_col)
                if next_row != -1: # col is not full
                    tempBoard[next_row][next_col] = self.player_number
                    tempBoardValue, tempCol = self.alpha_beta_val(depth+1, False, alpha, beta, tempBoard)
                    if tempBoardValue > v:
                        v = tempBoardValue
                        best_col = tempCol
                    alpha = max(alpha, v)
                    if beta<=alpha:
                        break
            return v, best_col
        else: # minimizer player
            v = np.inf
            min_col = 7
            for next_col in range(0,7): # for each successor state (opp player's possible moves)
                tempBoard = b.copy()
                next_row = self.next_free_space(tempBoard, next_col)
                if next_row !=-1:
                    tempBoard[next_row][next_col] = self.opponent_num()
                    tempBoardValue, tempCol = self.alpha_beta_val(depth+1, True, alpha, beta, tempBoard)
                    if tempBoardValue<v:
                        v = tempBoardValue
                        min_col = tempCol
                    if beta<=alpha:
                        break
            return v, min_col

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
    def get_alpha_beta_move(self, board):
        print()
        print()
        print()
        print("in alpha beta for player ", self.player_number)
        print()
        print()
        print()
        b = board.copy()
        #testing utility function
        #b[0][0] = self.player_number
        #b[1][1] = self.player_number
        #b[2][2] = self.player_number
        #b[3][3] = self.player_number
        #print(b)
        #self.evaluation_function(b)
        val, col = self.alpha_beta_val(0, True, np.NINF, np.Inf, board)
        return col
        

    def expectimax_val(self, depth, isCurrPlayer, b):
        def depth_reached(isMaxPlayer, b):
            if isMaxPlayer:
                v = np.NINF
                best_col = 7
                for col in range(0,7): # find the best val
                    tempBoard = b.copy()
                    next_row = self.next_free_space(tempBoard, col)
                    if next_row != -1: # col is not full
                        tempBoard[next_row][col] = self.player_number
                        tempBoardValue = self.evaluation_function(tempBoard)
                        if (tempBoardValue>v):
                            v = tempBoardValue
                            best_col = col
                return v, best_col
            else:
                avg_val = 0
                for next_col in range(0,7): # for each successor state (opp player's possible moves)
                    tempBoard = b.copy()
                    next_row = self.next_free_space(tempBoard, next_col)
                    if next_row !=-1:
                        tempBoard[next_row][next_col] = self.opponent_num()
                        tempBoardValue, tempCol = self.expectimax_val(depth+1, True, tempBoard)
                        avg_val +=tempBoardValue
                avg_val/=7
                col = 7*random()
                return avg_val, col

        if depth>=max_depth:
            return depth_reached(isCurrPlayer, b)
        
        if isCurrPlayer:
            v = np.NINF
            best_col = 7
            for next_col in range(0,7): # find the best val
                tempBoard = b.copy()
                next_row = self.next_free_space(tempBoard, next_col)
                if next_row != -1: # col is not full
                    tempBoard[next_row][next_col] = self.player_number
                    tempBoardValue, tempCol = self.expectimax_val(depth+1, False, tempBoard)
                    if (tempBoardValue>v):
                        v = tempBoardValue
                        best_col = tempCol
            return v, best_col
        else:
            avg_val = 0
            for next_col in range(0,7): # for each successor state (opp player's possible moves)
                tempBoard = b.copy()
                next_row = self.next_free_space(tempBoard, next_col)
                if next_row !=-1:
                    tempBoard[next_row][next_col] = self.opponent_num()
                    tempBoardValue, tempCol = self.expectimax_val(depth+1, True, tempBoard)
                    avg_val +=tempBoardValue
            avg_val/=7
            col = 7*random()
            return avg_val, col

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
        val, col = self.expectimax_val(0, True, board)
        return col


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

