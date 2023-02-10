import numpy as np

class Observer:
    def __init__(self):
        self.max_depth = 3
        self.max_radius = 3
    
        self.offsets = [(-1,-1),(1,1),(-1,0),(1,0),(-1,1),(1,-1),(0,-1),(0,1)]
    
    def get_actions(self, board):
        actions = []
        
        for col in range(board.shape[1]):
            result = np.where(board[:,col] == 0)
            if len(result) == 0:
                continue
            
            open_spots = result[0]
            if len(open_spots) <= 1:
                continue
            
            actions.append((np.max(open_spots), col))

        return actions
    
    def get_top_positions(self, board):
        """
        returns the position 
        """
        actions = []
        
        for col in range(board.shape[1]):
            result = np.where(board[:,col] == 0)

            # column is full
            if len(result) == 0:
                continue
            
            # no piece in this row
            open_spots = result[0]
            if len(open_spots) == 0 or len(open_spots) == 6:
                continue
            
            actions.append((np.max(open_spots) + 1, col))

        return actions

    def get_top_pieces(self, board):
        top_positions = self.get_top_positions(board)
        return [(board[pos[0]][pos[1]], pos) for pos in top_positions]

    def get_options(self, board, player_id):
        def create_option(row, col):
            option = np.copy(board)
            option[row][col] = player_id
            return option
        
        return [(pos[1], create_option(pos[0], pos[1])) for pos in self.get_actions(board)]

    
    def get_option_scores(self, board, player_id, row, col):
        def branch(row_idx, col_idx, offset, radius=1):
            curr_row_idx = row_idx + (offset[0] * radius)
            curr_col_idx = col_idx + (offset[1] * radius)

            if curr_row_idx < 0 or curr_row_idx >= board.shape[0]:
                return 0, False
            if curr_col_idx < 0 or curr_col_idx >= board.shape[1]:
                return 0, False
            if radius > self.max_radius:
                return 0, False # this does may not know if the next one is blocking
            if player_id != board[curr_row_idx][curr_col_idx]:
                if board[curr_row_idx][curr_col_idx] == 0:
                    return 0, False
                else:
                    return 0, True # reason for stop was opponent blocking
            
            result = branch(row_idx, col_idx, offset, radius + 1)
            return result[0] + 1, result[1]
       
        values = [branch(row, col, offset) for offset in self.offsets]
        result = []
        
        for i in range(0, len(values), 2):
            first, was_first_blocked = values[i]
            second, was_second_blocked = values[i + 1]
            total = first + second + 1
            
            # no need to see if total < 4 because if it was >= 4, the
            # game would have been over
            if was_first_blocked == True and was_second_blocked == True:
                total = 0

            result.append(total)
            
        return result
        
        
class AIPlayer:
    def __init__(self, player_number):
        self.player_number = player_number
        self.type = 'ai'
        self.player_string = 'Player {}:ai'.format(player_number)
        self.observer = Observer()
        

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
        # self.evaluation_function(board)
        # print(self.player_number, board)
        
        def compute_max(board, depth, max_depth, alpha, beta):
            if depth >= max_depth:
                return 0, self.evaluation_function(board)
            
            current_value = float("-inf")
            current_col = None
            
            states = self.observer.get_options(board, self.player_number)
            
            for state in states:
                next_col = state[0]
                next_board = state[1]
                
                next_col, next_value = compute_max(next_board, depth + 1, max_depth, alpha, beta)
                if current_value < next_value:
                    current_value = next_value
                    current_col = next_col
                    
                alpha = max(alpha, current_value)
                
                if current_value >= beta:
                    break
            
            return current_col, current_value
        
        def compute_min(board, depth, max_depth, alpha, beta):
            if depth >= max_depth:
                return 0, self.evaluation_function(board)
            
            current_value = float("-inf")
            current_col = None
            
            states = self.observer.get_options(board, self.player_number)
            
            for state in states:
                next_col = state[0]
                next_board = state[1]
                
                next_col, next_value = compute_max(next_board, depth + 1, max_depth, alpha, beta)
                if current_value > next_value:
                    current_value = next_value
                    current_col = next_col
                    
                beta = min(beta, current_value)
                
                if current_value >= beta:
                    break
            
            return current_col, current_value
        return self.get_expectimax_move(board)
        # return compute_max(board, 0, 3, float("-inf"), float("inf"))[0]
     

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
        
        # returns (column index, value)
        def compute(board, probs, depth, max_depth):
            if depth >= max_depth:
                return 0, self.evaluation_function(board)
            
            # (col, board) 
            states = self.observer.get_options(board, self.player_number)
            state_values = [(state[0], compute(state[1], probs, depth + 1, max_depth)) for state in states]
            state_values = list(filter(lambda x: x[1] != None, state_values))
            state_values = [(state_value[0], state_value[1][1]) for state_value in state_values]
            
            if len(state_values) == 0:
                some_actions = self.observer.get_actions(board)
                some_column = some_actions[0][1]
                return some_column, 0
           
            
            if depth % 2 == 0:
                state_values.sort(key=lambda x: x[1], reverse=True)
                return state_values[0]
            else:
                state_value = sum(state_values[i][1] * probs[i] for i in range(len(state_values)))
                return 0, state_value

        num_cols = board.shape[1]
        probs = np.array([1/num_cols] * num_cols)
        return compute(board, probs, 0, 3)[0]
    

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
        
        p1_score = 0
        p2_score = 0
        
        top_pieces = self.observer.get_top_pieces(board)
        for piece in top_pieces:
            player_id, position = piece
            row, col = position
            current_scores = self.observer.get_option_scores(board, player_id, row, col)
            
            # connect 4!
            if 4 in current_scores:
                if player_id == 1:
                    return float("inf")
                else:
                    return float("-inf")
            
            current_score_total = sum([pow(10, value) for value in current_scores])
            
            if player_id == 1:
                p1_score = p1_score + current_score_total
            else:
                p2_score = p2_score + current_score_total
        
        return p1_score - p2_score


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

