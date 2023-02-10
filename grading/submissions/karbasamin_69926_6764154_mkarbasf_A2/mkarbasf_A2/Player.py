import numpy as np

evals = {
    1: [
        ('1111', 1000), ('01110', 100),
        ('0111', 70), ('1110', 70),
        ('01100', 20), ('00110', 20), ('0011', 10), ('0110', 10), ('1100', 10),
    ],
}
evals[2] = [(run[0].replace('1', '2'), run[1]) for run in evals[1]]

ends = [evals[1][0][0], evals[2][0][0]]


def is_end(board):
    for row in board:
        for e in ends:
            if e in to_str(row):
                return True

    for col in board.T:
        for e in ends:
            if e in to_str(col):
                return True

    for op in [None, np.fliplr]:
        op_board = op(board) if op else board
        for offset in range(-2, 4):
            diag = np.diagonal(op_board, offset=offset).astype(np.int)
            for e in ends:
                if e in to_str(diag):
                    return True

    return False


def window_score(window, player):
    for run in evals[player]:
        if run[0] in window:
            return run[1]
    for run in evals[3-player]:
        if run[0] in window:
            return run[1]
    return 0


def to_str(a):
    return ''.join(a.astype(str))


def multi_window_score(a, player):
    score = 0
    wl = 5 if len(a) >= 5 else 4
    for s in range(len(a)-wl):
        score += window_score(to_str(a[s:s+wl]), player)
    return score


def eval_board(board, player):
    score = 0

    # Horizontal
    for row in board:
        score += multi_window_score(row, player)

    # Vertical
    for col in board.T:
        score += multi_window_score(col, player)

    # Diagonals
    for op in [None, np.fliplr]:
        op_board = op(board) if op else board

        for offset in range(-2, 4):
            diag = np.diagonal(op_board, offset=offset).astype(np.int)
            score += multi_window_score(diag, player)

    return score


def move_board(board, move, player):
    if not 0 in board[:, move]:
        return None

    board = board.copy()

    row = 0
    for i in range(1, board.shape[0]):
        if board[i, move] != 0:
            break
        row = i
    board[row, move] = player
    return board


class AIPlayer:
    max_depth = 6

    def __init__(self, player_number):
        self.player_number = player_number
        self.type = 'ai'
        self.player_string = 'Player {}:ai'.format(player_number)

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
        _, best_move = self.albe(
            board, AIPlayer.max_depth, -np.inf, np.inf, True)
        return best_move

    def albe(self, board, depth, a, b, maxi):
        if depth == 0 or is_end(board):
            return (self.evaluation_function(board), -1)

        val, play = ((-np.inf, self.player_number) if maxi else
                     (np.inf, 3-self.player_number))
        best_move = -1

        for move in range(board.shape[1]):
            moved = move_board(board, move, play)
            if moved is None:
                continue

            (move_val, _) = self.albe(moved, depth-1, a, b, not maxi)
            if (maxi and move_val > val) or (not maxi and move_val < val):
                best_move = move
                val = move_val

            if maxi:
                if val > b:
                    break
                a = max(a, val)
            else:
                if val < a:
                    break
                b = min(b, val)

        return (val, best_move)

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
        _, best_move = self.emax(board, AIPlayer.max_depth, True)
        return best_move

    def emax(self, board, depth, maxi):
        if depth == 0 or is_end(board):
            return (self.evaluation_function(board), -1)

        if maxi:
            best_move = -1
            a = -np.inf
            for move in range(board.shape[1]):
                moved = move_board(board, move, self.player_number)
                if moved is None:
                    continue
                (move_val, _) = self.emax(moved, depth-1, False)
                if move_val > a:
                    val, best_move = move_val, move
            return (val, best_move)

        a = 0
        cnt = 0
        for move in range(board.shape[1]):
            moved = move_board(board, move, 3-self.player_number)
            if moved is None:
                continue
            cnt += 1
            (move_val, _) = self.emax(moved, depth-1, True)
            a += move_val
        return (a/cnt, -1)

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

        return eval_board(board, self.player_number)


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
            if 0 in board[:, col]:
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
