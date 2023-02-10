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
        def update_board(ori_board, move, player_num):
            for row in range(5, -1 ,-1):
                if ori_board[row, move] == 0:
                    ori_board[row, move] = player_num
                    break
            return ori_board

        def find_move(board):
            valid_cols = []
            for col in range(board.shape[1]):
                if 0 in board[:,col]:
                    valid_cols.append(col)
            return valid_cols
            
        
        def beta(b_board, player, b, a, depth):
            valid_cols = find_move(b_board)
            branch = []
            for col in range(7):
                if col in valid_cols:
                    temp = update_board(b_board.copy(), col, player)
                    branch.append(temp.copy())
            if len(branch) == 0 or depth <= 0:
                return self.evaluation_function(b_board)

            for choice in branch:
                boardscore = float("inf")
                boardscore = np.minimum(boardscore, alpha(choice, player, b, a, depth - 1))
                b = np.minimum(b, boardscore)
                if b <= a:
                    return b
            return b

        def alpha(a_board, player, b, a, depth):
            valid_cols = find_move(a_board)
            branch = []
            for col in range(7):
                if col in valid_cols:
                    temp = update_board(a_board.copy(), col, player)
                    branch.append(temp.copy())
            if len(branch) == 0 or depth <= 0:
                return self.evaluation_function(a_board)
            for choice in branch:
                boardscore = float("-inf")
                boardscore = np.maximum(boardscore, beta(choice, player, b, a, depth - 1))
                a = np.maximum(a, boardscore)
                if a>= b:
                    return a
            return a
            
            
        valid_cols = find_move(board)

        move = 0
        score = float("-inf")
        a = float("-inf")
        b = float("inf")

        for choice in valid_cols:
            new_board = update_board(board.copy(), choice, self.player_number)
            boardscore = beta(new_board, self.player_number, b, a, 4)
            if boardscore > score:
                score = boardscore
                move = choice
                
        return move
        
        

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
                        return board
            return board

        def find_move(board):
            valid_cols = []
            for col in range(board.shape[1]):
                if 0 in board[:,col]:
                    valid_cols.append(col)
            return valid_cols

        def expect(board, player, depth):
            valid_cols = find_move(board)
            branch = []
            for col in range(7):
                if col in valid_cols:
                    temp = update_board(board.copy(), col, player)
                    branch.append(temp.copy())
            if len(branch) == 0 or depth <= 0:
                return self.evaluation_function(board)
            total = 0
            for choice in branch:
                total += expect(choice, player, depth - 1)

            return total
        
        valid_cols = find_move(board)
                   
        score = float("-inf")
        move = valid_cols[0]
                   
        for choice in valid_cols:
            simu_board = update_board(board.copy(), choice, self.player_number)
            boardscore = expect(simu_board, self.player_number, 3) / 4
            if boardscore > score:
                   score = boardscore
                   move = choice

        return move
        




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
        def Seq_count(board, player, length):
            
            def upvertical(row, col):
                count = 1
                if row < 5:
                    while board[row + 1, col] == board[row, col]:
                        count += 1
                        if row + 1 == 5:
                            break
                        else:
                            row += 1
                if count >= length:
                    return 1
                else:
                    return 0

            def dnvertical(row, col):
                count = 1
                if row > 0:
                    while board[row - 1, col] == board[row, col]:
                        count += 1
                        if row - 1 == 0:
                            break
                        else:
                            row -= 1
                if count >= length:
                    return 1
                else:
                    return 0
                
            def rhorizontal(row, col):
                count = 1
                if col < 6:
                    while board[row, col + 1] == board[row, col]:
                        count += 1
                        if col + 1 == 6:
                            break
                        else:
                            col += 1
                if count >= length:
                    return 1
                else:
                    return 0

            def lhorizontal(row, col):
                count = 1
                if col > 0:
                    while board[row, col - 1] == board[row, col]:
                        count += 1
                        if col - 1 == 0:
                            break
                        else:
                            col -= 1
                if count >= length:
                    return 1
                else:
                    return 0

            def dnrDiagonal(row, col):
                count = 1
                if row > 0 and col < 6:
                    while board[row - 1, col + 1] == board[row, col]:
                        count += 1
                        if row - 1 == 0 or col + 1 == 6:
                            break
                        else:
                            row -= 1
                            col += 1
                if count >= length:
                    return 1
                else:
                    return 0

            def dnlDiagonal(row, col):
                count = 1
                if row > 0 and col > 0:
                    while board[row - 1, col - 1] == board[row, col]:
                        count += 1
                        if row - 1 == 0 or col - 1 == 0:
                            break
                        else:
                            row -= 1
                            col -= 1
                if count >= length:
                    return 1
                else:
                    return 0

            def uprDiagonal(row, col):
                count = 1
                if row < 5 and col < 6:
                    while board[row + 1, col + 1] == board[row, col]:
                        count += 1
                        if row + 1 == 5 or col + 1 == 6:
                            break
                        else:
                            row += 1
                            col += 1
                if count >= length:
                    return 1
                else:
                    return 0

            def uplDiagonal(row, col):
                 count = 1
                 if row < 5 and col > 0:
                     while board[row + 1, col - 1] == board[row, col]:
                         count += 1
                         if row + 1 == 5 or col - 1 == 0:
                             break
                         else:
                             row += 1
                             col -= 1
                 if count >= length:
                     return 1
                 else:
                     return 0

            total = 0

            for row in range(6):
                for col in range(7):
                    if board[row, col] == player:
                        total += (upvertical(row, col) + dnvertical(row, col))
                        total += (rhorizontal(row, col) + lhorizontal(row, col))
                        total += (uprDiagonal(row, col) + uplDiagonal(row, col))
                        total += (dnrDiagonal(row, col) + dnlDiagonal(row, col))
            return total

        fours    = Seq_count(board, self.player_number, 4)
        threes   = Seq_count(board, self.player_number, 3)
        twos     = Seq_count(board, self.player_number, 2)
        score = fours * 1000 + threes * 50 + twos * 5
        
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

