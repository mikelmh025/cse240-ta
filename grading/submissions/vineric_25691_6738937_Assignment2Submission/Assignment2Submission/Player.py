import numpy as np

VERBOSE = True

class AIPlayer:
    def __init__(self, player_number):
        self.player_number = player_number
        self.type = 'ai'
        self.player_string = 'Player {}:ai'.format(player_number)
        self.opponent_number = 1 if self.player_number == 2 else 2
        self.max_depth=4

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
        moves = [(move, self.minimax_value(next_board, self.opponent_number, self.max_depth-1, -float('inf'), float('inf'))) for move, next_board in feasible_moves(board, self.player_number)]
        optimal_score = max(score for _, score in moves)
        optimal_moves = [move for move, score in moves if score == optimal_score]
        next_move =  sorted(optimal_moves)[0] # Sorted for reproducibility

        if VERBOSE:
            print(f"Player {self.player_number} picking move {next_move} with score {optimal_score}")

        return next_move

    def minimax_value(self, board, current_player, remaining_depth, alpha, beta):
        # Check for terminal depth or game completion
        if game_completed(board, 1) or game_completed(board, 2) or remaining_depth == 0:
            return self.evaluation_function(board)

        # Otherwise recurse
        if current_player == self.player_number:
            return self.max_value(board, current_player, remaining_depth, alpha, beta)
        else:
            return self.min_value(board, current_player, remaining_depth, alpha, beta)

    def max_value(self, board, current_player, remaining_depth, alpha, beta):
        value = -float('inf')
        for _, next_board in feasible_moves(board, current_player):
            value = max(value, self.minimax_value(next_board, 1 if current_player == 2 else 2, remaining_depth-1, alpha, beta))

            if value >= beta:
                return value

            alpha = max(alpha, value)

        return value

    def min_value(self, board, current_player, remaining_depth, alpha, beta):
        value = float('inf')
        for _, next_board in feasible_moves(board, current_player):
            value = min(value, self.minimax_value(next_board, 1 if current_player == 2 else 2, remaining_depth-1, alpha, beta))

            if value <= alpha:
                return value

            alpha = min(alpha, value)

        return value

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
        moves = [(move, self.expectimax_value(next_board, self.opponent_number, self.max_depth-1)) for move, next_board in feasible_moves(board, self.player_number)]
        optimal_score = max(score for _, score in moves)
        optimal_moves = [move for move, score in moves if score == optimal_score]
        next_move =  sorted(optimal_moves)[0] # Sorted for reproducibility

        if VERBOSE:
            print(f"Player {self.player_number} picking move {next_move} with score {optimal_score}")

        return next_move
    def expectimax_value(self, board, current_player, remaining_depth):
        # Check for terminal depth or game completion
        if game_completed(board, 1) or game_completed(board, 2) or remaining_depth == 0:
            return self.evaluation_function(board)

        # Otherwise recurse
        if current_player == self.player_number:
            return self.max_value_expectimax(board, current_player, remaining_depth)
        else:
            return self.expect_value(board, current_player, remaining_depth)

    def max_value_expectimax(self, board, current_player, remaining_depth):
        return max(self.expectimax_value(next_board, 1 if current_player == 2 else 2, remaining_depth-1) for _, next_board in feasible_moves(board, current_player))

    def expect_value(self, board, current_player, remaining_depth):
        values = [self.expectimax_value(next_board, 1 if current_player == 2 else 2, remaining_depth-1) for _, next_board in feasible_moves(board, current_player)]
        mean = sum(values)/len(values)
        return mean

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
        # Check if the game has been won
        if game_completed(board, self.player_number):
            return 4

        if game_completed(board, self.opponent_number):
            return -4

        # Give score based on max number of tokens in a row compared to opponent
        player_best = 0
        for check_num in [3,2]:
            if check_in_a_row(board, self.player_number, check_num):
                player_best = check_num
                break

        opponent_best = 0
        for check_num in [3,2]:
            if check_in_a_row(board, self.opponent_number, check_num):
                opponent_best = check_num
                break

        return player_best-opponent_best

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


def feasible_moves(board, player):
    moves = []

    assert not (game_completed(board, 1)) and (not game_completed(board, 2))

    for column in range(7):
        move = apply_move(board, column, player)

        if move is not None:
            moves.append((column, move))

    return moves

def apply_move(board, column, player):
    valid_cols = []
    for i, col in enumerate(board.T):
        if 0 in col:
            valid_cols.append(i)

    if column not in valid_cols:
        return None

    new_board = np.copy(board)

    for row in reversed(range(6)):
        if new_board[row,column] == 0:
            new_board[row,column] = player
            return new_board

    assert False

def game_completed(board, player_num):
    # Copied from ConnectFour.py
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

def check_in_a_row(board, player_num, check_num):
    # Modified from ConnectFour.py
    player_win_str = str(player_num)*check_num
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
