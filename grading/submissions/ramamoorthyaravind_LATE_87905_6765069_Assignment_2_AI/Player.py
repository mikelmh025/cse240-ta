
import numpy as np
import math
import random



class AIPlayer:
    def __init__(self, player_number):
        self.player_number = player_number
        self.type = 'ai'
        self.player_string = 'Player {}:ai'.format(player_number)




    #Alpha-Beta Pruning
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
        
        row = 7
        column = 6
        dot_length = 4 #connect 4 or what do you think
        def is_valid_location(board, col):
            return board[row - 1][col] == 0

        def move_piece(board, row, col, piece):
            board[row][col] = piece

        def get_valid_locations(board):
            valid_locations = []
            for col in range(column):
                if is_valid_location(board, col):
                    valid_locations.append(col)
            return valid_locations

        def is_terminal_node(board):
            return winning_move(board, self.player_number) or winning_move(board, self.player_number) or len(get_valid_locations(board)) == 0

        def get_next_open_row(board, col):
            for r in range(row):
                if board[r][col] == 0:
                    return r

        def winning_move(board, piece):
            # Check horizontal locations for win
            for c in range(column - 3):
                for r in range(row):
                    if board[r][c] == piece and board[r][c + 1] == piece and board[r][c + 2] == piece and board[r][ c + 3] == piece:
                        return True

            # Check vertical locations for win
            for c in range(column):
                for r in range(row - 3):
                    if board[r][c] == piece and board[r + 1][c] == piece and board[r + 2][c] == piece and board[r + 3][c] == piece:
                        return True

            # Check positively sloped diaganols
            for c in range(column - 3):
                for r in range(row - 3):
                    if board[r][c] == piece and board[r + 1][c + 1] == piece and board[r + 2][c + 2] == piece and board[r + 3][c + 3] == piece:
                        return True

            # Check negatively sloped diaganols
            for c in range(column - 3):
                for r in range(3, row):
                    if board[r][c] == piece and board[r - 1][c + 1] == piece and board[r - 2][c + 2] == piece and board[r - 3][c + 3] == piece:
                        return True

        def scoreboard_fn(window, piece):
            # print(piece)
            score = 0
            opp_piece = self.player_number
            if piece == self.player_number:
                opp_piece = self.player_number

            if window.count(piece) == 4:
                score += 100
            elif window.count(piece) == 3 and window.count(0) == 1:
                score += 5
            elif window.count(piece) == 2 and window.count(0) == 2:
                score += 2

            if window.count(opp_piece) == 3 and window.count(0) == 1:
                score -= 4

            return score
        def scores_func(board, piece):
            score = 0

            ## Score center column
            center_array = [int(i) for i in list(board[:, column // 2])]
            center_count = center_array.count(piece)
            score += center_count * 3

            ## Score Horizontal
            for r in range(row):
                row_array = [int(i) for i in list(board[r, :])]
                for c in range(column - 3):
                    window = row_array[c:c + dot_length]
                    score += scoreboard_fn(window, piece)

            ## Score Vertical
            for c in range(column):
                col_array = [int(i) for i in list(board[:, c])]
                for r in range(row - 3):
                    window = col_array[r:r + dot_length]
                    score += scoreboard_fn(window, piece)

            ## Score posiive sloped diagonal
            for r in range(row - 3):
                for c in range(column - 3):
                    window = [board[r + i][c + i] for i in range(dot_length)]
                    score += scoreboard_fn(window, piece)

            for r in range(row - 3):
                for c in range(column - 3):
                    window = [board[r + 3 - i][c + i] for i in range(dot_length)]
                    score += scoreboard_fn(window, piece)

            return score


        def minmax(board, depth, alpha, beta, maximizingPlayer):
            valid_locations = get_valid_locations(board)
            is_terminal = is_terminal_node(board)
            if depth == 0 or is_terminal:
                if is_terminal:
                    if winning_move(board, self.player_number):
                        return (None, math.inf)
                    elif winning_move(board, self.player_number):
                        return (None, -math.inf)
                    else:  # Game is over, no more valid moves
                        return (None, 0)
                else:  # Depth is zero (base case duh ::))))) )
                    return (None, scores_func(board, self.player_number))
            if maximizingPlayer:
                value = -math.inf
                column = random.choice(valid_locations)
                for col in valid_locations:
                    row = get_next_open_row(board, col)
                    b_copy = board.copy()
                    move_piece(b_copy, row, col, self.player_number)
                    new_score = minmax(b_copy, depth - 1, alpha, beta, False)[1]

                    if new_score > value:
                        value = new_score
                        column = col
                    alpha = max(alpha, value)
                    if alpha >= beta:
                        break
                return column, value

            else:  # Minimizing player
                value = math.inf
                column = random.choice(valid_locations)
                for col in valid_locations:

                    row = get_next_open_row(board, col)
                    b_copy = board.copy()
                    move_piece(b_copy, row, col, self.player_number)
                    new_score = minmax(b_copy, depth - 1, alpha, beta, True)[1]

                    if new_score < value:
                        value = new_score
                        column = col
                    beta = min(beta, value)
                    if alpha >= beta:
                        break
                return column, value

        board = board.T
        col, value = minmax(board, row - 1, -math.inf, math.inf, True)
        if is_valid_location(board, col):

            row = get_next_open_row(board, col)




        return col




        raise NotImplementedError('Whoops I don\'t know what to do')






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
        return self.final_value_function(board, True, 0)[1]
        raise NotImplementedError('Whoops I don\'t know what to do')




    def evaluation_function(self, board, number):
        """t
        Given the current stat of the board, return the scalar value tha
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
       
        row_index = 5
        col_index = 0
        num_adjacent = 0
        max_adjacent = 0
        score = 0

        offsets = [(-1, -1), (-1, 0), (-1, 1), (0, 1)]
        for row_index in range(5, 0, -1):
            for col_index in range(6):  # also count ajacent opponent pieces
                if board[row_index][col_index] == number:
                    for offset in offsets:
                        num_adjacent = 1
                        # check for adjacent entries
                        x_offset = offset[0]  # try with all four different offset combinations
                        y_offset = offset[1]
                        while self.on_board(row_index, col_index, y_offset, x_offset) and (
                                board[row_index + y_offset][col_index + x_offset] == number or
                                board[row_index + y_offset][col_index + x_offset] == 0):
                            num_adjacent = num_adjacent + 1
                            x_offset = x_offset + offset[0]
                            y_offset = y_offset + offset[1]
                            max_adjacent = max(max_adjacent, num_adjacent)
                        score = score + max_adjacent ** 2
        # print("in eval!")
        # print(board)
        # print("evaluages to: "+str(score))
        return score  # max_adjacent

    def probability(self, board, action, actions):
        return int(1 / len(actions))

    def exp_value(self, board, layer):
        util_val = 0
        actions = self.actions(board)  # pass the other player's number
        for action in actions:
            p = self.probability(board, action, actions)
            # print(self.final_value_function(self.result(board, action, (self.player_number * 2) % 3), True, layer + 1))
            util_val = util_val + p * \
                       self.final_value_function(self.result(board, action, (self.player_number * 2) % 3), True, layer + 1)[
                           0]
        return util_val

    def max_value_expectimax(self, board, layer):
        util_val = -math.inf
        actions = self.actions(board)
        move = 2
        for action in actions:
            # print("max")
            # print(action)
            if self.final_value_function(self.result(board, action, self.player_number), False, layer + 1) > util_val:
                move = action[1]
            util_val = max(util_val,
                           self.final_value_function(self.result(board, action, self.player_number), False, layer + 1))
        return (util_val, move)

    def on_board(self, row_index, col_index, y_offset, x_offset):
        if row_index + y_offset < 0 or row_index + y_offset > 5:
            return False
        if col_index + x_offset < 0 or col_index + x_offset > 6:
            return False
        return True

    def result(self, board, action, number):
        hypo_board = np.zeros([6, 7]).astype(np.uint8)
        for row_index in range(len(board)):
            if row_index != action[0]:
                hypo_board[row_index] = board[row_index]
            else:
                new_row = []
                for col_index in range(len(board[0])):
                    if col_index != action[1]:
                        new_row.append(board[row_index][col_index])
                    else:
                        new_row.append(number)
                hypo_board[row_index] = new_row
        return hypo_board

    def actions(self, board):
        actions = []
        for col in range(len(board[0]) - 1, 0, -1):
            row = 5
            while board[row][col] != 0 and row > 0:
                row = row - 1
            if board[row][col] == 0:
                actions.append((row, col))
        return actions

    def end_test(self, board):

        row_index = 5
        col_index = 0
        num_adjacent = 0
        offsets = [(-1, -1), (0, -1), (1, -1), (1, 0)]
        for row_index in range(5, 0, -1):
            for col_index in range(6):
                if board[row_index][col_index] == self.player_number:
                    for offset in offsets:
                        num_adjacent = 1
                        # check for adjacent entries
                        x_offset = offset[0]
                        y_offset = offset[1]
                        while board[row_index + y_offset][col_index + x_offset] == self.player_number:
                            # print(num_adjacent)
                            num_adjacent = num_adjacent + 1
                            x_offset = x_offset + offset[0]
                            y_offset = y_offset + offset[1]
                            if not self.on_board(row_index, col_index, y_offset, x_offset):
                                break
                        if num_adjacent >= 4:
                            return True
        return False

    def final_value_function(self, board, isMax, layer):
        if self.end_test(board) or layer >= 5:
            if isMax:
                return (self.evaluation_function(board, self.player_number) - self.evaluation_function(board, (
                        self.player_number * 2) % 3), 2)
            else:
                return self.evaluation_function(board, self.player_number) - self.evaluation_function(board, (
                        self.player_number * 2) % 3)
        # Q: how to tell if the next agent is MAX or EXP??
        # if next agent is max:
        if isMax:
            return self.max_value_expectimax(board, layer)
        else:
            return self.exp_value(board, layer)


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

