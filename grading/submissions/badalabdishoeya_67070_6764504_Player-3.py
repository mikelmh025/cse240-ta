#Name: Eya Badal Abdisho
#ID: 1388232 
#Assignment 2
#02/01/2023


import numpy as np

#Setting up Depth Limit for Testing 
max_depth=2

class AIPlayer:
    def __init__(self, player_number):
        self.player_number = player_number
        self.type = 'ai'
        self.player_string = 'Player {}:ai'.format(player_number)

#Check to see if players on board 
    def position(self,row,col,yOff,xOff):
        if row+yOff < 0:
            return False 
        if row+yOff > 5:
            return False
        if col+xOff < 0:
            return False 
        if col+xOff > 6:
            return False
        return True


#https://mblogscode.wordpress.com/2018/05/13/connect-four-artificial-intelligence-part-1-coding-the-game-in-python/
#Check and see if they connected 4 and in terminal state 
    def ifConnected4(self,board):
        out_positions =[(-1,-1),
        (0,-1),
        (1,-1),
        (1,0)]
        i = 5
        j = 0
        adj = 0

        for i in range(5,0):
            for j in range(5,0,-1):
                player_number=self.player_number
                if board[i][j]==player_number:
                    for out in out_positions:
                        adj = 1
                        xOff = out[0]
                        yOff = out[1]
                        while board[i+yOff][j+xOff]==player_number :
                            adj = adj+1
                            xOff = xOff + out[0]
                            yOff = yOff + out[1]
                            pos=self.position(i,j,yOff,xOff) 
                            if pos!= True:
                                break
                        if adj >= 4:
                            return True
        return False


    def actions(self,board):
        #In action Function 
        size=len(board[0])
        i = 5
        actions = []
        for j in range(size-1,0,-1):
            while board[i][j]!=0 and i>0:
                i= i - 1
            if board[i][j]==0:
                #Empty 
                actions.append((i,j))
                #print(board)
        return actions


    def result(self,board,action,n):
        #self.board = np.zeros([6,7]).astype(np.uint8),ConnectFour.py
        temporary = np.zeros([6,7]).astype(np.uint8)
        size=len(board)
        size1=len(board[0])

        for i in range(size):
            if i != action[0]:
                temporary[i] = board[i]
            else:
                i2 = []
                for j in range(size1):
                    if j != action[1]:
                        i2.append(board[i][j])
                    else:
                        i2.append(n)
                temporary[i] = i2
        return temporary  
 


    def p(self,board,actions):
        size=len(actions)
        ret=int(1/size)
        return ret

   
    #http://aima.cs.berkeley.edu/python/games.html
    #https://stackoverflow.com/questions/20340446/connect-4-minimax-algorithm-one-for-loop
    #http://web.cs.wpi.edu/~rich/courses/imgd4000-d10/lectures/E-MiniMax.pdf
    def min_value(self,board,alpha,beta,depth):
        print ("This is board in min function: " + str(board))
        #print("In Min")
        terminal=self.ifConnected4(board) 

        if terminal or depth>=max_depth:
            player1=self.evaluation_function(board)
            player2=self.eval2(board)
            vl=3
            #heuristic player value minus the opponents value. 
            h=(player1-player2,vl)
            return h
        #Beta
        utility = 1000000
        m = 0
        mp = (m,utility)
        acts = self.actions(board)
        
        for action in acts: 
            player_number_2=self.player_number*2
            res=self.result(board,action,player_number_2%3)
            maxvalue=self.max_value(res,alpha,beta,depth+1)
            utility_value = maxvalue[0]
            if utility_value < utility:
                m = action[1]
            utility=min(utility,utility_value) 
            if utility<alpha:
                return (utility,m)
            beta = min(beta,utility)
            mp = (utility,m)
        print ("This is depth in min: " + str(depth))
        return mp



    #http://aima.cs.berkeley.edu/python/games.html
    #https://stackoverflow.com/questions/20340446/connect-4-minimax-algorithm-one-for-loop
    #http://web.cs.wpi.edu/~rich/courses/imgd4000-d10/lectures/E-MiniMax.pdf
    def max_value(self,board,alpha,beta,depth):
        print ("This is board in max function: " + str(board))
        #print("In max")
        terminal=self.ifConnected4(board) 
        if terminal or depth>=max_depth:
            vl=4
            player1=self.evaluation_function(board)
            player2=self.eval2(board)
            h = (player1-player2,vl)
            return h
            print(h)
        #Alpha
        utility = -1000000
        m = 0
        mp = (m,utility)
        acts = self.actions(board)

        for action in acts: 
            player_number=self.player_number
            res=self.result(board,action,player_number)
            minvalue=self.min_value(res,alpha,beta,depth+1)
            utility_value = minvalue[0]
            if utility_value > utility:
                m = action[1]
            utility = max(utility,utility_value) 
            #Prunning
            if utility > beta:
                return (utility,m)
            alpha = max(alpha,utility)
            mp = (utility,m)
        print ("This is depth in max : " + str(depth))
    
        return mp

        
    def get_alpha_beta_move(self, board):
        print("Alpha Beta")
        print(board)
        m= self.max_value(board,0,0,0)
        return m[1]


    
    def value2(self,board, depth):
        utility = 0
        acts = self.actions(board) 
        for act in acts:
            probability = self.p(board,act,acts)
            player_number=self.player_number*4
            res=self.result(board,act,player_number%5)
            bolvalue=True
            v=self.value(res,bolvalue,depth+1)
            utility = utility + probability*v[0]
        return utility


    
    def expValue2(self,board,depth):
        utility_value = -1000000
        acts = self.actions(board)
        m = 2
        bolvalue=False 
        for act in acts:
            player_number=self.player_number
            res=self.result(board,act,player_number)
            selfvalue=self.value(res,bolvalue,depth+1)
            if selfvalue > utility_value:
                m = act[1]
            value=self.value(res,bolvalue,depth+1)
            utility_value = max(utility_value,value)
        return (utility_value,m)



    
    def value_max(self,board,maximum,depth):
        if self.ifConnected4(board):
            if depth>= 5:
                if maximum:
                    ev=self.evaluation_function(board)
                    ev4=self.eval4(board)
                    return (ev-ev4,4)
                else:
                    return (ev-ev4)
        if maximum:
            expv2=self.expValue2(board,depth)
            return expv2
        else:
            v2=self.value2(board,depth)
            return v2

    
    def max_move_get(self, board):
        value=True
        maxMove=self.value_max(board,value,0)[1]
        return maxMove
      

    #Output: The utility value for the current board
    def evaluation_function(self,board):
        #print(board)
        row = 5
        col = 0
        adjN = 0
        adjMax = 0
        point = 0
        off_positions = [(-1,-1),(-1,0),(-1,1),(0,1)]
        for row in range(5,0,-1):
            for col in range(6): 
                if board[row][col]==self.player_number:
                    for off in off_positions:
                        adjN = 1
                        x_off = off[0] 
                        y_off = off[1]
                        while self.position(row,col,y_off,x_off) and (board[row+y_off][col+x_off]==self.player_number or board[row+y_off][col+x_off]==0):
                            adjN = adjN+1
                            x_off = x_off + off[0]
                            y_off = y_off + off[1]
                            adjMax = max(adjMax,adjN)
                        point = point + adjMax**2
      
        return point

    def eval2(self,board):
        row = 5
        col = 0
        adjN = 0
        adjMax = 0
        point = 0
        off_positions = [(-1,-1),(-1,0),(-1,1),(0,1)]
        for row in range(5,0,-1):
            for col in range(6): 
                if board[row][col]==self.player_number*2%3:
                    for off in off_positions:
                        adjN = 1
                        x_off = off[0] 
                        y_off = off[1]
                        while self.position(row,col,y_off,x_off) and (board[row+y_off][col+x_off]==self.player_number*2%3 or board[row+y_off][col+x_off]==0):
                            adjN = adjN+1
                            x_off = x_off + off[0]
                            y_off = y_off + off[1]
                            adjMax = max(adjMax,adjN)
                        point = point + adjMax**2
      
        return point

    def eval4(self,board):
        row = 5
        col = 0
        adjN = 0
        adjMax = 0
        point = 0
        off_positions = [(-1,-1),(-1,0),(-1,1),(0,1)]
        for row in range(5,0,-1):
            for col in range(6): 
                if board[row][col]==self.player_number*4%5:
                    for off in off_positions:
                        adjN = 1
                        x_off = off[0] 
                        y_off = offset[1]
                        while self.position(row,col,y_off,x_off) and (board[row+y_off][col+x_off]==self.player_number*4%5 or board[row+y_off][col+x_off]==0):
                            adjN = adjN+1
                            x_off = x_off + off[0]
                            y_off = y_off + off[1]
                            adjMax = max(adjMax,adjN)
                        point = point + adjMax**2
      
        return point   


    """def evaluation_function(self, board):
        score=self.eval(board,self.player_number)
        return score"""



#Refrences: 
#https://medium.com/analytics-vidhya/artificial-intelligence-at-play-connect-four-minimax-algorithm-explained-3b5fc32e4a4f
#https://github.com/avteja/Connect-4
#https://identity.pub/2019/10/16/minimax-connect4.html



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

