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
       
        #following pseudocode
        def max_turn(board, ai_turn, depth, alpha, beta, opp_num):
            v = float('-inf')
            possible_moves = self.possibleMoves(board)
            column = np.random.choice(possible_moves) if len(possible_moves) != 0 else None
            for moves in possible_moves: 
                board_copy = board.copy()
                self.make_move(board_copy, moves, self.player_number)       
                score, _ = alpha_beta_helper(board_copy,  False , depth-1, alpha, beta, opp_num)
                if score > v:
                    v = score
                    column = moves
                if v >= beta:
                    return v, column
                alpha = max(alpha, v)
            return v, column
        
        #following pseudocode
        def min_turn(board, ai_turn, depth, alpha, beta, opp_num):
            v = float('inf')
            possible_moves = self.possibleMoves(board)
            column = np.random.choice(possible_moves) if len(possible_moves) != 0 else None
            for moves in possible_moves:
                board_copy = board.copy() 
                self.make_move(board_copy, moves, op_num)
                score, _ = alpha_beta_helper(board_copy, True, depth-1, alpha, beta, opp_num)
                if score < v:
                    v = score
                    column = moves
                if v <= alpha:
                    return v, column
                beta = min(beta, v)
            return v, column


        def alpha_beta_helper(board1, ai_turn, depth, alpha, beta, opp_num):
            if depth == 0 or self.is_Winner(board1, self.player_number) or self.is_Winner(board1, opp_num) or self.is_Tie(board1):
                return self.evaluation_function(board1), None
            if ai_turn:
                return max_turn(board1, ai_turn, depth, alpha, beta, opp_num )
            else:
                return min_turn(board1, ai_turn, depth, alpha, beta, opp_num )

        DEPTH  = 4
        op_num = 1 if self.player_number == 2 else 2  
        score, res = alpha_beta_helper(board, True, DEPTH, float('-inf'),  float('inf'), op_num) 
        return res


        # max_value(board, float('-inf'), float('inf')) 
        # raise NotImplementedError('Whoops I don\'t know what to do')
    

    #Burrow logic from game_compleded from ConnectFour.py
    def is_Winner(self, board, player_num):
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


        
    def is_Tie(self, board):
        return self.possibleMoves(board) == 0
    """
        Given the current board state get all the columns that are open

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
        Array of available column indicees
        """
    #Burrowed from HumanAI class
    def possibleMoves(self, board):
        valid_cols = []
        for col in range(board.shape[1]):
            if 0 in board[:,col]:
                valid_cols.append(col)
        return valid_cols
    

    #places piece of number player in appropiate location in board
    def make_move(self, board, col, player):
        row = len(board)-1
        while(row >= 0):
            if board[row][col] == 0:
                board[row][col] = player
                break
            row-=1
        
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

        def expectimax_helper(board1, ai_turn, depth, opp_num):

            #Follows Pseudocode
            def max_turn(board, ai_turn, depth, opp_num):
                v = float('-inf')
                possible_moves = self.possibleMoves(board)
                column = np.random.choice(possible_moves) if len(possible_moves) != 0 else None
                for moves in possible_moves: 
                    board_copy = board.copy()
                    self.make_move(board_copy, moves, self.player_number)         
                    score, _ = expectimax_helper(board_copy, False, depth-1, opp_num)
                    if score > v:
                        v = score
                        column = moves
                return v, column

             #Follows Pseudocode
            def chance_turn(board, ai_turn, depth, opp_num):
                v = 0
                possible_moves = self.possibleMoves(board)
                column = np.random.choice(possible_moves) if len(possible_moves) != 0 else None
                if not possible_moves:
                    return 0, None
                p = 1 / len(possible_moves)
                for moves in possible_moves:
                    board_copy = board.copy()
                    self.make_move(board_copy, moves, opp_num) 
                    score, _ = expectimax_helper(board_copy, True, depth-1, opp_num)
                    v += (p* score)
                return v, None



            if(self.is_Winner(board1, self.player_number) or self.is_Winner(board1,opp_num) or depth == 0):
                return self.evaluation_function(board1), None
            if ai_turn:
                return max_turn(board1, ai_turn, depth, opp_num)
    
            else:
                return chance_turn(board1, ai_turn, depth, opp_num)

        DEPTH = 4
        opp_num = 1 if self.player_number == 2 else 2  
        _,res = expectimax_helper(board, True, DEPTH, opp_num)
        return res

        # raise NotImplementedError('Whoops I don\'t know what to do')




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
        # main logic of evaluation function, logic described in report. 
        def calc_score(opp_num, temp):
            score = 0     
            if temp.count(self.player_number) == 4:
                score += 20000
                return
            elif temp.count(self.player_number) == 3 and temp.count(0) == 1:
                score += 100 
            elif temp.count(self.player_number) == 2 and temp.count(0) == 2:
                score += 50
            # if temp.count(opp_num) == 4:
            #     score -= 80

            if temp.count(opp_num) == 4:
                score -= 1500
            # if opp_num in temp and self.player_number in temp:
            #     score -= 3
            elif temp.count(opp_num) == 3 and temp.count(0) == 1:
                score -= 50

            
            return score   


        
                    

        # partition all horizontal windows
        def horizontal_score(player_num, opp_num):
            score = 0
            for row in board:
                temp = []
                for i in range(board.shape[1]-3):
                    temp = list (row[i:i+4])
                    if temp[2] == opp_num and temp[1] == opp_num and temp[0] == 0 and temp[3] == 0:
                        score -= 150
                    
                    score += calc_score(opp_num, temp)                
            return score
         # partition all vertical windows
        def vertical_score(player_num, opp_num):
            score = 0
            for col in board.T:
                temp = []
                for i in range(board.shape[0]-3):
                    temp = list (col[i:i+4])
                    score += calc_score(opp_num, temp)               
            return score

        # partition all diagonal windows
        def diag_score(opp_num):
           score = 0
           for op in [None, np.fliplr]:
                op_board = op(board) if op else board 
                root_diag = np.diagonal(op_board, offset=0).astype(int)
                for i in range(len(root_diag)-3):
                    temp = list(root_diag[i:i+4])
                    score += calc_score(opp_num, temp)
                for i in range(1, board.shape[1]-3):
                    for offset in [i, -i]:
                        diag = np.diagonal(op_board, offset=offset)
                        for i in range(len(diag)-3):
                            temp = list(diag[i:i+4])
                            score += calc_score(opp_num, temp)
                return score





        op_num = 1 if self.player_number == 2 else 2
        #return very large score to motivate player to take winning move
        if self.is_Winner(board, self.player_number):
            return 1000000
        #return an extremely negative score to motivate the player to avoid taking a move that leads the opponent to win
        elif self.is_Winner(board, op_num):
            return -1000000
        #no incentive if player ties
        elif self.is_Tie(board):
            return 0
        score = 0
        

        #incentivize the maximizer to select the middle most column 
        if self.player_number == board[board.shape[0]-1][board.shape[1]//2]:
            score += 70
        #check all possible 4 sized windows for all diagonals horizonal and vertical windows.
        score += horizontal_score(self.player_number,op_num)
        score += vertical_score(self.player_number, op_num)
        score += diag_score(op_num)
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

