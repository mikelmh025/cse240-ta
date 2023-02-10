import numpy as np
# I referenced the heuristic on this website, and wrote the following solution on my own
# https://github.com/AbdallahReda/Connect4/blob/master/minimaxAlphaBeta.py

def get_successors(board, player):
    valid_moves = []
    for col in range(board.shape[1]):
        if 0 in board[:, col]:
            valid_moves.append(col)
    successors = []
    for move in valid_moves:
        successor = np.copy(board)
        for row in range(1, successor.shape[0]):
            update_row = -1
            if successor[row, move] > 0 and successor[row - 1, move] == 0:
                update_row = row - 1
            elif row == successor.shape[0] - 1 and successor[row, move] == 0:
                update_row = row

            if update_row >= 0:
                successor[update_row, move] = player
        successors.append((successor, move))
    return successors


def game_completed(board, player_num):
    player_win_str = '{0}{0}{0}{0}'.format(player_num)
    to_str = lambda a: ''.join(a.astype(str))

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

            root_diag = np.diagonal(op_board, offset=0).astype(np.int)
            if player_win_str in to_str(root_diag):
                return True

            for i in range(1, b.shape[1] - 3):
                for offset in [i, -i]:
                    diag = np.diagonal(op_board, offset=offset)
                    diag = to_str(diag.astype(np.int))
                    if player_win_str in diag:
                        return True

        return False

    return (check_horizontal(board) or
            check_vertical(board) or
            check_diagonal(board))


def count_sequence(board, player, length):

    def check_vert(r, c):
        seq_length = 1
        # check next tree sequential spots
        for offset in range(1, 4):
            # get value at next spot
            try:
                spot = board[r + offset][c]
            # break if it is out of bounds
            except:
                break
            if board[r + offset][c] == board[r][c]:
                seq_length += 1
            else:
                break
        return 1 if seq_length >= length else 0

    def check_hor(r, c):
        seq_length = 1
        # check next tree sequential spots
        for offset in range(1, 4):
            # get value at next spot
            try:
                spot = board[r][c + offset]
            # break if it is out of bounds
            except:
                break
            if spot == board[r][c]:
                seq_length += 1
            else:
                break
        return 1 if seq_length >= length else 0

    def check_diag_down(r, c):
        seq_length = 1
        # check next tree sequential spots
        for offset in range(1, 4):
            # get value at next spot
            try:
                spot = board[r + offset][c + offset]
            # break if it is out of bounds
            except:
                break
            if spot == board[r][c]:
                seq_length += 1
            else:
                break
        return 1 if seq_length >= length else 0

    def check_diag_up(row, col):
        seq_length = 1
        # check next tree sequential spots
        for offset in range(1, 4):
            # get value at next spot
            try:
                spot = board[row - offset][col + offset]
            # break if it is out of bounds
            except:
                break
            if spot == board[row][col]:
                seq_length += 1
            else:
                break
        return 1 if seq_length >= length else 0

    total_sequences = 0
    for r in range(board.shape[0]):
        for c in range(board.shape[1]):
            if board[r][c] == player:
                total_sequences += check_vert(r, c)
                total_sequences += check_hor(r, c)
                total_sequences += check_diag_up(r, c)
                total_sequences += check_diag_down(r, c)
    return total_sequences


class AIPlayer:
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
        depth = 5
        valid_moves = get_successors(board, self.player_number)
        best_move = valid_moves[0][1]
        best_score = float('-inf')
        alpha = float('-inf')
        beta = float('inf')

        if self.player_number == 1:
            adv = 2
        else:
            adv = 1
        for successor, move in valid_moves:
            v = self.min_value(successor, depth - 1, alpha, beta, self.player_number, adv)
            print(v, move)
            if v > best_score:
                best_score = v
                best_move = move
        # print(f'best score: {best_score} best move: {best_move}')
        return best_move

    def min_value(self, board, depth, alpha, beta, agt, adv):
        valid_moves = get_successors(board, adv)
        if depth == 0 or len(valid_moves) == 0 or game_completed(board, 2) or game_completed(board, 2):
            return self.evaluation_function(board)
        cur_beta = beta
        v = float('inf')
        for successor, move in valid_moves:
            if alpha < cur_beta:
                v = self.max_value(successor, depth - 1, alpha, cur_beta, agt, adv)
            if v < cur_beta:
                cur_beta = v
        return cur_beta

    def max_value(self, board, depth, alpha, beta, agt, adv):
        valid_moves = get_successors(board, agt)
        if depth == 0 or len(valid_moves) == 0 or game_completed(board, 1) or game_completed(board, 2):
            return self.evaluation_function(board)
        cur_alpha = alpha
        v = float('-inf')
        for successor, move in valid_moves:
            if cur_alpha < beta:
                v = self.min_value(successor, depth - 1, cur_alpha, beta, agt, adv)
            if v > cur_alpha:
                cur_alpha = v
        return cur_alpha

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
        if self.player_number == 1:
            adv = 2
        else:
            adv = 1
        depth = 4
        valid_moves = get_successors(board, self.player_number)
        best_move = valid_moves[0][1]
        best_score = float('-inf')
        for successor, move in valid_moves:
            v = self.exp_value(successor, depth - 1, self.player_number, adv)
            print(v, move)
            if v > best_score:
                best_score = v
                best_move = move
        print(f'best score: {best_score} best move: {best_move}')
        return best_move

    def exp_max_value(self, board, depth, agt, adv):
        valid_moves = get_successors(board, agt)
        if depth == 0 or len(valid_moves) == 0 or game_completed(board, agt) or game_completed(board, adv):
            return self.evaluation_function(board)
        v = float('-inf')
        for successor, move in valid_moves:
            v = self.exp_value(successor, depth - 1, agt, adv)
        return v

    def exp_value(self, board, depth, agt, adv):
        valid_moves = get_successors(board, adv)
        if depth == 0 or len(valid_moves) == 0 or game_completed(board, agt) or game_completed(board, adv):
            return self.evaluation_function(board)
        v = 0
        for successor, move in valid_moves:
            v += self.exp_max_value(successor, depth - 1, agt, adv)
        v /= len(valid_moves)
        return v

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
        if self.player_number == 1:
            adv = 2
        else:
            adv = 1
        # (sequence size, sequence score multiplier)
        lengths = [(2, 1), (3, 10), (4, 100)]
        score = 0
        for length, multiplier in lengths:
            score += count_sequence(board, self.player_number, length) * multiplier
            score -= count_sequence(board, adv, length) * multiplier

        if count_sequence(board, adv, 4) > 0:
            return float('-inf')
        else:
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
