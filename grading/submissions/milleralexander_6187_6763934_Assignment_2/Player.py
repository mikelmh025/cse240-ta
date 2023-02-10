import numpy as np

class AIPlayer:
    def __init__(self, player_number):
        self.player_number = player_number
        self.type = 'ai'
        self.player_string = 'Player {}:ai'.format(player_number)

    def get_child_states(self, board, pnum):
        children = []
        for move in range(board.shape[1]):
            t_board = np.copy(board)
            if 0 in board[:,move]:
                update_row = -1
                for row in range(1, t_board.shape[0]):
                    update_row = -1
                    if t_board[row, move] > 0 and t_board[row-1, move] == 0:
                        update_row = row-1
                    elif row==t_board.shape[0]-1 and t_board[row, move] == 0:
                        update_row = row

                    if update_row >= 0:
                        t_board[update_row, move] = pnum
                        children += [(move, t_board)]
                        break
            else:
                err = 'Invalid move by player {}. Column {}'.format(player_num, move)
                raise Exception(err)

        return children

    def minimax(self, node, depth, maxDepth, alpha, beta, curTurn):
        if depth == 0:
            return self.evaluation_function(node)

        children = self.get_child_states(node, self.player_number - (1 - curTurn))
        print(children)

        if curTurn:
            best_move = []
            value = -np.inf
            for (col, child) in children:
                c = self.minimax(child, depth - 1, maxDepth, alpha, beta, 1 - curTurn)
                if value < c:
                    best_move = col
                    value = c
                if value > beta:
                    break
                alpha = max(alpha, value)
            if depth == maxDepth:
                print(best_move)
                return best_move
            else:
                return value
        else:
            value = np.inf
            for (col, child) in children:
                c = self.minimax(child, depth - 1, maxDepth, alpha, beta, 1 - curTurn)
                if value > c:
                    best_move = col
                    value = c
                if value < alpha:
                    break
                beta = min(beta, value)
            if depth == maxDepth:
                return best_move
            else:
                return value

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
        return self.minimax(board, 2, 2, -np.inf, np.inf, 1)

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
        raise NotImplementedError('Whoops I don\'t know what to do')

    def child_completed(self, child, player_num):
        player_win_str = '{0}{0}{0}{0}'.format(player_num)
        board = child
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

                for i in range(1, b.shape[1] - 3):
                    for offset in [i, -i]:
                        diag = np.diagonal(op_board, offset=offset)
                        diag = to_str(diag.astype(np.int))
                        if player_win_str in diag:
                            return True

            return False

        return (check_horizontal(board) or
                check_verticle(board) or
                check_diagonal(board))

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
        player_num = self.player_number

        if self.child_completed(board, player_num):
            return 1000000000

        to_str = lambda a: ''.join(a.astype(str))

        search_strs = dict()

        search_strs[(3, 1)] = ['{0}{1}{1}{1}'.format(0, player_num), '{1}{1}{1}{0}'.format(0, player_num),
                                 '{1}{0}{1}{1}'.format(0, player_num), '{1}{1}{0}{1}'.format(0, player_num)]
        search_strs[(2, 1)] = ['{0}{1}{1}'.format(0, player_num), '{1}{1}{0}'.format(0, player_num),
                                 '{1}{0}{1}'.format(0, player_num)]


        t_board = np.copy(board)

        seg_counts = dict()

        for l, num_open in [(3, 1), (2, 1)]:
            seg_counts[l] = 0
            for search_str in search_strs[(l, num_open)]:
                for x in range(t_board.shape[1] - len(search_str)):
                    for y in range(t_board.shape[0]):
                        cur_slice = np.s_[y, x:x + len(search_str)]


                        if search_str == to_str(t_board[cur_slice]):
                            seg_counts[l] += 1
                            t_board[cur_slice][np.where(t_board[cur_slice] == 0)] = 9

                # Vertical check:
                for x in range(t_board.shape[1]):
                    for y in range(t_board.shape[0] - len(search_str) + 1):
                        cur_slice = np.s_[t_board.shape[1] - (len(search_str) + y + 1):t_board.shape[1] - (y + 1),
                                    x]

                        if search_str == to_str(t_board[cur_slice]):
                            seg_counts[l] += 1
                            t_board[cur_slice][np.where(t_board[cur_slice] == 0)] = 9

                # Diag check down-right:
                for x in range(t_board.shape[1] - len(search_str)):
                    for y in range(t_board.shape[0] - len(search_str) + 1):
                        cx = [x + i for i in range(len(search_str))]
                        cy = [y + i for i in range(len(search_str))]
                        diag_idx = [(cx[i], cy[i]) for i in range(len(search_str))]

                        diag_match = True
                        for c, idx in enumerate(diag_idx):
                            if to_str(t_board[idx]) != search_str[c]:
                                diag_match = False
                                break

                        if diag_match:
                            seg_counts[l] += 1
                            for c, idx in enumerate(diag_idx):
                                if t_board[idx] == 0:
                                    t_board[idx] = 9

                # Diag check up-right:
                t_board = np.fliplr(t_board)
                for x in range(t_board.shape[1] - len(search_str)):
                    for y in range(t_board.shape[0] - len(search_str) + 1):
                        cx = [x + i for i in range(len(search_str))]
                        cy = [y + i for i in range(len(search_str))]
                        diag_idx = [(cx[i], cy[i]) for i in range(len(search_str))]

                        diag_match = True
                        for c, idx in enumerate(diag_idx):
                            if to_str(t_board[idx]) != search_str[c]:
                                diag_match = False
                                break

                        if diag_match:
                            seg_counts[l] += 1
                            for c, idx in enumerate(diag_idx):
                                if t_board[idx] == 0:
                                    t_board[idx] = 9

        return 20 * seg_counts[3] + 5 * seg_counts[2]

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

