import numpy as np

class AIPlayer:
    def __init__(self, player_number):
        self.player_number = player_number
        self.type = 'ai'
        self.player_string = 'Player {}:ai'.format(player_number)
        self.columns = 0
        self.rows = 0
        self.depth = 3
        self.next_player = 0
        

    def valid_move(self, board):
        valid_moves = []
        for c in range(board.shape[1]):
            if board[0][c] == 0:
                valid_moves.append(c)
        return valid_moves
    
    def make_move(self, board, c, player):
        new_board = board.copy()
        for r in range(board.shape[0]-1 , -1, -1):
            if new_board[r][c] ==0:
                new_board[r][c] = player
                return new_board
        

    def alpha_beta(self, board, depth, player, alpha, beta):
        if depth == 0:
            return 0
        else:
            score_now = self.evaluation_function(board)
            if score_now != 0:
                return score_now

        if player == self.next_player: # max player
            for column in range(board.shape[1]):
                if column in self.valid_move(board):
                    new_board = self.make_move(board, column, player)
                    value = self.alpha_beta(new_board, depth-1, 3 - self.next_player, alpha, beta)
                    alpha = max(alpha, value)
                    if beta <= alpha:
                        break
            return alpha
        else:
            for column in range(board.shape[1]):
                if column in self.valid_move(board):
                    new_board = self.make_move(board, column, player)
                    value = self.alpha_beta(new_board, depth-1, 3 - self.next_player, alpha, beta)
                    beta = min(beta, value)
                    if beta <= alpha:
                        break
            return beta

    def get_next_player(self, board):
        if np.sum(board == 1) > np.sum(board == 2):
            return 2
        else:
            return 1

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
        
        self.rows, self.columns = board.shape
        
        alpha = float('-inf')
        beta = float('inf')
        
        self.next_player = self.get_next_player(board)
        
        available_moves = self.valid_move(board)
        
        # Set the best move to None initially
        best_move = None
        
        # Loop through all the available moves
        for move in available_moves:
            

            new_board = self.make_move(board, move, self.next_player)
            
            # Evaluate the board with the alpha-beta search algorithm
            value = self.alpha_beta(new_board, self.depth, 3 - self.next_player, alpha, beta)
            
            # Check if the value of the new move is better than the current best move
            if value > alpha:
                alpha = value
                best_move = move
        
        # Return the best move
        return best_move

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
        def expectimax(board, depth, player):
            if depth == 0:
                
                score_now = self.evaluation_function(board)
                return score_now
                

            if player == self.next_player: # max player
                return max([expectimax(self.make_move(board, move, player), depth - 1, 3 - self.next_player) for move in self.valid_move(board)])
            else:
                next_states = [self.make_move(board, move, player) for move in self.valid_move(board)]
                probabilities = [len(self.valid_move(state)) / len(self.valid_move(board)) for state in next_states]
                return sum([probabilities[i] * expectimax(next_states[i], depth - 1, 3 - self.next_player) for i in range(len(next_states))])
                
        self.rows, self.columns = board.shape

        
        self.next_player = self.get_next_player(board)
        
        available_moves = self.valid_move(board)
        
        # Set the best move to None initially        
        best_move = None
        best_score = float('-inf')
        for move in available_moves:
            new_board = self.make_move(board, move, self.next_player)
            score = expectimax(new_board, self.depth, 3 - self.next_player)
            if score > best_score:
                best_score = score
                best_move = move
        return best_move



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
        depth = 1
        # Check for horizontal streaks
        for r in range(board.shape[0]):
            for c in range(board.shape[1]-3):
                window = board[r, c:c+4]
                if np.all(window == self.next_player):
                    score += 1000 * depth
                elif np.all(window != self.next_player):
                    score -= 1000 * depth
                elif np.sum(window == self.next_player) >=2 and np.sum(window != self.next_player) == 0:
                    score += 50 * depth
                elif np.sum(window != self.next_player) >=2 and np.sum(window == self.next_player) == 0:
                    score -= 50 * depth

        # Check for vertical streaks
        for c in range(board.shape[1]):
            for r in range(board.shape[0]-3):
                window = board[r:r+4, c]
                if np.all(window == self.next_player):
                    score += 1000 * depth
                elif np.all(window != self.next_player):
                    score -= 1000 * depth
                elif np.sum(window == self.next_player) >=2 and np.sum(window != self.next_player) == 0:
                    score += 50 * depth
                elif np.sum(window != self.next_player) >=2 and np.sum(window == self.next_player) == 0:
                    score -= 50 * depth
        # Check for positive diagonal streaks
        for r in range(board.shape[0]-3):
            for c in range(board.shape[1]-3):
                window = [board[r+i][c+i] for i in range(4)]
                if np.all(window == self.next_player):
                    score += 1000 * depth
                elif np.all(window != self.next_player):
                    score -= 1000 * depth
                elif np.sum(window == self.next_player) >=2 and np.sum(window != self.next_player) == 0:
                    score += 50 * depth
                elif np.sum(window != self.next_player) >=2 and np.sum(window == self.next_player) == 0:
                    score -= 50 * depth
        # Check for negative diagonal streaks
        for r in range(3, board.shape[0]):
            for c in range(board.shape[1]-3):
                window = [board[r-i][c+i] for i in range(4)]
                if np.all(window == self.next_player):
                    score += 1000 * depth
                elif np.all(window != self.next_player):
                    score -= 1000 * depth
                elif np.sum(window == self.next_player) >=2 and np.sum(window != self.next_player) == 0:
                    score += 50 * depth
                elif np.sum(window != self.next_player) >=2 and np.sum(window == self.next_player) == 0:
                    score -= 50 * depth
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

