import numpy as np
from operator import itemgetter

class AIPlayer:
    def __init__(self, player_number):
        self.player_number = player_number
        self.type = 'ai'
        self.player_string = 'Player {}:ai'.format(player_number)

 # To check all of the moves are valid between the AI and human player
    def validmove(self, board):
        moves = []
        for col in range(7):
            for row in range(5, -1, -1):
                if board[row][col] == 0:
                    moves.append([row, col])
                    break
        return moves
#To check all of the moves are valid between the AI and human player along with counting moves to ensure the player win game w connect 4
    def count_moves(self, board, num, player_num):
        #numberofwins = 0
        playerwin = '{0}' * num
        playerwin = playerwin.format(player_num)
        to_str = lambda a: ''.join(a.astype(str))

        def check_horizontal(b):
            count = 0
            for row in b:
                if playerwin in to_str(row):
                    count += to_str(row).count(playerwin)
            return count

        def check_verticle(b):
            return check_horizontal(b.T)

        def check_diagonal(b):
            count = 0
            for op in [None, np.fliplr]:
                op_board = op(b) if op else b
                root = np.diagonal(op_board, offset=0).astype(np.int)
                if playerwin in to_str(root ):
                    count += to_str(root).count(playerwin)

                for i in range(1, b.shape[1] - 3):
                    for offset in [i, -i]:
                        diag = np.diagonal(op_board, offset=offset)
                        diag = to_str(diag.astype(np.int))
                        if playerwin in diag:
                            count += diag.count(playerwin)
            return count

        variouswins = check_horizontal(board) + check_verticle(board) + check_diagonal(board)
        return variouswins


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
        values = []
#Implementation of Alpha beta algorithm 
        def alphabeta(board, depth, alpha, beta, player, enemy):
            for row, col in self.validmove(board):
                board[row][col] = player
                alpha = max(alpha, min_value(board, alpha, beta, depth + 1, player, enemy))
                values.append((alpha, col))
                board[row][col] = 0
            maxvalue = (max(values, key=itemgetter(1))[0])
            for item in values:
                if maxvalue in item:
                    max_indexs = item[1]
                    break

            return (max_indexs)

        def min_value(board, alpha, beta, depth, player, enemy):
            valid_moves = self.validmove(board)
            if (depth == 6 or not valid_moves):
                return (self.evaluation_value(board))
            for row, col in valid_moves:
                board[row][col] = enemy
                result = max_value(board, alpha, beta, depth + 1, player, enemy)
                beta = min(beta, result)
                board[row][col] = 0
                if beta <= alpha:
                    return beta
            return beta

        def max_value(board, alpha, beta, depth, player, enemy):
            valid_moves = self.validmove(board)
            if (depth == 6 or not valid_moves):
                return (self.evaluation_value(board))
            for row, col in valid_moves:
                board[row][col] = player
                result = min_value(board, alpha, beta, depth + 1, player, enemy)
                alpha = max(alpha, result)
                board[row][col] = 0
                if alpha >= beta:
                    return alpha
            return alpha

        player = self.player_number
        if (player == 1):
            enemy = 2
        else:
            enemy = 1
        return (alphabeta(board, 0, -100000, +100000, player, enemy))


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
        values = []
#Implementation of expectimax algorithm
        def expectimax(board, depth, player, enemy):
            alpha = - 1000000
            for row, col in self.validmove(board):
                board[row][col] = player
                alpha = max(alpha, expected_values(board, depth - 1, player, enemy))
                values.append((alpha, col))
                board[row][col] = 0

            maxvalue = (max(values, key=itemgetter(1))[0])
            for item in values:
                if maxvalue in item:
                    maxindex = item[1]
                    break

            return (maxindex)

        def max_val(board, depth, player, enemy):
            valid_moves = self.validmove(board)
            if (depth == 0 or not valid_moves):
                return (self.evaluation_value(board))
            bestValue = -100000
            for row, col in valid_moves:
                board[row][col] = player
                val = expected_values(board, depth - 1, player, enemy)
                bestValue = max(bestValue, val)
            return bestValue

        def expected_values(board, depth, player, enemy):
            valid_moves = self.validmove(board)
            lengthmoves = len(valid_moves)
            print(lengthmoves)
            if (depth == 0 or not valid_moves):
                return (self.evaluation_value(board))
            expectedValue = 0
            for row, col in valid_moves:
                board[row][col] = enemy
                val = max_val(board, depth - 1, player, enemy)
                expectedValue += val

            return (expectedValue / lengthmoves)

        player = self.player_number
        if (player == 1):
            enemy = 2
        else:
            enemy = 1
        return (expectimax(board, 8, player, enemy))

       # raise NotImplementedError('Whoops I don\'t know what to do')
    def evaluation_value(self, board):
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
        result_move = 0
        player = self.player_number
        if (player == 1):
            enemy = 2
        else:
            enemy = 1
        result_move = self.count_moves(board, 4, player) * 1000
        result_move += self.count_moves(board, 3, player) * 100
        result_move += self.count_moves(board, 2, player) * 10

        result_move -= self.count_moves(board, 4, enemy) * 950
        result_move -= self.count_moves(board, 3, enemy) * 100
        result_move -= self.count_moves(board, 2, enemy) * 10

        return (result_move)


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
