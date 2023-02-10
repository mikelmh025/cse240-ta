import numpy as np

class AIPlayer:
    def __init__(self, player_number):
        self.player_number = player_number
        self.type = 'ai'
        self.player_string = 'Player {}:ai'.format(player_number)

    def update_board(self, board, move, player_number):
        """
        """
        new_board = np.copy(board)
        for i in range(new_board.shape[0] - 1, -1, -1):
            if new_board[i][move] == 0:
                new_board[i][move] = player_number
                break
        return new_board

    # Copied from ConnectFour.py    
    def game_completed(self, board, player_num):
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

        def max_value(board, a, b, depth, max_depth, player_number):
            """
            Given the current state of the board, return the value
            and the next move to maximize utility.

            INPUTS:
            board - a numpy array containing the state of the board using the
                following encoding:
                - the board maintains its same two dimensions
                    - row 0 is the top of the board and so is
                      the last row filled
                - spaces that are unoccupied are marked as 0
                - spaces that are occupied by player 1 have a 1 in them
                - spaces that are occupied by player 2 have a 2 in them
            a - the value of alpha
            b - the value of beta
            depth - the recorded depth this call is within the tree
            max_depth - the max depth to explore before using the evaluation function
            player_number - the player number for this specific call

            RETURNS:
            A tuple in the format (value, move) where value is an int that indicates
            the utility of the move. move is an index representing one of the columns
            on the board.
            """
            opponent = 1 if player_number == 2 else 2
            v = float('-inf')
            move = 0
            for s in range(board.shape[1]):
                if board[0][s] == 0:
                    move = s
                    break
            for s in range(board.shape[1]):
                # check if the column is filled, if it is then not valid successor
                if board[0][s] != 0:
                    continue
                # if you have max depth, use eval function instead
                if depth == max_depth:
                    v = self.evaluation_function(board)
                else:
                    updated_board = self.update_board(board, s, player_number)
                    if self.game_completed(updated_board, player_number):
                        # print("found game completion on max:", move)
                        move = s
                        v = 100 # this should be the score for player game completion
                    m = min_value(updated_board, a, b, depth + 1, max_depth, opponent)
                    if v < m[0]:
                        v = m[0]
                        move = s

                if v >= b: 
                    return (v, move)
                a = max(a, v)
            return (v, move)

        def min_value(board, a, b, depth, max_depth, player_number):
            """
            Given the current state of the board, return the value
            and the next move to minimize utility.

            INPUTS:
            board - a numpy array containing the state of the board using the
                following encoding:
                - the board maintains its same two dimensions
                    - row 0 is the top of the board and so is
                      the last row filled
                - spaces that are unoccupied are marked as 0
                - spaces that are occupied by player 1 have a 1 in them
                - spaces that are occupied by player 2 have a 2 in them
            a - the value of alpha
            b - the value of beta
            depth - the recorded depth this call is within the tree
            max_depth - the max depth to explore before using the evaluation function
            player_number - the player number for this specific call

            RETURNS:
            A tuple in the format (value, move) where value is an int that indicates
            the utility of the move. move is an index representing one of the columns
            on the board.
            """
            opponent = 1 if player_number == 2 else 2
            v = float('inf')
            move = 0
            # default move to first valid successor
            for s in range(board.shape[1]):
                if board[0][s] == 0:
                    move = s
                    break
            for s in range(board.shape[1]):
                # check if the column is filled, if it is then not valid successor
                if board[0][s] != 0:
                    continue
                    # if you reach max depth, use eval function
                if depth == max_depth:
                    v = self.evaluation_function(board)
                else:
                    updated_board = self.update_board(board, s, player_number)
                    if self.game_completed(updated_board, player_number):
                        move = s
                        v = 0 # this should be the score for when the opponent gets game completion
                    m = max_value(updated_board, a, b, depth + 1, max_depth, opponent)
                    if v > m[0]:
                        v = m[0]
                        move = s
                if v <= a: 
                    return (v, move)
                b = min(b, v)
            return (v, move)
        
        alpha = float('-inf')
        beta = float('inf')
        # call max value on the board with alpha, beta, a max depth of 5, and the player number
        move = max_value(board, alpha, beta, 0, 5, self.player_number)
        return move[1]

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
        def get_avg_move(board, depth, max_depth, player_number):
            """
            Given the current state of the board, return the value
            and the next move to maximize utility.

            INPUTS:
            board - a numpy array containing the state of the board using the
                following encoding:
                - the board maintains its same two dimensions
                    - row 0 is the top of the board and so is
                      the last row filled
                - spaces that are unoccupied are marked as 0
                - spaces that are occupied by player 1 have a 1 in them
                - spaces that are occupied by player 2 have a 2 in them
            depth - the recorded depth this call is within the tree
            max_depth - the max depth to explore before using the evaluation function
            player_number - the player number for this specific call

            RETURNS:
            A tuple in the format (value, move) where value is an int that indicates
            the utility of the move. move is an index representing one of the columns
            on the board.
            """
            opponent = 1 if player_number == 2 else 2
            v = 0
            m = 0
            n_successors = 0
            # default move to first valid successor
            for s in range(board.shape[1]):
                if board[0][s] == 0:
                    n_successors += 1
                    m = s
            for s in range(board.shape[1]):
                # check if the column is filled, if it is then not valid successor
                if board[0][s] != 0:
                    continue

                # if you reach max depth, use eval function
                if depth == max_depth:
                    v += self.evaluation_function(board)
                # otherwise get the updated board, and check for game completion
                else:
                    updated_board = self.update_board(board, s, player_number)
                    m = get_avg_move(updated_board, depth + 1, max_depth, opponent)[1]
                    # if game completed, remember that move
                    if self.game_completed(updated_board, player_number):
                        m = s
                        v = 100 
                    else:
                        m = get_avg_move(updated_board, depth + 1, max_depth, opponent)[1]
            return (v / n_successors, m)
        
        moves = []
        n_successors = 0
        for s in range(board.shape[1]):
            if board[0][s] == 0:
                n_successors += 1
        opponent = 1 if self.player_number == 2 else 2
        for s in range(board.shape[1]):
            if board[0][s] != 0:
                continue

            updated_board = self.update_board(board, s, self.player_number)
            if self.game_completed(updated_board, self.player_number):
                m = s
                v = 100 # this should be the score for when the opponent gets game completion
                moves.append((v / n_successors, m))
            else:
                move = get_avg_move(updated_board, 0, 1, opponent) # call with a depth of 2
                moves.append(move)

        max_value_move = 0
        for index in range(len(moves)):
            if moves[index] > moves[max_value_move]:
                max_value_move = index

        return moves[index][1]
            





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

        def check_vertical(board, player_number):
            """
            Given the current state of the board and the player number, this function 
            will return a bool indicating whether there is a contiguous line of 3
            nodes that will allow a connect 4 for the current player
            """
            # go through each column and find the top most node within each column
            for i in range(board.shape[1] - 1, -1, -1): # loop through cols
                for j in range(board.shape[0] - 4, -1, -1): # loop through rows
                    if board[j][i] != player_number and board[j][i] != 0: # opponent node on top, therefore three not possible
                        break
                    if (board[j][i] == 0 and
                        board[j + 1][i] == player_number and  
                        board[j + 2][i] == player_number and
                        board[j + 3][i] == player_number):
                        return True
            return False

        def check_horizontal(board, player_number):
            """
            Given the current state of the board and the player number, this function
            will return a bool indicating whether there is a set of 3 horizontal nodes 
            that will allow the current player to get a connect 4
            """
            for i in range(board.shape[0]):
                for j in range(board.shape[1] - 4):
                    l = board[i][j: j + 4]
                    if np.count_nonzero(l == player_number) == 3 and np.count_nonzero(l == 0) == 1:
                        return True
            return False

        def check_diagonal(board, player_number):
            """
            """
            # checking forward diagonals
            for i in range(board.shape[1]):
                for j in range(board.shape[0] - 1, -1, -1):
                    l = np.fliplr(board[j: j + 4][i: i + 4]).diagonal()
                    if np.count_nonzero(l == player_number) == 3 and np.count_nonzero(l == 0) == 1:
                        return True
            # checking backward diagonals
            for i in range(board.shape[1] - 1, -1, -1):
                for j in range(board.shape[0] - 1, -1, -1):
                    l = np.array(board[j: j + 4][i: i + 4]).diagonal()
                    if np.count_nonzero(l == player_number) == 3 and np.count_nonzero(l == 0) == 1:
                        return True
            return False

        def check_connect_3(board, player_number):
            """
            """
            return (check_vertical(board, player_number) or
                    check_horizontal(board, player_number) or
                    check_diagonal(board, player_number))

        player_number = self.player_number
        opponent = 1 if player_number == 2 else 2

        eval = 1
        large = 10
        med = 2
        small = 1
        # if game completion for current player number, provide large reward
        if self.game_completed(board, player_number):
            eval += large
        # if 3 nodes that allow a connect 4 for current player, provide med reward
        if check_connect_3(board, player_number):
            eval += med
        # small reward for playing more towards the middle

        # no reward for making a move that allows the opponent to make a connect 4
        if self.game_completed(board, opponent):
            return 0
        return eval


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

