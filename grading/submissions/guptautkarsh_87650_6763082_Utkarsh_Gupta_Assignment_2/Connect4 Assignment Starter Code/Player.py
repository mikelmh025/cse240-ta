import numpy as np

class AIPlayer:
    def __init__(self, player_number):
        self.player_number = player_number
        if player_number==1:
            self.opponent_number = 2
        elif player_number==2:
            self.opponent_number = 1

        self.empty_number = 0
        self.type = 'ai'
        self.player_string = 'Player {}:ai'.format(player_number)
        self.row_count = 6
        self.col_count = 7

    def get_the_empty_spaces(self, board):
        empty_cols = []
        for col_idx in range(self.col_count):
            if 0 in board[:, col_idx]:
                empty_cols.append(col_idx)
        return empty_cols

    def get_the_corresponding_empty_row(self, column):
        for idx in range(self.row_count):
            if column[idx]!=0:
                return idx-1
        return self.row_count-1

    def is_a_winning_move(self, board, player_number):
        # Check horizontal locations for win
        for col_idx in range(self.col_count-3):
            for row_idx in range(self.row_count-1, -1, -1):
                if board[row_idx][col_idx] == player_number and \
                    board[row_idx][col_idx+1] == player_number and \
                        board[row_idx][col_idx+2] == player_number and \
                            board[row_idx][col_idx+3] == player_number:
                    return True

        # Check vertical locations for win
        for col_idx in range(self.col_count):
            for row_idx in range(self.row_count-1, self.row_count-4, -1):
                if board[row_idx][col_idx] == player_number and \
                    board[row_idx-1][col_idx] == player_number and \
                        board[row_idx-2][col_idx] == player_number and \
                            board[row_idx-3][col_idx] == player_number:
                    return True

        # Check positively sloped diaganols
        for col_idx in range(self.col_count-3):
            for row_idx in range(self.row_count-1, self.row_count-4, -1):
                if board[row_idx][col_idx] == player_number and \
                    board[row_idx-1][col_idx+1] == player_number and \
                        board[row_idx-2][col_idx+2] == player_number and \
                            board[row_idx-3][col_idx+3] == player_number:
                    return True

        # Check negatively sloped diaganols
        for col_idx in range(self.col_count-3):
            for row_idx in range(self.row_count-3):
                if board[row_idx][col_idx] == player_number and \
                    board[row_idx+1][col_idx+1] == player_number and \
                        board[row_idx+2][col_idx+2] == player_number and \
                            board[row_idx+3][col_idx+3] == player_number:
                    return True
    
    def is_a_terminal_node(self, board):
        return self.is_a_winning_move(board, self.opponent_number) or \
                    self.is_a_winning_move(board, self.player_number) or \
                        len(self.get_the_empty_spaces(board)) == 0

    def count_number_of_pieces(self, window):
        filled_coins = (window==self.player_number).sum()
        empty_coins = (window==0).sum()
        return filled_coins, empty_coins

    def get_score_for_a_window(self, window):
        score = 0

        filled_coins, empty_spaces = self.count_number_of_pieces(window)

        if filled_coins == 4:
            score += 200
        elif filled_coins == 3 and empty_spaces == 1:
            score += 5
        elif filled_coins == 2 and empty_spaces == 2:
            score += 2

        if list(window).count(self.opponent_number) == 3 and \
                list(window).count(self.empty_number) == 1:
            score -= 4

        return score
    
    def minimax(self, board, depth, alpha, beta, maximizingPlayer):
        valid_locations = self.get_the_empty_spaces(board)
        is_terminal = self.is_a_terminal_node(board)
        if depth == 0 or is_terminal:
            if is_terminal:
                if self.is_a_winning_move(board, self.player_number):
                    return (None, 100000000000000)
                elif self.is_a_winning_move(board, self.opponent_number):
                    return (None, -10000000000000)
                else: # Game is over, no more valid moves
                    return (None, 0)
            else: # Depth is zero
                return (None, self.evaluation_function(board))
        if maximizingPlayer:
            value = -float('inf')
            column = np.random.choice(valid_locations)
            for col_idx in valid_locations:
                row_idx = self.get_the_corresponding_empty_row(board[:, col_idx])
                b_copy = board.copy()
                b_copy[row_idx, col_idx] = self.player_number
                new_score = self.minimax(b_copy, depth-1, alpha, beta, False)[1]
                if new_score > value:
                    value = new_score
                    column = col_idx
                alpha = max(alpha, value)
                if alpha >= beta:
                    break
            return column, value

        else: # Minimizing player
            value = float("inf")
            column = np.random.choice(valid_locations)
            for col_idx in valid_locations:
                row_idx = self.get_the_corresponding_empty_row(board[:, col_idx])
                b_copy = board.copy()
                b_copy[row_idx, col_idx] = self.opponent_number
                new_score = self.minimax(b_copy, depth-1, alpha, beta, True)[1]
                if new_score < value:
                    value = new_score
                    column = col_idx
                beta = min(beta, value)
                if alpha >= beta:
                    break
            return column, value

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
        return self.minimax(board, 4, -float('inf'), float('inf'), True)[0]

    def run_expectimax_algorithm(self, board, depth, maximizingPlayer):
        valid_locations = self.get_the_empty_spaces(board)
        is_terminal = self.is_a_terminal_node(board)
        if depth == 0 or is_terminal:
            if is_terminal:
                if self.is_a_winning_move(board, self.player_number):
                    return (None, 100000000000000)
                elif self.is_a_winning_move(board, self.opponent_number):
                    return (None, -10000000000000)
                else: # Game is over, no more valid moves
                    return (None, 0)
            else: # Depth is zero
                return (None, self.evaluation_function(board))
        if maximizingPlayer:
            value = -float('inf')
            column = np.random.choice(valid_locations)
            for col_idx in valid_locations:
                row_idx = self.get_the_corresponding_empty_row(board[:, col_idx])
                b_copy = board.copy()
                b_copy[row_idx, col_idx] = self.player_number
                new_score = (self.run_expectimax_algorithm(b_copy, depth-1, False)[1])
                if new_score > value:
                    value = new_score
                    column = col_idx
            return column, value

        else: # Minimizing player will make a move with some Expectation
            column = np.random.choice(valid_locations)
            total_score = 0
            for col_idx in valid_locations:
                row_idx = self.get_the_corresponding_empty_row(board[:, col_idx])
                b_copy = board.copy()
                b_copy[row_idx, col_idx] = self.opponent_number
                total_score += (self.run_expectimax_algorithm(b_copy, depth-1, True)[1]) / 7
            return (None, total_score)

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
        return self.run_expectimax_algorithm(board, depth=3, maximizingPlayer=True)[0]

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

        ## Prefer center column
        center_filled_coins, _ = self.count_number_of_pieces(
                                                    board[:, self.col_count//2])
        score += center_filled_coins * 3
        window_length = 4

        ## Score Horizontal
        for row_idx in range(self.row_count-1, -1, -1):
            for col_idx in range(self.col_count-3):
                window = board[row_idx, col_idx:col_idx+window_length]
                score += self.get_score_for_a_window(window)

        ## Score Vertical
        for col_idx in range(self.col_count):
            for row_idx in range(self.row_count-1, self.row_count-4, -1):
                window = board[row_idx:row_idx-window_length, col_idx]
                score += self.get_score_for_a_window(window)

        ## Score posiive sloped diagonal
        for row_idx in range(self.row_count-1, self.row_count-4, -1):
            for col_idx in range(self.col_count-3):
                window = np.array([board[row_idx-idx][col_idx+idx] \
                                            for idx in range(window_length)])
                score += self.get_score_for_a_window(window)

        for row_idx in range(self.row_count-3):
            for col_idx in range(self.col_count-3):
                window = np.array([board[row_idx+idx][col_idx+idx] \
                                            for idx in range(window_length)])
                score += self.get_score_for_a_window(window)
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

