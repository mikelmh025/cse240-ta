import numpy as np

class AIPlayer:
    def __init__(self, player_number):
        self.player_number = player_number
        self.type = 'ai'
        self.player_string = 'Player {}:ai'.format(player_number)
        self.opponent = 2 if (player_number == 1) else 1
        self.c = 0

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

        value, move = self.max_value(0, board, float('-inf'), float('inf'), -1)
        return move

    def max_value(self, depth, board, a, b, move):
        #evaluate if terminal state or set depth reached
        if (self.consecutive_check(board, self.player_number) == 4 or
        self.consecutive_check(board, self.opponent) == 4 or depth == 2):
            return self.evaluation_function(board), move
        v = float('-inf')
        for col in range(board.shape[1]):
            if 0 in board[:, col]:
                # create a successor state by making a move on a copy of board
                board_copy = np.copy(board)
                for row in range(board.shape[0] - 1, -1, -1):
                    if board[row, col] == 0:
                        board_copy[row, col] = self.player_number
                        break
                successor_value, new_move = self.min_value(depth+1, board_copy, a, b, col)
                if successor_value > v:
                    v = successor_value
                    move = new_move
                if v >= b:
                    return v, col
                a = max(a, v)
        return v, move

    def min_value(self, depth, board, a, b, move):
        #evaluate if terminal state or set depth reached
        if (self.consecutive_check(board, self.player_number) == 4 or
        self.consecutive_check(board, self.opponent) == 4 or depth == 2):
            return self.evaluation_function(board), move
        v = float('inf')
        for col in range(board.shape[1]):
            if 0 in board[:, col]:
                # create a successor state by making a move on a copy of board
                board_copy = np.copy(board)
                for row in range(board.shape[0]-1, -1, -1):
                    if board[row, col] == 0:
                        board_copy[row, col] = self.opponent
                        break
                successor_value, new_move = self.max_value(depth+1, board_copy, a, b, col)
                if successor_value < v:
                    v = successor_value
                    move = new_move
                if v <= a:
                    return v, col
                b = min(b, v)
        return v, move

    def consecutive_check(self, board, player_num):
        """
        Checks for two, three or four consecutive positions occupied.
        This function is used by the evaluation function.
        """
        player_win_str = '{0}{0}{0}{0}'.format(player_num)
        player_three_str = '{0}{0}{0}'.format(player_num)
        player_two_str = '{0}{0}'.format(player_num)
        to_str = lambda a: ''.join(a.astype(str))

        def check_horizontal(b):
            for row in b:
                if player_win_str in to_str(row):
                    return 4
                if player_three_str in to_str(row):
                    return 3
                if player_two_str in to_str(row):
                    return 2
            return 0

        def check_verticle(b):
            return check_horizontal(b.T)

        def check_diagonal(b):
            for op in [None, np.fliplr]:
                op_board = op(b) if op else b

                root_diag = np.diagonal(op_board, offset=0).astype(np.int)
                if player_win_str in to_str(root_diag):
                    return 4
                if player_three_str in to_str(root_diag):
                    return 3
                if player_two_str in to_str(root_diag):
                    return 2

                for i in range(1, b.shape[1]-3):
                    for offset in [i, -i]:
                        diag = np.diagonal(op_board, offset=offset)
                        diag = to_str(diag.astype(np.int))
                        if player_win_str in diag:
                            return 4
                        if player_three_str in diag:
                            return 3
                        if player_two_str in diag:
                            return 2

            return 0

        return max(check_horizontal(board), check_verticle(board), check_diagonal(board))

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
        #raise NotImplementedError('Whoops I don\'t know what to do')
        value, move = self.emax_value(0, board, -1)
        return move

    def emax_value(self, depth, board, move):
        #evaluate if terminal state or set depth reached
        if (self.consecutive_check(board, self.player_number) == 4 or
        self.consecutive_check(board, self.opponent) == 4 or depth == 2):
            return self.evaluation_function(board), move
        v = float('-inf')
        for col in range(board.shape[1]):
            if 0 in board[:, col]:
                # create a successor state by making a move on a copy of board
                board_copy = np.copy(board)
                for row in range(board.shape[0] - 1, -1, -1):
                    if board[row, col] == 0:
                        board_copy[row, col] = self.player_number
                        break
                successor_value, new_move = self.exp_value(depth+1, board_copy, col)
                if successor_value > v:
                    v = successor_value
                    move = new_move
        return v, move

    def exp_value(self, depth, board, move):
        #evaluate if terminal state or set depth reached
        if (self.consecutive_check(board, self.player_number) == 4 or
        self.consecutive_check(board, self.opponent) == 4 or depth == 2):
            return self.evaluation_function(board), move
        v = 0
        successors = 0
        # count the number of successor states (available columns)
        for col in range(board.shape[1]):
            if 0 in board[:, col]:
                successors = successors + 1
        p = 1/successors
        for col in range(board.shape[1]):
            if 0 in board[:, col]:
                # create a successor state by making a move on a copy of board
                board_copy = np.copy(board)
                for row in range(board.shape[0]-1, -1, -1):
                    if board[row, col] == 0:
                        board_copy[row, col] = self.opponent
                        break
                successor_value, new_move = self.emax_value(depth+1, board, col)
                v += p * successor_value
        return v, move

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

        value = 0

        # heuristic function
        def depth_eval(board):
            player_state = self.consecutive_check(board, self.player_number)
            opponent_state = self.consecutive_check(board, self.opponent)

            if player_state == 4:
                return 10
            if opponent_state == 4:
                return -10

            if player_state == 3:
                return 3
            if player_state == 2:
                return 2
            if opponent_state == 3:
                return -3
            if opponent_state == 2:
                return -2

            return 0

        # create successors of given state for calculating sum
        for col in range(board.shape[1]):
            if 0 in board[:, col]:
                board_copy = np.copy(board)
                for row in range(board.shape[0] - 1, -1, -1):
                    if board[row, col] == 0:
                        board_copy[row, col] = self.player_number
                        break
                value += depth_eval(board_copy)
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

