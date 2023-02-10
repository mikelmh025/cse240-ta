import numpy as np
import random 


def check_for_row_termination(board):
    for i in range(len(board)):
        for j in range(len(board[0]) - 4):
            if board[i][j] == board[i][j + 1] == board[i][j + 2] == board[i][j + 3]:
                return True

def check_for_column_termination(board):
    for i in range(len(board) - 4):
        for j in range(len(board[0])):
            if board[i][j] == board[i + 1][j] == board[i  +2][j] == board[i+ 3][j]:
                return True

def check_for_diagonal_termination(board):
    for i in range(len(board) - 4):
        for j in range(len(board[0]) - 4):
            if board[i][j] == board[i + 1][j + 1] == board[i  +2][j + 2] == board[i+ 3][j + 3]:
                return True

def check_for_termination(board):
    if check_for_row_termination(board) or check_for_column_termination(board) or check_for_diagonal_termination(board):
        return True
    else:
        return False

def generate_successor_indices(board): 

    successor_indices = {}

    def generate_successor(board, column):
        first_non_zero_row = 0
        for row in board:
            if row[column] == 0:
               first_non_zero_row += 1
        return first_non_zero_row - 1

                
    num_columns = len(board[0])
    for columns in range(num_columns):
        row = generate_successor(board, columns)
        if row <= 0:
            continue
        else:
            successor_indices[columns] = row 
    return successor_indices

def left_heuristic(board, row, player):
    col_cons = 0
    for i in range(len(board[0]) - 1,0,-1):
        if board[row][i] == player:
            col_cons += 1
        else:
            break
    return col_cons

def right_heuristic(board, row, player):
    col_cons = 0
    for i in range(len(board[0])):
        if board[row][i] == player:
            col_cons += 1
        else:
            break
    return col_cons

def bottom_heuristic(board, start, col, player):
    row_cons = 0
    for i in range(start, len(board)):
        if board[i][col] == player:
            row_cons += 1
        else:
            break
    return row_cons



def evaluation_function(player, board):
    horizontal_value = 0
    bottom_value = 0
    heuristic = []
    vals = []
    largest_value = -np.inf
    max = -np.inf

    if player == 1:
        adversary = 2
    else:
        adversary = 1


    moves_indices = generate_successor_indices(board)
    
    for col in moves_indices:
        start = moves_indices[col]
        horizontal_value_player = right_heuristic(board, start, player)
        vals.append(horizontal_value_player)

        bottom_value_player = bottom_heuristic(board, start, col, player) 
        vals.append(bottom_value_player)

        horizontal_value_adversary = right_heuristic(board, start, adversary)
        bottom_value_adversary = bottom_heuristic(board, start, col, adversary)

        left_value_player = left_heuristic(board, start, player)
        vals.append(left_value_player)

        left_value_adversary = left_heuristic(board, start,  adversary)

        heuristic_value = horizontal_value_player + bottom_value_player + left_value_player
        
        if start >= 1 and board[start - 1][col] == 0:
            heuristic_value += 2

        if horizontal_value_adversary >= 2 or bottom_value_adversary >= 2 or left_value_adversary >= 2:
            for i in range(len(vals)):
                if largest_value < vals[i]:
                    largest_value = vals[i]
            larger_advantage = largest_value
            heuristic_value =  heuristic_value  +  100*(larger_advantage)

        heuristic.append(heuristic_value)

        
        for i in range(len(heuristic)):
            if max < heuristic[i]:
                max = heuristic[i]
        
    return max
    

def get_alpha_beta(board, alpha, beta, depth, player, adversary):

    value_indices = {}
    optimal_col = 0
    max = -np.inf
    successor_indices = generate_successor_indices(board)
    for col in successor_indices:
        board[successor_indices[col]][col] = player
        value = best_min(board, alpha, beta, player, adversary, depth + 1)
        if value > max:
            max = value
        value_indices[value] = col
        board[successor_indices[col]][col] = 0
    for key in value_indices:
        if key == max:
            optimal_col = value_indices[key]
          
    return optimal_col  

def best_min(board, alpha, beta, player, adversary, depth):

    successors = generate_successor_indices(board)
    if depth == 3 or len(successors) == 0:
        return evaluation_function(player, board)
    for column in successors:
        board[successors[column]][column] = adversary
        current_value = best_max(board, alpha, beta, player, adversary, depth + 1)
        if current_value <= beta:
            beta = current_value
        board[successors[column]][column] = 0
        if beta <= alpha:
            return beta
    return beta

def best_max(board, alpha, beta, player, adversary, depth):
    successors = generate_successor_indices(board)
    if(depth == 3 or len(successors) == 0):
        print(evaluation_function(player, board))
        return evaluation_function(player, board)
    for column in successors:
        board[successors[column]][column] = player
        current_value = best_min(board, alpha, beta, player, adversary, depth+ 1)
        if current_value > alpha:
            alpha = current_value
        board[successors[column]][column] = 0
        if beta < alpha or alpha == beta:
            return beta
    
    return beta

def get_expectimax(board, depth, player, adversary):

    value_indices = {}
    optimal_col = 0
    max = -np.inf
    successor_indices = generate_successor_indices(board)
    for col in successor_indices:
        board[successor_indices[col]][col] = player
        value = best_expectimax(board, player, adversary, depth - 1)
        if value >= max:
            max = value
        value_indices[value] = col
        board[successor_indices[col]][col] = 0
    for key in value_indices:
        if key == max:
            optimal_col = value_indices[key]
          
    return optimal_col  

def best_max_expectimax(board,  player, adversary, depth):
    successors = generate_successor_indices(board)
    max = -np.inf
    if depth == 3 or len(successors) == 0:
        return evaluation_function(player, board)
    for column in successors:
        board[successors[column]][column] = player
        current_value = best_expectimax(board,  player, adversary, depth - 1)
        if current_value > max:
            max = current_value       
    return max

def best_expectimax(board,  player, adversary, depth):
    successors = generate_successor_indices(board)
    max = -np.inf
    expectation = 0
    if depth == 3 or len(successors) == 0 :
        return evaluation_function(player, board)
    for column in successors:
        board[successors[column]][column] = player
        current_value = best_max_expectimax(board,  player, adversary, depth - 1)
        expectation += current_value      
    return expectation/len(successors)

class AIPlayer:
    def __init__(self, player_number):
        self.player_number = player_number
        self.type = 'ai'
        self.player_string = 'Player {}:ai'.format(player_number)
    
        
    

    
    def get_alpha_beta_move(self,board):
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

        '''
        player-1 is max, player-2 is min,...
        '''


        if self.player_number == 1:
            adversary = 2
        else:
            adversary = 1

        return get_alpha_beta(board, -np.inf, np.inf, 1, self.player_number, adversary)

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

        if self.player_number == 1:
            adversary = 2
        else:
            adversary = 1

        return get_expectimax(board, 4, self.player_number, adversary)

        raise NotImplementedError('Whoops I don\'t know what to do')




    #def evaluation_function(self, board):
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
       
       
        #return 0


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

