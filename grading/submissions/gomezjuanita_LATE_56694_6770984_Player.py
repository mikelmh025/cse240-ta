import numpy as np

class Node:
    """
    This class describes a single node contained within a graph. 
    """    
    def __init__(self, board, player_number, depth, col_move):
        self.board = board
        self.player_number = player_number
        self.depth = depth
        self.col_move = col_move
        
        if depth < 2:
            children_player_number = (self.player_number%2)+1
            children_depth = depth + 1
            children = []
            valid_cols = []
            for col in range(board.shape[1]):
                if 0 in board[:,col]:
                    valid_cols.append(col)
            for move in valid_cols:
                board_next = board.copy()
                row = 5
                for idx, x in enumerate(board_next[:,move]):
                    if x>0:
                        row=idx-1
                        break    
                board_next[row,move] = children_player_number
                children.append(Node(board_next, children_player_number, children_depth, move))
            self.children = children
        else:
            self.children = []
    
    
class AIPlayer:
    def __init__(self, player_number):
        self.player_number = player_number
        self.type = 'ai'
        self.player_string = 'Player {}:ai'.format(player_number)
    
    def alphabeta(self, node, is_max, alpha, beta):
         """
        Given a node, return the value for the board corresponding to the node
        using alpha beta pruning algorithm


        INPUTS:
        node - a tree like structure that contains the board configuration
        is_max - checks whether the node is a min or a max node
        alpha, beta - parameters for the pruning

        RETURNS:
        The utility value for the node
        """
        # alpha (a) = MAX's best option on path to root
        # beta (b)  = MIN's best option on path to root 
        
        if len(node.children) == 0:
            return self.evaluation_function(node.board)
        elif is_max==True:
            value = -np.inf
            for child in node.children:
                value = max(value, self.alphabeta(child, False, alpha, beta))
                alpha = max(alpha,value)
                if beta<=alpha:
                    break
            return value
        else:
            value = np.inf
            for child in node.children:
                value = min(value, self.alphabeta(child,True, alpha, beta))
                beta = min(beta,value)
                if beta<=alpha:
                    break
            return value
        
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
        alpha = -np.inf
        beta = np.inf
        
        next_player = (self.player_number%2)+1
        current_node = Node(board, next_player, 0, 100)
        values = []
        for child in current_node.children:
            values.append(self.alphabeta(child, False, alpha, beta))
        value = max(values)
        move_idx = values.index(value) 
        move = current_node.children[move_idx].col_move
        return move

    def expectimax(self, node, is_max):
        """
        Given a node, return the value for the board corresponding to the node
        using expectimax algorithm


        INPUTS:
        node - a tree like structure that contains the board configuration
        is_max - checks whether the node is a min or a max node

        RETURNS:
        The utility value for the node
        """
        if len(node.children) == 0:
            return self.evaluation_function(node.board)
        elif is_max==True:
            value = -np.inf
            for child in node.children:
                value = max(value, self.expectimax(child,False))
            return value
        else:
            value = 0
            probability = 1/len(node.children)
            for child in node.children:
                value += self.expectimax(child, True)*probability
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
        next_player = (self.player_number%2)+1
        current_node = Node(board, next_player, 0, 100)
        values = []
        for child in current_node.children:
            values.append(self.expectimax(child, False))
        value = max(values)
        move_idx = values.index(value) 
        move = current_node.children[move_idx].col_move
        return move
    
    
    def count_longest_string(self, board, player_number):
        """  
        Given the board and a player number returns an array with the longest string of the player number 
        in each: rows, columns and diagonals

        INPUTS:
        board - array with current board state
        player_number - number with current player number

        """   
        str_four = '{0}{0}{0}{0}'.format(player_number)
        str_three = ['{0}{0}{0}0'.format(player_number),'0{0}{0}{0}'.format(player_number)]
        str_two = ['0{0}{0}0'.format(player_number), '00{0}{0}'.format(player_number), '{0}{0}00'.format(player_number)]
        
        highest_str = [0, 0, 0]
        to_str = lambda a: ''.join(a.astype(str))
        
        # Check what is the greatest amount of player one horizontal spaces in a row
        for row in board:
            if str_four in to_str(row):
                highest_str[0] = 4
            elif any(string in to_str(row) for string in str_three):
                highest_str[0] = 3
            elif any(string in to_str(row) for string in str_two):
                highest_str[0] = 2
        # Check what is the greatest amount of player one vertical spaces in a row
        for row in board.T: 
            if str_four in to_str(row):
                highest_str[1] = 4
            elif any(string in to_str(row) for string in str_three):
                highest_str[1] = 3
            elif any(string in to_str(row) for string in str_two):
                highest_str[1] = 2
        
        # Check what is the greatest amount of player diaongal spaces in a row
        for op in [None, np.fliplr]:
            op_board = op(board) if op else board
            
            root_diag = np.diagonal(op_board, offset=0).astype(np.int)
            if str_four in to_str(root_diag):
                highest_str[2] = 4
            elif any(string in to_str(root_diag) for string in str_three):
                highest_str[2] = 3
            elif any(string in to_str(root_diag) for string in str_two):
                highest_str[2] = 2
    
            for i in range(1, board.shape[1]-3):
                for offset in [i, -i]:
                    diag = np.diagonal(op_board, offset=offset)
                    diag = to_str(diag.astype(np.int))
                    if highest_str[2]<4 and str_four in diag:
                        highest_str[2] = 4
                    elif highest_str[2]<3 and any(string in diag for string in str_three):
                        highest_str[2] = 3
                    elif highest_str[2]<2 and any(string in diag for string in str_two):
                        highest_str[2] = 2
    
        return highest_str
        
            
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
        current = self.player_number
        enemy = (current%2)+1
        high_current = self.count_longest_string(board, current)
        high_enemy = self.count_longest_string(board, enemy)
        
        if 4 in high_current:
            score += 1000
        if 4 in high_enemy:
            score += (- 1000)
        if 4 not in high_current and 4 not in high_enemy:
            if 3 in high_current:
                  score += 50
            if 2 in high_current:
                  score += 20
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

