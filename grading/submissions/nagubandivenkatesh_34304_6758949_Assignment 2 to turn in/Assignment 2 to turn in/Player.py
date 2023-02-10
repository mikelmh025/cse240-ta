import numpy as np

class AIPlayer:
    def __init__(self, player_number):
        self.player_number = player_number
        self.type = 'ai'
        self.player_string = 'Player {}:ai'.format(player_number)
  
    #This is Professors function for checking if the game has ended I used this to for the terminal states of alpha-beta and expectmax
    def game_completed_1(self, player_number, board):

        player_win_str = '{0}{0}{0}{0}'.format(player_number)
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


    #given a board and a valid column it returns a board with the move in the column.
    def make_move(self,board,col,num):

        for x in reversed(range(6)):
            if board[x][col]==0:
                board[x][col]=num
                break

        return board

    #returns a list of all the valid columns this is also the professors code.
    def valid_moves(self,board):
        
        valid_cols=[]

        for i,col in enumerate(board.T):
            if 0 in col:
                valid_cols.append(i)
        
        return valid_cols

    #returns a modified board for the currentplayer
    def current_temp_board(self,board,move):

        y = board.copy()
        y = self.make_move(y,move,self.player_number)

        return y
    
    #returns a modified board for the other player
    def other_temp_board(self,board,move):

        play_num = 1

        if (self.player_number==1):
            play_num=2

        y = board.copy()
        y = self.make_move(y,move,play_num)

        return y

    def alpha_beta_pruning(self,board,alpha,beta,depth):
        
        x = self.alpha_max(board,alpha,beta,depth)
        return x[1]

    def alpha_max(self,board,alpha,beta,depth):

        if(self.game_completed_1(self.player_number,board)):
            val_mover = (self.evaluation_function(board),None)

        if(depth<=0):
            val_mover = (self.evaluation_function(board),None)
            return val_mover

        v = -10000
        moves = self.valid_moves(board)
        move = -1

        for x in moves:
            v1 = self.beta_min(self.current_temp_board(board,x),alpha,beta,depth-1)

            if v1[0]>v:
                v = v1[0]
                move = x
                alpha = max(alpha,v)
            
            if v>=beta:
                return (v,move)

        return (v,move)
    
    #is the beta agent for the alpha beta algorithm folows the psuedocode as closely as possible but adds in a depth aspect
    def beta_min(self,board,alpha,beta,depth):

        if(self.game_completed_1(self.player_number,board)):
            val_mover = (self.evaluation_function(board),None)

        if(depth<=0):
            val_mover = (self.evaluation_function(board),None)
            return val_mover

        v = 10000
        moves = self.valid_moves(board)
        move = 0

        for x in moves:
            # v1 = self.alpha_max(self.other_temp_board(board,x),alpha,beta,depth-1)
            v1 = self.alpha_max(self.current_temp_board(board,x),alpha,beta,depth-1)


            if v1[0]<v:
                v = v1[0]
                move = v1[1]
                beta = min(beta,v)
            
            if v<=alpha:
                return (v,move)
        
        return (v,move)


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
        depth = 5
        alpha = -1000000
        beta = 1000000

        move = self.alpha_beta_pruning(board,alpha,beta,depth)

        return move


    #is the max agent in the expect max algorithm follows the psudocode as closely as possible but adds in a depth aspect
    def maxagent_expect(self,board,depth):

        if(self.game_completed_1(self.player_number,board)):
            val_mover = (self.evaluation_function(board)+8,None)

        if(depth<=0):
            val_mover = (self.evaluation_function(board),None)
            return val_mover

        v = -10000
        moves = self.valid_moves(board)
        move = -1

        for x in moves:
            val = self.expectmaxagent_expect(self.current_temp_board(board,x),depth-1)
            if val[0] > v:
                move = x
                v = val[0]

        return (v,move)

    #is the expectmax agent in the expect max algorithm follows the psudocode as closely as possible but adds in a depth aspect
    def expectmaxagent_expect(self,board,depth):      

        if(self.game_completed_1(self.player_number,board)):
            val_mover = (self.evaluation_function(board)+8,None)

        
        if(depth<=0):
            val_mover = (self.evaluation_function(board),None)
            return val_mover

        v = 0
        moves = self.valid_moves(board)
        move = -1
        probability = 1/len(moves)


        for x in moves:
            val = self.maxagent_expect(self.current_temp_board(board,x),depth-1)
            v = val[0] * probability + v

        return (v,None)
        
    # calls the expectmax algorithm is used by ConnectFour.py.
    def get_expectimax_move(self, board):

        depth = 4

        return self.maxagent_expect(board,depth)[1]

    #counts the instances of one that lead to more possibilities
    def one_in_row(self,y,x,player,board,r1):
        score = 0

        if board[y,x]!=player:
            return 0
        
        if x+1<7 and board[y,x+1]==0:
            score = score + r1

        if y-1>0 and board[y-1,x]==0:
            score = score + r1
        
        if y-1>0 and x+1<7 and board[y-1,x+1]==0:
            score = score + r1

        return score

    #counts the instances of two that lead to more possibilities
    def two_in_row(self,y,x,player,board,r2):
        score = 0

        if board[y,x]!=player:
            return 0

        if x+2<7 and (board[y,x+1]== player) and board[y,x+2]==0:
            score = score + r2

        if y-2>=0 and (board[y-1,x]== player) and board[y-2,x]==0:
            score = score + r2

        if y-2>=0 and x+2<7 and (board[y-1,x+1]==player) and (board[y-2,x+2]==0):
            score = score + r2

        if y+2<6 and x-2>=0 and (board[y+1,x-1]==player) and (board[y+2,x-2]==0):
            score = score + r2

        return score

    #counts the instances of three that lead to more possibilities
    def three_in_row(self,y,x,player,board,r3):
        score = 0

        if board[y,x]!=player:
            return 0

        if y-3>=0 and board[y-1,x]==player and board[y-2,x]==player and board[y-3,x]==0:
            score = score + r3

        if x+3<7 and board[y,x+1]==player and board[y,x+2]==player and board[y,x+3]==0:
            score = score + r3       

        if y+3<6 and board[y+1,x]==player and board[y+2,x]==player and board[y+3,x]==0:
            score = score+r3

        if y-3>=0 and x+3<7 and (board[y-1,x+1]==player and board[y-2,x+2]==player) and board[y-3,x+3]==0:
            score = score +r3

        if y+3<6 and x-3>=0 and (board[y+1,x-1]==player and board[y+2,x-2]==player) and board[y+3,x-3]==0:
            score = score +r3

        if y+3<6 and x+3<7 and board[y+1,x+1]==player and board[y+2,x+2]==player and board[y+3,x+3]==0:
            score = score + r3
        
        if y-3>=0 and x-3>=0 and board[y-1,x-1]==player and board[y-2,x-2]==player and board[y-3,x-3]==0:
            score = score + r3

        return score


    #is the evaluation function reuturns instances of (oneinrow + twoinrow + threeinrow)(of currentplayer) - (oneinrow + twoinrow + 2*threeinrow)(of otherplayer)
    def evaluation_function(self, board):

        score1 = 0
        score2 = 0
        score3 = 0
        r1,r2,r3 = 0.4,1.6,7
        r4,r5,r6 = 0.4,2,15

        #loops through all the positions on the board to figure out the number of instances
        for y in reversed(range(6)):
            for x in (range(7)):
                score1 = self.one_in_row(y,x,self.player_number,board,r1) + score1
                score2 = self.two_in_row(y,x,self.player_number,board,r2) + score2
                score3 = self.three_in_row(y,x,self.player_number,board,r3) + score3
        

        score1_2 = 0
        score2_2 = 0
        score3_2 = 0
        player2 = 1        

        #switches the players
        if self.player_number == 1:
            player2 = 2

        #loops through all the positions on the board to figure out the number of instances for the other player.
        for y in reversed(range(6)):
            for x in (range(7)):
                score1_2 = self.one_in_row(y,x,player2,board,r4) + score1_2
                score2_2 = self.two_in_row(y,x,player2,board,r5) + score2_2
                score3_2 = self.three_in_row(y,x,player2,board,r6) + score3_2


        final_score = score1 + score2 +  score3 -  score1_2 - score2_2 - 3*score3_2


        return final_score

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

