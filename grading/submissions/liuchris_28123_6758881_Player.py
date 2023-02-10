import numpy as np

to_str = lambda a: "".join(a.astype(str))


def calc_horizontal_value(b, feature):
    """Calculate the number of horizontal lines of a given length."""
    value = 0
    for row in b:
        if feature in to_str(row):
            value += 1
    return value


def calc_vertical_value(b, feature):
    """Calculate the number of vertical lines of a given length."""
    return calc_horizontal_value(b.T, feature)


def calc_diagonal_value(b, feature):
    """Calculate the number of diagonal lines of a given length."""
    value = 0
    for op in [None, np.fliplr]:
        op_board = op(b) if op else b
        for i in range(-op_board.shape[0] + 1, op_board.shape[1]):
            diag = np.diag(op_board, i)
            if feature in to_str(diag):
                value += 1
    return value


def line_feature(board, player_number, line_length):
    """Give 1 value for each line of a given length."""
    feature = str(player_number) * line_length
    return (
        calc_horizontal_value(board, feature)
        + calc_vertical_value(board, feature)
        + calc_diagonal_value(board, feature)
    )


def block_vertical_feature(board, player_number, line_length):
    """
    Give 1 value for each vertical line blocked by self.
    """
    feature = str(player_number) + str(3 - player_number) * line_length
    return calc_vertical_value(board, feature)


def block_horizontal_feature(board, player_number, line_length):
    """
    Give 1 value for each horizontal line blocked by self.
    """
    feature = []
    for i in range(line_length + 1):
        feature.append(
            str(3 - player_number) * i
            + str(player_number)
            + str(3 - player_number) * (line_length - i)
        )
    # Type 1 block feature: 1222, 2221
    feature_1 = [s for s in feature if str(3 - player_number) * 3 in s]
    # Type 2 block feature: 2122, 2212
    # feature_2 = [s for s in feature if s not in feature_1]
    value = 0
    for row in board:
        if all(p_str in to_str(row) for p_str in feature_1):
            value += 1
        if any(p_str in to_str(row) for p_str in feature):
            value += 1
    return value


def block_diagonal_feature(board, player_number, line_length):
    """
    Give 1 value for each diagonal line blocked by self.
    """
    feature = []
    for i in range(line_length + 1):
        feature.append(
            str(3 - player_number) * i
            + str(player_number)
            + str(3 - player_number) * (line_length - i)
        )
    feature_1 = [s for s in feature if str(3 - player_number) * 3 in s]
    value = 0
    for op in [None, np.fliplr]:
        op_board = op(board) if op else board
        for i in range(-op_board.shape[0] + 1, op_board.shape[1]):
            diag = np.diag(op_board, i)
            if all(p_str in to_str(diag) for p_str in feature_1):
                value += 1
            if any(p_str in to_str(diag) for p_str in feature):
                value += 1
    return value


def line_value(board, player_number, lengths, weights):
    """
    Calculate the value of a line of a given length.
    """
    return sum(
        [w * line_feature(board, player_number, l) for l, w in zip(lengths, weights)]
    )


def block_value(board, player_number, lengths, weights):
    """
    Calculate the value of a line blocked by self.
    """
    return sum(
        [
            w * block_vertical_feature(board, player_number, l)
            + w * block_horizontal_feature(board, player_number, l)
            + w * block_diagonal_feature(board, player_number, l)
            for l, w in zip(lengths, weights)
        ]
    )


class AIPlayer:
    def __init__(self, player_number):
        self.player_number = player_number
        self.type = "ai"
        self.player_string = "Player {}:ai".format(player_number)
        self.turn_count = 0
        self.depth = 1  # uncomment when using the unmodified script

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

        # If the board is empty or has only one piece, return a random move
        if np.sum(board != 0) <= 1:
            valid_moves = self.get_valid_moves(board)
            return 3 if 3 in valid_moves else np.random.choice(valid_moves)

        def alpha_beta(board, depth, alpha, beta, maximizing_player):
            """
            Given the current state of the board, return the next move based on
            the alpha-beta pruning algorithm
            """
            if depth <= 0 or self.game_completed(board):
                return self.evaluation_function(board)
            if maximizing_player:
                best_value = -np.inf
                for move in self.get_valid_moves(board):
                    new_board = self.make_move(board, move)
                    value = alpha_beta(new_board, depth - 1, alpha, beta, False)
                    best_value = max(best_value, value)
                    alpha = max(alpha, best_value)
                    if beta <= alpha:
                        break
                return best_value
            else:
                best_value = np.inf
                for move in self.get_valid_moves(board):
                    new_board = self.make_move(board, move)
                    value = alpha_beta(new_board, depth - 1, alpha, beta, True)
                    best_value = min(best_value, value)
                    beta = min(beta, best_value)
                    if beta <= alpha:
                        break
                return best_value

        best_move = None
        best_value = -np.inf
        for move in self.get_valid_moves(board):
            new_board = self.make_move(board, move)
            value = alpha_beta(new_board, self.depth - 1, -np.inf, np.inf, False)
            if value > best_value:
                best_value = value
                best_move = move
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
        # If the board is empty or has only one piece, return a random move
        if np.sum(board != 0) <= 1:
            valid_moves = self.get_valid_moves(board)
            return 3 if 3 in valid_moves else np.random.choice(valid_moves)

        def expectimax(board, depth, maximizing_player):
            """
            Given the current state of the board, return the next move based on
            the expectimax algorithm.
            """
            if depth <= 0 or self.game_completed(board):
                return self.evaluation_function(board)
            if maximizing_player:
                best_value = -np.inf
                for move in self.get_valid_moves(board):
                    new_board = self.make_move(board, move)
                    value = expectimax(new_board, depth - 1, False)
                    best_value = max(best_value, value)
                return best_value
            else:
                best_value = 0
                for move in self.get_valid_moves(board):
                    new_board = self.make_move(board, move)
                    value = expectimax(new_board, depth - 1, True)
                    best_value += value
                num_valid_moves = (
                    len(self.get_valid_moves(board))
                    if len(self.get_valid_moves(board)) > 0
                    else 1
                )
                return best_value / num_valid_moves

        best_move = None
        best_value = -np.inf
        for move in self.get_valid_moves(board):
            new_board = self.make_move(board, move)
            value = expectimax(new_board, self.depth - 1, False)
            if value > best_value:
                best_value = value
                best_move = move
        return best_move

    def evaluation_function(self, board):
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
        self_line_values = line_value(
            board, self.player_number, [2, 3, 4], [1e-2, 1e-1, 1.0]
        )
        opp_line_values = line_value(
            board, 3 - self.player_number, [2, 3, 4], [1e-2, 1e-1, 1.0]
        )
        block_values = block_value(board, self.player_number, [2, 3], [1e-1, 1.0])
        return self_line_values - opp_line_values + block_values

    def game_completed(self, board):
        """
        Given the current state of the board, return whether the game is
        completed or not.
        """
        player_win_str = "{0}{0}{0}{0}".format(self.player_number)
        to_str = lambda a: "".join(a.astype(str))

        def check_horizontal(b):
            for row in b:
                if player_win_str in to_str(row):
                    return True
            return False

        def check_vertical(b):
            return check_horizontal(b.T)

        def check_diagonal(b):
            for op in [None, np.fliplr]:
                op_board = op(b) if op else b

                root_diag = np.diagonal(op_board, offset=0).astype(int)
                if player_win_str in to_str(root_diag):
                    return True

                for i in range(1, b.shape[1] - 3):
                    for offset in [i, -i]:
                        diag = np.diagonal(op_board, offset=offset)
                        diag = to_str(diag.astype(int))
                        if player_win_str in diag:
                            return True

            return False

        return check_horizontal(board) or check_vertical(board) or check_diagonal(board)

    def get_valid_moves(self, board):
        """Get the indices of the columns that are not full."""
        return [i for i, col in enumerate(board.T) if 0 in col]

    def make_move(self, board, move):
        """Update the board with the move for the current player.
        The move should be placed at the lowest available row in the column.
        """
        new_board = board.copy()
        col = new_board.T[move]
        row = np.where(col == 0)[0][-1]
        new_board[row, move] = self.player_number
        return new_board


class RandomPlayer:
    def __init__(self, player_number):
        self.player_number = player_number
        self.type = "random"
        self.player_string = "Player {}:random".format(player_number)

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
        self.type = "human"
        self.player_string = "Player {}:human".format(player_number)

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

        move = int(input("Enter your move: "))

        while move not in valid_cols:
            print("Column full, choose from:{}".format(valid_cols))
            move = int(input("Enter your move: "))

        return move
