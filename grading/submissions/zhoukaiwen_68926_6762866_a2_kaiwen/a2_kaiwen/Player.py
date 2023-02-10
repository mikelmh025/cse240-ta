import numpy as np
import copy 

class AIPlayer:
    def __init__(self, player_number):
        self.player_number = player_number
        self.type = 'ai'
        self.player_string = 'Player {}:ai'.format(player_number)

    def update_board(self, move, board, number):
        board_ = copy.deepcopy(board)
        update_row = -1
        for row in range(1, board.shape[0]):
            update_row = -1
            if board[row, move] > 0 and board[row-1, move] == 0:
                update_row = row-1
            elif row==board.shape[0]-1 and board[row, move] == 0:
                update_row = row

            if update_row >= 0:
                board_[update_row, move] = number
                break
            
        return board_
                
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
        depth = 6
        
        best_value = float("-inf")
        best_move = None
        valid_cols = []
        for col in range(board.shape[1]):
            if 0 in board[:,col]:
                valid_cols.append(col)
                
        for move in valid_cols:
            board_ = self.update_board( move, board, self.player_number)
            value = self.alphabeta(board_, depth - 1, float("-inf"), float("inf"), False)
            if value > best_value:
                best_value = value
                best_move = move
        print(self.evaluation_function(self.update_board(best_move, board, self.player_number)))
        return best_move
    
    def alphabeta(self, board, depth, alpha, beta, maximizing_player):
        
        valid_cols = []
        for col in range(board.shape[1]):
            if 0 in board[:,col]:
                valid_cols.append(col)
        
        if depth == 0 or len(valid_cols)==0:
            return self.evaluation_function( board)
        
        if maximizing_player:
            value = float("-inf")
            for move in valid_cols:
                board_ = self.update_board( move, board, self.player_number)
                value = max(value, self.alphabeta(board_, depth - 1, alpha, beta, False))
                alpha = max(alpha, value)
                if alpha >= beta:
                    break
            return value
        else:
            value = float("inf")
            for move in valid_cols:
                board_ = self.update_board( move, board, 3-self.player_number)
                value = min(value, self.alphabeta(board_, depth - 1, alpha, beta, True))
                beta = min(beta, value)
                if alpha >= beta:
                    break
            return value
        
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
        depth = 5
        best_value = float("-inf")
        best_move = None
        
        valid_cols = []
        for col in range(board.shape[1]):
            if 0 in board[:,col]:
                valid_cols.append(col)
                
        for move in valid_cols:
            board_ = self.update_board(move, board, self.player_number)
            value = self.expectimax(board_, depth - 1, False)
            if value > best_value:
                best_value = value
                best_move = move
        print(self.evaluation_function(self.update_board(best_move, board, self.player_number)))
        return best_move
    
    def expectimax(self, board, depth, maximizing_player):

        valid_cols = []
        for col in range(board.shape[1]):
            if 0 in board[:,col]:
                valid_cols.append(col)
        
        if depth == 0 or len(valid_cols)==0:
            return self.evaluation_function( board)
        
        if maximizing_player:
            value = float("-inf")
            for move in valid_cols:
                board_ = self.update_board(move, board, self.player_number)
                value = max(value, self.expectimax(board_, depth - 1, False))
            return value
        else:
            value = 0
            n = len(valid_cols)
            for move in valid_cols:
                board_ = self.update_board(move, board, 3-self.player_number)
                value += self.expectimax(board_, depth - 1, True) / n
            return value

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
        score = 0
        for row in board:
            concecutive_self = 0
            concecutive_other = 0
            for number in row:
                if number == self.player_number:
                    if concecutive_other > 0:
                        score -= 2*concecutive_other ** 4
                    concecutive_self += 1
                    concecutive_other = 0
                elif number == 3-self.player_number:
                    if concecutive_self > 0:
                        score += concecutive_self ** 4
                    concecutive_self = 0
                    concecutive_other += 1
                else:
                    if concecutive_self > 0:
                        score += concecutive_self ** 4
                    if concecutive_other > 0:
                        score -= 2*concecutive_other ** 4
                    concecutive_self = 0
                    concecutive_other = 0
        
            if concecutive_self > 0:
                score += concecutive_self ** 4
            if concecutive_other > 0:
                score -= 2*concecutive_other ** 4
            
        for col in board.T:
            concecutive_self = 0
            concecutive_other = 0
            for number in col:
                if number == self.player_number:
                    if concecutive_other > 0:
                        score -= 2*concecutive_other ** 4
                    concecutive_self += 1
                    concecutive_other = 0
                elif number == 3-self.player_number:
                    if concecutive_self > 0:
                        score += concecutive_self ** 4
                    concecutive_self = 0
                    concecutive_other += 1
                else:
                    if concecutive_self > 0:
                        score += concecutive_self ** 4
                    if concecutive_other > 0:
                        score -= 2*concecutive_other ** 4
                    concecutive_self = 0
                    concecutive_other = 0
        
            if concecutive_self > 0:
                score += concecutive_self ** 4
            if concecutive_other > 0:
                score -= 2*concecutive_other ** 4
                    
        # upwards diag
        for i in [3,4,5]:
            concecutive_self = 0
            concecutive_other = 0
            for j in range(i+1):
                number = board[i-j, j]
                if number == self.player_number:
                    if concecutive_other > 0:
                        score -= 2*concecutive_other ** 4
                    concecutive_self += 1
                    concecutive_other = 0
                elif number == 3-self.player_number:
                    if concecutive_self > 0:
                        score += concecutive_self ** 4
                    concecutive_self = 0
                    concecutive_other += 1
                else:
                    if concecutive_self > 0:
                        score += concecutive_self ** 4
                    if concecutive_other > 0:
                        score -= 2*concecutive_other ** 4 
                    concecutive_self = 0
                    concecutive_other = 0
        
            if concecutive_self > 0:
                score += concecutive_self ** 4
            if concecutive_other > 0:
                score -= 2*concecutive_other ** 4
               
        for i in [1,2,3]:
            concecutive_self = 0
            concecutive_other = 0
            for j in range(7-i):
                number = board[5-j, i+j]
                if number == self.player_number:
                    if concecutive_other > 0:
                        score -= 2*concecutive_other ** 4
                    concecutive_self += 1
                    concecutive_other = 0
                elif number == 3-self.player_number:
                    if concecutive_self > 0:
                        score += concecutive_self ** 4
                    concecutive_self = 0
                    concecutive_other += 1
                else:
                    if concecutive_self > 0:
                        score += concecutive_self ** 4
                    if concecutive_other > 0:
                        score -= 2*concecutive_other ** 4
                    concecutive_self = 0
                    concecutive_other = 0
        
            if concecutive_self > 0:
                score += concecutive_self ** 4
            if concecutive_other > 0:
                score -= 2*concecutive_other ** 4
            
        # downwards diag
        for i in [0,1,2]:
            concecutive_self = 0
            concecutive_other = 0
            for j in range(6-i):
                number = board[i+j, j]
                if number == self.player_number:
                    if concecutive_other > 0:
                        score -= 2*concecutive_other ** 4
                    concecutive_self += 1
                    concecutive_other = 0
                elif number == 3-self.player_number:
                    if concecutive_self > 0:
                        score += concecutive_self ** 4
                    concecutive_self = 0
                    concecutive_other += 1
                else:
                    if concecutive_self > 0:
                        score += concecutive_self ** 4
                    if concecutive_other > 0:
                        score -= 2*concecutive_other ** 4
                    concecutive_self = 0
                    concecutive_other = 0
        
            if concecutive_self > 0:
                score += concecutive_self ** 4
            if concecutive_other > 0:
                score -= 2*concecutive_other ** 4
              
        for i in [1,2,3]:
            concecutive_self = 0
            concecutive_other = 0
            for j in range(7-i):
                number = board[j, i+j]
                if number == self.player_number:
                    if concecutive_other > 0:
                        score -= 2*concecutive_other ** 4
                    concecutive_self += 1
                    concecutive_other = 0
                elif number == 3-self.player_number:
                    if concecutive_self > 0:
                        score += concecutive_self ** 4
                    concecutive_self = 0
                    concecutive_other += 1
                else:
                    if concecutive_self > 0:
                        score += concecutive_self ** 4
                    if concecutive_other > 0:
                        score -= 2*concecutive_other ** 4
                    concecutive_self = 0
                    concecutive_other = 0
        
            if concecutive_self > 0:
                score += concecutive_self ** 4
            if concecutive_other > 0:
                score -= 2*concecutive_other ** 4
            
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

