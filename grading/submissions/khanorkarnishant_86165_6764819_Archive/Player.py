import numpy as np

N_MAX = 3

class AIPlayer:
    def __init__(self, player_number):
        self.player_number = player_number
        self.type = 'ai'
        self.player_string = 'Player {}:ai'.format(player_number)
    
    def get_next_moves(self, board, r, c, c_row):
        return [[c_row[j], j] for j in range(c) if c_row[j] >=0 and board[c_row[j]][j] == 0]	
        
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
        
        def alpha_beta_search(nth_move, board, r, c, c_row, alpha, beta, p1, p2):
            value_move = []
            v = -np.inf
            for i, j in self.get_next_moves(board, r, c, c_row):
                board[i][j] = p1
                c_row[j] -= 1
                val = min_value(nth_move + 1, board, r, c, c_row, alpha, beta, p1, p2)
                board[i][j] = 0
                c_row[j] += 1
                value_move.append([val, j])
                v = max(v, val)
            if v == -np.inf:
                return 0
            return np.random.choice([move for val, move in value_move if val == v])
        
        def max_value(nth_move, board, r, c, c_row, alpha, beta, p1, p2):
            if nth_move <= N_MAX:
                v = -np.inf
                for i, j in self.get_next_moves(board, r, c, c_row):
                    board[i][j] = p1
                    c_row[j] -= 1
                    v = max(v, min_value(nth_move + 1, board, r, c, c_row, alpha, beta, p1, p2))
                    board[i][j] = 0
                    c_row[j] += 1
                    if v >= beta:
                        return v
                    alpha = max(alpha, v)
                if v != -np.inf:
                    return v
            return self.evaluation_function(board)
        
        def min_value(nth_move, board, r, c, c_row, alpha, beta, p1, p2):
            if nth_move <= N_MAX:
                v = +np.inf
                for i, j in self.get_next_moves(board, r, c, c_row):
                    board[i][j] = p2
                    c_row[j] -= 1
                    v = min(v, max_value(nth_move + 1, board, r, c, c_row, alpha, beta, p1, p2))
                    board[i][j] = 0
                    c_row[j] += 1
                    if v <= alpha:
                        return v
                    beta = min(beta, v)
                if v != +np.inf:
                    return v
            return self.evaluation_function(board)
        
        r = len(board)
        c = len(board[0])
        c_row = [0] * c
        for j in range(c):
            for i in range(r - 1, -1, -1):
                if board[i][j] == 0:
                    c_row[j] = i
                    break
        alpha = -np.inf 
        beta = +np.inf
        p1 = self.player_number
        p2 = 1 + p1 % 2
        
        alpha_beta_move = alpha_beta_search(0, board, r, c, c_row, alpha, beta, p1, p2)
        return alpha_beta_move
	
        raise NotImplementedError('Whoops I don\'t know what to do')

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
        
        def expectimax_search(nth_move, board, r, c, c_row, p1, p2):
            value_move = []
            v = -np.inf
            for i, j in self.get_next_moves(board, r, c, c_row):
                board[i][j] = p1
                c_row[j] -= 1
                val = exp_value(nth_move + 1, board, r, c, c_row, p1, p2)
                board[i][j] = 0
                c_row[j] += 1
                value_move.append([val, j])
                v = max(v, val)
            
            return np.random.choice([move for val, move in value_move if val == v])
        
        def max_value(nth_move, board, r, c, c_row, p1, p2):
            if nth_move <= N_MAX:
                v = -np.inf
                for i, j in self.get_next_moves(board, r, c, c_row):
                    board[i][j] = p1
                    c_row[j] -= 1
                    v = max(v, exp_value(nth_move + 1, board, r, c, c_row, p1, p2))
                    board[i][j] = 0
                    c_row[j] += 1
                if v != -np.inf:
                    return v
            return self.evaluation_function(board)
        
        def exp_value(nth_move, board, r, c, c_row, p1, p2):
            if nth_move > 0:
                v = 0
                next_moves = self.get_next_moves(board, r, c, c_row)
                for i, j in next_moves:
                    board[i][j] = p2
                    c_row[j] -= 1
                    v += max_value(nth_move + 1, board, r, c, c_row, p1, p2)
                    board[i][j] = 0
                    c_row[j] += 1
                if v != 0:
                    return v / len(next_moves)
            return self.evaluation_function(board)   
        
        r = len(board)
        c = len(board[0])
        c_row = [0] * c
        for j in range(c):
            for i in range(r - 1, -1, -1):
                if board[i][j] == 0:
                    c_row[j] = i
                    break
        p1 = self.player_number
        p2 = 1 + p1 % 2
        
        expectimax_move = expectimax_search(0, board, r, c, c_row, p1, p2)
        return expectimax_move
        
        raise NotImplementedError('Whoops I don\'t know what to do')
    
    def evaluation_function_poor(self, board):
        
        r = len(board)
        c = len(board[0])
        p1 = self.player_number
        p2 = 1 + p1 % 2
        
        def matches(board, r, c, x, y, p):
            m = np.array([0] * 5)
            n = 0
            for i in range(x, min(x + 4, r)):
                if board[i][y] != p:
                    break
                n += 1
                m[n] += 1
            
            if y + 1 < c and p == board[x][y] == board[x][y + 1]:
                m[2] += 1
                if y + 2 < c and p == board[x][y + 2]:
                    m[3] += 1
                    if y + 3 < c and p == board[x][y + 3]:
                        m[4] += 1
            
            if x + 1 < r and y + 1 < c and p == board[x][y] == board[x + 1][y + 1]:
                m[2] += 1
                if x + 2 < r and y + 2 < c and p == board[x + 2][y + 2]:
                    m[3] += 1
                    if x + 3 < r and y + 3 < c and p == board[x + 3][y + 3]:
                        m[4] += 1
            
            
            if x + 1 < r and y - 1 >= 0 and p == board[x][y] == board[x + 1][y - 1]:
                m[2] += 1
                if x + 2 < r and y - 2 >= 0 and p == board[x + 2][y - 2]:
                    m[3] += 1
                    if x + 3 < r and y - 3 >= 0 and p == board[x + 3][y - 3]:
                        m[4] += 1
            
            return m
        
        hue = 0
        for j in range(c):
            for i in range(r):
                if board[i][j] == 0:
                    continue
                m = matches(board, r, c, i, j, p1)
                if board[i][j] != p1:
                    m *= -1
                hue += 1000 * m[4] + 100 * m[3] + 10 * m[2]
                #break
         
        return hue
    
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
        
        def matches(board, n, p):
            def getc(s1, s2):
                return s2.count(s1) if s1 in s2 else 0
           
            def getp(s):
                return ''.join(s.astype(str))
 
            def hc(b, ptrn):
                mat = 0
                for row in b:
                     mat += getc(ptrn, getp(row))
                return mat
            
            def plankc(b, ptrn):
                mat = 0
                for op in [None, np.fliplr]:
                    board1 = op(b) if op else b
                    mat += getc(ptrn, getp(np.diagonal(board1, offset = 0).astype(np.int64)))
                    for i in range(1, b.shape[1] - 3):
                        for j in [i, -i]:
                            mat += getc(ptrn, getp(np.diagonal(board1, offset = j).astype(np.int64)))
                return mat
            ptrn = ('{0}' * n).format(p)
            return hc(board, ptrn) + hc(board.T, ptrn) + plankc(board, ptrn)

        p1 = self.player_number
        p2 = 1 + p1 % 2
        
        '''
        s14 = ('{0}' * 4).format(p1)
        s13 = ('{0}' * 3).format(p1) #+ '0'
        s12 = ('{0}' * 2).format(p1) #+ '00'
               
        s24 = ('{0}' * 4).format(p2)
        s23 = ('{0}' * 3).format(p2) #+ '0'
        s22 = ('{0}' * 2).format(p2) #+ '00'

        import itertools


        s13 = ["".join(s) for s in list(set(itertools.permutations(s13)))]
        s12 = ["".join(s) for s in list(set(itertools.permutations(s12)))]
        s23 = ["".join(s) for s in list(set(itertools.permutations(s23)))]
        s22 = ["".join(s) for s in list(set(itertools.permutations(s22)))]
        '''
        hue = (matches(board, 4, p1) - matches(board, 4, p2)) * 100 \
            + (matches(board, 3, p1) - matches(board, 3, p2)) * 10 \
            + (matches(board, 2, p1) - matches(board, 2, p2)) * 1
        return hue

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

