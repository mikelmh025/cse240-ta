import numpy as np
DEPTH = 3
EMPTY = 0

class AIPlayer:
    def __init__(self, player_number):
        self.player_number = player_number
        self.type = 'ai'
        self.player_string = 'Player {}:ai'.format(player_number)
        self.values_ab = []
        self.values_emax = []

    def get_valid_columns(self, board):
        # Find out the valid columns
        valid_cols = []
        for col in range(board.shape[1]):
            for row in range(board.shape[0]):
                if board[row, col] == 0:
                    valid_cols.append([row, col])
        return valid_cols
    
    def minimize_beta(self, board, alpha, beta, depth, player, opponent):
        # Minimum value: beta
        valid_columns = self.get_valid_columns(board)
        if depth >= DEPTH or not valid_columns:
            return self.evaluation_function(board)
        for row, col in valid_columns:
            board[row][col] = opponent
            min_val = self.maximize_alpha(board, alpha, beta, depth + 1, player, opponent)
            beta = min(beta, min_val)
            board[row][col] = 0
            if alpha >= beta:
                return beta
        return beta
    
    def maximize_alpha(self, board, alpha, beta, depth, player, opponent):
        # Maximize value: alpha
        valid_columns = self.get_valid_columns(board)
        if depth >= DEPTH or not valid_columns:
            return self.evaluation_function(board)
        for row, col in valid_columns:
            board[row][col] = player
            max_val = self.minimize_beta(board, alpha, beta, depth + 1, player, opponent)
            alpha = max(alpha, max_val)
            board[row][col] = 0
            if alpha >= beta:
                return alpha
        return alpha
    
    def alphabeta(self, board, alpha, beta, depth, player, opponent):
        for row, col in self.get_valid_columns(board):
            board[row][col] = player
            alpha = max(alpha, self.minimize_beta(board, alpha, beta, depth + 1, player, opponent))
            self.values_ab.append((alpha, col))
            board[row][col] = 0
            out = max(self.values_ab, key = lambda i : i[0])
        return out[1]

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
        # Find out the current player number and opponent number
        player = self.player_number
        opponent = 2 if player == 1 else 1

        alpha = -np.inf
        beta = np.inf

        return self.alphabeta(board, alpha, beta, 0, player, opponent)

        # raise NotImplementedError('Whoops I don\'t know what to do')

    def exp_val(self, board, depth, player, opponent):
        exp = 0
        valid_columns = self.get_valid_columns(board)
        if depth == 0 or not valid_columns:
            return  self.evaluation_function(board)
        for row, col in valid_columns:
            board[row][col] = opponent
            tmp = self.maximum_val(board, depth - 1, player, opponent)
            exp += tmp
        p = 1 / len(valid_columns)
        return exp * p

    def maximum_val(self, board, depth, player, opponent):
        val = -np.inf
        valid_columns = self.get_valid_columns(board)
        if depth == 0 or not valid_columns:
            return  self.evaluation_function(board)
        for row, col in valid_columns:
            board[row][col] = player
            tmp = self.exp_val(board, depth - 1, player, opponent)
            val = max(val, tmp)
        return val

    def expectimax_values(self, board, depth, player, opponent):
        e = -np.inf
        valid_columns = self.get_valid_columns(board)
        for row, col in valid_columns:
            board[row, col] = player
            expval = self.exp_val(board, depth - 1, player, opponent)
            e = max(e, expval)
            self.values_emax.append([e, col])
            board[row, col] = 0
        out = max(self.values_ab, key = lambda i : i[0])[1]
        return out

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
        player = self.player_number
        opponent = 2 if player == 1 else 1

        return self.expectimax_values(board, DEPTH, player, opponent)
        # raise NotImplementedError('Whoops I don\'t know what to do')

    def eval_window(self, window, player):
        player = self.player_number
        opponent = 2 if player == 1 else 1
        
        window_score = 0
        if window.count(player) == 4:
            window_score += 100
        elif window.count(player) == 3 and window.count(EMPTY) == 1:
            window_score += 50
        elif window.count(player) == 2 and window.count(EMPTY) == 2:
            window_score += 25
        
        if window.count(opponent) == 3 and window.count(EMPTY) == 1:
            window_score -= 25
        elif window.count(opponent) == 2 and window.count(EMPTY) == 2:
            window_score -= 10
        elif window.count(opponent) == 4:
            window_score -= 50
        return window_score

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
        player = self.player_number
        opponent = 2 if player == 1 else 1

        score = 0
        rows = 6
        columns = 7
        window_len = 4

        center = [int(i) for i in list(board[:, 7 // 2])]
        center_count = center.count(self.player_number)
        score += center_count * 3

        # Horizontal score
        for row in range(rows):
            row_arr = [int(a) for a in list(board[row,:])]
            for col in range(columns - 3):
                window = row_arr[col:col + window_len]
                score += self.eval_window(window, player)

        # Vertical score
        for col in range(columns):
            column_arr = [int(a) for a in list(board[:, col])]
            for row in range(rows - 3):
                window = column_arr[row:row + window_len]
                score += self.eval_window(window, player)
        
        # Positive diagnol score
        for row in range(rows - 3):
            for col in range(columns - 3):
                window = [board[row + a][col + a] for a in range(window_len)]
                score += self.eval_window(window, player)
        
        # Negative diagnol score
        for row in range(rows - 3):
            for col in range(columns - 3):
                window = [board[row + 3 - a][col + a] for a in range(window_len)]
                score += self.eval_window(window, player)

        return score

# Reference: https://medium.com/analytics-vidhya/artificial-intelligence-at-play-connect-four-minimax-algorithm-explained-3b5fc32e4a4f


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

