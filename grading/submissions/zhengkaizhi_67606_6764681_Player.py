import numpy as np

class AIPlayer:
    def __init__(self, player_number):
        self.player_number = player_number
        self.type = 'ai'
        self.player_string = 'Player {}:ai'.format(player_number)

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
        depth = 4
        
        best_value = -np.inf
        best_move = None
        valid_cols = []
        for col in range(board.shape[1]):
            if 0 in board[:,col]:
                valid_cols.append(col)
                
        for move in valid_cols:
            _board = self.imagine_move(board, move, self.player_number)
            value = self.alpha_beta(_board, depth - 1, -np.inf, np.inf, node_type='min')
            if value > best_value:
                best_value = value
                best_move = move
        print('Player {} chose column {} with expect value {}'.format(self.player_number, best_move, best_value))
        return best_move

    def alpha_beta(self, board, depth, alpha, beta, node_type='max'):
        
        valid_cols = []
        for col in range(board.shape[1]):
            if 0 in board[:,col]:
                valid_cols.append(col)
        
        current_score = self.evaluation_function(board)
        if depth == 0 or len(valid_cols)==0 or abs(current_score)==1000:
            return current_score
        
        if node_type=='max':
            value = -np.inf
            for move in valid_cols:
                _board = self.imagine_move(board, move, self.player_number)
                value = max(value, self.alpha_beta(_board, depth - 1, alpha, beta, 'min'))
                alpha = max(alpha, value)
                if alpha >= beta:
                    break
            return alpha
        else:
            value = np.inf
            for move in valid_cols:
                _board = self.imagine_move(board, move, 3-self.player_number)
                value = min(value, self.alpha_beta(_board, depth - 1, alpha, beta, 'max'))
                beta = min(beta, value)
                if alpha >= beta:
                    break
            return beta
        
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
        best_value = -np.inf
        best_move = None
        
        valid_cols = []
        for col in range(board.shape[1]):
            if 0 in board[:,col]:
                valid_cols.append(col)
                
        for move in valid_cols:
            _board = self.imagine_move(board, move, self.player_number)
            value = self.expectimax(_board, depth - 1, 'min')
            if value > best_value:
                best_value = value
                best_move = move
        print('Player {} chose column {} with expect value {}'.format(self.player_number, best_move, best_value))
        return best_move
    
    def expectimax(self, board, depth, node_type='max'):

        valid_cols = []
        for col in range(board.shape[1]):
            if 0 in board[:,col]:
                valid_cols.append(col)
        
        current_score = self.evaluation_function(board)
        if depth == 0 or len(valid_cols)==0 or abs(current_score)==1000:
            return current_score
        
        if node_type=='max':
            value = -np.inf
            for move in valid_cols:
                _board = self.imagine_move(board, move, self.player_number)
                value = max(value, self.expectimax(_board, depth - 1, 'min'))
            return value
        else:
            value = 0
            n = len(valid_cols)
            for move in valid_cols:
                _board = self.imagine_move(board, move, 3-self.player_number)
                value += self.expectimax(_board, depth - 1, 'max') / n
            return value

    def imagine_move(self, board, col, player_number):
        """
        Given the current state of the board, return a new board with the
        specified move made

        INPUTS:
        board - a numpy array containing the state of the board using the
                following encoding:
                - the board maintains its same two dimensions
                    - row 0 is the top of the board and so is
                      the last row filled
                - spaces that are unoccupied are marked as 0
                - spaces that are occupied by player 1 have a 1 in them
                - spaces that are occupied by player 2 have a 2 in them
        col - the 0 based index of the column that represents the next move
        player_number - the player number of the player making the move

        RETURNS:
        A new board with the specified move made
        """
        new_board = board.copy()
        for row in range(new_board.shape[0]-1, -1, -1):
            if new_board[row,col]==0:
                new_board[row,col] = player_number
                break

        return new_board
    
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
        def check_pattern(b, pattern, positive_value=2, negative_value=-1):
            to_str = lambda a: ''.join(a.astype(str))
            positive_agent = pattern.format(self.player_number)
            negative_agent = pattern.format(3-self.player_number)

            def check_horizontal(b, c_pattern, value):
                scores = 0
                for row in b:
                    if c_pattern in to_str(row):
                        scores+=value
                return scores

            def check_verticle(b, c_pattern, value):
                return check_horizontal(b.T, c_pattern, value)

            def check_diagonal(b, c_pattern, value):
                scores = 0
                for op in [None, np.fliplr]:
                    op_board = op(b) if op else b
                    
                    root_diag = np.diagonal(op_board, offset=0).astype(np.int)
                    if c_pattern in to_str(root_diag):
                        scores += value

                    for i in range(1, b.shape[1]-3):
                        for offset in [i, -i]:
                            diag = np.diagonal(op_board, offset=offset)
                            diag = to_str(diag.astype(np.int))
                            if c_pattern in diag:
                                scores += value

                return scores
            
            positive_score = check_horizontal(b, positive_agent, positive_value)+check_verticle(b, positive_agent, positive_value)+check_diagonal(b, positive_agent, positive_value)+check_diagonal(b, positive_agent, positive_value)
            negative_score = check_horizontal(b, negative_agent, negative_value)+check_verticle(b, negative_agent, negative_value)+check_diagonal(b, negative_agent, negative_value)+check_diagonal(b, negative_agent, negative_value)

            return positive_score+negative_score, positive_score, negative_score

        pattern1 = '{0}{0}'
        pattern2 = '{0}{0}{0}'
        pattern3 = '{0}{0}{0}{0}'

        _, win_score, lose_score = check_pattern(board, pattern3, positive_value=1, negative_value=-1)
        if win_score>0:
            score = 1000
        elif lose_score<0:
            score = -1000
        else:
            pattern1_score,_,_ = check_pattern(board, pattern1, positive_value=2, negative_value=-1)
            pattern2_score,_,_ = check_pattern(board, pattern2, positive_value=20, negative_value=-10)
            score = pattern1_score+pattern2_score
       
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

