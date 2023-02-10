import numpy as np
import math
import random

BLUE = (0,0,255)
BLACK = (0,0,0)
RED = (255,0,0)
YELLOW = (255,255,0)

class AIPlayer:
    def __init__(self, player_number):
        self.player_number = player_number
        self.type = 'ai'
        self.player_string = 'Player {}:ai'.format(player_number)
        self.r1, self.c1, self.r2, self.c2 = 0,0,0,0
        self.values = []

    def actions(self, board):
        action = []
        for column in range(7):
            for row in range(5, -1, -1):
                if board[row][column] == 0:
                    action.append([row, column])
                    break
        return action


    def game_over(self, board):

        ai_no = self.player_number
        opp_no = 2 if ai_no == 1 else 1
        
        for rows in board:
            rows = rows.tolist()
            for i in range(len(rows) - 3):
                if rows[i:i+4] == [ai_no, ai_no, ai_no, ai_no]:
                    return True
                if rows[i:i+4] == [opp_no, opp_no, opp_no, opp_no]:
                    return True
        for rows in board.T:
            rows = rows.tolist()
            for i in range(len(rows) - 3):
                if rows[i:i+4] == [ai_no, ai_no, ai_no, ai_no]:
                    return True
                if rows[i:i+4] == [opp_no, opp_no, opp_no, opp_no]:
                    return True
        
        return False

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

        if(not np.any(board)):
            return 3

        def minimax(board, depth, alpha, beta, max_player):
            # print(board)
            if depth == 0 or self.game_over(board):
                return self.evaluation_function(board)
            
            if max_player:
                maxE = -float('inf')
                for row, column in self.actions(board):
                    board[row][column] = 1
                    # print("max", board)
                    eva = minimax(board, depth - 1, alpha, beta, False)
                    if(eva > maxE):
                        maxE = eva
                        self.r1, self.c1 = row, column
                        self.values.append([maxE, column])
                    alpha = max(alpha, eva)
                    board[row][column] = 0
                    if beta <= alpha:
                        break
                return maxE
            else:
                minE = float('inf')
                for row, column in self.actions(board):
                    board[row][column] = 2
                    # print("min", board)
                    eva = minimax(board, depth - 1, alpha, beta, True)
                    if(eva < minE):
                        minE = eva
                        self.r2, self.c2 = row, column
                        self.values.append([minE, column])
                    beta = min(beta, eva)
                    board[row][column] = 0
                    if beta <= alpha:
                        break
                return minE
            
        if self.player_number == 1:
            minimax(board, 5, -float('inf'), float('inf'), True)
        else:
            minimax(board, 5, -float('inf'), float('inf'), False)
        
        # print(sorted(self.values, key = lambda x: x[0])[1][1])
        # return sorted(self.values, key = lambda x: x[0])[1][1]
        # return minimax(board, 3, -float('inf'), float('inf'), True)
        return min(self.values, key = lambda x: x[0])[1]
        return self.c1


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
        if(not np.any(board)):
            return 3

        def expecti(board, depth, alpha, beta, max_player):
            # print(board)
            if depth == 0 or self.game_over(board):
                return self.evaluation_function(board)
            
            if max_player:
                maxE = -float('inf')
                for row, column in self.actions(board):
                    board[row][column] = 1
                    # print("max", board)
                    eva = expecti(board, depth - 1, alpha, beta, False)
                    if(eva > maxE):
                        maxE = eva
                        self.r1, self.c1 = row, column
                        self.values.append([maxE, column])
                    
                    board[row][column] = 0
                    
                return maxE
            else:
                minE = 0
                for row, column in self.actions(board):
                    board[row][column] = 2
                    # print("min", board)
                    eva = expecti(board, depth - 1, alpha, beta, True)
                    minE += eva / 7
                        # minE = eva
                        # self.r2, self.c2 = row, column
                        # self.values.append([minE, column])
                    # beta = min(beta, eva)
                    board[row][column] = 0
                    # if beta <= alpha:
                        # break
                return minE
            
        if self.player_number == 1:
            expecti(board, 3, -float('inf'), float('inf'), True)
        else:
            expecti(board, 3, -float('inf'), float('inf'), False)
        
        # print(self.r1, self.c1, self.r2, self.c2)
        # print(self.values)

        # for i in range(len(self.values)):

        # print(sorted(self.values, key = lambda x: x[0])[1][1])
        return sorted(self.values, key = lambda x: x[0])[1][1]
        # return minimax(board, 3, -float('inf'), float('inf'), True)
        # return min(self.values, key = lambda x: x[0])[1]
        return self.c1




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
        ai_no = self.player_number
        opp_no = 2 if ai_no == 1 else 1

        # print(ai_no, opp_no)
        player_two = 0
        score = 0
        for rows in board:
            rows = rows.tolist()
            for i in range(len(rows) - 3):
                if rows[i:i+4] == [ai_no, ai_no, ai_no, ai_no]:
                    score += 3000
                if rows[i:i+4] == [opp_no, opp_no, opp_no, opp_no]:
                    score -= 3000
            # for i in range(len(rows) - 2):
                if rows[i:i+4] == [ai_no, ai_no, ai_no, 0]:
                    score += 850 
                if rows[i:i+4] == [opp_no, opp_no, opp_no, 0]:
                    score -= 900
            for i in range(len(rows) - 1):
                if rows[i] == ai_no and rows[i + 1] == ai_no:
                    score += 50
                # if rows[i] == opp_no and rows[i + 1] == opp_no:
                #     score -= 5
                

        for rows in board.T:
            rows = rows.tolist()
            for i in range(len(rows) - 3):
                if rows[i:i+4] == [ai_no, ai_no, ai_no, ai_no]:
                    score += 3000
                if rows[i:i+4] == [opp_no, opp_no, opp_no, opp_no]:
                    score -= 5000
            # for i in range(len(rows) - 2):
                if rows[i:i+4] == [ai_no, ai_no, ai_no, 0]:
                    score += 850 
                if rows[i:i+4] == [opp_no, opp_no, opp_no, 0]:
                    score -= 900
            for i in range(len(rows) - 1):
                if rows[i] == ai_no and rows[i + 1] == ai_no:
                    score += 50
                # if rows[i] == opp_no and rows[i + 1] == opp_no:
                #     score -= 5

        for row in range(3):
            for column in range(3, 7):
                if(board[row][column] == 
                board[row+1][column-1] == 
                board[row+2][column-2] == 
                board[row+3][column-3] == ai_no):
                    score += 3000
                if(board[row][column] == 
                board[row+1][column-1] == 
                board[row+2][column-2] == 
                board[row+3][column-3] == opp_no):
                    score -= 3000
        
        # for row in range(4):
            # for column in range(2, 7):
                if(board[row][column] == 
                board[row+1][column-1] == 
                board[row+2][column-2] == ai_no and
                board[row+3][column-3] == 0):
                    score += 850
                if(board[row][column] == 
                board[row+1][column-1] == 
                board[row+2][column-2] == opp_no and 
                board[row+3][column-3] == 0):
                    score -= 900
        # for row in range(5):
        #     for column in range(1, 7):
        #         if(board[row][column] == 
        #         board[row+1][column-1] == ai_no):
        #             score += 50
        #         if(board[row][column] == 
        #         board[row+1][column-1] == opp_no):
        #             score -= 5
        for row in range(3):
            for column in range(3, 7):
                if(board[row][column-3] == 
                board[row+1][column-2] == 
                board[row+2][column-1] == 
                board[row+3][column] == ai_no):
                    score += 3000
                if(board[row][column-3] == 
                board[row+1][column-2] == 
                board[row+2][column-1] == 
                board[row+3][column] == ai_no):
                    score -= 3000
                # for row in range(4):
            # for column in range(2, 7):
                if(board[row][column-3] == 
                board[row+1][column-2] == 
                board[row+2][column-1] == ai_no):
                    score += 850
                if(board[row][column-3] == 
                board[row+1][column-2] == 
                board[row+2][column-1] == opp_no):
                    score -= 900
                

        # print(score)
        return score




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

