import numpy as np
import random
import math

# CONSTANT 
DEPTH = 10

class AIPlayer:
    def __init__(self, player_number):
        self.player_number = player_number
        self.type = 'ai'
        self.player_string = 'Player {}:ai'.format(player_number)
        self.max_score = -10
        self.max_idx = -1
        self.min_score = -300
        self.min_idx = -1

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

        print("IN evaluation function")
        score = self.scoring(board)
        
        return score

    # checks if the given player is at win state
    # will severely increse their score so that they can win
    def terminal_state(self, board, num):

        print("In terminal states")

        row_count = board.shape[0]
        col_count = board.shape[1]
        
        # first checking for 4 in a row horizontally
        for c in range(col_count - 3):
            for r in range(row_count):
                if board[r][c] == num and board[r][c+1] == num and board[r][c + 2] == num and board[r][c + 3] == num:
                    return True
        
        # checking for 4 in a row vertically through each row
        for c in range(col_count):
            for r in range(row_count - 3):
                if board[r][c] == num and board[r+1][c] == num and board[r+2][c] == num and board[r+3][c] == num:
                    return True
        
        # checking for 4 in a row diagonlly downwards 
        for c in range(col_count - 3):
            for r in range(row_count - 3):
                if board[r][c] == num and board[r+1][c+1] == num and board[r+2][c + 2] == num and board[r+3][c + 3] == num:
                    return True

        # checking for 4 in a row diagonally upwards 
        for c in range(col_count - 3):
            for r in range(3, row_count):
                if board[r][c] == num and board[r-1][c+1] == num and board[r-2][c + 2] == num and board[r-3][c + 3] == num:
                    return True
        
        return False

    def valid_moves(self,board):

        print("In valid moves")
        row_count = board.shape[0]
        col_count = board.shape[1]
        succesor_states = []

        for col in range(col_count):
            if board[row_count - 1][col]==0:
                succesor_states.append(col)
        
        return succesor_states
    
    def valid_cols(self, board):
        succesor_states = []

        for col in range(len(board[0])-1,0,-1):
            row = 5
            while board[row][col] != 0 and row>0:
                 row = row - 1
            if board[row][col]==0:
                succesor_states.append((row, col))
        
        return succesor_states

    # scoring based on looking at scoring scopes/windows of size 4 within each
    # row and column of the board
    def scoring(self, board):

        row_count = board.shape[0]
        col_count = board.shape[1]

        score = 0
       
        # extracting the center column to score (since odd number of columns, use seperate
        # loops to check the right and lewft side columns ); middle column (column 4)
        center_arr = [int(i) for i in list(board[:, col_count // 2])]
        center_count = center_arr.count(self.player_number)

        # score this manually by just scoring based on how many player-nums were found in the col in a row
        # and multiplying by some factor
        score += center_count * 10

        # scoring horizontal windows of 4 
        for r in range(row_count):

             # look at all the columns in the row 
            row_arr = [int(i) for i in list(board[r, :])]

            for c in range(col_count - 3):
                #looking at 4 columns in a row ; iterating through the cols in row and
                # scorind each window
                board_scope = row_arr[c:c + 4]
                # give the the window a score baseed on how many of players pieacs in a row in this function
                score += self.scope_evaluation(board_scope, self.player_number)
        
        # scoring verticle windows of 4
        for c in range(col_count):

            # this time we create  verticle windows to look at 
            col_arr = [int(i) for i in list(board[:, c])]

            for r in range(row_count - 3):
                # section of verticle scopes/windows of 4 to evaluate
                board_scope = col_arr[r:r + 4]
                score += self.scope_evaluation(board_scope, self.player_number)

        # scoring diagonal downward windows of 4
        for r in range(row_count - 3):

            for c in range(col_count - 3):

                # sectioning off diagonal windows of 4 
                board_scope = [board[r + i][c + i] for i in range(4)]
                score += self.scope_evaluation(board_scope, self.player_number)

        # scoring diagonal upwards windows of 4
        for r in range(row_count - 3):

            for c in range(col_count - 3):

                #sectioning off diagonal upwards windows of 4
                board_scope = [board[r + 3 - i][c + i] for i in range(4)]
                score += self.scope_evaluation(board_scope, self.player_number)
        
        return score

    def scope_evaluation(self, board_scope, player_num):

        score = 0
        
        # figure out which player we are scoring and how it the opposition 
        if player_num == 1:
            turn = 1 
            opp = 2
        else:
            turn = 2
            opp = 1

        # 4 in a row is the best score 
        if board_scope.count(player_num) == 4:
            score += 100
        
        # found 3 in a row in window and last spot is still open
        elif board_scope.count(player_num) == 3 and board_scope.count(0) == 1:
            score += 50

        # found 2 in a row in wondow and 2 spots in window are open 
        elif board_scope.count(player_num) == 2 and board_scope.count(0) == 2:
            score += 20
        
        # opposer has 3 in a row in a window and there is one empty spot in the window
        if board_scope.count(opp) == 3 and board_scope.count(0) == 1:
            score -= 100
        
        return score
    
    def next_row(self, board, col):

        row_count = board.shape[0]
        col_count = board.shape[1]

        # check if there are empty spots in a row to return a row
        # that we can drop a pieace in
        for r in range(row_count):

            if board[r][col] == 0:
                return r
    
    def is_terminal(self, board):

        # check for wins and return if we have any wins or if there are any more 
        # moves that we can make (is the board filled up?)
        player1_win = self.terminal_state(board, 1)
        player2_win = self.terminal_state(board, 2)
        return player1_win or player2_win or len(self.valid_moves(board)) == 0
            
    def minimax(self, board, depth, alpha, beta, maxPlayer):
        print("This is player: ", self.player_number)

        # self.player_number == 1 (Maximizer)
        # self.player_number == 2 (Minimizer)

       # get all valid moves
       # used to be valid_moves
        succesor_states = self.valid_cols(board)
        print("Successor_states: ", succesor_states)

        is_terminal = self.is_terminal(board)
        print("depth: ", depth)

        # terminal state checks
    
        if depth == 0 or is_terminal:

            # one of the players has won or board is filled up
            if is_terminal:
                
                # if player 2 won
                if self.terminal_state(board, 2):
                    return (None, 99999999)
                
                # if player 1 won
                elif self.terminal_state(board, 1):
                    return (None, -99999999)
                
                # board filled up
                else:
                    return (None,0)
            else:
                # reached max bepth of minimax tree
                return None, self.evaluation_function(board)
        
        # Maximizing Player 
        if self.player_number == 1:

            value = -10000
            s = random.choice(succesor_states)
            print("s: ", s)

            #chosen_column = random.choice(succesor_states)
            chosen_column = s[1] # only want the column

            for state in succesor_states:

                #which row to look at
                row = self.next_row(board, state[1])
                board_copy = board.copy()

                # get the new board state with most recent pieaces filled in 
                new_board = self.board_state(board, state, self.player_number)

                # recur down the tree to get all scoeres
                new_score = self.minimax(new_board, depth-1, alpha, beta, False)[1]

                # if we find a higher score, update value to higher score
                if new_score > value:
                    value = new_score
                    chosen_column = state[1]
                
                # set alpha at this level to the highest value found
                alpha = max(alpha, value)

                # prune branch of scores if alpha already greater than beta
                if alpha >= beta:
                    break
            
            print("Chose column:", chosen_column)
            return chosen_column, value
        
        # Minimizing player
        else:
            value = 10000
            s = random.choice(succesor_states)
            print("s: ", s)

            #chosen_column = random.choice(succesor_states)
            chosen_column = s[1]

            for state in succesor_states:

                # which row to look at
                row = self.next_row(board, state[1])
                board_copy = board.copy()

                # get the new baord state with the most recent pieaces filled in 
                new_board = self.board_state(board, state, self.player_number)

                # recur down the tree to get all scoeres
                new_score = self.minimax(new_board, depth-1, alpha, beta, True)[1]

                # if we find a lower score, update value to lower score
                if new_score < value:
                    value = new_score
                    chosen_column = state[1] # only want to column
                
                # set beta at this level to the lowest value found on path
                beta = min(beta, value)

                # prune branch of scores if beta already less than alpha
                if alpha >= beta:
                    break
            
            return chosen_column, value


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

        print("This is player: ", self.player_number)

        # self.player_number == 1 (Maximizer)
        # self.player_number == 2 (Minimizer)

        infinity = float('inf')
        best_move = None
        
        num_nonzeros = np.count_nonzero(board)
        #if num_nonzeros == 0:
        depth = 4
        #depth = 0
        alpha = -infinity
        beta = infinity
        if self.player_number == 1:
            maxPlayer = True
        else:
            maxPlayer = False
        #maxPlayer = True

        print("MaxPLayer: ", maxPlayer)
        move = self.minimax(board, depth, alpha, beta, maxPlayer)
        
        
        print("Move: ", move)
        # returned as a tuple of (value, move)
        return move[0]
    
    def board_state(self, board, move, player_num):
        new_board = np.zeros([6,7]).astype(np.uint8)

        # update borad state based on where player pieaces are located
        for row in range(len(board)):

            # if row does not exist, copy it over
            if row != move[0]:
                
                #copying over row from board into new_board
                new_board[row] = board[row]
            
            # row exists
            else:

                # adding in a new row 
                new_row = []

                #append rows if they don't exist
                for col in range (len(board[0])):

                    # if column does not exsist, copy it over
                    if col != move[1]:
                        new_row.append(board[row][col])
                    
                    # otherwsie, we copy in the players peiace into the row
                    else:
                        new_row.append(player_num)
                
                # add in the new_row we created into the new board
                new_board[row] = new_row
        
        return new_board
    
    # function to get the chance node probabilities
    def probability(self, board, mv, moves):

        p =  int(1/len(moves)) 
        return p
    
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
        infinity = float('inf')
        
        depth = 10
        #depth = 0
        alpha = -infinity
        beta = 0

        col, expectimx_score = self.expectimax(board, depth, alpha, beta, True)
        return col
       
        #raise NotImplementedError('Whoops I don\'t know what to do')

    def expectimax(self, board, depth, alpha, beta, isMax):

        succesor_states = self.valid_cols(board)
        print("Successor_states: ", succesor_states)

        infinity = float('inf')

        is_terminal = self.is_terminal(board)
        print("depth: ", depth)

        # terminal state check first 
        # are we at the max depth of the search tree or has someone already won or 
        # is the board filled up
        if depth == 0 or is_terminal:

            # if someone has won or the board is all filled up
            if is_terminal:

                # if player 1 has won
                if self.terminal_state(board, 1):
                    return (None, 9999999)

                # if player 2 has won
                elif self.terminal_state(board, 2):
                    return (None, -9999999)
                
                # if the board is filled up
                else:
                    return (None,0)
            
            # max depth of the tree has been reached
            else:
                return None, self.evaluation_function(board)
        
        # Maximizing players turn 
        if self.player_number == 1:

            value = -infinity

            s = random.choice(succesor_states)
            chosen_column = s[1]

            # iterate through successor states to score and evaluate 
            # which moves/states are better than others
            for state in succesor_states:

                # which row to look at
                row = self.next_row(board, state[1])
                board_copy = board.copy()

                # get the new updated board state to evaluate potential moves on
                new_board = self.board_state(board, state, self.player_number)

                # score the moves
                new_score = self.expectimax(new_board, depth-1, alpha, beta, False)[1]

                # if the score found is better than current best value, then reset the value to higher score
                if new_score > value:
                    value = new_score
                    chosen_column = state[1]
                
                # set alpha to highest value found on path to root
                alpha = max(alpha, value)

                # prune potential move branches if the alpha found is already better than beta
                if alpha >= beta:
                    break

            print("Chose column:", chosen_column)
            return chosen_column, value
        
        # miminimizing player
        else:

            value = 0
            s = random.choice(succesor_states)
            chosen_column = s[1]

            # iterate through successor states to score and evaluate 
            # which moves/states are better than others
            for state in succesor_states:

                 # which row to look at
                row = self.next_row(board, state[1])
                board_copy = board.copy()

                # get the new updated board state to evaluate potential moves on
                new_board = self.board_state(board, state, self.player_number)

                # score the moves
                new_score = self.expectimax(new_board, depth-1, alpha, beta, True)[1]

                # if the score found is less than current best value, then reset the value to the lower score
                if new_score < value:
                    value = new_score
                    chosen_column = state[1]

                # set beta to the chance node probability 
                beta = math.floor(value/len(succesor_states))

                # prune potential move branches if the beta found is already less than the alpha found
                if alpha >= beta:
                    break

            return chosen_column, value




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

