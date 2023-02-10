import numpy as np

DEPTH_LIMIT = 4

class AIPlayer:
    def __init__(self, player_number):
        self.player_number = player_number
        self.type = 'ai'
        self.player_string = 'Player {}:ai'.format(player_number)
        self.time_total_nodes = 0 # Added for timing purposes

    # ADDED Function to obtain valid moves
    def get_valid_cols(self, board):
        valid_cols = []
        for col in range(board.shape[1]):
            if 0 in board[:,col]:
                valid_cols.append(col)
        return valid_cols    
    
    # ADDED Function to update board with moves
    def add_move_to_board(self, board, move, player_num):
        update_row = -1
        for row in range(1, board.shape[0]):
            update_row = -1
            if board[row, move] > 0 and board[row-1, move] == 0:
                update_row = row-1
            elif row==board.shape[0]-1 and board[row, move] == 0:
                update_row = row

            if update_row >= 0:
                board[update_row, move] = player_num
                break
    
    # ADDED Function to determine if a node is terminal
    def game_completed(self, player_num, board):
            player_win_str = '{0}{0}{0}{0}'.format(player_num)
            to_str = lambda a: ''.join(a.astype(str))

            def check_horizontal(b):
                for row in b:
                    if player_win_str in to_str(row):
                        return True
                return False

            def check_verticle(b):
                return check_horizontal(b.T)

            def check_diagonal(b):
                for op in [None, np.fliplr]:
                    op_board = op(b) if op else b
                    
                    root_diag = np.diagonal(op_board, offset=0).astype(np.int)
                    if player_win_str in to_str(root_diag):
                        return True

                    for i in range(1, b.shape[1]-3):
                        for offset in [i, -i]:
                            diag = np.diagonal(op_board, offset=offset)
                            diag = to_str(diag.astype(np.int))
                            if player_win_str in diag:
                                return True
                return False

            return (check_horizontal(board) or
                    check_verticle(board) or
                    check_diagonal(board))
        

    def get_alpha_beta_move(self, board):
        """
        Given the current state of the board, return the next move based on
        the alpha-beta pruning algorithm

        This will play against either itself or a human player

        INPUTS:
        board - a numpy array containing the state of the board using thec
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

        # CONSTANTS
        WINNING_SCORE = 999999
        LOSING_SCORE = -999999
        
        depth = DEPTH_LIMIT
        player_number = self.player_number
        enemy_number = (player_number % 2) + 1
        valid_moves = self.get_valid_cols(board)
        best_move = np.random.choice(valid_moves)
        self.time_total_nodes = 0

        def is_terminal_state(board):
            return len(valid_moves) == 0 or self.game_completed(player_number, board) or self.game_completed(enemy_number, board) 


        # Alpha-Beta implementation
        def hminimax (board, depth, alpha, beta, isMaximizing):
            # Case 0: Terminal state or 0 depth
            self.time_total_nodes += 1
            #Added to determine how many nodes were explored #
            print("Total nodes explored: {0}".format(self.time_total_nodes))
            is_terminal = is_terminal_state(board)
            if is_terminal or depth == 0:
                if is_terminal:
                    if self.game_completed(player_number, board):
                        return (None, WINNING_SCORE)
                    elif self.game_completed(enemy_number, board):
                        return (None, LOSING_SCORE)
                    else:
                         return (None, 0) # out of moves
                else:
                    return (None, self.evaluation_function(board))
            
            if isMaximizing:    # def MAX
                v = float('-inf')
                for move in valid_moves:
                    board_clone = board.copy()
                    self.add_move_to_board(board_clone, move, self.player_number)
                    score = hminimax(board_clone, depth - 1, alpha, beta, False)[1]
                    if score > v:
                        v = score
                        best_move = move
                    alpha = max(alpha, v)
                    if alpha >= beta:
                        break
                return best_move, v

            else: # def MIN
                v = float('inf')
                for move in valid_moves:
                    board_clone = board.copy()
                    self.add_move_to_board(board_clone, move, enemy_number)
                    score = hminimax(board_clone, depth - 1, alpha, beta, True)[1]
                    if score < v:
                        v = score
                        best_move = move
                    beta = min(beta, v)
                    if alpha >= beta:
                        break
                return best_move, v

        alpha = float('-inf')
        beta = float('inf')
        best_move, best_score = hminimax(board, depth, alpha, beta, True)
        
        return best_move

       
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

        
        # CONSTANTS
        WINNING_SCORE = 999999
        LOSING_SCORE = -999999

        depth = DEPTH_LIMIT
        player_number = self.player_number
        enemy_number = (player_number % 2) + 1
        valid_moves = self.get_valid_cols(board)
        best_move = np.random.choice(valid_moves)
        self.time_total_nodes = 0

        def is_terminal_state(board):
            return len(valid_moves) == 0 or self.game_completed(player_number, board) or self.game_completed(enemy_number, board) 

        # Expectimax implementation
        def expectimax (board, depth, isMaximizing):
            # Case 0: Terminal state or 0 depth
            self.time_total_nodes += 1
            best_move = 3
            is_terminal = is_terminal_state(board)
            if is_terminal or depth == 0:
                if is_terminal:
                    if self.game_completed(player_number, board):
                        return (None, WINNING_SCORE)
                    elif self.game_completed(enemy_number, board):
                        return (None, LOSING_SCORE)
                    else:
                         return (None, 0) # out of moves
                else:
                    return (None, self.evaluation_function(board))
            
            # If maximizing, return the max node!
            if isMaximizing:   
                v = float('-inf')
                for move in valid_moves:
                    board_clone = board.copy()
                    self.add_move_to_board(board_clone, move, self.player_number)
                    score = expectimax(board_clone, depth - 1, False)[1]
                    if score > v:
                        v = score
                        best_move = move
                return best_move, v

            # When minimizing, expected value!
            else: # MIN: exp_value
                v = 0
                for move in valid_moves:
                    p = float(1/len(valid_moves))
                    board_clone = board.copy()
                    self.add_move_to_board(board_clone, move, enemy_number)
                    v = p * expectimax(board_clone, depth - 1, True)[1]
                return best_move, v

        best_move, best_score = expectimax(board, depth, True)

        return best_move

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
        # CONSTANTS
        ## Scores
        MAXIMUM_SCORE = 100
        HIGH_SCORE = 10
        MEDIUM_SCORE = 5
        MINIMUM_SCORE = -8

        ## Definitions
        WINNING_ROW_LENGTH = 4
        EMPTY_SLOT = 0

        # VARIABLES
        player_number = self.player_number
        enemy_number = (player_number % 2) + 1
        final_score = 0

        # Analyzes a board to look for sequences of a specfic length for a player 
        def evaluate_sequence_score(row):
            score = 0
            # Enemy validations
            if np.count_nonzero(row == enemy_number) == 3 and np.count_nonzero(row == EMPTY_SLOT) == 1:
                score += MINIMUM_SCORE

            # PLayer validations
            if np.count_nonzero(row == player_number) == 4:
                score += MAXIMUM_SCORE

            elif np.count_nonzero(row == player_number) == 3 and np.count_nonzero(row == EMPTY_SLOT) == 1:
                score += HIGH_SCORE
            
            elif np.count_nonzero(row == player_number) == 2 and np.count_nonzero(row == EMPTY_SLOT) == 2:
                score += MEDIUM_SCORE

            return score

        
        def check_horizontal(b):
            score = 0
            for row in b:
                for c in range(len(row)-3):
                    score += evaluate_sequence_score(row[c:c+4])
            return score
        
        def check_verticle(b):
                return check_horizontal(b.T)
        
        def check_diagonal(b):
            score = 0
            to_str = lambda a: ''.join(a.astype(str))

            for op in [None, np.fliplr]:
                op_board = op(b) if op else b
    
                root_diag = np.diagonal(op_board, offset=0).astype(np.int)
                if len(root_diag) >= 4:
                    for c in range(len(root_diag)-4):
                        score += evaluate_sequence_score(root_diag[c:c+4])
                
                for i in range(1, b.shape[1]-3):
                    for offset in [i, -i]:
                        diag = np.diagonal(op_board, offset=offset)
                        diag = to_str(diag.astype(np.int))
                        if len(diag) >= 4:
                            for c in range(len(diag)-4):
                                score += evaluate_sequence_score(diag[c:c+4])
            return score

        # 1. Define the terminal states (Winning/Losing boards)
        # 2. Analyze the board
        final_score += check_horizontal(board)
        final_score += check_verticle(board)
        final_score += check_diagonal(board)

        return final_score


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

