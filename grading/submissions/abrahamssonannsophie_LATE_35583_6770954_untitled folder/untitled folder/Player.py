import numpy as np
import copy
# import random # CHANGE

class AIPlayer:
    def __init__(self, player_number):
        self.player_number = player_number
        self.type = 'ai'
        self.player_string = 'Player {}:ai'.format(player_number)

    # def max_value(self, board, alpha, beta):
    #     v = float("-inf")
    #     valid_moves = self.get_valid_moves(board)


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
        alpha = float("-inf")
        beta = float("inf")

        # https://github.com/AbdallahReda/Connect4/blob/master/minimaxAlphaBeta.py

        # move = self.best_move(board)
        # # print("move: ", move)
        # return move

        score, child = self.alpha_beta_minimax(board, True, alpha, beta, 0)
        # self.evaluation_function(board)
        return child
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
        # self.evaluation_function(board)
        # print("HELLOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOO")
        # move = self.expValue(board)
        # print("move: ", move)
        score, move = self.value(board, True, 0)
        # move = self.best_move(board)
        return move
        # raise NotImplementedError('Whoops I don\'t know what to do')

    def maxValue(self, board, depth):
        v = -100000000000
        valid_moves = self.get_valid_moves(board)

        bestMove = np.random.choice(valid_moves)
        for succ in valid_moves:
                for row in range(0,6):
                    if row != 5:
                        if board[row][succ] == 0 and board[row+1][succ] != 0:
                            temp_board = copy.deepcopy(board)
                            temp_board[row][succ] = self.player_number

                            value, col = self.value(temp_board, False, depth+1)
                            # print("value: ", value)
                            # print("1stv", v)
                            if value > v:
                                # print("no")
                                bestMove = succ

                            # value = self.evaluation_function(temp_board)
                            # value, throws = self.value(temp_board, False, depth+1)
                            v = max(v, value)
                            # if bestMove < score:
                            #     bestChoice = succ
                            #     bestSeen = score
                    else:
                        if board[row][succ] == 0: # and board[row+1][col] != 0
                            temp_board = copy.deepcopy(board)
                            temp_board[row][succ] = self.player_number
                            # score = self.evaluation_function(temp_board)
                            # value = self.evaluation_function(temp_board)
                            value, col = self.value(temp_board, False, depth+1)
                            # print("value: ", value)
                            # print("2ndv", v)
                            if value > v:
                                # print("no")
                                bestMove = succ

                            # value, throws = self.value(temp_board, True, depth+1)
                            v = max(v, value)
        # print("MAX: v: ", v, "bestmove: ", bestMove)
        return v, bestMove

    def expValue(self, board, depth):
        opp_player = 1
        if self.player_number == 1:
            opp_player = 2
        else:
            opp_player = 1
        v = 0 
        valid_moves = self.get_valid_moves(board)
        probability = 1/3

        for succ in valid_moves:
            for row in range(0,6):
                    if row != 5:
                        if board[row][succ] == 0 and board[row+1][succ] != 0:
                            temp_board = copy.deepcopy(board)
                            temp_board[row][succ] = self.player_number

                            p = probability
                            # value = self.evaluation_function(temp_board)\
                            value, colum = self.value(temp_board, True, depth+1)
                            v += p*value
                            
                            
                            # if bestMove < score:
                            #     bestChoice = succ
                            #     bestSeen = score
                    else:
                        if board[row][succ] == 0: # and board[row+1][col] != 0
                            temp_board = copy.deepcopy(board)
                            temp_board[row][succ] = self.player_number
                            # score = self.evaluation_function(temp_board)
                            p = probability
                            # value = self.evaluation_function(temp_board)
                            value, colum = self.value(temp_board, True, depth+1)
                            v += p*value
        # print("min: v: ", v, "bestmove: ", succ)
        return v, succ

    def value(self, board, maxNode, depth):

        if self.check_if_will_win(board):
            return 10000000, None
        if self.check_if_opp_will_win(board):
            return -10000000, None
        if depth >= 3:
            # print(board)
            return self.evaluation_function(board), None

        if maxNode:
            v, succ = self.maxValue(board, depth) # temp board here
            # print("valmax: v: ", v, "bestmove: ", succ)
            return v, succ

        else:
            v, succ = self.expValue(board, depth)
            # v, succ = self.maxValue(board, depth) # temp board here
            # print("valmin: v: ", v, "bestmove: ", succ)
            return v, succ
    # def expValue(self, board, maxNode):

    #     v = 0 
    #     valid_moves = self.get_valid_moves(board)

    #     for succ in valid_moves:

        # v = 0
        # probability = 1/7
        # valid_moves = self.get_valid_moves(board)
        # bestMove = np.random.choice(valid_moves)

        # if self.check_if_will_win(board):
        #     return 10000000, None
        # if self.check_if_opp_will_win(board):
        #     return -10000000, None
        # if depth == 3:
        #     return self.evaluation_function(board), None
        # if maxNode:
        #     v = float("-inf")

        #     for succ in valid_moves:
        #         for row in range(0,6):
        #             if row != 5:
        #                 if board[row][succ] == 0 and board[row+1][succ] != 0:
        #                     temp_board = copy.deepcopy(board)
        #                     temp_board[row][succ] = self.player_number

        #                     value, col = self.expValue(temp_board, maxNode, depth+1, False)
        #                     v = max(v, value)
        #                     # score = self.evaluation_function(temp_board)
        #                     v += probability*score
        #                     bestMove = succ
        #                     if bestMove < score:
        #                         bestChoice = succ
        #                         bestSeen = score
        #             else:
        #                 if board[row][succ] == 0: # and board[row+1][col] != 0
        #                     temp_board = copy.deepcopy(board)
        #                     temp_board[row][succ] = self.player_number
        #                     # score = self.evaluation_function(temp_board)
        #                     v += probability*score
        #                     bestMove = succ
        # return bestMove
    # def value(s):

    def get_valid_moves(self, board):
        valid_moves = []
        for col in range(0,7):
            # print("printing what's at that space: ", board[0][col])
            if board[0][col] == 0:
                valid_moves.append(col)
        # print("in func: ", valid_moves)
        return valid_moves

    def alpha_beta_minimax(self, board, max_node, alpha, beta, depth):

        if self.check_if_will_win(board):
            # print("here")
            return 1000000, None
        if self.check_if_opp_will_win(board):
            return -1000000, None
        if depth == 4: # DO I NEED???????????????????????????????????????????
            # print("MAX: v: ", v, "bestmove: ", bestMove)
            # print("eval: ", self.evaluation_function(board))
            # print(board)
            return self.evaluation_function(board), None

        opp_player = 1
        if self.player_number == 1:
            opp_player = 2
        else:
            opp_player = 1

        valid_moves = self.get_valid_moves(board)

        if max_node:
            v = float("-inf")
            bestMove = np.random.choice(valid_moves)
            for child in valid_moves:
                for row in range(0,6):
                    if row != 5:
                        if board[row][child] == 0 and board[row+1][child] != 0:
                            temp_board = copy.deepcopy(board)
                            temp_board[row][child] = self.player_number
                            # print("temp: ", temp_board)
                            # score = self.evaluation_function(temp_board)
                            vcurr, throws = self.alpha_beta_minimax(temp_board, False, alpha, beta, depth+1)
                            # bestVal = max( bestVal, value) is the below equivalent
                            if v < vcurr:
                                v = vcurr
                                bestMove = child
                            alpha = max(alpha, v)
                            if beta <= alpha:
                                # print(temp_board)
                                # print("valmax: v: ", v, "bestmove: ", bestMove)
                                return v, bestMove
            
                    else:
                        if board[row][child] == 0: # and board[row+1][col] != 0
                            temp_board = copy.deepcopy(board)
                            temp_board[row][child] = self.player_number
                            # score = self.evaluation_function(temp_board)
                            vcurr, throws = self.alpha_beta_minimax(temp_board, False, alpha, beta, depth+1)
                            # bestVal = max( bestVal, value)  is the below equivalent
                            if v < vcurr:
                                v = vcurr
                                bestMove = child
                            alpha = max(alpha, v)
                            if beta <= alpha:
                                # print(temp_board)
                                # print("valmax: v: ", v, "bestmove: ", bestMove)
                                return v, bestMove
                #     if beta <= alpha:
                #         break
                # if beta <= alpha:
                    # break
            # print(temp_board)
            # print("MAX: v: ", v, "bestmove: ", bestMove)
            return v, bestMove

        else:
            v = float("inf")
            bestMove = np.random.choice(valid_moves)
            for child in valid_moves:
                for row in range(0,6):
                    if row != 5:
                        if board[row][child] == 0 and board[row+1][child] != 0:
                            temp_board = copy.deepcopy(board)
                            temp_board[row][child] = opp_player
                            # score = self.evaluation_function(temp_board)
                            vcurr,throws = self.alpha_beta_minimax(temp_board, True, alpha, beta, depth+1)
                            # bestVal = min( bestVal, value) is the below equivalent
                            if v > vcurr:
                                v = vcurr
                                bestMove = child
                            beta = min(beta, v)
                            if beta <= alpha:
                                # print(temp_board)
                                # print("valmin: v: ", v, "bestmove: ", bestMove)
                                return v, bestMove
            
                    else:
                        if board[row][child] == 0: # and board[row+1][col] != 0
                            temp_board = copy.deepcopy(board)
                            temp_board[row][child] = opp_player
                            # score = self.evaluation_function(temp_board)
                            vcurr, throws = self.alpha_beta_minimax(temp_board, True, alpha, beta, depth+1)
                            # bestVal = min( bestVal, value) is the below equivalent
                            if v < vcurr:
                                v = vcurr
                                bestMove = child
                            beta = min(beta, v)
                            if beta <= alpha:
                                # print(temp_board)
                                # print("valmin: v: ", v, "bestmove: ", bestMove)
                                return v, bestMove
                #     if beta <= alpha:
                #         break
                # if beta <= alpha:
                #     break
            # print(temp_board)
            # print("MIN: v: ", v, "bestmove: ", bestMove)
            return v, bestMove

           

    
    def check_if_opp_will_win(self, board):
        opp_player = 1
        if self.player_number == 1:
            opp_player = 2
        else:
            opp_player = 1

        #  HORIZONTAL
        for row in range(0,6):
            row_ind = []
            for s in board[row,:]:
                row_ind.append(s)
            
            for col in range(0,4):
                count = row_ind[col:col+4]
                
                # best move because it causes a win
                # print("here")
                if count.count(opp_player) == 4:
                    # print("no H")
                    # print("4!")
                    return True
        # VERTICAL
        for col in range(0,7):
            col_ind = []
            for s in board[:,col]:
                col_ind.append(s)
            # print("window: ", col_ind)
            for row in range(0,3):
                count = col_ind[row:row+4]
                # print("coutn window: ", count)
                if count.count(opp_player) == 4:
                    # print("4!")
                    # print("no V")
                    return True
        # print("end")
        # DIAGONAL
        for row in range(0,3):
            for col in range(0,4):
                count = []
                for offset in range(0,4):
                    count.append(board[row+offset][col+offset])
                if count.count(opp_player) == 4:
                    # print("4!")
                    # print("no D")
                    return True
        for row in range(0,3):
            for col in range(0,4):
                count = []
                for offset in range(0,4):
                    count.append(board[row-offset+3][col+offset])
                if count.count(opp_player) == 4:
                    # print("4!")
                    # print("no D")
                    return True

    def check_if_will_win(self, board):

        #  HORIZONTAL
        for row in range(0,6):
            row_ind = []
            for s in board[row,:]:
                row_ind.append(s)
            
            for col in range(0,4):
                count = row_ind[col:col+4]
                
                # best move because it causes a win
                # print("here")
                if count.count(self.player_number) == 4:
                    # print("4!")
                    # print("yay H")
                    return True
        # VERTICAL
        for col in range(0,7):
            col_ind = []
            for s in board[:,col]:
                col_ind.append(s)
            # print("window: ", col_ind)
            for row in range(0,3):
                count = col_ind[row:row+4]
                # print("coutn window: ", count)
                if count.count(self.player_number) == 4:
                    # print("4!")
                    # print("yay V")
                    return True
        # print("end")
        # DIAGONAL
        for row in range(0,3):
            for col in range(0,4):
                count = []
                for offset in range(0,4):
                    count.append(board[row+offset][col+offset])
                if count.count(self.player_number) == 4:
                    # print("4!")
                    # print("yay D")
                    return True
        for row in range(0,3):
            for col in range(0,4):
                count = []
                for offset in range(0,4):
                    count.append(board[row-offset+3][col+offset])
                if count.count(self.player_number) == 4:
                    # print("4!")
                    # print("yay D")
                    return True


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
        # https://www.youtube.com/watch?v=MMLtza3CZFM for below
        # row = 0
        # for i in range(0,6):
        #     for j in range(0,7):
        #         print(board[i][j], end = " ")

        #     print('\n')
        #     # row = row+1
        #     # for j in i:
        #     #     print(j, end= " ")
            
        # # Finding all horizontal
        # print("player: ", self.player_number)
        # print("board: ", board)
        # print("0,0: ", board[5][0])
        utilityValue = 0
        if self.player_number == 1:
            opp_player = 2
        else:
            opp_player = 1

        #  HORIZONTAL
        for row in range(0,6):
            row_ind = []
            for s in board[row,:]:
                row_ind.append(s)
            
            for col in range(0,4):
                count = row_ind[col:col+4]
                
                # best move because it causes a win
                # print("here")
                if count.count(self.player_number) == 4:
                    # print("4!")
                    utilityValue += 10000 # CHANGE
                elif count.count(self.player_number) == 3 and count.count(0) == 1:
                    # print("3!")
                    utilityValue += 100
                elif count.count(self.player_number) == 2 and count.count(0) == 2:
                    # print("2!")
                    utilityValue += 50
                if count.count(opp_player) == 3 and count.count(0) == 1:
                    utilityValue -= 500
        # VERTICAL
        for col in range(0,7):
            col_ind = []
            for s in board[:,col]:
                col_ind.append(s)
            # print("window: ", col_ind)
            for row in range(0,3):
                count = col_ind[row:row+4]
                # print("coutn window: ", count)
                if count.count(self.player_number) == 4:
                    # print("4!")
                    utilityValue += 10000 # CHANGE
                elif count.count(self.player_number) == 3 and count.count(0) == 1:
                    # print("3!")
                    utilityValue += 100
                elif count.count(self.player_number) == 2 and count.count(0) == 2:
                    # print("2!")
                    utilityValue += 50
                if count.count(opp_player) == 3 and count.count(0) == 1:
                    utilityValue -= 500
        # print("end")
        # DIAGONAL
        for row in range(0,3):
            for col in range(0,4):
                count = []
                for offset in range(0,4):
                    count.append(board[row+offset][col+offset])
                if count.count(self.player_number) == 4:
                    # print("4!")
                    utilityValue += 10000 # CHANGE
                elif count.count(self.player_number) == 3 and count.count(0) == 1:
                    # print("3!")
                    utilityValue += 100
                elif count.count(self.player_number) == 2 and count.count(0) == 2:
                    # print("2!")
                    utilityValue += 50
                if count.count(opp_player) == 3 and count.count(0) == 1:
                    utilityValue -= 500

        for row in range(0,3):
            for col in range(0,4):
                count = []
                for offset in range(0,4):
                    count.append(board[row-offset+3][col+offset])
                if count.count(self.player_number) == 4:
                    # print("4!")
                    utilityValue += 10000 # CHANGE
                elif count.count(self.player_number) == 3 and count.count(0) == 1:
                    # print("3!")
                    utilityValue += 100
                elif count.count(self.player_number) == 2 and count.count(0) == 2:
                    # print("2!")
                    utilityValue += 50
                if count.count(opp_player) == 3 and count.count(0) == 1:
                    utilityValue -= 500
        # for row in range(0,6):
        #     for col in range(0,7):
        #         if board[row][col] == 1:
        #             if self.player_number == 1:
        #                 utilityValue+=1
        #             else:
        #                 utilityValue-=1

        #         if board[row][col] == 2:
        #             if self.player_number == 2:
        #                 utilityValue+=1
        #             else:
        #                 utilityValue-=1

        # finding all vertical 
        # for row in range(0,6):
        #     for col in range(0,7):
        #         if board[col][row] == 1:
        #             if self.player_number == 1:
        #                 utilityValue+=1
        #             else:
        #                 utilityValue-=1

        #         if board[col][row] == 2:
        #             if self.player_number == 2:
        #                 utilityValue+=1
        #             else:
        #                 utilityValue-=1


        # for row in range(0,7):
        #     if board[0][row]

            # print(i)
            # while nextTile == 1:


        # if self.player_number == 1 and value>0:

        # else
        # print('util: ', utilityValue)
       
        return utilityValue


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