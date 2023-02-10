import numpy as np
# from ConnectFour import Game

class AIPlayer:
    def __init__(self, player_number):
        self.player_number = player_number
        self.type = 'ai'
        self.player_string = 'Player {}:ai'.format(player_number)

    # REUSING FUNCTIONS or CAN USE DECORATORS
    def update_board(self, move, player_num, board):
        demo_board = board.copy()
        if 0 in demo_board[:,move]:
            update_row = -1
            for row in range(1, demo_board.shape[0]):
                update_row = -1
                if demo_board[row, move] > 0 and demo_board[row-1, move] == 0:
                    update_row = row-1
                elif row==demo_board.shape[0]-1 and demo_board[row, move] == 0:
                    update_row = row

                if update_row >= 0:
                    demo_board[update_row, move] = player_num
                    # self.c.itemconfig(self.gui_board[move][update_row],
                    #                   fill=self.colors[self.current_turn])
                    break
        else:
            err = 'Invalid move by AI player {}. Column {}'.format(player_num, move)
            raise Exception(err)
        return demo_board
   
    def game_completed(self, player_num, board):
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

    def end_condition(self, player_num, board):
        return self.game_completed(player_num, board)

    # count = 0
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
        # alpha = MAX's best option on path to root
        # beta = MIN's best option on path to root
        # here, board = state
        # -1 if game is not over
        count = 0
        # max in minimax
        def max_func_alphabeta(self,board,alpha,beta, depth, move_col, depth_deepest, count):

            # count = count + 1
            # print(count)
            # if depth<depth_deepest:
            #     depth_deepest = depth
            #     print(depth_deepest)

            if self.end_condition(self.player_number, board):
                return self.evaluation_function(board), move_col, depth_deepest, count
            elif depth <=0:
                return self.evaluation_function(board), move_col, depth_deepest, count 

            # print(depth)
            val = -np.inf
            # depth_deepest = 0
            best_act = -1

            valid_actions = []
            to_iter = board.shape[1]
            unoccupied = 0     ### unoccupied marked by 0s
            for act in range(to_iter):
                if unoccupied in board[:,act]:          
                    valid_actions.append(act)

            for i in range(len(valid_actions)):
                demo_board = self.update_board(valid_actions[i], self.player_number, board)  ## or see if we can do depth+1
                val_new, column, depth_deepest, count = min_func_alphabeta(self,demo_board,alpha,beta, depth-1, valid_actions[i], depth_deepest, count)
                if val_new >= beta: # if alpha >= beta
                    val = val_new
                    move_col = valid_actions[i]
                    break
                elif val_new > val:
                    val = val_new
                    move_col = column
                count = count + 1
                # print(count)
                alpha = max(val, alpha)
                
                
            return val, move_col, depth_deepest, count 

        if self.player_number == 1:
                opp = 2
        else:
                opp = 1
        
        #min in minimax
        def min_func_alphabeta(self,board,alpha,beta, depth, move_col, depth_deepest, count):

            # if self.player_number == 1:
            #     opp = 2
            # else:
            #     opp = 1
            # print(depth)
            
            # count = count + 1
            # print(count)

            # if depth<depth_deepest:
            #     depth_deepest = depth
            #     print(depth_deepest)
                

            if self.end_condition(opp, board):
                return self.evaluation_function(board), move_col, depth_deepest, count
            elif depth <=0:
                return self.evaluation_function(board), move_col, depth_deepest, count 

            val = np.inf
            # depth_deepest = 0
            best_act = -1
            
            valid_actions = []
            to_iter = board.shape[1]
            unoccupied = 0     ### unoccupied marked by 0s
            for act in range(to_iter):
                if unoccupied in board[:,act]:          
                    valid_actions.append(act)
            # print(valid_actions)

            for i in range(len(valid_actions)):
                demo_board = self.update_board(valid_actions[i], opp, board)
                val_new, column, depth_deepest, count = max_func_alphabeta(self,demo_board,alpha,beta, depth-1, valid_actions[i], depth_deepest, count)  
                if alpha >= val_new: # if alpha >= beta
                    val = val_new
                    move_col = valid_actions[i]
                    break
                elif val_new < val:
                    val = val_new
                    move_col = column
                count = count + 1
                # print(count)
                beta = min(val, beta)
            # print(depth_deepest)   
            return val, move_col, depth_deepest, count 

        depth = 6
        depth_deepest = 6
        init_column = -1
        
        _, next_move, depth_traversed, count = max_func_alphabeta(self, board, -np.inf, np.inf, depth-1, init_column, depth_deepest, count)
        # print(depth_traversed)
        return next_move


        # raise NotImplementedError('Whoops I don\'t know what to do')

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
        
        # implement a max function
        # implement an exptation function (weighted sums)
        # implement a calculate value function
        # flag = 0 means send next to expectation
        # flag = 1 means send next to max_func

        def max_func(self, board, depth, move_col, count):
            # print(depth)
            if self.end_condition(self.player_number, board):
                return self.evaluation_function(board), move_col, count
            elif depth <=0:
                return self.evaluation_function(board), move_col, count 

            flag = 0       ###  
            val = -np.inf
            depth_deepest = 0
            best_act = -1

            valid_actions = []
            to_iter = board.shape[1]
            unoccupied = 0     ### unoccupied marked by 0s
            for act in range(to_iter):
                if unoccupied in board[:,act]:          
                    valid_actions.append(act)
            
            for i in range(len(valid_actions)):
                val_new, column, count = expect_func(self, board, depth-1, valid_actions[i], count)
                if val_new > val:
                    val = val_new
                    move_col = column
                count = count + 1
                # print(count)
            # print(val, move_col)
            return val, move_col, count

        def expect_func(self, board, depth, move_col, count):
            # print(depth)
            if self.end_condition(self.player_number, board):
                return self.evaluation_function(board), move_col, count
            elif depth <=0:
                return self.evaluation_function(board), move_col, count 

            flag = 0       ###  
            val = 0
            depth_deepest = 0
            best_act = -1

            valid_actions = []
            to_iter = board.shape[1]
            unoccupied = 0     ### unoccupied marked by 0s
            for act in range(to_iter):
                if unoccupied in board[:,act]:          
                    valid_actions.append(act)

            for i in range(len(valid_actions)):
                prob = 1/len(valid_actions)  ## because of equal probability
                new_val, _, count = max_func(self, board, depth-1, valid_actions[i], count)
                val = val + (prob * new_val)
                count = count + 1
                # print(count)
            # print(val, move_col)
            return val, move_col, count
        depth = 4
        count = 0
        init_column = -1
        _, next_move, count = max_func(self, board, depth, init_column, count)
        return next_move




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
        eval_score = 0
        # print(board.shape[0])
        # print(board.shape[1])

        for i in range(board.shape[0]):     # rows (6)
            for j in range(board.shape[1]):   # columns (7)
            ##### VERTICAL up check
                if i+3 < board.shape[0]:
                    if board[i][j] == board[i+1][j] == 1:    # streak of 2
                        eval_score = eval_score + 1
                    if board[i][j] == board[i+1][j] == board[i+2][j] == 1:  # streak of 3
                        eval_score = eval_score + 10
                    if board[i][j] == board[i+1][j] == board[i+2][j] == board[i+3][j] == 1:  # streak of 4
                        eval_score = eval_score + 1000

                    # penalize the placement of player 2   (try by double)
                    if board[i][j] == board[i+1][j] == 2:    # streak of 2
                        eval_score = eval_score - 1*2
                    if board[i][j] == board[i+1][j] == board[i+2][j] == 2:  # streak of 3
                        eval_score = eval_score - 10*2
                    if board[i][j] == board[i+1][j] == board[i+2][j] == board[i+3][j] == 2:  # streak of 4
                        eval_score = eval_score - 1000*2

            ##### VERTICAL down check
                if i-3 >= 0:
                    if board[i][j] == board[i-1][j] == 1:    # streak of 2
                        eval_score = eval_score + 1
                    if board[i][j] == board[i-1][j] == board[i-2][j] == 1:  # streak of 3
                        eval_score = eval_score + 10
                    if board[i][j] == board[i-1][j] == board[i-2][j] == board[i-3][j] == 1:  # streak of 4
                        eval_score = eval_score + 1000

                    # penalize the placement of player 2   (try by double)
                    if board[i][j] == board[i-1][j] == 2:    # streak of 2
                        eval_score = eval_score - 1*2
                    if board[i][j] == board[i-1][j] == board[i-2][j] == 2:  # streak of 3
                        eval_score = eval_score - 10*2
                    if board[i][j] == board[i-1][j] == board[i-2][j] == board[i-3][j] == 2:  # streak of 4
                        eval_score = eval_score - 1000*2
            

            ##### HORIZONTAL right check
                if j+3 < board.shape[1]:
                    if board[i][j] == board[i][j+1] == 1:    # streak of 2
                        eval_score = eval_score + 1
                    if board[i][j] == board[i][j+1] == board[i][j+2] == 1:  # streak of 3
                        eval_score = eval_score + 10
                    if board[i][j] == board[i][j+1] == board[i][j+2] == board[i][j+3] == 1:  # streak of 4
                        eval_score = eval_score + 1000

                    # penalize the placement of player 2   (try by double)
                    if board[i][j] == board[i][j+1] == 2:    # streak of 2
                        eval_score = eval_score - 1*2
                    if board[i][j] == board[i][j+1] == board[i][j+2] == 2:  # streak of 3
                        eval_score = eval_score - 10*2
                    if board[i][j] == board[i][j+1] == board[i][j+2] == board[i][j+3] == 2:  # streak of 4
                        eval_score = eval_score - 1000*2

            ##### HORIZONTAL left check
                if j-3 >=0:
                    if board[i][j] == board[i][j-1] == 1:    # streak of 2
                        eval_score = eval_score + 1
                    if board[i][j] == board[i][j-1] == board[i][j-2] == 1:  # streak of 3
                        eval_score = eval_score + 10
                    if board[i][j] == board[i][j-1] == board[i][j-2] == board[i][j-3] == 1:  # streak of 4
                        eval_score = eval_score + 1000

                    # penalize the placement of player 2   (try by double)
                    if board[i][j] == board[i][j-1] == 2:    # streak of 2
                        eval_score = eval_score - 1*2
                    if board[i][j] == board[i][j-1] == board[i][j-2] == 2:  # streak of 3
                        eval_score = eval_score - 10*2
                    if board[i][j] == board[i][j-1] == board[i][j-2] == board[i][j-3] == 2:  # streak of 4
                        eval_score = eval_score - 1000*2
            

            ##### diagonal to the right check
                if i+3 < board.shape[0] and j+3 < board.shape[1]:
                        if board[i][j] == board[i+1][j+1] == 1:
                            eval_score = eval_score + 1
                        if board[i][j] == board[i+1][j+1] == board[i+2][j+2] == 1:
                            eval_score = eval_score + 10
                        if board[i][j] == board[i+1][j+1] == board[i+2][j+2] == board[i+3][j+3] == 1:
                            eval_score = eval_score + 1000

            ##### diagonal to the left check
                if i+3 < board.shape[0] and j-3 >=0:
                        if board[i][j] == board[i+1][j-1] == 1:
                            eval_score = eval_score + 1
                        if board[i][j] == board[i+1][j-1] == board[i+2][j-2] == 1:
                            eval_score = eval_score + 10
                        if board[i][j] == board[i+1][j-1] == board[i+2][j-2] == board[i+3][j-3] == 1:
                            eval_score = eval_score + 1000

            
            ##### diagonal to the right check (penalize player 2)
                if i+3 < board.shape[0] and j+3 < board.shape[1]:
                        if board[i][j] == board[i+1][j+1] == 2:
                            eval_score = eval_score - 1*2
                        if board[i][j] == board[i+1][j+1] == board[i+2][j+2] == 2:
                            eval_score = eval_score - 10*2
                        if board[i][j] == board[i+1][j+1] == board[i+2][j+2] == board[i+3][j+3] == 2:
                            eval_score = eval_score - 1000*2

            ##### diagonal to the left check (penalize player 2)
                if i+3 < board.shape[0] and j-3 >=0:
                        if board[i][j] == board[i+1][j-1] == 2:
                            eval_score = eval_score - 1*2
                        if board[i][j] == board[i+1][j-1] == board[i+2][j-2] == 2:
                            eval_score = eval_score - 10*2
                        if board[i][j] == board[i+1][j-1] == board[i+2][j-2] == board[i+3][j-3] == 2:
                            eval_score = eval_score - 1000*2
        return eval_score



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

