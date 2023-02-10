import numpy as np
"""
sources used for this assignment: 
    Jesh's section material
    Lecture 5, 6, and 7 slides
    https://www.geeksforgeeks.org/find-all-adjacent-elements-of-given-element-in-a-2d-array-or-matrix/
    https://www.youtube.com/watch?v=trKjYdBASyQ&ab_channel=TheCodingTrain
    https://www.youtube.com/watch?time_continue=3516&v=MMLtza3CZFM&embeds_euri=https%3A%2F%2Fwww.google.com%2Fsearch%3Fq%3Dexpectimax%2Bconnectfour%26rlz%3D1C5CHFA_enUS861US864%26ei%3Dw_3fY-qvIcm40PEPy5mOiA0%26ved%3D0ahUKEwiqnYSvif_8&feature=emb_logo&ab_channel=KeithGalli
    https://www.cs.rpi.edu/~xial/Teaching/2020SAI/slides/IntroAI_7.pdf
    https://www.geeksforgeeks.org/expectimax-algorithm-in-game-theory/
    https://www.youtube.com/watch?v=8392NJjj8s0&ab_channel=freeCodeCamp.org
"""

class AIPlayer:
    def __init__(self, player_number):
        self.player_number = player_number
        self.type = 'ai'
        self.player_string = 'Player {}:ai'.format(player_number)
    
    #function that returns all the valid moves based on the size of the connect four game board. 
    def getValidMoves(self, board):
        valid_moves = []
        for column in range(7):
            for row in range(6):
                if board[row][column] == 0:
                    valid_moves.append([row, column])
                    break
        return valid_moves

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
        
        """
        pseudocode given in class:

        alpha = MAX's best option on path to root 
        beta = MIN's best option on path to root

        def min-value(state, alpha, beta):
            initialize v to positive infinity
            for each successor of state:
                v = min(v, value(successor, alpha, beta))
                if v is less than or equal to alpha, return v
                beta = min(beta, v)
            return v

        def max-value(state, alpha, beta):
            initialize v to negative infinity
            for each successor of state:
                v = max(v, value(successor, alpha, beta))
                if v is greater than or equal to beta, return v
                alpha = max(alpha, v)
            return v
        """
        #uses the valid moves function and the board, depth, alpha, beta, and player1 and player2 to 
        #come up with the best place to put the coin
        def alpha_beta_search(self, board):
            v = []
            depth = 4
            alpha = -1000000
            beta = 1000000
            other = 1
            player = self.player_number
            if (player == 1):
                other = 2

            utility = self.getValidMoves(board)
            for row, col in utility:
                board[row][col] = player
                alpha = max(alpha, min_value(board, depth-1, alpha, beta, 
                            player, other))
                v.append((alpha, col))
                board[row][col] = 0

            value = max(v, key=lambda x: x[1])[0]
            for item in v:
                if value in item:
                    index = item[1]
                    break

            return (index)

        #function that finds the beta value and returns it
        def min_value(board, depth, alpha, beta, player, other):
            utility = self.getValidMoves(board)
            if (depth == 0 or not utility):
                return (self.evaluation_function(board))

            for row, col in utility:
                board[row][col] = other
                beta = min(beta, max_value(board, depth-1, alpha, beta, 
                                           player, other))
                board[row][col] = 0
                if beta <= alpha:
                     return (beta)

            return (beta)
                
        #function that fidns the alpha value and returns it 
        def max_value(board, depth, alpha, beta, player, other):
            utility = self.getValidMoves(board)
            if (depth == 0 or not utility):
                return (self.evaluation_function(board))

            for row, col in utility:
                board[row][col] = player
                beta = max(alpha, min_value(board, depth-1, alpha, beta, 
                                            player, other))
                board[row][col] = 0
                if alpha >= beta:
                     return (alpha)

            return (alpha)


        return (alpha_beta_search(self, board))
        #return 0
        #raise NotImplementedError('Whoops I don\'t know what to do')

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
        """ def maxValue(board, depth, player, opponent):
            valid_moves = self.valid_moves(board)
            if (depth == 0):
                return (self.evaluation_function(board))
        
        def expValue(board, ) """
            
        """
        pseudocode given in class:

        def values(s)
            if s is a max node return maxValue(s)
            if s is an exp node return expValue(s)
            if s is a terminal node return evalutaion(s)
        def maxValues(s)
            values = [value(s') for s' in successors]
            return maxValue
        def expValue(s)
            values value(s') for s' in successors(s)] 
            weights = [probability(s, s') for s' in successors(s)] 
            return expectation(values, weights)

        OTHER CODE FOR expValue(value)
        def exp-value(state):
            initialize v/value to 0 NOT INFINITY
            for each successor of state:
                p = probability(successor)
                v += p*value(successor)
            return v
        """
        #function that finds the best index to plave the coin
        #this funciton is similar to alpha_beta_search as it gives almost the same info. 
        # it also has all the same code as that function, just changed to fit expectimax.
        def expectimax_search(self, board):
            v = []
            depth = 8
            best = 0
            other = 1
            player = self.player_number
            if (player == 1):
                other = 2

            utility = self.getValidMoves(board)
            for row, col in utility:
                board[row][col] = player
                best = max(best, exp_value(board, depth-1, player, other))
                v.append((best, col))
                board[row][col] = 0
            # chooses the first available spot based on prob and score given to each possible move
            value = max(v, key=lambda x: x[1])[0]
            for item in v:
                if value in item:
                    index = item[1] 
                    break
            return (index)
            
        #followed the pseudocode given in class
        #also followed a youtube video that is linked at the top of this file
        def max_value(board, depth, player, other):
            utility = self.getValidMoves(board)
            if (depth == 0 or not utility):
                return (self.evaluation_function(board))

            v = -1000000
            for row, col in utility:
                board[row][col] = player
                v = max(v, exp_value(board, depth-1, player, other))

            return (v)

        #followed the pseudocode given in class
        #also followed a youtube video that is linked at the top of this file
        def exp_value(board, depth, player, other):
            utility = self.getValidMoves(board)
            if (depth == 0 or not utility):
                return (self.evaluation_function(board))
            v = 0
            m = len(utility)
            for row, col in utility:
                board[row][col] = other
                v += max_value(board, depth-1, player, other)
                

            return (v/m)

        return (expectimax_search(self, board))
        
        #raise NotImplementedError('Whoops I don\'t know what to do')



    #All this function does is call the evaluate function I have below
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
        utility = self.evaluate_value(board)
        return (utility)


    # reused ConnectFour.py::game_completed() code
    # I added the format for two in a row, three in a row, and four in a row.
    # I also added the score based on how many are in a row for vertical, horizontal, and diagonal. 
    def evaluate_value(self, board):
        two = '{0}{0}'.format(self.player_number)
        three = '{0}{0}{0}'.format(self.player_number)
        four = '{0}{0}{0}{0}'.format(self.player_number)
        to_str = lambda a: ''.join(a.astype(str))
        def check_horizontal(b):
            count = 0
            two_weightage = 10
            three_weightage = 20
            four_weightage = 100
            for row in b:
                if two in to_str(row):
                    count += two_weightage
                if three in to_str(row):
                    count += three_weightage
                if four in to_str(row):
                    count += four_weightage
            return (count)

        def check_verticle(b):
            return check_horizontal(b.T)

        def check_diagonal(b):
            count = 0
            two_weightage = 8
            three_weightage = 16
            four_weightage = 100
            for op in [None, np.fliplr]:
                op_board = op(b) if op else b

                root_diag = np.diagonal(op_board, offset=0).astype(np.int)
                if two in to_str(root_diag):
                    count += two_weightage
                if three in to_str(root_diag):
                    count += three_weightage
                if four in to_str(root_diag):
                    count += four_weightage

                for i in range(1, b.shape[1]-3):
                    for offset in [i, -i]:
                        diag = np.diagonal(op_board, offset=offset)
                        diag = to_str(diag.astype(np.int))
                        if two in to_str(root_diag):
                            count += two_weightage
                        if three in to_str(root_diag):
                            count += three_weightage
                        if four in to_str(root_diag):
                            count += four_weightage

            return (count)

        return (check_horizontal(board) + check_verticle(board) + check_diagonal(board))
        # same as connectfour.py, only difference is you want to return all the points, rather than one. 
        # in connect four it is or not +


        """check to see if the rows and columns have adjacent coins
            - check horizontally
            - check vertically
            - check diagonally

        += 1 for every diagonal
        subtract player 1 total and player 2 total
        then 

        who the current player is:
            so if player 1 is playing then player 1 - player 2
            so if player 1 is playing then player 2 - player 1
         
        depends on the player number:
            return negative number if player is doing bad  
            return 0 if players have same number of adjacent coins
            return positive if player is doing well
        """
    #heuristic to score each move in the function 
       
        return 0


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


