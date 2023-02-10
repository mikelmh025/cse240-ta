#import pdb; pdb.set_trace()
import numpy as np

ply = 0

class AIPlayer:
    def __init__(self, player_number):
        self.player_number = player_number
        self.type = 'ai'
        self.player_string = 'Player {}:ai'.format(player_number)

    def get_valid_cols (self, board) : 
        valid_cols = []
        for col in range(board.shape[1]):
            if 0 in board[:,col]:
                valid_cols.append(col)
        return valid_cols
    
    def get_row_for_col (self, board, col) :
        row = 0
        while row < 6 :
            if board[row, col] == 0 :
                row+=1
            else :
                break
        row-=1
        return row

    def get_max (self, board, depth, alpha, beta) :
        v = -100000
        best_col = 0
        depth = depth + 1
        valid_cols = self.get_valid_cols(board)

        if depth == 5 :
            for eval_col in valid_cols :
                new_board = board.copy()
                row = self.get_row_for_col(new_board, eval_col)
                new_board[row, eval_col] = self.player_number
                eval_v = self.evaluation_function (new_board)
                if eval_v > v :
                    v = eval_v
                    best_col = eval_col
            return v, best_col

        for eval_col in valid_cols :
            new_board = board.copy()
            row = self.get_row_for_col(new_board, eval_col)
            new_board[row, eval_col] = self.player_number
            eval_v = self.evaluation_function (new_board)
            if eval_v > 20 :
                return eval_v, eval_col
            min_v, min_v_col = self.get_min (new_board, depth, alpha, beta)
            if min_v > v :
                v = min_v
                best_col = eval_col
            if v >= beta :
                return v, best_col
            if v > alpha :
                alpha = v
        return v, best_col

    def get_min (self, board, depth, alpha, beta) :
        v = 100000
        best_col = 0
        depth = depth + 1
        valid_cols = self.get_valid_cols(board)

        if depth == 5 :
            for eval_col in valid_cols :
                new_board = board.copy()
                row = self.get_row_for_col(new_board, eval_col)
                new_board[row, eval_col] = self.player_number
                eval_v = self.evaluation_function (new_board)
                if eval_v > v :
                    v = eval_v
                    best_col = eval_col
            return v, best_col

        for eval_col in valid_cols :
            new_board = board.copy()
            row = self.get_row_for_col(new_board, eval_col)
            if self.player_number == 1 :
                new_board[row, eval_col] = 2
            else :
                new_board[row, eval_col] = 1
            eval_v = self.evaluation_function (new_board)
            if eval_v > 20 :
                return eval_v, eval_col
            max_v, max_v_col = self.get_max (new_board, depth, alpha, beta)
            if max_v < v :
                v = max_v
                best_col = eval_col
            if v <= alpha :
                return v, best_col
            if v < beta :
                beta = v
        return v, best_col

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



        #get valid cols
        '''valid_cols = []
        for col in range(board.shape[1]):
            if 0 in board[:,col]:
                valid_cols.append(col)'''

        '''if self.player_number == 1 :
            best_move_val = -6
        else :
            best_move_val = 6'''
        
        '''global ply
        if ply < 5 :
            ply += 1
            valid_cols = self.get_valid_cols(board)
            return np.random.choice(valid_cols)'''

        alpha = -100000
        beta = 100000
        best_col = 0
        depth = 0
        #breakpoint();
        '''import time, sys
        start_time = time.time()'''
        v, v_col = self.get_max (board, depth, alpha, beta)
        #print(time.time() - start_time, "seconds", flush=True)
        #sys.stdout.flush()
        if v > alpha :
            alpha = v
            best_col = v_col
            '''
            row = 0
            while row < 6 :
                #breakpoint();
                if board[row, eval_col] == 0 :
                    row+=1
                else :
                    break
            row-=1
            new_board[row, eval_col] = self.player_number
            move_val = self.evaluation_function(new_board)
            if self.player_number == 1 :
                if move_val > best_move_val :
                    best_move_val = move_val
                    best_col = eval_col
            else :
                if move_val < best_move_val :
                    best_move_val = move_val
                    best_col = eval_col'''

        return best_col

    def get_expecti_max (self, board, depth, alpha, beta) :
        v = 0
        run_v = 0
        best_col = 0
        depth = depth + 1
        valid_cols = self.get_valid_cols(board)

        if depth == 5 :
            for eval_col in valid_cols :
                new_board = board.copy()
                row = self.get_row_for_col(new_board, eval_col)
                new_board[row, eval_col] = self.player_number
                eval_v = self.evaluation_function (new_board)
                if eval_v > v :
                    v = eval_v
                    best_col = eval_col
            return v, best_col

        num_valid_cols = len(valid_cols)
        p = 1 / num_valid_cols
        for eval_col in valid_cols :
            new_board = board.copy()
            row = self.get_row_for_col(new_board, eval_col)
            new_board[row, eval_col] = self.player_number
            min_v, min_v_col = self.get_min (new_board, depth, alpha, beta)
            run_v = run_v + (p * min_v)
            if run_v > v :
                v = run_v
                best_col = eval_col
            if v >= beta :
                return v, best_col
            if v > alpha :
                alpha = v
        return v, best_col

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
        alpha = -100000
        beta = 100000
        best_col = 0
        depth = 0
        #breakpoint();
        
        v, v_col = self.get_expecti_max (board, depth, alpha, beta)
        #if v > alpha :
        #    alpha = v
        best_col = v_col
        return best_col




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
        Heuristic - always considering it is my move next -
        Get max continuous for player and opponent - max_p and max_o
        If max_p == 4 ->  return 5
        else if max_o == 4 -> return -5
        else if max_p == 3 -> return 4
        else if max_o == 3 -> return -4
        else return max_p - max_o
        
        valid_cols = []
        for i, col in enumerate(board.T):
            if 0 in col:
                valid_cols.append(i)
        
        valid_cols = []
        for col in range(board.shape[1]):
            if 0 in board[:,col]:
                valid_cols.append(col)        
                
        """
        #find max_p and max_o
        max_p = 0
        max_o = 0
       
        valid_cols = self.get_valid_cols(board)

        temp_p = 0
        temp_o = 0

        for col in valid_cols :
            row = self.get_row_for_col(board, col)
            if row != 5:
                row = row + 1
            #check horizontal
            if board[row,col] == 1 :
                temp_p+=10
                if temp_o > max_o :
                    max_o = temp_o
                    temp_o = 0
            elif board[row,col] == 2 :
                temp_o+=10
                if temp_p > max_p :
                    max_p = temp_p
                    temp_p = 0
            else :
                if temp_o > max_o :
                    max_o = temp_o
                    temp_o = 0       			
                if temp_p > max_p :
                    max_p = temp_p
                    temp_p = 0
                    
            if temp_p > max_p :
                max_p = temp_p
            temp_p = 0
            if temp_o > max_o :
                max_o = temp_o
            temp_o = 0  		
       			
        #check vertical
        for col in valid_cols :
            row = self.get_row_for_col(board, col)
            if row != 5:
                row = row + 1
            for eval_row in range (row, min(row + 3, 5)) :
                if board[eval_row,col] == 1 :
                    temp_p+=10
                    if temp_o > max_o :
                        max_o = temp_o
                    temp_o = 0
                elif board[eval_row,col] == 2:
                    temp_o+=10
                    if temp_p > max_p :
                        max_p = temp_p
                    temp_p = 0
                else :
                    if temp_o > max_o :
                        max_o = temp_o
                    temp_o = 0       			
                    if temp_p > max_p :
                        max_p = temp_p
                    temp_p = 0
                    
            if temp_p > max_p :
                max_p = temp_p
            temp_p = 0
            if temp_o > max_o :
                max_o = temp_o
            temp_o = 0

        #check diagonal
        row = 0
        col = 0
        temp_p =0
        temp_o = 0
        for row in range (board.shape[0]) :
            for col in range (board.shape[1]) :
                if row < 5 and col < 6 and board[row][col] == 1 and board[row+1][col+1] == 1:
                    temp_p += 20
                    if row < 4 and col < 5 and board[row+2][col+2] == 1:
                        temp_p += 10   
                        if row < 3 and col < 4 and board[row+3][col+3] == 1:
                            temp_p += 10  
                        else :
                            if temp_p > max_p :
                                max_p = temp_p
                    else :
                        if temp_p > max_p :
                            max_p = temp_p

                if row > 0 and col < 6 and board[row][col] == 1 and board[row-1][col+1] == 1:
                    temp_p += 20
                    if row > 1 and col < 5 and board[row-2][col+2] == 1:
                        temp_p += 10   
                        if row > 2 and col < 4 and board[row-3][col+3] == 1:
                            temp_p += 10  
                        else :
                            if temp_p > max_p :
                                max_p = temp_p
                    else :
                        if temp_p > max_p :
                            max_p = temp_p

                if row < 5 and col < 6 and board[row][col] == 2 and board[row+1][col+1] == 2:
                    temp_o += 20
                    if row < 4 and col < 5 and board[row+2][col+2] == 2:
                        temp_o += 10   
                        if row < 3 and col < 4 and board[row+3][col+3] == 2:
                            temp_o += 10  
                        else :
                            if temp_o > max_o :
                                max_o = temp_o
                    else :
                        if temp_o > max_o :
                            max_o = temp_o

                if row > 0 and col < 6 and board[row][col] == 2 and board[row-1][col+1] == 2:
                    temp_o += 20
                    if row > 1 and col < 5 and board[row-2][col+2] == 2:
                        temp_o += 10   
                        if row > 2 and col < 4 and board[row-3][col+3] == 2:
                            temp_o += 10  
                        else :
                            if temp_o > max_o :
                                max_o = temp_o
                    else :
                        if temp_o > max_o :
                            max_o = temp_o
                    
            if temp_p > max_p :
                max_p = temp_p
            temp_p = 0
            if temp_o > max_o :
                max_o = temp_o
            temp_o = 0

        # invert based on turn
        # above this max_p is player 0 
        #if Game.current_turn == 1 :
        if self.player_number == 2 : 
            max_p, max_o = max_o, max_p
            '''temp = max_p
       	    max_p = max_o
       	    max_o = temp'''
        # below this max_p is the player whose turn is next
       
       # apply heuristic
        if max_p == 40 :
            return 50
        elif max_o == 40 :
            return -45
        elif max_o == 30 :
            return 40
        elif max_p == 30 :
            return -30
        else :
            return max_p - max_o


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
