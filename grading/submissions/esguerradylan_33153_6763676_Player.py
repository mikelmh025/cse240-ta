import numpy as np
#taking files from Game
class AIPlayer:
    def __init__(self, player_number):
        self.player_number = player_number
        self.type = 'ai'
        self.player_string = 'Player {}:ai'.format(player_number)

#added function to check board for sequences of 1 or 2

    def valid_moves(self,board):
        valid_cols = []
        for col in range(board.shape[1]):
            if 0 in board[:,col]:
                valid_cols.append(col)
        return valid_cols

    def check_board(self,board,in_a_row):
        to_str = lambda a: ''.join(a.astype(str))

        def check_horizontal(b,in_a_row):
            count = 0
            for row in b:
                if in_a_row in to_str(row):
                    count = count + 1
            return count

        def check_verticle(b,in_a_row):
            return check_horizontal(b.T,in_a_row)

        def check_diagonal(b,in_a_row):
            count = 0
            for op in [None, np.fliplr]:
                op_board = op(b) if op else b

                root_diag = np.diagonal(op_board, offset=0).astype(np.int)
                if in_a_row in to_str(root_diag):
                    count = count + 1

                for i in range(1, b.shape[1]-3):
                    for offset in [i, -i]:
                        diag = np.diagonal(op_board, offset=offset)
                        diag = to_str(diag.astype(np.int))
                        if in_a_row in diag:
                            count = count + 1
            return count
        return (check_horizontal(board,in_a_row) +
                check_verticle(board,in_a_row) +
                check_diagonal(board,in_a_row))
    #checks if game over
    def game_over(self,board):
        my_win_str = '{1}{1}{1}{1}'
        op_win_str = '{2}{2}{2}{2}'
        if (self.check_board(board,my_win_str) > 0 or self.check_board(board,op_win_str) > 0):
            return True
        else:
            return False
    def change_board(self, board, move, player_num):
        new_board = board.copy()
        col = board[:,move]
        zeros = np.where(col == 0)[0]
        new_board[max(zeros), move] = player_num
        return new_board


    def get_alpha_beta_move(self,board,depth,isMax,alpha,beta): # i added depth
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
        #raise NotImplementedError('Whoops I don\'t know what to do')
        # first implenent with just minimax

        #print(isMax)
        #print(board)




        best_move = None

        valid_cols = self.valid_moves(board)

        #base case "if n is terminal"
        if (depth == 0 or self.game_over(board) or len(valid_cols)==0):
            return self.evaluation_function(board), best_move




        if isMax:
            player_num = self.player_number

            v = float("-inf")
            for move in valid_cols:

                new_board = self.change_board(board, move, player_num)
                [curr_v,curr_move] = self.get_alpha_beta_move(new_board,depth-1,False,alpha,beta)

                if curr_v > v:
                    v = curr_v
                    best_move = move
                alpha = max(alpha,v)
                if v >= beta:
                    return v, best_move
                    break
            return v, best_move


        else:
            player_num = 3 - self.player_number

            v = float("inf")
            for move in valid_cols:

                new_board = self.change_board(board, move, player_num) # last zero in that column = player_num
                [curr_v,cur_move] = self.get_alpha_beta_move(new_board,depth-1,True,alpha,beta)

                if curr_v < v:
                    v = curr_v
                    best_move = move
                beta = min(v,beta)
                if v <= alpha:
                    return v, best_move
                    break
            return v, best_move



#I have alpha and beta unused because needed when calling pfunc in ConnectFour
    def get_expectimax_move(self, board, depth, isMax,alpha,beta):
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
        #raise NotImplementedError('Whoops I don\'t know what to do')
        best_move = None

        valid_cols = self.valid_moves(board)



        if (depth == 0 or self.game_over(board) or len(valid_cols)==0):
            return self.evaluation_function(board), best_move



            #max
        if isMax: # max # is it always max at first
            player_num = self.player_number
            #opponent_num = 3 - player_num
            v = float("-inf")
            for move in valid_cols:
                new_board = self.change_board(board, move, player_num) # last zero in that column = player_num
                curr_v = self.get_expectimax_move(new_board,depth-1,False,alpha,beta)
                #v = max(curr_v,v)
                if curr_v > v:
                    v = curr_v
                    best_move = move
            return v, best_move

            #min
        else:
            player_num = 3 - self.player_number

            v = float("inf")
            values = np.zeros(len(valid_cols))
            moves = np.zeros(len(valid_cols))
            weights = np.ones(len(valid_cols))/len(valid_cols)
            i = -1
            for move in valid_cols: # will change to list of possible moves
                i = i + 1
                new_board = self.change_board(board, move, player_num) # last zero in that column = player_num
                [values[i],moves[i]] = self.get_alpha_beta_move(new_board,depth-1,True,alpha,beta)
                #v = min(curr_v,v)
            v = np.dot(np.transpose(values),weights)
            return v



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

        #using functions from Game to give inf weight to winning / losing moves
        #if isMax:
        #    player_num = self.player_number
        #    opponent_num = 3 - player_num
        #else:
        #    opponent_num = self.player_number
        #    player_num = 3 - opponent_num
        player_num = self.player_number
        opponent_num = 3 - player_num
        my_win_str = '{0}{0}{0}{0}'.format(player_num)
        my_lose_str = '{0}{0}{0}{0}'.format(opponent_num)
        my_three = '{0}{0}{0}'.format(player_num)
        op_three = '{0}{0}{0}'.format(opponent_num)
        my_two = '{0}{0}'.format(player_num)
        op_two = '{0}{0}'.format(opponent_num)
        my_one = '{0}'.format(player_num)
        op_one = '{0}'.format(opponent_num)
        values = np.zeros(6)
        weights = np.array([1,1,1,1,1,1])*(1/7)
        #if self.check_board(board,my_win_str):
            #values[0] =  500
        values[0] =  500*self.check_board(board,my_win_str)
        #if self.check_board(board,my_lose_str):
            #values[1] = -10000
        values[1] = -10000*self.check_board(board,my_lose_str)
        #if self.check_board(board,my_three):
            #values[2] = 100
        values[2] = 200*self.check_board(board,my_three)
        #if self.check_board(board,op_three):
            #values[3] = -100
        values[3] = -100*self.check_board(board,op_three)
        #if self.check_board(board,my_two):
            #values[4] = 50
        values[4] = 100*self.check_board(board,my_two)
        #if self.check_board(board,op_two):
            #values[5] = -50
        values[5] = -50*self.check_board(board,op_two)
        #if self.check_board(board,my_one):
            #values[4] = 20
        values[4] = 20*self.check_board(board,my_one)
        #if self.check_board(board,op_one):
            #values[5] = -20
        values[5] = -20*self.check_board(board,op_one)
        #else:
            #values[6] = 10
        return np.dot(np.transpose(values),weights)


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
