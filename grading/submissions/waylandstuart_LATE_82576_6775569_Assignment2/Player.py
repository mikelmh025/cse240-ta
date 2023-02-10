import numpy as np

class AIPlayer:
    def __init__(self, player_number):
        self.player_number = player_number
        self.type = 'ai'
        self.player_string = 'Player {}:ai'.format(player_number)
    
    def gen_child(self, board, player_number, i):
        """Generates the next (or child) board after making move i: ie playing the move i
        
        INPUTS: 
        board - np array containing current board state
        player_number - which player is making move
        i - which move is to be made 
        
        RETURNS:
           The board after making move i"""
        child = board.copy()
        for j in range(5,-1,-1):
            if child[j][i] == 0:
                child[j][i] = player_number
                return child
    
    def gen_children(self, board, player_number):
        """Generates the possible children of this board
        
        INPUTS: 
        board - np array containing current board state
        player_number - which player is making move
        
        RETURNS:
        The possible boards after player makes a move"""
        children = []
        for i in range(0,7):
            child = board.copy()
            for j in range(5,-1,-1):
                if child[j][i] == 0:
                    child[j][i] = player_number
                    children.append(child.copy())
                    break
            return children
    

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
        max_depth = 3
        best_move = 0
        best_score = -np.infty
        alpha = -np.infty
        beta = np.infty
        for i in range(0,7):
            child = self.gen_child(board, self.player_number, i)
            if child is None:
                continue
            child_score,alpha,beta = self.alpha_beta_max(child,1,max_depth,alpha, beta,(self.player_number%2 + 1))
            if(best_score < child_score):
                best_score = child_score
                best_move = i
        return best_move
    
    def alpha_beta_max(self, board, h, max_depth, alpha, beta, move):
        if(move == self.player_number):
            if(h == max_depth):
                return self.evaluation_function(board), alpha, beta
            values = []
            children = self.gen_children(board,move)
            if(len(children) == 0):
                return self.evaluation_function(board), alpha, beta
            for child in children:
                value, alpha, beta = self.alpha_beta_max(child, h+1, max_depth, alpha, beta, (move%2+1))
                values.append(value)
                if value > beta: 
                    break
            max_v = max(values)
            if(max_v < beta):
                beta = max_v
            return max_v, alpha, beta
        
        else:
            if(h == max_depth):
                return self.evaluation_function(board), alpha, beta
            values = []
            children = self.gen_children(board,move)
            if(len(children) == 0):
                return self.evaluation_function(board), alpha, beta
            for child in children:
                value,alpha,beta = self.alpha_beta_max(child, h+1, max_depth, alpha, beta, (move%2+1))
                values.append(value)
                if value < alpha: 
                    break
            min_v = min(values)
            if(min_v > alpha):
                alpha = min_v
            return min_v, alpha, beta

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
        max_depth = 2
        best_move = 0
        best_score = -np.infty
        
        for i in range(0,7):
            child = self.gen_child(board, self.player_number, i)
            child_score = self.expectimax(child,1,max_depth,self.player_number%2 + 1)
            print(i,child_score)
            if(best_score < child_score):
                best_score = child_score
                best_move = i
        return best_move
    
    def expectimax(self, board, h, max_depth, move):
        """Recusive implementation of expectimax helper function
        INPUT: 
        board - a possible future game board of the current board state 
        h - the height of this board in the predicted game tree 
        max_depth - the number of potential moves to look ahead
        move - whether this is a max move (current player) or min move (opponent)
        
        RETURNS:
        - The evaluation of the board if the height = max_depth 
        - the best choice according the minimax algorithm
        """
        if(h == max_depth):
            return self.evaluation_function(board)
        values = []
        children = self.gen_children(board,move)
        if(len(children) == 0):
            return self.gen_children(board,move)
        for child in children:
            values.append(1/len(children) * self.expectimax(child, h+1, max_depth, (move%2+1)))
        if(move == self.player_number):
            return max(values)
        else:    
            return min(values)

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

        potential_wins = self.number_of_pvw(board, self.player_number)
        + self.number_of_phw(board, self.player_number) 
        + 0.3*self.number_of_pdw(board, self.player_number)
        
        potential_losses = self.number_of_pvw(board, self.player_number%2 + 1)
        + self.number_of_phw(board, self.player_number%2 + 1)
        + self.number_of_pdw(board, self.player_number%2 + 1)
        
        v_wins, v_threes, v_twos = self.number_of_vertical_links(board, self.player_number) 
        h_wins, h_threes, h_twos = self.number_of_horizontal_links(board, self.player_number)  
        d_wins, d_threes, d_twos =  self.number_of_diagonal_links(board, self.player_number)
        
        wins = v_wins + h_wins + d_wins
        threes = v_threes + h_threes + d_threes
        twos = v_twos + h_twos + d_twos 
        
        
        
        v_losses, vl_threes, vl_twos = self.number_of_vertical_links(board, self.player_number%2 + 1)
        h_losses, hl_threes, hl_twos =  self.number_of_horizontal_links(board, self.player_number%2 + 1) 
        d_losses, dl_threes, dl_twos =  self.number_of_diagonal_links(board, self.player_number%2 + 1)
        
        losses = v_losses + h_losses + d_losses
        l_threes = vl_threes + hl_threes + dl_threes
        l_twos = vl_twos + hl_twos + 0.3*dl_twos

        h = self.max_height(board)
        
        return  1000*wins - 1000*losses + threes - l_threes + 0.5*twos - 0.5*l_twos + potential_wins - potential_losses- (10+h)**2
       

    

    def max_height(self, board):
        max_height = 5
        for i in range(0,7):
            for j in range(5,-1,-1):
                if board[j][i] > 0:
                    if(max_height > j):
                        max_height = j
        max_height = 5 - max_height
        return max_height

    
    def number_of_pvw(self, board, player):
        num_in_line = 0
        vertical_wins = 0
        for i in range(0,7):
            for j in range(5,-1,-1):
                if(board[j][i] == player or board[j][i] == 0):
                    num_in_line +=1
                else:
                    num_in_line = 0
                if num_in_line >= 4:
                    vertical_wins += 1
            num_in_line = 0
        return vertical_wins
    
    def number_of_phw(self, board, player):
        num_in_line = 0
        horizontal_wins = 0
        for j in range(5,-1,-1):
            for i in range(0,7):
                if(board[j][i] == player or board[j][i] == 0):
                    num_in_line +=1
                else:
                    num_in_line = 0
                if num_in_line >= 4:
                    horizontal_wins += 1
            num_in_line = 0
        return horizontal_wins
    
    
    def number_of_pdw(self, board, player):
        # Counting number of forward diagnol wins 
        f_diagnol_wins = 0
        num_diagnol = 0
        for i in range(4):
            for j in range(5,2,-1):
                num_diagnol = 0
                for k in range(4):
                    if(board[j-k][i+k] == player or board[j-k][i+k] == 0):
                        num_diagnol += 1
                if num_diagnol >= 4:
                    f_diagnol_wins += 1
                    
        # Counting number of backward diagnol possible wins 
        d_diagnol_wins = 0
        num_diagnol = 0
        for i in range(6, 2, -1):
            for j in range(5,2,-1):
                num_diagnol = 0
                for k in range(4):
                    if(board[j-k][i-k] == player or board[j-k][i-k] == 0):
                        num_diagnol += 1
                if num_diagnol >= 4:
                    d_diagnol_wins += 1
        return (d_diagnol_wins + f_diagnol_wins) 
    
    
    def number_of_vertical_links(self, board, player):
        num_in_line = 0
        v_wins = 0
        v_threes = 0
        v_twos = 0
        for j in range(5,-1,-1):
            for i in range(0,7):
                if(board[j][i] == player):
                    num_in_line +=1
                else:
                    num_in_line = 0
                if num_in_line == 2:
                    v_twos += 1
                if num_in_line == 3:
                    v_threes += 1
                if num_in_line >= 4:
                    v_wins += 1
            num_in_line = 0
        return v_wins, v_threes, v_twos 
    
    def number_of_horizontal_links(self, board, player):
        num_in_line = 0
        h_wins = 0
        h_threes = 0
        h_twos = 0 
        for j in range(5,-1,-1):
            for i in range(0,7):
                if(board[j][i] == player):
                    num_in_line +=1
                else:
                    num_in_line = 0
                if num_in_line == 2:
                    h_twos += 1
                if num_in_line == 3:
                    h_threes += 1
                if num_in_line >= 4:
                    h_wins += 1
            num_in_line = 0
        return h_wins, h_threes, h_twos
    
    def number_of_diagonal_links(self, board, player):
        # Counting number of forward diagnol wins 
        fd_wins = 0
        fd_threes = 0
        fd_twos = 0
        num_diagnol = 0
        for i in range(4):
            for j in range(5,2,-1):
                num_diagnol = 0
                for k in range(4):
                    if(board[j-k][i+k] == player):
                        num_diagnol += 1
                    else:
                        num_diagnol = 0
                if num_diagnol == 2:
                    fd_twos += 1
                if num_diagnol == 3:
                    fd_threes += 1
                if num_diagnol >= 4:
                    fd_wins += 1
                    
        # Counting number of backward diagnol possible wins 
        dd_wins = 0
        dd_threes = 0 
        dd_twos = 0
        num_diagnol = 0
        for i in range(6, 2, -1):
            for j in range(5,2,-1):
                num_diagnol = 0
                for k in range(4):
                    if(board[j-k][i-k] == player or board[j-k][i-k] == 0):
                        num_diagnol += 1
                    else:
                        num_diagnol = 0
                if num_diagnol == 2:
                    dd_twos += 1
                if num_diagnol == 3:
                    dd_threes += 1 
                if num_diagnol >= 4:
                    dd_wins += 1
        return (dd_wins + fd_wins), (dd_threes + fd_threes), (dd_twos + fd_twos)

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

