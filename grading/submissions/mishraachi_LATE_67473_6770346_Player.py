import numpy as np
depth = 0 # depth of tree

class AIPlayer:
    def __init__(self, player_number):
        self.player_number = player_number
        self.type = 'ai'
        self.player_string = 'Player {}:ai'.format(player_number)

    # calcs number of possible col wins
    def col_wins(self, board, col, p_num):
        # if empty col
        if not np.any(board[:, col]):
            num_col_wins = 3
        # if not empty col
        else:
            for i in range(len(board[:, col])):
                if board[:, col][i] != 0:
                    # print(board[:i+1, col])
                    # when the last token is player's
                    if board[:, col][i] == p_num:
                        if len(board[:i + 1, col]) >= 4:
                            num_col_wins = len(board[:i + 1, col]) - 3
                        else:
                            num_col_wins = 0
                    # when the last token is not player's
                    else:
                        if len(board[:i + 1, col]) - 1 >= 4:
                            num_col_wins = len(board[:i + 1, col]) - 1 - 3
                        else:
                            num_col_wins = 0
                    # print(num_col_wins)
                    break
        return num_col_wins

    # calcs number of possible row wins
    def row_wins(self, board, col, p_num):
        if not np.any(board[:, col]):
            row = board[5]
            # print(row)
        else:
            for i in range(len(board[:, col])):
                if board[:, col][i] != 0:
                    row = board[i - 1]
                    # print(row)
                    break
        temp_row = []
        for i in range(len(row)):
            # print(row[i])
            if row[i] == 0:
                temp_row.append(p_num)
            else:
                temp_row.append(row[i])
        # print(temp_row)
        in_row = 0
        store_in_row = []
        for i in temp_row:
            if i == p_num:
                in_row += 1
            else:
                store_in_row.append(in_row)
                in_row = 0
        store_in_row.append(in_row)
        # print(store_in_row)
        num_row_wins = 0
        for val in store_in_row:
            if val - 3 > 0:
                num_row_wins += val - 3
        # print(num_row_wins)
        return num_row_wins

    # calcs number of possible diag wins
    def diag_wins(self, board, col, p_num):
        if not np.any(board[:, col]):
            diag_row_start = 5
        else:
            for i in range(len(board[:, col])):
                if board[:, col][i] != 0:
                    diag_row_start = i - 1
                    break
        # print("Start: (", diag_row_start, ", ", col, ")")
        # print(board)
        # print(np.diag(board, k= col-diag_row_start))
        temp_diag = []
        for i in np.diag(board, k=col - diag_row_start):
            if i != 0:
                temp_diag.append(p_num)
            else:
                temp_diag.append(i)
        in_diag = 0
        store_in_diag = []
        for i in temp_diag:
            if i == p_num:
                in_diag += 1
            else:
                store_in_diag.append(in_diag)
                in_diag = 0
        store_in_diag.append(in_diag)
        # print(store_in_row)
        num_diag_wins = 0
        for val in store_in_diag:
            if val - 3 > 0:
                num_diag_wins += val - 3
        return num_diag_wins
    """
    def update_board(self, board, move, player_num):
        # print(self.board)
        temp_board = board
        if 0 in temp_board[:, move]:
            update_row = -1
            for row in range(1, temp_board.shape[0]):
                update_row = -1
                if temp_board[row, move] > 0 and temp_board[row - 1, move] == 0:
                    update_row = row - 1
                elif row == temp_board.shape[0] - 1 and temp_board[row, move] == 0:
                    update_row = row

                if update_row >= 0:
                    temp_board[update_row, move] = player_num
                    
        return temp_board
        """

    # gets max's best move
    def get_max(self, board):
        global depth
        alpha = -np.inf
        next_states = self.evaluation_function(board)
        for i in range(len(next_states)):
            if next_states[i] > alpha:
                alpha = next_states[i]
                choice = i
        if depth < 2:
            depth += 1
            return self.get_min(board)
        else:
            depth = 0
            return choice

    # gets min's best move
    def get_min(self, board):
        global depth
        beta = np.inf
        next_states = self.evaluation_function(board)
        for i in range(len(next_states)):
            if next_states[i] < beta:
                beta = next_states[i]
                choice = i
        if depth <2 :
            depth += 1
            return self.get_max(board)
        else:
            flag = 0
            return choice

    # for expectimax random portion
    def get_min_expect(self, board):
        choice = np.random.randint(7) #https://www.javatpoint.com/numpy-random
        if depth <2 :
            depth += 1
            return self.get_max(board)
        else:
            flag = 0
            return choice

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

        if (np.count_nonzero(board == 1) <= np.count_nonzero(board == 2)):
            choice = self.get_max(board)
        else:
            choice = self.get_min(board)

        return choice

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
        if (np.count_nonzero(board == 1) <= np.count_nonzero(board == 2)):
            choice = self.get_max(board)
        else:
            choice = self.get_min_expect(board)

        # raise NotImplementedError('Whoops I don\'t know what to do')
        return choice

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
        evals = [] # array of values for next states

        for i in range(7):
            evals.append(2*self.col_wins(board, i, 1) + 2*self.row_wins(board, i, 1) + self.diag_wins(board, i, 1) - (
                            2*self.col_wins(board, i, 2) + 2*self.row_wins(board, i, 2) + self.diag_wins(board, i, 2)))
        if not np.any(board[:, 3]):
            evals[3] = evals[3]+100
        print(evals)

        return evals


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
