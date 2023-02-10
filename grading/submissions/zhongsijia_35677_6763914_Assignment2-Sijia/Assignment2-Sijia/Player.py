# Sijia Zhong - szhong16@ucsc.edu - 1690286
import numpy as np

# I discussed some of the ideas with my friend Yanwen Xu - yxu149@ucsc.edu
# there is no code being share

# Example idea and code comes from:
# https://cis.temple.edu/~pwang/5603-AI/Project/2021S/Sawwan/AI%20Project.pdf
# https://www.geeksforgeeks.org/minimax-algorithm-in-game-theory-set-4-alpha-beta-pruning/
# Also from class and other source will be cited at the place it is being used
# since it is too expensive to explore the entire game tree
# we make a depth-limited search
max_depth = 7
# got the number from ConnectFour
num_of_rows = 6
num_of_columns = 7

class AIPlayer:
    def __init__(self, player_number):
        self.player_number = player_number
        self.type = 'ai'
        self.player_string = 'Player {}:ai'.format(player_number)

    def check_if_unoccupied(self, board):
        moves = []
        for column in range(0, num_of_columns):
            for row in range(0, num_of_rows):
                # if unoccupied, we can go there next
                if board[row][column] == 0:
                    moves.append([row, column])
                    break
        # print(moves)
        return moves

    # for getting who is the opponent player
    def check_player(self, player1):
        if player1 == 1: 
            player2 = 2
        else: 
            player2 = 1
        return player2

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

        # Alpha: MAX's best option on path to root
        # Beta: MIN's best option on path to root
        alpha = float("-inf")
        beta = float("inf")
        # depth = max_depth
        depth = 0
        player1 = self.player_number
        player2 = self.check_player(player1)

        # I don't want to change the original board
        # I copy a new one
        board_copy = board.copy()
        
        # save the possible moves for this level
        moves = []
        # print("player1 = " + str(player1) + "player2 = " + str(player2))

        all_moves = self.check_if_unoccupied(board_copy)
        for row, column in all_moves:
            # we are in the max level and want the best for main player
            board_copy[row][column] = player1
            depth = depth + 1
            alpha = max(alpha, self.alpha_beta_min_value(alpha, beta, depth, player1, player2, board_copy))
            # if we find a possible move, we add it to the list
            # we don't need the row, since at the end we only care about the best value
            moves.append([alpha, column])
            # reset the place back to empty because we have not decide which one to put
            board_copy[row][column] = 0

        # we find the best alpha of all
        best = max(moves, key=lambda x: x[0])
        # print(moves)
        # print("alpha_beta: [score, column] = " + str(best))
        # return the column that we want to choose
        return best[1]

    # def max_value(state, alpha. beta):
    #     initialize v = -inf
    #     for each successor of state:
    #         v = max(v, value(successor, alpha, beta))
    #         if v >= beta:
    #             return v
    #         alpha = max(alpha, v)
    #     return v
    # in the alpha_beta_max_value, we choose the best option for the player1
    # which is the main player
    # since we are in the MAX layer
    def alpha_beta_max_value(self, alpha, beta, depth, player1, player2, board):

        max_v = float("-inf")

        # print("max_v = " + str(max_v))
        # board_copy = board.copy()

        all_moves = self.check_if_unoccupied(board)
        # print("all_moves = " + str(all_moves))
        # if we reach the largest depth we can go or there is no moves
        if depth >= max_depth or not all_moves:
            return self.evaluation_function(board)

        for row, column in all_moves:
            # we want the max value for the main player
            board[row][column] = player1
            depth = depth + 1
            min_val = self.alpha_beta_min_value(alpha, beta, depth, player1, player2, board)
            # print("min_val = " + str(min_val))
            max_v = max(max_v, min_val)
            if max_v >= beta:
                return max_v
            alpha = max(alpha, max_v)
            board[row][column] = 0
            # print("alpha = " + str(alpha))

        return max_v

    # def min_value(state, alpha. beta):
    #     initialize v = inf
    #     for each successor of state:
    #         v = min(v, value(successor, alpha, beta))
    #         if v <= alpha:
    #             return v
    #         beta = min(beta, v)
    #     return v
    # in the alpha_beta_min_value, we choose the best option for the player2
    # which is the opponent player
    # since we are in the MIN layer
    def alpha_beta_min_value(self, alpha, beta, depth, player1, player2, board):

        min_v = float("inf")

        all_moves = self.check_if_unoccupied(board)
        # if we reach the largest depth or there is no moves
        if depth >= max_depth or not all_moves:
            return self.evaluation_function(board)

        for row, column in all_moves:
            # now we want to best for opponent
            board[row][column] = player2
            depth = depth + 1
            max_val = self.alpha_beta_max_value(alpha, beta, depth, player1, player2, board)
            min_v = min(min_v, max_val)
            if min_v <= alpha:
                return min_v
            beta = min(beta, min_v)
            board[row][column] = 0

        return min_v

        # raise NotImplementedError('Whoops I don\'t know what to do')

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

        alpha = float("-inf")
        depth = 0

        player1 = self.player_number
        player2 = self.check_player(player1)

        moves = []

        board_copy = board.copy()

        # def value(s):
        #     if s is a max node return maxValue(s)
        #     if s is an exp node return expValue(s)
        #     if s is a terminal node return evaluation(s)
        # the same code with alpha_beta
        all_moves = self.check_if_unoccupied(board_copy)
        for row, column in all_moves:
            # we are in the max level and want the best for main player
            board_copy[row][column] = player1
            depth = depth + 1
            alpha = max(alpha, self.max_value(depth, player1, player2, board_copy))
            # if we find a nice alpha, we add it to the list
            moves.append([alpha, column])
            # reset the place back to empty because we have not decide which one to put
            board_copy[row][column] = 0

        # we find the best of all
        best = max(moves, key=lambda x: x[0])
        # print(moves)
        # print("expectimax: [score, column] = " + str(best))
        # since we cannot decide the row, we just return the column
        return best[1]

    # def maxValue(s):
    #     values = [value(s') for s' in successors(s)]
    #     return max(values)
    def max_value(self, depth, player1, player2, board):
        max_v = float("-inf")

        all_moves = self.check_if_unoccupied(board)
        # if we reach the largest depth or there is no moves
        if depth >= max_depth or not all_moves:
            return self.evaluation_function(board)

        for row, column in all_moves:
            # we want the max value for the main player
            board[row][column] = player1
            depth = depth + 1
            min_val = self.exp_value(depth, player1, player2, board)
            max_v = max(max_v, min_val)
            board[row][column] = 0

        return max_v

    # def expValue(s):
    #     values = [value(s') for s' inn successors(s)]
    #     weights = [probability(s, s') for s' in successors(s)]
    #     return expectation(values, weights)
    # def exp_value(state):
    #     v = 0
    #     for successor in state:
    #         p = probability(successor)
    #         v += p * value(successor)
    #     return v
    def exp_value(self, depth, player1, player2, board):
        v = 0

        all_moves = self.check_if_unoccupied(board)

        # if we reach the largest depth or there is no moves
        if depth >= max_depth or not all_moves:
            return self.evaluation_function(board)

        # the probability p = 1 / num_of_successors
        p = 1 / len(all_moves)

        for row, column in all_moves:
            # now we want to best for opponent
            board[row][column] = player2
            depth = depth + 1
            max_val = self.max_value(depth, player1, player2, board)
            v += max_val * p
            board[row][column] = 0

        return v

        # return value(alpha, max_depth, player1, player2, board)

        # raise NotImplementedError('Whoops I don\'t know what to do')

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

        player1 = self.player_number
        player2 = self.check_player(player1)

        final_score = 0

        # checking idea from:
        # https://github.com/KeithGalli/Connect4-Python
        # https://github.com/zakuraevs/connect4-ai/tree/a7e2e52745d68ae100d81293daabe422c710f01a
        # from youtube video: https://www.youtube.com/watch?v=MMLtza3CZFM

        def evaluate_window(window, player1, player2):

            score = 0

            # 如果之前+5200被运行了，说明我们已经有一个可以走的点了，所以我们就不专注于堵
            # 但是如果+5200没有被运行，优先堵对方
            # is_connect4 = False

            # 有tradeoff，如果想要避免做错误选择，就要提高减去的数字
            # 但是减太多会导致一直在补负数，反而导致无法找到optimal的做法
            # tradeoff, if we want to avoid doing the wrong choice, we need to increase the punishment
            # but if the punishment is big, the score will keep decrease
            # lead to not able to find the optimal 

            # 表明此处有赢的可能，优先选择赢的那步
            # 爷要赢
            # put there will make player1 win, so we add a large score
            if window.count(player1) == 4:
                score += 52000
                # is_connect4 == True
            # almost there, give higher score to make it go here
            # 如果下这步就还差一步完成，也给比较好的数值，证明这一步是好文明
            elif window.count(player1) == 3 and window.count(0) == 1:
                score += 500
            # 如果下这步就有两个连在一起，还不错，给一点点鼓励
            # if place here, there are 2 connects, good but not good enough
            elif window.count(player1) == 2 and window.count(0) == 2:
                score += 200
            elif window.count(player1) == 1 and window.count(0) == 3:
                score += 50

            # here is a bit bad since opponent will have 3 connects
            # don't go here
            # 下这里有点危险，等于给对方比较大的机会，所以尽量别下
            if window.count(player2) == 3 and window.count(0) == 1:
                score -= 666
            # 这里还行，对方有两个连在一起，情况并不危机
            # okay, just 2 connects, still have chance
            elif window.count(player2) == 2 and window.count(0) == 2:
                score -= 300
            # 下这里就马上寄，狗都不下
            # got lose right way, NO!!!
            # but don't let the score to be larger than the +5200 or it will make the wrong
            elif window.count(player2) == 4:
                score -= 1000
            elif window.count(player2) == 1 and window.count(0) == 3:
                score -= 60

            return score

            # print("not implemented yet")

        # check_horizontal
        for r in range(num_of_rows):
            row_array = [int(i) for i in list(board[r, :])]
            for c in range(num_of_columns - 3):
                window = row_array[c:c + 4]
                final_score += evaluate_window(window, player1, player2)

        # check_vertical
        for c in range(num_of_columns):
            col_array = [int(i) for i in list(board[:, c])]
            for r in range(num_of_rows - 3):
                window = col_array[r:r + 4]
                final_score += evaluate_window(window, player1, player2)

        # check_positive_diagonals
        for r in range(num_of_rows - 3):
            for c in range(num_of_columns - 3):
                window = [board[r + i][c + i] for i in range(4)]
                final_score += evaluate_window(window, player1, player2)

        # check_negative_diagonals
        for r in range(num_of_rows - 3):
            for c in range(num_of_columns - 3):
                window = [board[r + 3 - i][c - i] for i in range(4)]
                final_score += evaluate_window(window, player1, player2)

        return final_score
        # return 0


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
