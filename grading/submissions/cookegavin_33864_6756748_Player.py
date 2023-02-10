import numpy as np

depth_limit = 4
chance_depth_limit = 3

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
        valid_moves = get_valid_cols(board)
        
        if len(valid_moves) == 0:
            raise Exception('No valid moves.')
        
        # shuffle board (for the case when all moves have the same rating)
        np.random.shuffle(valid_moves)
        
        # get the board states after each possible move
        successor_board_states = []
        for move in valid_moves:
            successor = np.copy(board)
            update_board(successor, move, self.player_number)
            successor_board_states += [successor]
        
        values = []
        alpha = np.NINF
        beta = np.Inf
        for successor in successor_board_states:
            value = 0
            beta = np.Inf
            # If the successor is an ending state, no need to go further
            if check_connected(successor, self.player_number, 4):
                value = 2000
                # can't get better than this, so end loop here
                values += [value]
                break
            else:
                value = min_value(self, successor, 1, alpha, beta)
            values += [value]
            
            # Keep track of alpha after each iteration
            if alpha < value:
                alpha = value
        
        index_max = np.argmax(values)
        
        chosen_move = valid_moves[index_max]
        
        return chosen_move

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
        valid_moves = get_valid_cols(board)
        
        if len(valid_moves) == 0:
            raise Exception('No valid moves.')
        
        # shuffle board (for the case when all moves have the same rating)
        np.random.shuffle(valid_moves)
        
        # get the board states after each possible move
        successor_board_states = []
        for move in valid_moves:
            successor = np.copy(board)
            update_board(successor, move, self.player_number)
            successor_board_states += [successor]
        
        # evaluate each possible move
        values = []
        for successor in successor_board_states:
            value = 0
            # If the successor is an ending state, no need to go further down the tree
            if check_connected(successor, self.player_number, 4):
                value = 1000
                # can't get better than this, so end loop here
                values += [value]
                break
            else:
                value = chance_value(self, successor, 1)
            values += [value]
        
        index_max = np.argmax(values)
        
        chosen_move = valid_moves[index_max]
        
        return chosen_move

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
        value = 0
        # if the ai wins we want a large positive weight
        if check_connected(board, self.player_number, 4):
            return 1000
        
        # find if ai has a 2 in a row / 3 in a row
        for i in range(2,4):
            if check_connected(board, self.player_number, i):
                value += np.power(i, 5)
        
        # set value for opponent
        opponent = 2
        if self.player_number == 2:
            opponent = 1
        
        # if the ai loses we want a large negative weight
        if check_connected(board, opponent, 4):
            return -1000
        
        # find if opponent has has a 3 in a row
        if check_connected(board, opponent, 3):
            value -= np.power(3, 4)
        
        return value


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

# helper functions
# chance node for expectimax
def chance_value(player, board, depth):
    # get all possible moves from this state
    valid_moves = get_valid_cols(board)
    
    if len(valid_moves) == 0:
        return player.evaluation_function(board)
    
    # get the board states after each possible move
    successor_board_states = []
    # change player number to opponents number in update board
    opponent = 2
    if player.player_number == 2:
        opponent = 1
        
    for move in valid_moves:
        successor = np.copy(board)
        update_board(successor, move, opponent)
        successor_board_states += [successor]
    
    # calculate values of sucessors
    values = []
    if depth >= chance_depth_limit:
        # if at limit estimate the values of successors
        for successor in successor_board_states:
            value = player.evaluation_function(successor)
            values += [value]
    else:
        for successor in successor_board_states:
            value = 0
            if check_connected(successor, opponent, 4):
                value = -1000 - (1000 / depth)
            else:
                value = chance_max_value(player, successor, depth + 1)
            values += [value]
    
    returned_value = 0
    
    # All possibilities are weighed equally
    for value in values:
        returned_value += value
    
    returned_value = value / len(values) 
    
    return returned_value

# Non root max node for expectimax
def chance_max_value(player, board, depth):
    # get all possible moves from this state
    valid_moves = get_valid_cols(board)
    
    if len(valid_moves) == 0:
        return player.evaluation_function(board)
    
    # get the board states after each possible move
    successor_board_states = []
    for move in valid_moves:
        successor = np.copy(board)
        update_board(successor, move, player.player_number)
        successor_board_states += [successor]
    
    # calculate values of sucessors
    values = []
    if depth >= chance_depth_limit:
        for successor in successor_board_states:
            value = player.evaluation_function(successor)
            values += [value]
    else:
        for successor in successor_board_states:
            value = 0
            if check_connected(successor, player.player_number, 4):
                value = 1000 + (1000/(depth+1))
            else:
                value = chance_value(player, successor, depth + 1)
            values += [value]
    
    returned_value = max(values)
    
    return returned_value

# Non root max node for alpha-beta minimax
def max_value(player, board, depth, alpha=np.NINF, beta=np.Inf):
    # get all possible moves from this state
    valid_moves = get_valid_cols(board)
    
    if len(valid_moves) == 0:
        return player.evaluation_function(board)
    
    # get the board states after each possible move
    successor_board_states = []
    for move in valid_moves:
        successor = np.copy(board)
        update_board(successor, move, player.player_number)
        successor_board_states += [successor]
    
    # calculate values of sucessors
    values = []
    if depth >= depth_limit:
        for successor in successor_board_states:
            value = player.evaluation_function(successor)
            values += [value]
    else:
        for successor in successor_board_states:
            value = 0
            if check_connected(successor, player.player_number, 4):
                value = 1000 + (1000/(depth+1))
            else:
                value = min_value(player, successor, depth + 1, alpha, beta)
            values += [value]
            # Prune if max value is guarenteed to be no lower than beta.
            # Since the min layer will never choose this path.
            if alpha < value:
                alpha = value
            if value >= beta:
                break
    
    returned_value = max(values)
    
    return returned_value

# Min node for alpha-beta minimax
def min_value(player, board, depth, alpha=np.NINF, beta=np.Inf):
    # get all possible moves from this state
    valid_moves = get_valid_cols(board)
    
    if len(valid_moves) == 0:
        return player.evaluation_function(board)
    
    # get the board states after each possible move
    successor_board_states = []
    # change player number to opponents number in update board
    opponent = 2
    if player.player_number == 2:
        opponent = 1
        
    for move in valid_moves:
        successor = np.copy(board)
        update_board(successor, move, opponent)
        successor_board_states += [successor]
    
    # calculate values of sucessors
    values = []
    if depth >= depth_limit:
        # if at limit estimate the values of successors
        for successor in successor_board_states:
            value = player.evaluation_function(successor)
            values += [value]
    else:
        for successor in successor_board_states:
            value = 0
            if check_connected(successor, opponent, 4):
                value = -1000 - (1000 / depth)
            else:
                value = max_value(player, successor, depth + 1, alpha, beta)
            
            values += [value]
            # Prune if min value is already guarenteed to be no higher than alpha
            # Since the max layer will never choose this path.
            if beta > value:
                beta = value
            if value <= alpha:
                break
    
    returned_value = min(values)
    
    return returned_value

# returns list of valid moves
# copied from random player
def get_valid_cols(board):
    valid_cols = []
    for col in range(board.shape[1]):
        if 0 in board[:,col]:
            valid_cols.append(col)
    return valid_cols

# copied and modified from the version in ConnectFour.py
# takes a board, move(column id?), and player_number and updates the board accordingly
def update_board(board, move, player_num):
    if 0 in board[:,move]:
        update_row = -1
        for row in range(1, board.shape[0]):
            update_row = -1
            if board[row, move] > 0 and board[row-1, move] == 0:
                update_row = row-1
            elif row==board.shape[0]-1 and board[row, move] == 0:
                update_row = row

            if update_row >= 0:
                board[update_row, move] = player_num
                break
    else:
        err = 'Invalid move by player {}. Column {}'.format(player_num, move)
        raise Exception(err)

# copied and modified from the version in ConnectFour.py
# takes board, player number, and the length of the in-a-row to match.
def check_connected(board, player_num, length):
    player_str = ""
    for i in range(0, length):
        player_str += '{0}'
    
    player_str = player_str.format(player_num)
    to_str = lambda a: ''.join(a.astype(str))
    
    def check_horizontal(b):
        for row in b:
            if player_str in to_str(row):
                return True
        return False

    def check_verticle(b):
        return check_horizontal(b.T)

    def check_diagonal(b):
        for op in [None, np.fliplr]:
            op_board = op(b) if op else b
            
            root_diag = np.diagonal(op_board, offset=0).astype(np.int)
            if player_str in to_str(root_diag):
                return True

            for i in range(1, b.shape[1]-3):
                for offset in [i, -i]:
                    diag = np.diagonal(op_board, offset=offset)
                    diag = to_str(diag.astype(np.int))
                    if player_str in diag:
                        return True

        return False

    return (check_horizontal(board) or
            check_verticle(board) or
            check_diagonal(board))