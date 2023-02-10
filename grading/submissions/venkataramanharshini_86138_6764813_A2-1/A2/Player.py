import numpy as np
import random
import copy


#Name: Harshini Venkataraman
#SID: 2005385


#Reference Material: https://www.youtube.com/watch?v=MMLtza3CZFM&t=3321s
#https://medium.com/analytics-vidhya/artificial-intelligence-at-play-connect-four-minimax-algorithm-explained-3b5fc32e4a4f



# ROW_COUNT = 6
# COLUMN_COUNT = 7
# DEPTH = 6
# EMPTY = 0
MAX_SCORE = 10000
MIN_SCORE = -1000




class AIPlayer:
    def __init__(self, player_number):
        self.player_number = player_number
        self.opponent_number = 2 if self.player_number== 1 else 1
        self.type = 'ai'
        self.player_string = 'Player {}:ai'.format(player_number)


#Takes in all the places the coin can be placed in each column
    def available_slots(self, board):
        available = []
        for col in range(board.shape[1]):
            if 0 in board[:,col]:
                available.append(col)
        return available



#Referrence - https://www.youtube.com/watch?v=MMLtza3CZFM&t=958s

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

        print("Inside Alpha Beta")


        def minimax(board, curr_depth, max_depth, alpha, beta, maximizingPlayer):
            available_cols = self.available_slots(board)
            if not available_cols:
                return None, 0

            if curr_depth == max_depth:
                return None, self.evaluation_function(board)

            if maximizingPlayer:
                max_value = float('-inf')
                selected_column = random.choice(available_cols)
                for col in available_cols:
                    row = board.shape[0]-1
                    while board[row, col] != 0:
                        row -= 1

                    copy_boardstate = copy.deepcopy(board)
                    copy_boardstate[row, col] = self.player_number
                    score = minimax(copy_boardstate, curr_depth+1, max_depth, alpha, beta, False)[-1]
                    if score > max_value:
                        max_value = score
                        selected_column = col
                    alpha = max(alpha, max_value)
                    if alpha >= beta:
                        break
                return selected_column, max_value


            else:
                min_value = float('inf')
                selected_column = random.choice(available_cols)
                for col in available_cols:
                    row = board.shape[0]-1
                    while board[row, col] != 0:
                        row -= 1

                    copy_boardstate = copy.deepcopy(board)
                    copy_boardstate[row, col] = self.opponent_number
                    score = minimax(copy_boardstate, curr_depth+1, max_depth, alpha, beta, True)[-1]
                    if score < min_value:
                        min_value = score
                        selected_column = col
                    beta = min(beta, min_value)
                    if beta <= alpha:
                        break
                return selected_column, min_value



        final_choice = minimax(board, 0, 4, float('-inf'), float('inf'), True)[0]
        return final_choice






    def expectimax_implement(self, board, curr_depth, max_depth, maximizingPlayer):
        available_cols = self.available_slots(board)
        if not available_cols:
            return None, 0

        if curr_depth == max_depth:
            return None, self.evaluation_function(board)

        if maximizingPlayer:
            max_value = float('-inf')
            selected_column = random.choice(available_cols)
            for col in available_cols:
                row = board.shape[0]-1
                while board[row, col] != 0:
                    row -= 1
                copy_boardstate = copy.deepcopy(board)
                copy_boardstate[row, col] = self.player_number
                score = self.expectimax_implement(copy_boardstate, curr_depth+1, max_depth, False)[-1]
                if score > max_value:
                    max_value = score
                    selected_column = col
            
            return selected_column, max_value


        else:
            min_value = 0
            for col in available_cols:
                row = board.shape[0]-1
                while board[row, col] != 0:
                    row -= 1
                copy_boardstate = copy.deepcopy(board)
                copy_boardstate[row, col] = self.opponent_number
                min_value += self.expectimax_implement(copy_boardstate, curr_depth+1, max_depth, True)[-1]
            
            return None, min_value/len(available_cols)



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

        return self.expectimax_implement(board, 0, 4, True)[0]
        # raise NotImplementedError('Whoops I don\'t know what to do')






    def evaluation_function(self, board):

        def evaluate(board, row, col, row_score, col_score):
            player_score = 0
            opp_score = 0

            opp_number = self.opponent_number
            player_number = self.player_number

            for _ in range(4):
                if board[row, col] == opp_number:
                    opp_score += 1
                elif board[row, col] == player_number:
                    player_score += 1

                row += row_score
                col += col_score
            
            if opp_score == 4:
                return MIN_SCORE
            elif player_score == 4:
                return MAX_SCORE
            else:
                return player_score

        
        rows, cols = board.shape
        vertical = 0
        horizontal = 0 
        diagonal1 = 0
        diagonal2 = 0

        for row in range(rows):
            for col in range(cols-3):
                score = evaluate(board, row, col, 0, 1)
                if score in [MAX_SCORE, MIN_SCORE]:
                    return score
                horizontal += score



        for row in range(rows-3):
            for col in range(cols):
                score = evaluate(board, row, col, 1, 0)
                if score in [MAX_SCORE, MIN_SCORE]:
                    return score
                vertical += score



        for row in range(rows-3):
            for col in range(cols-3):
                score = evaluate(board, row, col, 1, 1)
                if score in [MAX_SCORE, MIN_SCORE]:
                    return score
                diagonal1 += score



        for row in range(3, rows):
            for col in range(cols-3):
                score = evaluate(board, row, col, -1, 1)
                if score in [MAX_SCORE, MIN_SCORE]:
                    return score
                diagonal2 += score


        overall_score = horizontal + vertical + diagonal1 + diagonal2
        return overall_score
       



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

