import numpy as np

# CONSTANTS
MAX_COLUMN = 6
MAX_ROW = 5
MAX_AB_DEPTH = 4
MAX_EXP_DEPTH = 4

class AIPlayer:
    def __init__(self, player_number):
        self.player_number = player_number
        self.type = 'ai'
        self.player_string = 'Player {}:ai'.format(player_number)
    

    # HELPER FUNCTIONS
    
    def get_valid_cols(self, board):
        valid_cols = []
        
        for i, col in enumerate(board.T):
            if 0 in col:
                valid_cols.append(i)
                        
        return valid_cols
            
    
    def get_succesors(self, board, player):

        # list of (column, board) tuples
        succs = []
        
        
        # iterate through columns
        for column in self.get_valid_cols(board):
            curr_column = board.T[column]
            
            board_copy = np.copy(board)
            # find next available row
            row = MAX_ROW
            while row > 0 and curr_column[row] != 0:
                row -= 1

            # set new board as successor
            board_copy[row][column] = player
            succs.append((column, board_copy))
        
        return succs

        
    def max_move_ab(self, board, a, b, player, depth):
        v = np.NINF
        # initialise column to random valid col
        chosen_col = np.random.choice(self.get_valid_cols(board))

        # get successors and set opponent player
        succ = self.get_succesors(board, player)
        opponent = 1 if player == 2 else 2
        
        # loop through successors
        # i is chosen column, succ[i] is move
        # of putting coin in that column
        for col, s in succ:
            # set v = min(v, value(successor)),
            # but also update move if better
            _, new_v = self.get_alpha_beta_helper(s, a, b, opponent, depth + 1)
            if new_v > v:
                chosen_col = col
                v = new_v

            if v >= b:
                return chosen_col, v

            a = max(a, v)
    
        # return move and value
        return chosen_col, v
    
    def min_move_ab(self, board, a, b, player, depth):
        v = np.inf
        chosen_col = np.random.choice(self.get_valid_cols(board))

        
        # get successors and set opponent player
        succ = self.get_succesors(board, player)
        opponent = 1 if player == 2 else 2
        
        # loop through successors
        # i is chosen column, succ[i] is move
        # of putting coin in that column
        for col, s in succ:
            # set v = min(v, value(successor)),
            # but also update move if better
            _, new_v = self.get_alpha_beta_helper(s, a, b, opponent, depth + 1)
            if new_v < v:
                chosen_col = col
                v = new_v

            if v <= a:
                return chosen_col, v

            b = min(b, v)
    
        return chosen_col, v
    
    def max_move(self, board, player, depth):
        v = np.NINF
        chosen_col = np.random.choice(self.get_valid_cols(board))

        # get successors and set opponent player
        succ = self.get_succesors(board, player)
        opponent = 1 if player == 2 else 2
        
        # loop through successors
        # i is chosen column, succ[i] is move
        # of putting coin in that column
        for col, s in succ:
            # set v = min(v, self.value(s, a, b)),
            # but also update move if better
            _, new_v = self.get_expectimax_helper(s, opponent, depth + 1)
            if new_v > v:
                chosen_col = col
                v = new_v
    
        # return move and value
        return chosen_col, v
    
    def exp_move(self, board, player, depth):
        v = 0
        
        # get successors and set opponent player
        succ = self.get_succesors(board, player)
        opponent = 1 if player == 2 else 2
        probability = (1 / len(succ))
        
        # loop through successors
        # i is chosen column, succ[i] is move
        # of putting coin in that column
        for _, s in succ:
            # set v = min(v, self.value(s, a, b)),
            # but also update move if better
            _, next_val = self.get_expectimax_helper(s, opponent, depth + 1)
            v += probability * next_val

        # TODO: improve design, maybe only return value in expectimax?
        return None, v
    
    def get_alpha_beta_helper(self, board, a, b, player, depth):

        # return evaluation value
        # no move to be returned, just value
        if depth == MAX_AB_DEPTH or self.is_terminal(board):
            return None, self.evaluation_function(board)
        # MAXIMISING
        elif player == self.player_number:
            return self.max_move_ab(board, a, b, player, depth)
        # MINIMISING
        else:
            return self.min_move_ab(board, a, b, player, depth);
    
    def get_expectimax_helper(self, board, player, depth):
        
        # return evaluation value
        # no move to be returned, just value
        if depth == MAX_EXP_DEPTH or self.is_terminal(board):  
            return None, self.evaluation_function(board)
        # MAXIMISING
        elif player == self.player_number:
            return self.max_move(board, player, depth)
        # EXPECTED
        else:
            return self.exp_move(board, player, depth)

    def is_terminal(self, board):
        # terminal if board is full or someone has won
        opponent = 2 if self.player_number == 1 else 2
        return (
            (0 not in board) or
            (self.n_in_a_row(self.player_number, board, 4)) > 0 or
            (self.n_in_a_row(opponent, board, 4)) > 0
        )

    # returns number of occurrences of n
    # pieces for given player in a row
    def n_in_a_row(self, player, board, n):
        player_win_str = str(player) * n
        to_str = lambda a: ''.join(a.astype(str))
    
        def check_horizontal(b):
            total = 0
            for row in b:
                if player_win_str in to_str(row):
                    total += 1
            return total

        def check_verticle(b):
            return check_horizontal(b.T)

        def check_diagonal(b):
            total = 0
            for op in [None, np.fliplr]:
                op_board = op(b) if op else b
                
                root_diag = np.diagonal(op_board, offset=0).astype(np.int)
                if player_win_str in to_str(root_diag):
                    total += 1

                for i in range(1, b.shape[1]-3):
                    for offset in [i, -i]:
                        diag = np.diagonal(op_board, offset=offset)
                        diag = to_str(diag.astype(np.int))
                        if player_win_str in diag:
                            total += 1

            return total

        return (check_horizontal(board) +
                check_verticle(board) +
                check_diagonal(board))

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
        # call helper function with initial a and b, self playing,
        # and 0 as current depth, returns tuple of (column, value)
        # return chosen column as next move
        return self.get_alpha_beta_helper(
            board,
            np.NINF,
            np.inf,
            self.player_number,
            0
        )[0]

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
        return self.get_expectimax_helper(
            board,
            self.player_number,
            0
        )[0]


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
                
        # if board is full, draw is reached - no reward
        if 0 not in board:
            return 0
        
        player = self.player_number
        opponent = 1 if self.player_number == 2 else 2
        
        # if winning for current player, high reward
        if self.n_in_a_row(player, board, 4) > 0:
            return np.inf
        
        # if winning for opponent, high punishment
        if self.n_in_a_row(opponent, board, 4) > 0:
            return np.NINF
        
        value = 0
        
        # if 3 in row for current player, medium reward
        # 2 in a row is small reward, and 1 is tiny reward
        value += (
            (self.n_in_a_row(player, board, 3) * 3) +
            (self.n_in_a_row(player, board, 2) * 2) +
            self.n_in_a_row(player, board, 1)
        )
        
        # same values but negative for opponent
        value -= (
            (self.n_in_a_row(opponent, board, 3) * 4) +
            (self.n_in_a_row(opponent, board, 2) * 3) +
            self.n_in_a_row(opponent, board, 1)
        )
                
        return value


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

