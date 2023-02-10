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
        # raise NotImplementedError('Whoops I don\'t know what to do')
        # print("===== a new move =====")
        best_value = float('-inf')
        best_col = -1
        depth = 3
        for col in range(board.shape[1]):
            row = self.next_empty_row(board, col)
            if row < 0:
                continue
            
            board[row][col] = self.player_number
            # print("Moves. col: ", col, end = "; ")
            value = self.alpha_beta(board, float('-inf'), float('inf'), False, depth)
            # print("=== , max value: ", value)
            if value > best_value:
                best_value = value
                best_col = col
            board[row][col] = 0 

        return best_col

    def alpha_beta(self, board, alpha, beta, maximazing, depth):
        state = self.is_game_over(board)
        if state == self.player_number:
            return 10000000
        elif state == self.get_opp_player(self.player_number):
            return -10000000
        if depth == 0:
            return self.evaluation_function(board)
        
        if maximazing:
            value = float('-inf')
            for col in range(board.shape[1]):
                row = self.next_empty_row(board, col)
                if row < 0:
                    continue

                board[row][col] = self.player_number
                # print("self col: ", col, end = "; ")
                value = max(value, self.alpha_beta(board, alpha, beta, False, depth-1))
                # print(", max value: ", value)
                board[row][col] = 0

                alpha = max(alpha, value)
                if alpha >= beta: 
                    break
            return value
        else:
            value = float('inf')
            for col in range(board.shape[1]):
                row = self.next_empty_row(board, col)
                if row < 0:
                    continue
                
                board[row][col] = self.get_opp_player(self.player_number)
                # print("opp col: ", col, end = "; ")
                value = min(value, self.alpha_beta(board, alpha, beta, True, depth-1))
                # print(", min value: ", value)
                board[row][col] = 0

                beta = min(beta, value)
                if alpha >= beta: 
                    break
            return value
        
    
    def next_empty_row(self, board, col):
        for row in range(board.shape[0] - 1, -1, -1):
            if board[row][col] == 0:
                return row
        return -1
    
    def get_opp_player(self, cur_player):
        if cur_player == 1:
            return 2
        return 1

    def game_completed(self, board, player_num):
        player_win_str = '{0}{0}{0}{0}'.format(player_num)
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
                
                root_diag = np.diagonal(op_board, offset=0).astype(np.int)
                if player_win_str in to_str(root_diag):
                    return True

                for i in range(1, b.shape[1]-3):
                    for offset in [i, -i]:
                        diag = np.diagonal(op_board, offset=offset)
                        diag = to_str(diag.astype(np.int))
                        if player_win_str in diag:
                            return True

            return False

        return (check_horizontal(board) or
                check_verticle(board) or
                check_diagonal(board))
    
    def is_game_over(self, board): # 0: draw, -1: game not over, or winner player num
        if self.game_completed(board, self.get_opp_player(self.player_number)):
            return self.get_opp_player(self.player_number)
        if self.game_completed(board, self.player_number):
            return self.player_number
        # check if any empty blocks are remaining
        for row in range(board.shape[0]):
            for col in range(board.shape[1]):
                if board[row][col] == 0:
                    return -1
        return 0 # draw

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
        # raise NotImplementedError('Whoops I don\'t know what to do')
        # print("===== a new move =====")
        best_value = float('-inf')
        best_col = -1
        depth = 3
        for col in range(board.shape[1]):
            row = self.next_empty_row(board, col)
            if row < 0:
                continue
            
            board[row][col] = self.player_number
            # print("Moves. col: ", col, end = "; ")
            value = self.expectimax(board, False, depth)
            # print("=== , max value: ", value)
            if value > best_value:
                best_value = value
                best_col = col
            board[row][col] = 0 

        return best_col
    
    def expectimax(self, board, maximazing, depth):
        state = self.is_game_over(board)
        if state == self.player_number:
            return 1000000
        elif state == self.get_opp_player(self.player_number):
            return -1000000
        if depth == 0:
            return self.evaluation_function(board)
        
        if maximazing:
            value = float('-inf')
            for col in range(board.shape[1]):
                row = self.next_empty_row(board, col)
                if row < 0:
                    continue

                board[row][col] = self.player_number
                # print("self col: ", col, end = "; ")
                value = max(value, self.expectimax(board, False, depth-1))
                # print(", max value: ", value)
                board[row][col] = 0
            return value
        else:
            value = 0
            count = 0
            for col in range(board.shape[1]):
                row = self.next_empty_row(board, col)
                if row < 0:
                    continue
                
                board[row][col] = self.get_opp_player(self.player_number)
                # print("opp col: ", col, end = "; ")
                value += self.expectimax(board, True, depth - 1)
                count += 1
                # print(", avg value: ", value)
                board[row][col] = 0
            return value/count

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
        points = [0, 1, 2, 25]
        def horizontalScore(row, col, player):
            count = 0
            for i in range(3):
                if col + i < board.shape[1] and board[row][col + i] == player:
                    count += 1
                else:
                    break
            return points[count]
        
        def verticalScore(row, col, player):
            count = 0
            for i in range(3):
                if row + i < board.shape[0] and board[row + i][col] == player:
                    count += 1
                else:
                    break
            return points[count]
        
        def leftDiagonalScore(row, col, player):
            count = 0
            for i in range(3):
                if row + i < board.shape[0] and col + i < board.shape[1] and board[row + i][col + i] == player:
                    count += 1
                else:
                    break
            return points[count]
        
        def rightDiagonalScore(row, col, player):
            count = 0
            for i in range(3):
                if row + i < board.shape[0] and col - i < board.shape[1] and board[row + i][col - i] == player:
                    count += 1
                else:
                    break
            return points[count]
        
        def score(player):
            score = 0
            for row in range(board.shape[0]):
                for col in range(board.shape[1]):
                    if board[row][col] == player:
                        score += horizontalScore(row, col, player)
                        score += verticalScore(row, col, player)
                        score += leftDiagonalScore(row, col, player)
                        score += rightDiagonalScore(row, col, player)
                        score -= 3
            return score
        
        score_cur = score(self.player_number)
        score_opp = score(self.get_opp_player(self.player_number))
        # score1 for current player
        return score_cur - score_opp


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

