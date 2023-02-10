import numpy as np
DEPTH_LIMIT = 100

class AIPlayer:
    def __init__(self, player_number):
        self.player_number = player_number
        self.type = 'ai'
        self.player_string = 'Player {}:ai'.format(player_number)

# ================================ TERMINAL/UTILITY/ACTIONS/RESULTS ===========================
    def is_terminal(self, board):
        for i in range(6):
            for j in range(7):
                if board[i][j] == 0:
                    return False
            return True
        return False

    def utility(self, board):
        return self.evaluation_function(board)

    def get_actions(self, board):
        actions = [] 
        for i in range(7): 
            if 0 in board[:,i]: 
                actions.append(i) 
        return actions

    def result(self, board, action):
        new_board = board.copy()
        if 0 not in board[:, action]:
            return None 
        for i in range(5, -1, -1): 
            if new_board[i][action] == 0: 
                new_board[i][action] = self.player_number
                break
        return new_board
# ===========================================================================================

# ================================ ALPHA BETA ================================================
    def min_value(self, board, alpha, beta, depth):
        if self.is_terminal(board) or depth == DEPTH_LIMIT:
            return self.utility(board)
        v = np.inf
        for action in self.get_actions(board):
            v = min(v, self.max_value(self.result(board, action), alpha, beta, depth))
            if v <= alpha:
                return v
            beta = min(beta, v)
        return v

    def max_value(self, board, alpha, beta, depth):
        if self.is_terminal(board) or depth == DEPTH_LIMIT:
            return self.utility(board)
        v = -np.inf
        for action in self.get_actions(board):
            v = max(v, self.min_value(self.result(board, action), alpha, beta, depth))
            if v >= beta:
                return v
            alpha = max(alpha, v)
        return v

    def alpha_beta_value(self, board, alpha, beta, depth):
        if self.is_terminal(board) or depth == DEPTH_LIMIT:
            if self.player_number == 1:
                return self.max_value(board, alpha, beta, depth)
            else:
                return self.min_value(board, alpha, beta, depth)

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
        return self.alpha_beta_value(board, -np.inf, np.inf, DEPTH_LIMIT)
       # raise NotImplementedError('Whoops I don\'t know what to do')
# ===========================================================================================

# ================================ EXPECTIMAX ================================================
    def probability(self, board):
        return 1/len(self.get_actions(board)) if self.get_actions(board) else 0

    def expected_value(self, board, depth=0):
        if self.is_terminal(board) or depth == DEPTH_LIMIT: 
            return self.utility(board)
        v = 0.0
        v = sum(self.probability(board) * self.value(self.result(board, action), depth+1) for action in self.get_actions(board))
        return v

    def expectimax_max_value(self, board, depth):
        if self.is_terminal(board) or depth == DEPTH_LIMIT:
            return self.utility(board)
        v = -np.inf
        for action in self.get_actions(board): 
            v = max(v, self.value(self.result(board, action)))
        return v

    def value(self, board, depth):
        if self.is_terminal(board) or depth == DEPTH_LIMIT:
            return self.utility(board)
        if self.player_number == 1:
            return self.expectimax_max_value(board)
        else:
            return self.expected_value(board)

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
        return self.value(board, DEPTH_LIMIT)
       # raise NotImplementedError('Whoops I don\'t know what to do')
# ===========================================================================================

# ================================ EVALUATION FUNCTION ======================================    
    def evaluation_function(self, board):
        """
        Given the current state of the board, return a score for the current
        state of the game

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
        A score for the current state of the game
        """

        row_ind = 0
        col_ind = 0
        num_adjacent = 0
        max_adjacent = 0
        score = 0
        offsets = [(-1, 0), (0, -1), (-1, -1), (-1, 1)]
        
        # Check for 4 in a row for the current player
        for row_ind in range(5,0,-1): 
            for col_ind in range(6): 
                if board[row_ind][col_ind] == self.player_number: 
                    for offset in offsets: 
                        num_adjacent = 1 
                        x_offset = offset[0] 
                        y_offset = offset[1] 
                        while True:
                            if row_ind + x_offset >= 0 and row_ind + x_offset < 6 and col_ind + y_offset >= 0 and col_ind + y_offset < 7:
                                if board[row_ind + x_offset][col_ind + y_offset] == self.player_number: 
                                    num_adjacent += 1 
                                    x_offset += offset[0] 
                                    y_offset += offset[1] 
                                else:
                                    break
                            else:
                                break
                            if num_adjacent > max_adjacent: 
                                max_adjacent = num_adjacent 
                    if self.player_number == 1:
                        if num_adjacent == 1:
                            score += 1
                        elif num_adjacent == 2:
                            score += 10
                        elif num_adjacent == 3:
                            score += 100
                        elif num_adjacent == 4:
                            score += 1000
                        else:
                            score += 0
                    elif self.player_number == 2:
                        if num_adjacent == 1:
                            score -= 1
                        elif num_adjacent == 2:
                            score -= 10
                        elif num_adjacent == 3:
                            score -= 100
                        elif num_adjacent == 4:
                            score -= 1000
                        else:
                            score -= 0
        
        # Check for 4 in a row for the opponent player
        opponent = 2 if self.player_number == 2 else 1
        for row_ind in range(5,0,-1): 
            for col_ind in range(6): 
                if board[row_ind][col_ind] == opponent: 
                    for offset in offsets: 
                        num_adjacent = 1 
                        x_offset = offset[0] 
                        y_offset = offset[1] 
                        while True:
                            if row_ind + x_offset >= 0 and row_ind + x_offset < 6 and col_ind + y_offset >= 0 and col_ind + y_offset < 7:
                                if board[row_ind + x_offset][col_ind + y_offset] == opponent: 
                                    num_adjacent += 1 
                                    x_offset += offset[0] 
                                    y_offset += offset[1] 
                                else:
                                    break
                            else:
                                break
                            if num_adjacent > max_adjacent:
                                max_adjacent = num_adjacent
                    if opponent == 1:
                        if num_adjacent == 1:
                            score += 1
                        elif num_adjacent == 2:
                            score += 10
                        elif num_adjacent == 3:
                            score += 100
                        elif num_adjacent == 4:
                            score += 1000
                        else:
                            score += 0
                    elif opponent == 2:
                        if num_adjacent == 1:
                            score -= 1
                        elif num_adjacent == 2:
                            score -= 10
                        elif num_adjacent == 3:
                            score -= 100
                        elif num_adjacent == 4:
                            score -= 1000
                        else:
                            score -= 0
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

