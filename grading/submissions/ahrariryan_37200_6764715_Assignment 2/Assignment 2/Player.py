import numpy as np

class AIPlayer:
    def __init__(self, player_number):
        self.player_number = player_number
        self.type = 'ai'
        self.it = 0 
        self.player_string = 'Player {}:ai'.format(player_number)
        if self.player_number == 1:
            self.enemy_player = 2
        else:
            self.enemy_player = 1

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
        best_choice = 0
        ma = 0
        self.depth = 1
        for j in range(0, 7):
            for i in range(0, 6):
                if (board[i, j] == 0):
                    new_board = board.copy()
                    self.update_board(j, new_board, self.player_number)
                    # print('About to calculate in minimax')
                    new = self.minimax(new_board, self.enemy_player, 0, -999999, 999999)
                    if new:
                        # print('Iterations: '+str(self.it))
                        # print('New: '+ str(new))
                        if new > ma:
                            ma = new
                            best_choice = j
                            # print('J: '+str(j) )
                            # print('New ma: '+ str(ma))
                            # print('Best choice in main: '+ str(best_choice))
                    break
        #print('Iterations: '+str(self.it))
        return best_choice

    def minimax(self, board, agent, depth, alpha, beta):
        #print(board)
        if self.game_completed(board, agent) or depth == self.depth:
            best_choice = self.evaluation_function(board)
            # print('Done recurring depth: ' + str(depth))
            # print('Best choice is: '+ str(best_choice))
            return best_choice
        elif agent == self.player_number:
            return self.max_value(board, agent, depth, alpha, beta)
        else: 
            return self.min_value(board, agent, depth, alpha, beta)

    def max_value(self, board, agent, depth, alpha, beta):       
        ma = -999999
        for j in range(0, 7):
            for i in range(0, 6):
                if (board[i, j] == 0):
                    new_board = board.copy()
                    self.update_board(j, new_board, self.player_number)
                    #print('New board in max: '+ str(new_board))
                    new = self.minimax(new_board, self.enemy_player, depth, -999999, 999999)
                    # if new:
                    #     print('In max, new is:')
                    #     print(new)
                    #     print('Alpha is:')
                    #     print(alpha)
                    #     print('Beta is:')
                    #     print(beta)

                    if new and new < alpha:
                        return new
                    if new is not None and new > ma:
                        alpha = new
                        ma = new
                    break
    
    def min_value(self, board, agent, depth, alpha, beta):       
        mi = 999999
        depth += 1
        for j in range(0, 7):
            for i in range(0, 6):
                if (board[i,j] == 0):   
                    new_board = board.copy()
                    self.update_board(j, new_board, self.enemy_player)
                    #print('New board in min: '+ str(new_board))
                    new = self.minimax(new_board, self.player_number, depth, -999999, 999999)
                    # if new:
                    #     print('In min, new is:')
                    #     print(new)
                    #     print('Alpha is:')
                    #     print(alpha)
                    #     print('Beta is:')
                    #     print(beta)
                    if new and new > beta:
                        return new
                    if new is not None and new < mi:
                        beta = new
                        mi = new
                    break
    
    

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
        best_choice = 0
        ma = 0
        self.depth = 1
        for j in range(0, 7):
            for i in range(0, 6):
                if (board[i, j] == 0):
                    # print(i, j)
                    # print('\n\n\n\n\n\n\n\n\n')
                    new_board = board.copy()
                    self.update_board(j, new_board, self.player_number)
                    # print('About to calculate in minimax')
                    new = self.expectimax(new_board, self.enemy_player, 0)
                    if new:
                        #print('Iterations: '+str(self.it))
                        # print('New: '+ str(new))
                        if new >= ma:
                            ma = new
                            best_choice = j
                            # print('J: '+str(j) )
                            # print('New ma: '+ str(ma))
                            # print('Best choice in main: '+ str(best_choice))
                    break
        #print('Iterations: '+str(self.it))
        return best_choice


    def expectimax(self, board, agent, depth):
        #print(board)
        if self.game_completed(board, agent) or depth == self.depth:
            best_choice = self.evaluation_function(board)
            # print('Done recurring depth: ' + str(depth))
            # print('Best choice is: '+ str(best_choice))
            return best_choice
        elif agent == self.player_number:
            return self.expmax_value(board, agent, depth)
        else: 
            return self.exp_value(board, agent, depth)

    def expmax_value(self, board, agent, depth):       
        ma = -999999
        for j in range(0, 7):
            for i in range(0, 6):
                if (board[i, j] == 0):
                    new_board = board.copy()
                    self.update_board(j, new_board, self.player_number)
                    #print('New board in max: '+ str(new_board))
                    new = self.expectimax(new_board, self.enemy_player, depth)
                    # if new:
                    #     print('In max, new is:')
                    #     print(new)
                    #     print('Alpha is:')
                    #     print(alpha)
                    #     print('Beta is:')
                    #     print(beta)
                    if new is not None and new > ma:
                        ma = new
                    break
    
    def exp_value(self, board, agent, depth):       
        values = []
        len = 0
        depth += 1
        breaker = False
        for j in range(0, 7):
            for i in range(0, 6):
                if (board[i,j] == 0):   
                    new_board = board.copy()
                    self.update_board(j, new_board, self.enemy_player)
                    #print('New board in exp: '+ str(new_board))
                    new = self.expectimax(new_board, self.player_number, depth)
                    # if new:
                    #     print('In min, new is:')
                    #     print(new)
                    #     print('Alpha is:')
                    #     print(alpha)
                    #     print('Beta is:')
                    #     print(beta)
                    if new is not None:
                        len += 1
                        values.append(new)
                        breaker = True
                if breaker:
                    break
        if values:
            return (sum(values)/len)
        else: 
            return 0
                    

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
        self.it+=1
        valid_cols = []
        best_choice = []
        me = self.player_number
        en = self.enemy_player
        illegal_coords_i = [-2, -1, 6, 7]
        illegal_coords_j = [-2, -1, 7, 8]
        
        for j in range(0, 7):
            for i in range(0, 6):
                player = board[i, j]
                diag1 = (i+1, j+1)
                diag2 = (i+1, j-1)
                diag3 = (i-1, j-1)
                diag4 =  (i-1, j+1 )
                up = (i+1, j)
                down = (i-1, j)
                up2 = (i+2, j)
                down2 = (i-2, j)
                right = (i, j+1)
                left = (i, j-1)
                right2 = (i, j+2)
                left2 = (i, j-2)
                coords = [diag1, diag2, diag3, diag4, up, down, right, left, right2, left2, up2, down2]
                origs = [diag1, diag2, diag3, diag4, up, down, right, left]
                if (player == 0):
                    if j in valid_cols:
                        for pos in coords:
                            # print('Pos')
                            # print(pos)
                            if (pos[0] not in illegal_coords_i and pos[1] not in illegal_coords_j):
                                other = board[pos]
                                if other == me or other == en:
                                    if pos[1] == j:
                                        best_choice[valid_cols.index(j)] += (1/abs(pos[1]-j-1))
                                    else:
                                        best_choice[valid_cols.index(j)] += (1/abs(pos[1]-j))
                        
                    else:
                        valid_cols.append(j)
                        best_choice.append(0)
                        for pos in coords:
                            # print('Pos')
                            # print(pos)
                            if (pos[0] not in illegal_coords_i and pos[1] not in illegal_coords_j):
                                other = board[pos]
                                if other == me or other == en:
                                    if pos[1] == j:
                                        best_choice[valid_cols.index(j)] += (1/abs(pos[1]-j-1))
                                    else:
                                        best_choice[valid_cols.index(j)] += (1/abs(pos[1]-j))
            
                elif (player == me):
                    if j in valid_cols:
                        for pos in coords:
                            # print('Pos')
                            # print(pos)
                            if (pos[0]  not in illegal_coords_i and pos[1]  not in illegal_coords_j):
                                other = board[pos]
                                if other == me or other == en:
                                    if pos[1] == j:
                                        best_choice[valid_cols.index(j)] += (1/abs(pos[1]-j-1))
                                    else:
                                        best_choice[valid_cols.index(j)] += (1/abs(pos[1]-j))
                    else:
                        valid_cols.append(j)
                        best_choice.append(0)

                        for pos in coords:
                            # print('Pos')
                            # print(pos)
                            if (pos[0]  not in illegal_coords_i and pos[1]  not in illegal_coords_j):
                                other = board[pos]
                                if other == me or other == en:
                                    if pos[1] == j:
                                        best_choice[valid_cols.index(j)] += (1/abs(pos[1]-j-1))
                                    else:
                                        best_choice[valid_cols.index(j)] += (1/abs(pos[1]-j))
                elif (player == en):
                    if j in valid_cols:
                        for pos in coords:
                            # print('Pos')
                            # print(pos)
                            if (pos[0]  not in illegal_coords_i and pos[1]  not in illegal_coords_j):
                                other = board[pos]
                                if other == me or other == en:
                                    if pos[1] == j:
                                        best_choice[valid_cols.index(j)] += (1/abs(pos[1]-j-1))
                                    else:
                                        best_choice[valid_cols.index(j)] += (1/abs(pos[1]-j))
                    else:
                        valid_cols.append(j)
                        best_choice.append(0)
                        for pos in coords:
                            if (pos[0]  not in illegal_coords_i and pos[1]  not in illegal_coords_j):
                                other = board[pos]
                                if other == me or other == en:
                                    if pos[1] == j:
                                        best_choice[valid_cols.index(j)] += (1/abs(pos[1]-j-1))
                                    else:
                                        best_choice[valid_cols.index(j)] += (1/abs(pos[1]-j))
        return max(best_choice)

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
    

    def update_board(self, move, board, player_num):
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
                    #return board
        else:
            err = 'Invalid move by player {}. Column {}'.format(player_num, move)
            raise Exception(err)


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

# Old eval function logic
# Did not work but took a while to write so I'd like to remember it
#print(valid_cols)
#                 if (board[i,j] == 0):
#                     #print('It '+str(self.it)+' in zero section') 
#                     if(j not in valid_cols):  
#                         valid_cols.append(j)
#                         best_choice.append(-1)
#                 elif (board[i, j] == self.player_number):
#                     #print('It '+str(self.it)+' in player section') 
#                     if(j not in valid_cols):  
#                         valid_cols.append(j)
#                         best_choice.append(1)
#                     else:
#                         if (j>=1 and j<6 and i>=1 and i<5):
#                             if(board[i+1, j]  == self.enemy_player):
#                                 best_choice[valid_cols.index(j)] += 20
#                                 if(board[i-1, j]  == self.enemy_player):
#                                     best_choice[valid_cols.index(j)] -= 10
#                                 elif(board[i-1, j]  == self.player_number):
#                                     best_choice[valid_cols.index(j)] += 100
#                                 # elif(board[i-1, j]  == 0):
#                                 #     best_choice[valid_cols.index(j)] += 1

#                             if(board[i, j+1]  == self.enemy_player):
#                                 best_choice[valid_cols.index(j)] += 20
#                                 if(board[i, j-1]  == self.enemy_player):
#                                     best_choice[valid_cols.index(j)] -= 10
#                                 elif(board[i, j-1]  == self.player_number):
#                                     best_choice[valid_cols.index(j)] += 100
#                                 # elif(board[i-1, j-1]  == 0):
#                                 #     best_choice[valid_cols.index(j)] += 1

#                             # if(board[i+1, j+1]  == self.enemy_player):
#                             #     best_choice[valid_cols.index(j)] += 20
#                             #     if(board[i-1, j-1]  == self.enemy_player):
#                             #         best_choice[valid_cols.index(j)] += 10
#                             #     elif(board[i-1, j-1]  == self.player_number):
#                             #         best_choice[valid_cols.index(j)] += 100
#                             #     elif(board[i-1, j-1]  == 0):
#                             #         best_choice[valid_cols.index(j)] += 1
                                    
#                             # if(board[i-1, j+1]  == self.enemy_player):
#                             #     best_choice[valid_cols.index(j)] += 20
#                             #     if(board[i+1, j-1]  == self.enemy_player):
#                             #         best_choice[valid_cols.index(j)] += 10
#                             #     elif(board[i+1, j-1]  == self.player_number):
#                             #         best_choice[valid_cols.index(j)] += 100
#                             #     elif(board[i, j-1]  == 0):
#                             #         best_choice[valid_cols.index(j)] += 1    
                            
#                             if(board[i+1, j]  == self.player_number):
#                                 best_choice[valid_cols.index(j)] += 10
#                                 if(board[i-1, j]  == self.player_number):
#                                     best_choice[valid_cols.index(j)] -= 1
#                                 elif(board[i-1, j]  == self.enemy_player):
#                                     best_choice[valid_cols.index(j)] += 100
#                                 # elif(board[i-1, j]  == 0):
#                                 #     best_choice[valid_cols.index(j)] += 1

#                             if(board[i, j+1]  == self.player_number):
#                                 best_choice[valid_cols.index(j)] += 10
#                                 if(board[i, j-1]  == self.player_number):
#                                     best_choice[valid_cols.index(j)] -= 1
#                                 elif(board[i, j-1]  == self.enemy_player):
#                                     best_choice[valid_cols.index(j)] += 100
#                                 # elif(board[i, j-1]  == 0):
#                                 #     best_choice[valid_cols.index(j)] += 1

#                             # if(board[i+1, j+1]  == self.player_number):
#                             #     best_choice[valid_cols.index(j)] -= 10
#                             #     if(board[i-1, j-1]  == self.player_number):
#                             #         best_choice[valid_cols.index(j)] += 1
#                             #     elif(board[i-1, j-1]  == self.enemy_player):
#                             #         best_choice[valid_cols.index(j)] += 100
#                             #     elif(board[i-1, j-1]  == 0):
#                             #         best_choice[valid_cols.index(j)] += 1

#                             # if(board[i+1, j-1]  == self.player_number):
#                             #     best_choice[valid_cols.index(j)] -= 10
#                             #     if(board[i-1, j+1]  == self.player_number):
#                             #         best_choice[valid_cols.index(j)] += 1
#                             #     elif(board[i-1, j+1]  == self.enemy_player):
#                             #         best_choice[valid_cols.index(j)] += 100
#                             #     elif(board[i-1, j+1]  == 0):
#                             #         best_choice[valid_cols.index(j)] += 1

#                             best_choice[valid_cols.index(j)] += 1
#                         else:
#                             best_choice[valid_cols.index(j)] += 1
#                 elif (board[i, j] == self.enemy_player): 
#                     #print('It '+str(self.it)+' in enemy section') 
#                     if(j not in valid_cols):  
#                         valid_cols.append(j)
#                         best_choice.append(5)
#                     else:
#                         if (j>=1 and j<6 and i>=1 and i<5):
#                             if(board[i+1, j]  == self.player_number):
#                                 best_choice[valid_cols.index(j)] += 20
#                                 if(board[i-1, j]  == self.player_number):
#                                     best_choice[valid_cols.index(j)] -= 10
#                                 elif(board[i-1, j]  == self.enemy_player):
#                                     best_choice[valid_cols.index(j)] += 100
#                                 # elif(board[i-1, j]  == 0):
#                                 #     best_choice[valid_cols.index(j)] += 1

#                             if(board[i, j+1]  == self.player_number):
#                                 best_choice[valid_cols.index(j)] += 20
#                                 if(board[i, j-1]  == self.player_number):
#                                     best_choice[valid_cols.index(j)] -= 10
#                                 elif(board[i, j-1]  == self.enemy_player):
#                                     best_choice[valid_cols.index(j)] += 100
#                                 # elif(board[i, j-1]  == 0):
#                                 #     best_choice[valid_cols.index(j)] += 1

#                             # if(board[i+1, j+1]  == self.player_number):
#                             #     best_choice[valid_cols.index(j)] += 10
#                             #     if(board[i-1, j-1]  == self.player_number):
#                             #         best_choice[valid_cols.index(j)] += 1
#                             #     elif(board[i-1, j-1]  == self.enemy_player):
#                             #         best_choice[valid_cols.index(j)] += 100
#                             #     elif(board[i-1, j-1]  == 0):
#                             #         best_choice[valid_cols.index(j)] += 1

#                             # if(board[i+1, j-1]  == self.player_number):
#                             #     best_choice[valid_cols.index(j)] += 10
#                             #     if(board[i-1, j+1]  == self.player_number):
#                             #         best_choice[valid_cols.index(j)] += 1
#                             #     elif(board[i-1, j+1]  == self.enemy_player):
#                             #         best_choice[valid_cols.index(j)] += 100
#                             #     elif(board[i-1, j+1]  == 0):
#                             #         best_choice[valid_cols.index(j)] += 1

#                             if(board[i+1, j]  == self.enemy_player):
#                                 best_choice[valid_cols.index(j)] += 10
#                                 if(board[i-1, j]  == self.enemy_player):
#                                     best_choice[valid_cols.index(j)] -= 1
#                                 elif(board[i-1, j]  == self.player_number):
#                                     best_choice[valid_cols.index(j)] += 100
#                                 # elif(board[i-1, j]  == 0):
#                                 #     best_choice[valid_cols.index(j)] += 1

#                             if(board[i, j+1]  == self.enemy_player):
#                                 best_choice[valid_cols.index(j)] += 10
#                                 if(board[i, j-1]  == self.enemy_player):
#                                     best_choice[valid_cols.index(j)] -= 1
#                                 elif(board[i, j-1]  == self.player_number):
#                                     best_choice[valid_cols.index(j)] += 100
#                                 # elif(board[i-1, j-1]  == 0):
#                                 #     best_choice[valid_cols.index(j)] += 1

#                             # if(board[i+1, j+1]  == self.enemy_player):
#                             #     best_choice[valid_cols.index(j)] -= 10
#                             #     if(board[i-1, j-1]  == self.enemy_player):
#                             #         best_choice[valid_cols.index(j)] += 1
#                             #     elif(board[i-1, j-1]  == self.player_number):
#                             #         best_choice[valid_cols.index(j)] += 100
#                             #     elif(board[i-1, j-1]  == 0):
#                             #         best_choice[valid_cols.index(j)] += 1
                                    
#                             # if(board[i-1, j+1]  == self.enemy_player):
#                             #     best_choice[valid_cols.index(j)] -= 10
#                             #     if(board[i+1, j-1]  == self.enemy_player):
#                             #         best_choice[valid_cols.index(j)] += 1
#                             #     elif(board[i+1, j-1]  == self.player_number):
#                             #         best_choice[valid_cols.index(j)] += 100
#                             #     elif(board[i, j-1]  == 0):
#                             #         best_choice[valid_cols.index(j)] += 1  

#                             best_choice[valid_cols.index(j)] += 1
#                         else:
#                             best_choice[valid_cols.index(j)] += 1