import numpy as np

class BoardWrapper:
    def __init__(self, board, is_leaf=False):
        self.board = board
        self.value = 0
        self.is_leaf = is_leaf

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
        search_tree = self.create_search_tree(board, limit=6)
        best_value = self.minimax(search_tree, True, float("-inf"), float("inf"))
        for child_board in search_tree.next:
            if child_board.value == best_value:
                return child_board.col
        return -1



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
        search_tree = self.create_search_tree(board, limit=6)
        best_value = self.expectimax(search_tree, True)
        for child_board in search_tree.next:
            if child_board.value == best_value:
                return child_board.col
        return -1



    def expectimax(self, board, is_max=True):
        """
        """

        if board.is_leaf:
            return board.value

        if is_max:
            value = float("-inf")
            for child_board in board.next:
                child_value = self.expectimax(child_board, False)
                value = max(value, child_value)
        else:
            value = 0
            num_children = len(board.next)
            for child_board in board.next:
                value += self.expectimax(child_board, True) / num_children
        board.value = value
        return value



    def minimax(self, board, is_max, alpha, beta):
        """
        """

        if board.is_leaf:
            return board.value

        if is_max:
            best_val = float("-inf")
            for child_board in board.next:
                value = self.minimax(child_board, False, alpha, beta)
                best_val = max(best_val, value)
                alpha = max(alpha, best_val)
                if beta <= alpha:
                    break
        else:
            best_val = float("inf")
            for child_board in board.next:
                value = self.minimax(child_board, True, alpha, beta)
                best_val = min(best_val, value)
                beta = min(beta, best_val)
                if beta <= alpha:
                    break
        board.value = best_val
        return best_val



    def create_search_tree(self, board, limit=4):
        """
        """

        root_board = BoardWrapper(np.copy(board), False)
        current_boards = [root_board]
        next_boards = []
        num = self.player_number
        for step in range(limit):
            while len(current_boards) > 0:
                cur_board = current_boards.pop()
                if cur_board.is_leaf:
                    continue
                cur_board.next = []
                for col in range(board.shape[1]):
                    if cur_board.board[0][col] != 0:
                        continue
                    next_board = self.get_next_board(cur_board, col, num)
                    board_value = self.evaluation_function(next_board.board)
                    # Evaluate the "leaf" boards
                    if step == limit - 1 or board_value == 4:
                        next_board.value = board_value
                        next_board.is_leaf = True
                    cur_board.next.append(next_board)
                    next_boards.append(next_board)
            current_boards = next_boards
            next_boards = []
            num = 2 if num == 1 else 1
        return root_board



    def get_next_board(self, board, col, num):
        """
        Get a copy of the board after inserting a dot in the given column.
        """

        next_board = BoardWrapper(np.copy(board.board))
        next_board.col = col
        for i in range(next_board.board.shape[0] - 1, -1, -1):
            if (next_board.board[i][col] == 0):
                next_board.board[i][col] = num
                break
        return next_board



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
        # Find the max sequence for other player
        cur_value = self.max_sequence(board, 2 if self.player_number == 1 else 1)
        value -= 2 * cur_value;
        # Find the max sequence for this player
        cur_value = self.max_sequence(board, self.player_number)
        value += cur_value;
        return value



    def max_sequence(self, board, player_number):
        """
        Find the maximum sequence of dots for the current player.
        """

        # Count from up to bottom in the following directions
        #   - Down
        #   - Left down diagonal
        #   - Right down diagonal
        #   - Left
        #   - Right

        max_seq = 0
        board_list = board.tolist()
        row = len(board_list)
        col = len(board_list[0])
        for i in range(row):
            for j in range(col):
                # Find sequences starting from (i,j)
                if board_list[i][j] == player_number:
                    # Go down
                    max_seq = max(max_seq, self.count_occ(board_list, i, j, 1, 0, row, col, player_number))
                    # Go left
                    max_seq = max(max_seq, self.count_occ(board_list, i, j, 0, -1, row, col, player_number))
                    # Go right
                    max_seq = max(max_seq, self.count_occ(board_list, i, j, 0, 1, row, col, player_number))
                    # Go left down
                    max_seq = max(max_seq, self.count_occ(board_list, i, j, 1, -1, row, col, player_number))
                    # Go right down
                    max_seq = max(max_seq, self.count_occ(board_list, i, j, 1, 1, row, col, player_number))
        return max_seq 



    def count_occ(self, board_list, i, j, ii, jj, row, col, num):
        seq = 0
        jump = False
        while (-1 < i and i < row and -1 < j and j < col):
            if (board_list[i][j] != num):
                break
            i += ii
            j += jj
            seq += 1
        i += ii
        j += jj
        # Check if this sequence is a potential 4
        pot_seq = seq
        while (pot_seq < 4):
            i += ii
            j += jj
            if (-1 < i and i < row and -1 < j and j < col and board_list[i][j] == 0):
                pot_seq += 1
            else:
                return 0
        return seq



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

