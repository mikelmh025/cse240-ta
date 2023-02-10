import numpy as np

# Global Variables
COLUMNS = 7
ROWS = 6
WINDOW = 4
AB_DEPTH = 5
EXP_DEPTH = 4


class AIPlayer:
    def __init__(self, player_number):
        self.player_number = player_number
        self.type = 'ai'
        self.player_string = 'Player {}:ai'.format(player_number)

    # Taken from ConnectFour.py file
    def game_completed(self, board, player_number):
        player_win_str = '{0}{0}{0}{0}'.format(player_number)
        def to_str(a): return ''.join(a.astype(str))

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

                root_diag = np.diagonal(op_board, offset=0).astype(int)
                if player_win_str in to_str(root_diag):
                    return True

                for i in range(1, b.shape[1]-3):
                    for offset in [i, -i]:
                        diag = np.diagonal(op_board, offset=offset)
                        diag = to_str(diag.astype(int))
                        if player_win_str in diag:
                            return True

            return False

        return (check_horizontal(board) or
                check_verticle(board) or
                check_diagonal(board))

    # Returns array of integers that represent columns with available spaces for a piece
    def get_valid_moves(self, board):
        valid_cols = []
        for i, col in enumerate(board.T):
            if 0 in col:
                valid_cols.append(i)
        return valid_cols

    # Places piece at next available space in column
    def simulate_move(self, board, col, player):
        for (row, cell) in enumerate(board.T[col]):
            if cell == 0:
                board.T[col][row] = player
                return

    # Checks if current player or opponent has won, or if there are no more valid moves
    def game_over(self, board, player, opponent, valid_moves):
        return self.game_completed(board, player) or self.game_completed(board, opponent) or len(valid_moves) == 0

    # Returns column for next alpha beta move
    def get_alpha_beta_move(self, board):
        # Initialize player and opponent
        player = self.player_number
        opponent = 1 if player == 2 else 2

        # Helper function that performs minimax algorithm
        def ab_move(board, depth, alpha, beta, max_player):
            # Store valid moves and boolean for if game is over
            valid_moves = self.get_valid_moves(board)
            is_game_over = self.game_over(board, player, opponent, valid_moves)

            # Alpha beta base case
            if depth == 0 or is_game_over:
                if is_game_over:
                    # Return high score if player wins, low score if opponent wins, 0 if tie
                    if self.game_completed(board, player):
                        return None, 100000000000000
                    elif self.game_completed(board, opponent):
                        return None, -10000000000000
                    else:
                        return None, 0
                else:
                    return None, self.evaluation_function(board)

            # Maximizing player logic
            if max_player:
                val = float("-inf")
                column = np.random.choice(COLUMNS)
                for col in valid_moves:
                    # Copy board and simulate move, pass board with simulated move to next recursive call
                    board_copy = board.copy()
                    self.simulate_move(board_copy, col, player)
                    score = ab_move(board_copy, depth - 1, alpha,
                                    beta, False)[1]
                    if score > val:
                        val = score
                        column = col
                    alpha = max(alpha, val)
                    # Prune if alpha >= beta
                    if alpha >= beta:
                        break
                return column, val
            # Minimizing player logic
            else:
                val = float("inf")
                column = np.random.choice(COLUMNS)
                for col in valid_moves:
                    # Copy board and simulate move, pass board with simulated move to next recursive call
                    board_copy = board.copy()
                    self.simulate_move(board_copy, col, opponent)
                    score = ab_move(board_copy, depth - 1,
                                    alpha, beta, True)[1]
                    if score < val:
                        val = score
                        column = col
                    # Prune if alpha >= beta
                    beta = min(beta, val)
                    if alpha >= beta:
                        break
                return column, val

        # Call helper function
        next_col, next_score = ab_move(
            board, AB_DEPTH, float("-inf"), float("inf"), True)
        return next_col

    def get_expectimax_move(self, board):
        # Expectimax helper function
        def expectimax_move(e_board, depth, myTurn):
            # Initialize player and opponent
            player = self.player_number
            opponent = 1 if player == 2 else 2

            # Expectimax base case
            if self.game_completed(e_board, player) or self.game_completed(e_board, opponent) or depth == 0:
                return None, self.evaluation_function(e_board)

            # Max values
            if myTurn == False:
                val = float("-inf")
                valid_moves = self.get_valid_moves(e_board)
                column = valid_moves[np.random.choice(len(valid_moves))]
                for col in valid_moves:
                    # Simulate move and pass board with simulated move to next recursive call
                    board_copy = e_board.copy()
                    self.simulate_move(board_copy, col, player)
                    _, score = expectimax_move(board_copy, depth - 1, False)
                    if score > val:
                        val = score
                        column = col
                return column, val
            # Exp values
            else:
                val = 0
                valid_moves = self.get_valid_moves(e_board)
                # Checks for tie
                if len(valid_moves) == 0:
                    return None, 0
                column = valid_moves[np.random.choice(len(valid_moves))]
                # Calculate weights of each move using 1 / # of valid moves
                p = 1 / len(valid_moves)
                for col in valid_moves:
                    # Simulate move and pass board with simulated move to next recursive call
                    board_copy = e_board.copy()
                    self.simulate_move(board_copy, col, opponent)
                    _, score = expectimax_move(board_copy, depth - 1, True)
                    val += (score * p)
                return column, val

        next_col, next_score = expectimax_move(board, EXP_DEPTH, True)
        return next_col

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
        opponent = 1 if player == 2 else 2

        # Function to calculate score for each window
        def score(window, player, opponent):
            score = 0

            if window.count(player) == 4:
                score += 30000
            elif window.count(player) == 3 and window.count(0) == 1:
                score += 200
            elif window.count(player) == 2 and window.count(0) == 2:
                score += 50

            if window.count(opponent) == 3 and window.count(0) == 1:
                score -= 125
            if opponent in window and player in window:
                score -= 5
            return score

        total = 0

        if self.player_number in board.T[board.shape[1]//2]:
            total += 75

        # Check horizontal
        for r in range(ROWS):
            row = [int(i) for i in list(board[r, :])]
            for c in range(COLUMNS-3):
                window = row[c:c+WINDOW]
                total += score(window, player, opponent)

        # Check vertical
        for c in range(COLUMNS):
            col = [int(i) for i in list(board[:, c])]
            for r in range(ROWS - 3):
                window = col[r:r+WINDOW]
                total += score(window, player, opponent)

        # Check for positive diag
        for r in range(ROWS - 3):
            for c in range(COLUMNS - 3):
                window = [board[r+i][c+i]
                          for i in range(WINDOW)]
                total += score(window, player, opponent)

        # Check for negative diag
        for r in range(ROWS - 3):
            for c in range(COLUMNS - 3):
                window = [board[r+3-i][c+i]
                          for i in range(WINDOW)]
                total += score(window, player, opponent)

        return total


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
