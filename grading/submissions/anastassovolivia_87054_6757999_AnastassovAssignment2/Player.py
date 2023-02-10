import numpy as np
#python3 ConnectFour.py ai ai --time 3
#Respurces used:
#AI topics: Russell Stuart and Peter Norvig. 2010. Artificial Intelligence: A Modern Approach. 4th edition, 2020. and their github https://github.com/aimacode/aima-python/blob/master/games.py
class AIPlayer:
    def __init__(self, player_number):
        self.player_number = player_number
        self.type = 'ai'
        self.player_string = 'Player {}:ai'.format(player_number)

    def actions(self, board):
        free_cols = []
        for col in range(7):
            for row in range(5, -1, -1):
                if board[row][col] == 0:
                    free_cols.append([row, col])
                    break
        return free_cols

    def get_alpha_beta_move(self, board):
        scores = []
        tree = []
        def alpha_beta_pruning(board, alpha, beta, depth, player_1, player_2): 
            for row, col in self.actions(board):
                board[row][col] = player_1
                alpha = max(alpha, min_value(board, alpha, beta, depth + 1 , player_1, player_2))
                scores.append((alpha,col))
                board [row][col] = 0
            best_score = max(scores, key = lambda x: x[0])
            best_column = best_score[1]
            return best_column


        def max_value(board, alpha, beta, depth, player_1, player_2):
            actions = self.actions(board)
            if (depth == 5 or not actions):
                return (self.evaluation_function(board))
            for row, col in actions:
                tree.append((row, col))
                board[row][col] = player_1
                alpha = max(alpha, min_value(board, alpha, beta,depth + 1 , player_1, player_2))
                board[row][col] = 0
                if alpha >= beta:
                    return alpha
            performance = len(tree)
            print("tree = ", performance)
            return alpha


        def min_value(board, alpha, beta, depth, player_1, player_2):
            actions = self.actions(board)
            if (depth == 5 or not actions):
                return (self.evaluation_function(board))
            for row, col in actions:
                board[row][col] = player_2
                beta = min(beta, max_value(board, alpha, beta,depth + 1 , player_1, player_2))
                board[row][col] = 0
                if beta <= alpha:
                    return beta
            return beta

        player_1 = self.player_number
        if (player_1 == 1): 
            player_2 = 2
        else:
            player_2 = 1
        return(alpha_beta_pruning(board, -np.inf, np.inf, 0, player_1, player_2))
        
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
        raise NotImplementedError('Whoops I don\'t know what to do')

    def get_expectimax_move(self, board):
        scores = []
        def expectimax(board, depth, player_1, player_2): 
            alpha = -np.inf
            for row, col in self.actions(board):
                board[row][col] = player_1
                alpha = max(alpha, exp_value(board, depth - 1 , player_1, player_2))
                scores.append((alpha,col))
                board [row][col] = 0
            best_score = max(scores, key = lambda x: x[0])
            best_column = best_score[1]
            return best_column


        def max_value(board, depth, player_1, player_2):
            actions = self.actions(board)
            if (depth == 0 or not actions):
                return (self.evaluation_function(board))
            alpha = -np.inf
            for row, col in actions:
                board[row][col] = player_1
                alpha = max(alpha, exp_value(board, depth - 1 , player_1, player_2))
            return alpha

        def exp_value(board, depth, player_1, player_2):
            actions = self.actions(board)
            actions_length = len(actions)
            if (depth == 0 or not actions):
                return (self.evaluation_function(board))
            expected_value = 0
            for row, col in actions:
                board[row][col] = player_1
                v = max_value(board, depth - 1 , player_1, player_2)
                expected_value += v
            return (expected_value / actions_length)

        player_1 = self.player_number
        if (player_1 == 1): 
            player_2 = 2
        else:
            player_2 = 1
        return(expectimax(board, 5, player_1, player_2))
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

    def score(self, board, num, player_num):
        wins = 0
        player_win_str = '{0}' * num
        player_win_str = player_win_str.format(player_num)
        to_str = lambda a: ''.join(a.astype(str))

        def check_horizontal(b):
            count = 0
            for row in b:
                if player_win_str in to_str(row):
                    count += to_str(row).count(player_win_str)
            return count

        def check_verticle(b):
            return check_horizontal(b.T)

        def check_diagonal(b):
            count = 0
            for op in [None, np.fliplr]:
                op_board = op(b) if op else b
                
                root_diag = np.diagonal(op_board, offset=0).astype(np.int)
                if player_win_str in to_str(root_diag):
                    count += to_str(root_diag).count(player_win_str)

                for i in range(1, b.shape[1]-3):
                    for offset in [i, -i]:
                        diag = np.diagonal(op_board, offset=offset)
                        diag = to_str(diag.astype(np.int))
                        if player_win_str in diag:
                            count += diag.count(player_win_str)
            return count
        wins = check_horizontal(board) + check_verticle(board) + check_diagonal(board)
        return wins

    def evaluation_function(self, board):
        utility_value = 0
        player_1 = self.player_number
        if (player_1 == 1): 
            player_2 = 2
        else:
            player_2 = 1
        utility_value = self.score(board, 4, player_1) * 100
        utility_value += self.score(board, 3, player_1) * 50
        utility_value += self.score(board, 2, player_1) * 10
        utility_value -= self.score(board, 4, player_2) * 100
        utility_value -= self.score(board, 3, player_2) * 50
        utility_value -= self.score(board, 2, player_2) * 10
        return(utility_value)

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

