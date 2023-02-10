import numpy as np
import time

#We need to import time
"""We have to define a new Class called "Board_Bit to act our game board as a bitboard, as bitboard class is
famouse in solving boardgames with AI algorithms.
Defining the board_bit class to treat the connect four board as a 7x6 bitboard """
class board_bit:

    def __init__(self, player_number, board_matrix=None):
        """We have to define Player and Opponent piece as it is not defined in the
        main ConnectFour.py file"""
        #The player piece
        self.player = 0
        #The Opponent piece
        self.opponent = 0
        #Assigning the Player and Opponent number 1 and 2 as player numbers
        self.player_number = player_number
        self.opponent_number = 1 if player_number == 2 else 2

        if board_matrix is not None:
            player, opponent = '', ''
            for col in range(6, -1, -1):
                player += '0'
                opponent += '0'
                for row in range(0, 6):
                    player += '1' if board_matrix[row, col] == self.player_number else '0'
                    opponent += '1' if board_matrix[row, col] == self.opponent_number else '0'
            self.player = int(player, 2)
            self.opponent = int(opponent, 2)

    # Return array of non-full columns
    def valid_moves(self):
        mask = self.player | self.opponent
        moves = []
        for col in range(7):
            if (mask & (1 << ((col * 7) + 5))) == 0:
                moves.append(col)
        return moves

    def move(self, col, player_number):
        new = board_bit(self.player_number)
        mask = self.player | self.opponent
        mask |= mask + (1 << (col * 7))
        if player_number == self.player_number:
            new.player = self.opponent ^ mask
            new.opponent = self.opponent
        else:
            new.player = self.player
            new.opponent = self.player ^ mask
        return new

# for TERMINAL stage we need to define game_over function
    def game_over(self):
        """
        To have the TERMINAL stage:

        We need to check when the game is over.
        A game over can happen when:
        1- The game board is full
        2- We have 4 circles in a row

        """
        #  This is the bitstring value of Board when board is full, generating that giving a full matrix
        board_is_full = 279258638311359

        #  Check if board is full for any of the player turns
        if (self.player | self.opponent) == board_is_full:
            return 0

        #  Check for 4 in a row for both player and opponent
        for p, n in [(self.player, self.player_number), (self.opponent, self.opponent_number)]:
            # Check for horizontal win
            if self.connected_four(p, 7):
                return n
            # Check for diagonal win
            if self.connected_four(p, 6):
                return n
            # Check for diagonal win
            if self.connected_four(p, 8):
                return n
            # Check for vertical win
            if self.connected_four(p, 1):
                return n
        return 0

    def connected_four(self, p, shift_by):
        m = p & (p >> shift_by)
        # print(m)
        if m & (m >> (shift_by * 2)):
            return True
        return False


class AIPlayer:

    def __init__(self, player_number):
        self.player_number = player_number
        self.opponent_number = 1 if player_number == 2 else 2
        self.type = 'ai'
        self.player_string = 'Player {}:ai'.format(player_number)

    def get_alpha_beta_move(self, board):

        # Best depth_limit_alpha_beta is 7 as it takes average time and gives the best result
        depth_limit_alpha_beta = 7
        board = board_bit(self.player_number, board)
        print("Alpha-Beta depth limit is:", depth_limit_alpha_beta)
        print("Player", self.player_number, "is playing")
        print(board)

        # For the Max we have
        def maximizing(board, alpha, beta, current_depth):
            #Check if it is the TERMINAL stage or not
            if current_depth >= depth_limit_alpha_beta or board.game_over():
                return self.evaluation_function(board)
            # Using the float infinity as told in class
            value = -float("inf")
            for col in board.valid_moves():
                value = max(value, minimizing(board.move(col, self.player_number), alpha, beta, current_depth + 1))
                if value >= beta:
                    return value
                alpha = max(alpha, value)
            return value

        # For the Min we have
        def minimizing(board, alpha, beta, current_depth):
            # Check if it is the TERMINAL stage or not
            if current_depth >= depth_limit_alpha_beta or board.game_over():
                return self.evaluation_function(board)
            # Using the float infinity as told in class
            value = float("inf")
            for col in board.valid_moves():
                value = min(value, maximizing(board.move(col, self.opponent_number), alpha, beta, current_depth + 1))
                if value <= alpha:
                    return value
                beta = min(beta, value)
            return value

        start_time = time.time()

        best_score = -float("inf")
        next_alpha_beta_move = None
        for col in board.valid_moves():
            value = minimizing(board.move(col, self.player_number), best_score, float("inf"), 1)
            if value > best_score:
                best_score = value
                next_alpha_beta_move = col

        print ('⏰ Time for this move:', time.time() - start_time)
        return next_alpha_beta_move

    def get_expectimax_move(self, board):

        # Best and most efficient depth for expectimax is 5
        depth_limit_expectimax = 5
        board = board_bit(self.player_number, board)

        print("Expectimax depth limit is:", depth_limit_expectimax)
        print("Player", self.player_number, "is playing")
        print(board)

        def value(board, depth, agent):
            if depth >= depth_limit_expectimax or board.game_over():
                return self.evaluation_function(board)
            return max_value(board, depth + 1) if agent else exp_value(board, depth + 1)

        def max_value(board, depth):
            return max([value(board.move(col, self.player_number), depth, False) for col in board.valid_moves()])

        def exp_value(board, depth):
            return np.mean([value(board.move(col, self.opponent_number), depth, True) for col in board.valid_moves()])

        start_time = time.time()

        best_score = -np.inf
        next_expectimax_move = None
        for col in board.valid_moves():
            score = value(board.move(col, self.player_number), 1, False)
            if score > best_score:
                best_score = score
                next_expectimax_move = col

        print ('⏰ Time for this move:',time.time() - start_time)
        return next_expectimax_move


    """Making a List of all possibel gatherings of 4 connected circles in 
    vertical,left-right Diagonal and right-left Diagonal positions to claculated the possible points"""
    row, col = 6, 7
    connected_main = []
    a_differences = [1, 0, 1, -1]
    b_differences = [0, 1, 1, 1]
    a_ranges = [range(row - 3), range(col), range(col - 3), range(3, col)]
    b_ranges = [range(row), range(row - 3), range(row - 3), range(row - 3)]
    connected_main = []

    # As we have 4 connected circles, we check for each of the states
    for i in range(4):
        for col in a_ranges[i]:
            for row in b_ranges[i]:
                a = col
                b = row
                connected = []
                for _ in range(4):
                    connected.append(1 << ((a * 7) + 5 - b))
                    a += a_differences[i]
                    b += b_differences[i]
                connected_main.append(connected)

    def evaluation_function(self, board):
        Eval = 0
        """
        Let's assume player 1 and player 2 scores start form 0.
        At each stage we will check if the player 1 or player 2 having a score of 0.
        If we start from player 1 with a score of 0, then if the difference between it's score with player 2 is
        going to be 2, we will decrease the game evaluation output by 1. If the opposite happens, we will increase the evaluation output by 1.
    
        """

        for connected in self.connected_main:
            player_one = 0
            player_two = 0
            for i in connected:
                if board.player & i != 0:
                    player_one += 1
                elif board.opponent & i != 0:
                    player_two += 1

            if player_two == 0:
                if player_one == 2:
                    Eval += 1
                elif player_one == 3:
                    Eval += 3
                elif player_one == 4:
                    Eval += 7
            elif player_one == 0:
                if player_two == 2:
                    Eval -= 1
                elif player_two == 3:
                    Eval -= 3
                elif player_two == 4:
                    Eval -= 7

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

        return Eval


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
        np.random.seed()
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

