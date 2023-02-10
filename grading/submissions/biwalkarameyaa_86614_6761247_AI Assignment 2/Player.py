import numpy as np

row_count = 6
column_count = 7    
class AIPlayer:
    def __init__(self, player_number):
        self.player_number = player_number
        self.type = 'ai'
        self.player_string = 'Player {}:ai'.format(player_number)


    ''' 
    def check_win(board, row, col, player):
    # Check horizontal
    count = 0
    for j in range(len(board[0])):
        if board[row][j] == player:
            count += 1
            if count == 4:
                return True
        else:
            count = 0

    # Check vertical : Transpose of the horizontal 
    count = 0
    for i in range(len(board)):
        if board[i][col] == player:
            count += 1
            if count == 4:
                return True
        else:
            count = 0

    # Check diagonal top-left to bottom-right
    count = 0
    i = row
    j = col
    while i >= 0 and i < len(board) and j >= 0 and j < len(board[0]):
        if board[i][j] == player:
            count += 1
            if count == 4:
                return True
        else:
            break
        i += 1
        j += 1

    # Check diagonal top-right to bottom-left
    count = 0
    i = row
    j = col
    while i >= 0 and i < len(board) and j >= 0 and j < len(board[0]):
        if board[i][j] == player:
            count += 1
            if count == 4:
                return True
        else:
            break
        i += 1
        j -= 1

    return False

    '''
#Checking the possible combinations for winning - check horizontal, vertical, as well as diagonals
    def position_count(self, board, digit, player_no):

        win_number = 0 
        win_string = str(player_no) * digit
        c_str = lambda a: ''.join(map(str, a))

        def horizontal_check(x):
          hcount = sum(c_str(row).count(win_string) for row in x)
          return hcount

        def diagonal_check(x):
          dcount = 0
          win_string = str(player_no) * digit
          for operation in [None, np.fliplr]:
              operation_board = operation(x) if operation else x
              diag = np.diagonal(operation_board, offset=0).astype(np.int)
              dcount += c_str(diag).count(win_string)

              
              for i in range(1, x.shape[1] - 3):
                  for offset in [i, -i]:
                      diag = np.diagonal(operation_board, offset=offset).astype(np.int)
                      dcount += c_str(diag).count(win_string)

          return dcount

        def vertical_check(x):
            return horizontal_check(x.T)

        x1=horizontal_check(board)
        y1=vertical_check(board)
        z1=diagonal_check(board)
        win_number = x1+y1+z1
        return win_number

    def Moves(self, board):
        valid_list_moves = []
        #Iterating through the board to make a valid list
        for col in range(column_count):
            for row in range(row_count-1,-1,-1):
                if board[row][col] == 0:
                    valid_list_moves.append([row, col])
                    break
        return valid_list_moves


#Provides the utility score for evaluation using heuristics
    def evaluation_function(self, board):
        
        player = self.player_number
        final_result = 0
        opp_player = 2 if player == 1 else 1
        final_result = self.position_count( board, 4, player) * 2000
        final_result= final_result+self.position_count( board, 3, player) * 200
        final_result= final_result+self.position_count( board, 2, player) * 20
        final_result =final_result-self.position_count( board, 3, opp_player) * 200
        final_result =final_result-self.position_count( board, 2, opp_player) * 20
        final_result =final_result-self.position_count( board, 4, opp_player) * 1950 
        
        
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

        return (final_result)

    
#Alpha Beta Algorithm
    def get_alpha_beta_move(self, board):
        test = []
    
        def alphabeta( board, depth, alpha, beta, player, opp_player):
            for row, col in self.Moves(board):
                board[row][col] = player
                alpha = max(alpha, mini_value(board,alpha, beta,depth + 1 , player, opp_player))
                test.append((alpha,col))
                board[row][col] = 0
            max_tuple = max(test, key=lambda x: x[1])
            maxvalue = max_tuple[0]
            maxindex = [item[1] for item in test if maxvalue in item][0]
            return maxindex

        def mini_value(board,alpha,beta,depth,player, opp_player):
            check_moves = self.Moves(board)
            if(check_moves==False or depth==4):
                return (self.evaluation_function(board))
            for row,col in check_moves:
                board[row][col] = opp_player 
                imp = maxi_value(board, alpha, beta, depth+1, player, opp_player)
                beta = min (beta, imp)
                board[row][col] = 0
                if beta<= alpha:
                    return beta 
            return beta

        def maxi_value(board,alpha, beta, depth, player, opp_player):
            check_moves = self.Moves(board)
            if(check_moves==False or depth==4):
                return (self.evaluation_function(board))
            for row, col in check_moves:
                board[row][col] = player 
                imp = mini_value(board,alpha,beta,depth+1, player, opp_player)
                alpha = max(alpha, imp)
                board[row][col] = 0
                if alpha >= beta:
                    return alpha
            return alpha

        player = self.player_number
        opp_player = 2 if player == 1 else 1
        return (alphabeta(board, 0, float('-inf'),float('inf'), player, opp_player)) 
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
        raise NotImplementedError('Whoops I don\'t know what to do')


#Expectimax algorithm
    def get_expectimax_move(self, board):
        test = []
        def expect_max(board, depth, player, opp_player):
            alpha = float('-inf')
            for row, col in self.Moves(board):
                board[row][col] = player
                alpha = max(alpha, expect_val(board,depth - 1 , player, opp_player))
                test.append((alpha,col))
                board[row][col] = 0

            max_value = max(test, key=lambda x: x[1])[0]
            max1 = next((item[1] for item in test if max_value in item), None)
            return max1

        def maximum_val(board, depth, player,opp_player):
            check_moves = self.Moves(board)
            test_value = float('-inf')
            if (check_moves==False or depth==0): 
                return (self.evaluation_function(board))
            
            for row,col in check_moves:
                board[row][col] = player 
                val = expect_val(board, depth - 1, player, opp_player)
                test_value = max(test_value, val)
            return test_value
        def expect_val(board, depth, player, opp_player): 
            check_moves = self.Moves(board)
            l = len(check_moves)
            print (l)
            expected_value = 0
            if (check_moves==False or depth==0): 
                return (self.evaluation_function(board))
            
            for row,col in check_moves:
                board[row][col] = opp_player 
                val = maximum_val(board , depth-1, player, opp_player)
                expected_value =expected_value+ val


            return (expected_value/l)

        player = self.player_number
        opp_player = 2 if player == 1 else 1
        return (expect_max(board, 8 , player, opp_player))
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

        raise NotImplementedError('Whoops I don\'t know what to do')


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


#References
#https://medium.com/analytics-vidhya/artificial-intelligence-at-play-connect-four-minimax-algorithm-explained-3b5fc32e4a4f
#https://www.youtube.com/watch?v=MMLtza3CZFM
#https://oscarnieves100.medium.com/programming-a-connect-4-game-on-python-f0e787a3a0cf
#https://www.askpython.com/python/examples/connect-four-game

