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
        if (board == self.player_number).sum() == 0 or (board == (3 - self.player_number)).sum() == 1:
            if board[5][3] == 0:
                return 3
            else:
                return 2
        def alpha_beta_search(board, depth, alpha, beta, player):
            if depth == 0 or self.game_completed(board):
                return self.evaluation_function(board)
            if player:
                value = float('-inf')
                for action in self.get_move(board):
                    new_board = self.get_next_board(board, action)
                    value = max(value, alpha_beta_search(new_board, depth - 1, alpha, beta, False))
                    alpha = max(alpha, value)
                    if alpha >= beta:
                        break
                return value
            else:
                value = float('inf')
                for action in self.get_move(board):
                    new_board = self.get_next_board(board, action)
                    value = min(value, alpha_beta_search(new_board, depth - 1, alpha, beta, True))
                    beta = min(beta, value)
                    if alpha >= beta:
                        break
                return value

        best_score = float('-inf')
        best_move = None
        for action in self.get_move(board):
            new_board = self.get_next_board(board, action)
            v = alpha_beta_search(new_board, 0, float('-inf'), float('inf'), False)
            if v > best_score:
                best_score = v
                best_move = action
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
        if (board == self.player_number).sum() == 0 or (board == (3 - self.player_number)).sum() == 1:
            if board[5][3] == 0:
                return 3
            else:
                return 2
        def value(board, depth, player):
            if depth <= 0 or self.game_completed(board):
                return self.evaluation_function(board)
            if player:
                return max_value(board, depth)
            else:
                return exp_value(board, depth)
            
        def max_value(board, depth):
            v = float('-inf')
            for action in self.get_move(board):
                v = max(v, value(self.get_next_board(board, action), depth - 1, False))
            return v
        
        def exp_value(board, depth):
            v = 0
            for action in self.get_move(board):
                v += value(self.get_next_board(board, action), depth - 1, True)
            return v/len(self.get_move(board))
        
        best_score = float('-inf')
        best_action = None
        for action in self.get_move(board):
            new_board = self.get_next_board(board, action)
            v = value(new_board, 0, False)
            if v > best_score:
                best_score = v
                best_action = action
        return best_action
        




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
        self_connect_two = self.self_connected_nodes(board, 2)
        self_connect_three = self.self_connected_nodes(board, 3)
        self_connect_four = self.self_connected_nodes(board, 4)
        block_nodes_three = self.block_nodes_of_three(board)
        block_nodes_two = self.block_nodes_of_two(board)
        return self_connect_two + self_connect_three * 3 + self_connect_four * 10000 + block_nodes_three + block_nodes_two
    
    
    
    def block_nodes_of_three(self, board):
        block_list = []
        for i in range(4):
            temp = (str(3-self.player_number) * (3-i) 
            + str(self.player_number) + str(3-self.player_number)* i)
            block_list.append(temp)

        to_str = lambda a: ''.join(a.astype(str))
        
        def check_horizontally(b):
            count = 0
            for row in b:
                if block_list[0] in to_str(row) and block_list[3] in to_str(row):
                    count += 5000
                elif any(f in to_str(row) for f in block_list):
                    count += 1000
            return count
        def check_vertically(b):
            return check_horizontally(b.T)
        def check_diagonally(b):
            count = 0
            for op in [None, np.fliplr]:
                op_board = op(b) if op else b
                root_diag = np.diagonal(op_board, offset=0).astype(int)
                if block_list[0] in to_str(root_diag) and block_list[3] in to_str(root_diag):
                    count+=5000
                if any(b in to_str(root_diag) for b in block_list):
                    count+=1000

                for i in range(1, b.shape[1]-3):
                    for offset in [i, -i]:
                        diag = np.diagonal(op_board, offset=offset)
                        diag = to_str(diag.astype(int))
                        if block_list[0] in diag and block_list[3] in diag:
                          count+=5000
                        if any(b in diag for b in block_list):
                          count+=1000
            return count
        return check_horizontally(board) + check_vertically(board)  + check_diagonally(board)
    
    def block_nodes_of_two(self, board):
        block_list = []
        for i in range(3):
            temp = (str(3-self.player_number) * (2-i) 
            + str(self.player_number) + str(3-self.player_number)* i)
            block_list.append(temp)

        to_str = lambda a: ''.join(a.astype(str))
        
        def check_horizontally(b):
            count = 0
            for row in b:
                if block_list[0] in to_str(row) and block_list[2] in to_str(row):
                    count += 20
                elif any(f in to_str(row) for f in block_list):
                    count += 15
            return count
        def check_vertically(b):
            return check_horizontally(b.T)
        def check_diagonally(b):
            count = 0
            for op in [None, np.fliplr]:
                op_board = op(b) if op else b
                root_diag = np.diagonal(op_board, offset=0).astype(int)
                if block_list[0] in to_str(root_diag) and block_list[2] in to_str(root_diag):
                    count+=20
                if any(b in to_str(root_diag) for b in block_list):
                    count+=10

                for i in range(1, b.shape[1]-3):
                    for offset in [i, -i]:
                        diag = np.diagonal(op_board, offset=offset)
                        diag = to_str(diag.astype(int))
                        if block_list[0] in diag and block_list[2] in diag:
                          count+=20
                        if any(b in diag for b in block_list):
                          count+=10
            return count
        return check_horizontally(board) + check_vertically(board)  + check_diagonally(board)    
      
    def self_connected_nodes(self, board, num):
        player_win_str = str(self.player_number) * num
        to_str = lambda a: ''.join(a.astype(str))
        
        def check_horizontal(b):
            count = 0
            for row in b:
                if player_win_str in to_str(row):
                    count += 5
            return count

        def check_verticle(b):
            return check_horizontal(b.T)

        def check_diagonal(b):
            count = 0
            for op in [None, np.fliplr]:
                op_board = op(b) if op else b
                
                root_diag = np.diagonal(op_board, offset=0).astype(int)
                if player_win_str in to_str(root_diag):
                    count+= 4

                for i in range(1, b.shape[1]-3):
                    for offset in [i, -i]:
                        diag = np.diagonal(op_board, offset=offset)
                        diag = to_str(diag.astype(int))
                        if player_win_str in diag:
                            count+=4

            return count

        return (check_horizontal(board) +
                check_verticle(board) +
                check_diagonal(board))
    
    
    
    def game_completed(self, board):
        player_win_str = '{0}{0}{0}{0}'.format(self.player_number)
        to_str = lambda a: ''.join(a.astype(str))

        def check_horizontal(b):
            for row in b:
                if player_win_str in to_str(row):
                    return True
            return False

        def check_verticle(b):
            return check_horizontal(b.T)

        def check_diagonal(b):
            for op in [None, np.fliplr]:
                op_board = op(b) if op else b
                
                root_diag = np.diagonal(op_board, offset=0).astype(int)
                if player_win_str in to_str(root_diag):
                    return True

                for i in range(1, b.shape[1]-3):
                    for offset in [i, -i]:
                        diag = np.diagonal(op_board, offset=offset)
                        diag = to_str(diag.astype(int))
                        if player_win_str in diag:
                            return True

            return False

        return (check_horizontal(board) or
                check_verticle(board) or
                check_diagonal(board))
    
    def get_move(self, board):
        valid_cols = []
        for col in range(board.shape[1]):
            if 0 in board[:,col]:
                valid_cols.append(col)

        return valid_cols
    
    def get_next_board(self, board, col):
        next_board = board.copy()
        # take the last 0 in the column
        update_row = np.where(board[:, col] == 0)[0][-1]
        next_board[update_row, col] = self.player_number
        return next_board
    

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

