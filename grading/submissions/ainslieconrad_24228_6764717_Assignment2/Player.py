import numpy as np

class AIPlayer:
    def __init__(self, player_number):
        self.player_number = player_number
        self.type = 'ai'
        self.player_string = 'Player {}:ai'.format(player_number)
        self.player_heuristic_score = int(0)
        self.opponent_heuristic_score = int(0)
        self.heuristic_score_params = [2, 10, np.Inf]
        
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
        #set presets for fist call of minimax
        depth = 3
        my_score = self.player_heuristic_score
        opp_score = self.opponent_heuristic_score 
        alpha = -np.Inf
        beta = np.Inf
        
        #call minimax
        value, placement = self.minimax(board, my_score, opp_score, self.player_number, True, depth, alpha, beta)
        row, column = placement
        
        #update player and opponent heuristic scores
        self.player_heuristic_score -= self.evaluation_function(board, row, column, self.player_number) 
        self.opponent_heuristic_score -= self.evaluation_function(board, row, column, (1+(self.player_number)%2))
        tempboard = board.copy()
        tempboard[row,column] = self.player_number 
        self.player_heuristic_score += self.evaluation_function(tempboard, row, column, self.player_number) 
        self.opponent_heuristic_score += self.evaluation_function(tempboard, row, column, (1+(self.player_number)%2))
        
        return column
        
        
    def minimax(self, board, maxi_score, mini_score, player_number, maximizing_player, depth, alpha, beta):
        if maxi_score - mini_score == np.Inf:
            return np.Inf, None
        if maxi_score - mini_score == -np.Inf:
            return -np.Inf, None
        if depth == 0: 
            return maxi_score - mini_score, None
        valid_placements = []
        for i, col in enumerate(board.T):
            if 0 in col:
                for j in range(len(col),0,-1):
                    if col[j-1] == 0:
                        valid_placements.append((j-1,i))
                        break
        if valid_placements == None: #tie
            return 0, None
        if maximizing_player:
            value = -np.Inf
            value_index = -1
            for x in range(len(valid_placements)):
                row,col = valid_placements[x]
                maxi_score_temp = maxi_score
                mini_score_temp = mini_score
                tempboard = board.copy()

                #remove old values from possibly impacted peices given planned move
                maxi_score_temp -= self.evaluation_function(tempboard, row, col, player_number)
                mini_score_temp -= self.evaluation_function(tempboard, row, col, (1+(player_number)%2))

                tempboard[row,col] = player_number
                #add new values from possibly impacted pieces after move has been made
                maxi_score_temp += self.evaluation_function(tempboard, row, col, player_number) 
                mini_score_temp += self.evaluation_function(tempboard, row, col, (1+(player_number)%2))
                
                current_eval, placement = self.minimax(tempboard, maxi_score_temp, mini_score_temp, 
                                     (1+(player_number)%2), not(maximizing_player), depth -1, alpha, beta)
                if value < current_eval:
                    value = current_eval
                    value_index = x
                if value == current_eval:
                    if np.random.randint(2):
                        value = current_eval
                        value_index = x
                if value > beta:
                    break
                alpha = max(alpha, value)
            return value, valid_placements[value_index]
        else: 
            value = np.Inf
            value_index = -1
            for x in range(len(valid_placements)):
                
                row,col = valid_placements[x]
                maxi_score_temp = maxi_score
                mini_score_temp = mini_score
                tempboard = board.copy()
                
                #remove old values from possibly impacted peices given planned move
                maxi_score_temp -= self.evaluation_function(tempboard, row, col, (1+(player_number)%2)) 
                mini_score_temp -= self.evaluation_function(tempboard, row, col, player_number)
                
                tempboard[row,col] = player_number 
                
                #add new values from possibly impacted pieces after move has been made
                maxi_score_temp += self.evaluation_function(tempboard, row, col, (1+(player_number)%2)) 
                mini_score_temp += self.evaluation_function(tempboard, row, col, player_number)
                current_eval, placement = self.minimax(tempboard, maxi_score_temp, mini_score_temp, 
                                     (1+(player_number)%2), not(maximizing_player), depth -1, alpha, beta)                
                if value > current_eval:
                    value = current_eval
                    value_index = x
                if value == current_eval:
                    if np.random.randint(2):
                        value = current_eval
                        value_index = x
                if value < alpha:
                    break
                beta = min(beta, value)
            return value, valid_placements[value_index]
            
            
            
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
        depth = 3
        my_score = self.player_heuristic_score
        opp_score = self.opponent_heuristic_score 
        alpha = -np.Inf
        beta = np.Inf
        
        #call expectsum
        value, placement = self.expectsum(board, my_score, opp_score, self.player_number, True, depth, alpha, beta)
        row, column = placement
        
        #update player and opponent heuristic scores
        self.player_heuristic_score -= self.evaluation_function(board, row, column, self.player_number) 
        self.opponent_heuristic_score -= self.evaluation_function(board, row, column, (1+(self.player_number)%2))
        tempboard = board.copy()
        tempboard[row,column] = self.player_number 
        self.player_heuristic_score += self.evaluation_function(tempboard, row, column, self.player_number) 
        self.opponent_heuristic_score += self.evaluation_function(tempboard, row, column, (1+(self.player_number)%2))
        
        
        return column
    
    def expectsum(self, board, maxi_score, mini_score, player_number, maximizing_player, depth, alpha, beta):
        if maxi_score - mini_score == np.Inf:
            return np.Inf, None
        if maxi_score - mini_score == -np.Inf:
            return -np.Inf, None
        if depth == 0: 
            return maxi_score - mini_score, None
        valid_placements = []
        for i, col in enumerate(board.T):
            if 0 in col:
                for j in range(len(col),0,-1):
                    if col[j-1] == 0:
                        valid_placements.append((j-1,i))
                        break
        if valid_placements == None: #tie
            return 0, None
        if maximizing_player:
            value = -np.Inf
            value_index = -1
            for x in range(len(valid_placements)):
                row,col = valid_placements[x]
                maxi_score_temp = maxi_score
                mini_score_temp = mini_score
                tempboard = board.copy()

                #remove old values from possibly impacted peices given planned move
                maxi_score_temp -= self.evaluation_function(tempboard, row, col, player_number)
                mini_score_temp -= self.evaluation_function(tempboard, row, col, (1+(player_number)%2))

                tempboard[row,col] = player_number
                #add new values from possibly impacted pieces after move has been made
                maxi_score_temp += self.evaluation_function(tempboard, row, col, player_number) 
                mini_score_temp += self.evaluation_function(tempboard, row, col, (1+(player_number)%2))
                
                current_eval, placement = self.expectsum(tempboard, maxi_score_temp, mini_score_temp, 
                                     (1+(player_number)%2), not(maximizing_player), depth -1, alpha, beta)
                if value < current_eval:
                    value = current_eval
                    value_index = x
                if value == current_eval:
                    if np.random.randint(2):
                        value = current_eval
                        value_index = x
                if value > beta:
                    break
                alpha = max(alpha, value)
            return value, valid_placements[value_index]
        else: 
            value = np.Inf
            value_index = -1
            for x in range(len(valid_placements)):
                
                row,col = valid_placements[x]
                maxi_score_temp = maxi_score
                mini_score_temp = mini_score
                tempboard = board.copy()
                
                #remove old values from possibly impacted peices given planned move
                maxi_score_temp -= self.evaluation_function(tempboard, row, col, (1+(player_number)%2)) 
                mini_score_temp -= self.evaluation_function(tempboard, row, col, player_number)
                
                tempboard[row,col] = player_number 
                
                #add new values from possibly impacted pieces after move has been made
                maxi_score_temp += self.evaluation_function(tempboard, row, col, (1+(player_number)%2)) 
                mini_score_temp += self.evaluation_function(tempboard, row, col, player_number)
                current_eval, placement = self.expectsum(tempboard, maxi_score_temp, mini_score_temp, 
                                     (1+(player_number)%2), not(maximizing_player), depth -1, alpha, beta)                
                current_eval *= 1/6
                if value > current_eval:
                    value = current_eval
                    value_index = x
                if value == current_eval:
                    if np.random.randint(2):
                        value = current_eval
                        value_index = x
                if value < alpha:
                    break
                beta = min(beta, value)
            return value, valid_placements[value_index]
        
        
        




    def evaluation_function(self, board, row, column, player_num):
        """
        Given the current stat of the board, and the planned move, update the 
        evaluation scores for both players based on the effet of the next move.
        This does not calculate the eval function on the whole board, only the 
        area of the board that has been changed by placing said peice. This is 
        faster as we don't have to re-calculate anything
       
        INPUTS:
        board - a numpy array containing the state of the board using the
                following encoding:
                - the board maintains its same two dimensions
                    - row 0 is the top of the board and so is
                      the last row filled
                - spaces that are unoccupied are marked as 0
                - spaces that are occupied by player 1 have a 1 in them
                - spaces that are occupied by player 2 have a 2 in them
        row - int spesifying the row number of planned move
        column - int spesifying the column number of planned move
        player_num - bool spesifying the current player

        RETURNS:
        The change in utility value for current board based on current move
        """
        
        col_window = (max(row-3,0),min(row+3,5))  #row window of possible changed values
        row_window = (max(column-3,0),min(column+3,6))#column window of possibly changed values
        tempmin1 = min(row, column, 3)
        tempmin2 = min(5-row, 6 - column, 3)
        l_diag_window = ((row-tempmin1, column-tempmin1),  #diagonal window of possibly values 
                         (row + tempmin2, column + tempmin2))
        tempmin1 = min(row, 6 - column, 3)
        tempmin2 = min(5-row, column, 3)
        r_diag_window = ((row + tempmin2, column - tempmin2), #diagonal window of possibly values 
                         (row - tempmin1, column + tempmin1))
        changed_score = 0
        for x in range(2,5): #update number of length 2,3 and 4 horizontal 
            for peek_index in range(row_window[0], + row_window[1] - x + 2):
                peek = board[row , peek_index:peek_index+x]
                if peek.all() == player_num:
                    changed_score += self.heuristic_score_params[x-2] 
        for x in range(2,5): #update number of length 2,3 and 4 vertical 
            for peek_index in range(col_window[0], col_window[1] - x + 2):
                peek = board[peek_index:peek_index+ x , column]
                if peek.all() == player_num:
                    changed_score += self.heuristic_score_params[x-2] 
        for x in range(2,5): #update number of length 2,3 and 4 left-diagonal 
            for peek_index in range(l_diag_window[0][0], l_diag_window[1][0]- x + 2):
                peek = np.array([]).astype(np.uint8) 
                for ind in range(0,x):
                    peek = np.append(peek, board[peek_index + ind ,l_diag_window[0][1] - l_diag_window[0][0] + peek_index + ind])
                if peek.all() == player_num:
                    changed_score += self.heuristic_score_params[x-2] 
        for x in range(2,5): #update number of length 2,3 and 4 left-diagonal 
            for peek_index in range(r_diag_window[0][0], r_diag_window[1][0] + x - 2,-1):
                peek = np.array([]).astype(np.uint8)
                for ind in range(0,x):
                    peek = np.append(peek, board[peek_index - ind, r_diag_window[0][1] + 
                                                         r_diag_window[0][0] - peek_index + ind])
                if peek.all() == player_num:
                   changed_score += self.heuristic_score_params[x-2] 
        return changed_score #the total changed score given a peice is dropped
                             # at row, column.
        
        
        


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

