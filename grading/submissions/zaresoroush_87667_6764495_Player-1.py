import numpy as np

class AIPlayer:
    def __init__(self, player_number):
        self.player_number = player_number
        self.type = 'ai'
        self.player_string = 'Player {}:ai'.format(player_number)
        self.alpha = float('-inf')
        self.beta = float('inf')

    def __game_completed(self, board, player_num): # copied from the other file
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

    def set_alpha_beta(self, a, b): 
        # since we can't pass the alpha and beta from the parent node 
        # (the signature of the function is defined in the assignment and can't be changed)
        self.alpha = a
        self.beta = b

    def __get_other_player_number(self):
        return 3 ^ self.player_number

    def __get_playable_cols(self, board):
        valid_cols = []
        for col in range(board.shape[1]):
            if 0 in board[:,col]:
                valid_cols.append(col)

        return valid_cols

    def alpha_beta_mini(self, board, remaining_depth):
        if self.__game_completed(board, self.__get_other_player_number()):
            return (-100, None)
        if remaining_depth == 0:
            return (self.evaluation_function(board), None)

        v = (float('inf'), None)

        valid_cols = self.__get_playable_cols(board)

        if not valid_cols:
            return (self.evaluation_function(board), None)

        for col in valid_cols:
            result_board = np.copy(board)
            for j in reversed(range(board.shape[0])):
                if board[j][col] == 0:
                    result_board[j][col] = self.player_number
                    break
            ai_player = AIPlayer(self.__get_other_player_number())
            ai_player.set_alpha_beta(self.alpha, self.beta)
            candidate = ai_player.alpha_beta_maxi(result_board, remaining_depth - 1)[0]
            if candidate < v[0]:
                v = (candidate, col)
            if v[0] <= self.alpha:
                    return (v[0], col)
            self.beta = min(self.beta, v[0])
        return v

    def alpha_beta_maxi(self, board, remaining_depth):
        if self.__game_completed(board, self.__get_other_player_number()):
            return (-100, None)
        if remaining_depth == 0:
            return (self.evaluation_function(board), None)

        v = (float('-inf'), None)

        valid_cols = self.__get_playable_cols(board)

        if not valid_cols:
            return (self.evaluation_function(board), None)

        for col in valid_cols:
            result_board = np.copy(board)
            for j in reversed(range(board.shape[0])):
                if board[j][col] == 0:
                    result_board[j][col] = self.player_number
                    break
            ai_player = AIPlayer(self.__get_other_player_number())
            ai_player.set_alpha_beta(self.alpha, self.beta)
            candidate = ai_player.alpha_beta_mini(result_board, remaining_depth - 1)[0]
            if candidate > v[0]:
                v = (candidate, col)
            if v[0] >= self.beta:
                    return (v[0], col)
            self.alpha = max(self.alpha, v[0])
        return v

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

        return self.alpha_beta_maxi(board, 5)[1]


    def __get_expect(self, board, remaining_depth):
        if remaining_depth == 0:
            return self.evaluation_function(board)

        v = 0

        valid_cols = []
        for col in range(board.shape[1]):
            if 0 in board[:,col]:
                valid_cols.append(col)

        for col in valid_cols:
            result_board = np.copy(board)
            for j in reversed(range(board.shape[0])):
                if board[j][col] == 0:
                    result_board[j][col] = self.player_number
                    break
            ai_player = AIPlayer(self.__get_other_player_number())
            v += ai_player.__get_maxi(result_board, remaining_depth - 1)[0]
        return v/len(valid_cols)

    def __get_maxi_move(self, board, remaining_depth):
        return self.__get_maxi(board, remaining_depth)[1]


    def __get_maxi(self, board, remaining_depth):
        v = (float('-inf'), None)

        valid_cols = []
        for col in range(board.shape[1]):
            if 0 in board[:,col]:
                valid_cols.append(col)

        for col in valid_cols:
            result_board = np.copy(board)
            for j in reversed(range(board.shape[0])):
                if board[j][col] == 0:
                    result_board[j][col] = self.player_number
                    break
            ai_player = AIPlayer(self.__get_other_player_number())
            candidate = ai_player.__get_expect(result_board, remaining_depth - 1)
            if candidate > v[0]:
                v = (candidate, col)
        return v

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

        return self.__get_maxi_move(board, 5)

    def __shift(self, corner, dx, dy):
        return (int(corner[0] + dx), int(corner[1] + dy))

    def __is_inside_board(self, board, cell):
        if cell[0] < 0 or cell[1] < 0:
            return False
        if cell[0] >= board.shape[0]:
            return False
        if cell[1] >= board.shape[1]:
            return False
        return True


    def __count_expandable(self, board, corner, dx, dy, lim):
        corner = (int(corner[0]), int(corner[1]))
        if lim <= 0:
            return 0
        if self.__is_inside_board(board, corner) == False:
            return 0
        if board[corner[0]][corner[1]]:
            return 0

        return 1 + self.__count_expandable(board,
                                      self.__shift(corner, dx, dy),
                                      dx, dy, lim - 1)

    def __stretch(self, board, middle_point, direction):
        corner1 = middle_point
        corner2 = middle_point
        counter = 1
        while self.__is_inside_board(board, self.__shift(corner1, -direction[0], -direction[1])):
            cell = self.__shift(corner1, -direction[0], -direction[1])
            if board[cell[0]][cell[1]] != board[middle_point[0]][middle_point[1]]:
                break
            corner1 = cell
            counter += 1

        while self.__is_inside_board(board, self.__shift(corner2, direction[0], direction[1])):
            cell = self.__shift(corner2, direction[0], direction[1])
            if board[cell[0]][cell[1]] != board[middle_point[0]][middle_point[1]]:
                break
            corner2 = cell
            counter += 1

        return (corner1, corner2, counter)


    def __get_all_directions(self):
        dxs = [0,  0, 1, -1, 1, -1,  1, -1]
        dys = [1, -1, 0,  0, 1, -1, -1,  1]
        return zip(dxs, dys)

    def __is_expandable_to4(self, board, corner1, corner2):
        if corner1 == corner2:
            for direction in self.__get_all_directions():
                a = self.__count_expandable(board,
                                            self.__shift(corner1, -direction[0], -direction[1]),
                                            direction[0], direction[1], 3)
                b = self.__count_expandable(board, self.__shift(corner1, direction[0], direction[1]),
                                            direction[0], direction[1], 3 - a)
                if  a + b + 1 >= 4:
                    return True
            return False

        else:
            dx = corner2[0] - corner1[0]
            dy = corner2[1] - corner1[1]
            diffAbs = max(abs(dx), abs(dy))
            count_so_far = diffAbs + 1
            dx /= diffAbs;
            dy /= diffAbs;
            a = self.__count_expandable(board, self.__shift(corner1, -dx, -dy),
                                        dx, dy , 4 - count_so_far)
            b = self.__count_expandable(board, self.__shift(corner2, dx, dy),
                                        dx , dy, 4 - count_so_far - a)
            if a + b + count_so_far >= 4:
                return True
            return False



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

        # TODO: improve this 
        # (for example, take into account the evaluation of other player too!)
        evaluation = 0
        for x in range(board.shape[0]):
            for y in range(board.shape[1]):
                if board[x][y] == self.player_number:
                    for direction in self.__get_all_directions():
                        corner1, corner2, cell_counter = self.__stretch(board, (x, y), direction)
                        if self.__is_expandable_to4(board, corner1, corner2):
                            evaluation = max(evaluation, cell_counter)

        evaluation_other_player = 0
        for x in range(board.shape[0]):
            for y in range(board.shape[1]):
                if board[x][y] == self.__get_other_player_number():
                    for direction in self.__get_all_directions():
                        corner1, corner2, cell_counter = self.__stretch(board, (x, y), direction)
                        if self.__is_expandable_to4(board, corner1, corner2):
                            evaluation_other_player = max(evaluation, cell_counter)

        if self.__game_completed(board, self.player_number):
            return 100
        elif self.__game_completed(board, self.__get_other_player_number()):
            return -100

        return evaluation - evaluation_other_player


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

