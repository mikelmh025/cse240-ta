import numpy as np

class AIPlayer:
    def __init__(self, player_number):
        self.player_number = player_number
        self.type = 'ai'
        self.player_string = 'Player {}:ai'.format(player_number)

    def ab(self, board, a, b):
        #state == 1 max else min


        top = self.selfsucc(board)
        #nex = self.othersucc(top)
        bf = - 1

        v = float('inf')
        lists = []
        for i in top:


            v1, b1f, b1p, a, b = self.minv(i[0], a, b)
            if v1 < v:
                v = v1
                lists.append((v1, b1f, b1p, a, b))
            if v <= a:
                break
            b = min(b,v)
        v = float('-inf')
        for i in lists:
            if i[0] > v:    

                v, bf, bp, a, b = i
            if v >= b:
                break
            a = max(v,a)
            # if v1 < v:
            #     v, bf, bp, a, b = v1, b1f, b1p, a1, b1

        if(bf == -1):
            v, bf, bp, a, b = self.maxv(board, -float('inf'), float('inf'))

        #v, bf, bp, a, b = self.maxv(bp, a, b)

        columntoreturn = bf

        return (columntoreturn)

    def maxv(self, board, a, b):
        v = -float('inf')
        bs = self.selfsucc(board)
        bf = bs[-1][1]
        bp = bs[-1][2]
        for bn in bs:
            if(v < self.evaluation_function(bn[0])):
                bf = bn[1]
                bp = bn[2]
                v = self.evaluation_function(bn[0])
            if v >= b:
                return v, bf, bp, a, b
            a = max(a,v)
        return v, bf, bp, a, b

    def minv(self, board, a, b):
        v = float('inf')
        bs = self.othersucc(board)
        bf = bs[-1][1]
        for bn in bs:
            if v >self.evaluation_function(bn[0]):
                v = self.evaluation_function(bn[0])
                bf = bn[1]
                bp = bn[2]
            if v <= a:
                return v, bf, bp, a, b
            b = min(b,v)
        return v, bf, bp, a, b

    def selfsucc(self, board):
        if(self.player_number==1):
            other = 2
        else:
            other = 1

        max = 0

        row = 5

        listofsucc = []

        evaluate= -float('inf')
        columntoreturn = 0
        for column in range(0,7): 
            row = 5
            if(board[row][column] ==0):
                #add new board to tree with player on this spot
                b = np.copy(board)
                b[row][column] = self.player_number
                listofsucc.append((b,column,board))

            else:
                while(board[row][column] != 0):
                    row-=1
                    if(row<0):
                        break    
                    if(board[row][column] ==0):
                        b = np.copy(board)
                        b[row][column] = self.player_number
                        listofsucc.append((b,column,board))
                        
        return (listofsucc)

    def othersucc(self, board):
        if(self.player_number==1):
            other = 2
        else:
            other = 1

        max = 0

        row = 5

        listofsucc = []

        evaluate= -float('inf')
        columntoreturn = 0
        for column in range(0,7): 
            row = 5
            if(board[row][column] ==0):
                #add new board to tree with player on this spot
                b = np.copy(board)
                b[row][column] = other
                listofsucc.append((b,column,board))

            else:
                while(board[row][column] != 0):
                    row-=1
                    if(row<0):
                        break    
                    if(board[row][column] ==0):
                        b = np.copy(board)
                        b[row][column] = other
                        listofsucc.append((b,column,board))
                        
        return (listofsucc)

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
        #raise NotImplementedError('Whoops I don\'t know what to do')
        
        

        return self.ab(board, -float('inf'), float('inf'))

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
        #raise NotImplementedError('Whoops I don\'t know what to do')

        #Evaultate all movements

        #Each 1/7 chance of happening

        #So pick max out of all moves

        #Look ahead: first move to all locations
   
        if(self.player_number==1):
            other = 2
        else:
            other = 1

        max = 0

        row = 5

        evaluate= -float('inf')
        columntoreturn = 0
        for column in range(0,7): 
            row = 5
            if(board[row][column] ==0):
                #add new board to tree with player on this spot
                b = np.copy(board)
                b[row][column] = self.player_number
                e = self.evaluation_function(b)
                if(e >= evaluate):
                    evaluate= e
                    columntoreturn = column
            else:
                while(board[row][column] != 0):
                    row-=1
                    if(row<0):
                        break    
                    if(board[row][column] ==0):
                        b = np.copy(board)
                        b[row][column] = self.player_number
                        e = self.evaluation_function(b)
                        if(e >= evaluate):
                            evaluate= e
                            columntoreturn = column


        #create a tree function thingy to pick path            

            #iterate starting from bottom row going up to see 
            #  each open spot in the colum
            #Place your piece in each open column
            # evaulate

        return columntoreturn



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
        if(self.player_number==1):
            other = 2
        else:
            other = 1

        weight = 0

        p1 = 0
        p2 = 0
        rp1 = 0
        rp2 = 0
        cp1 = 0
        cp2 = 0
        rdp1 = 0
        rdp2 = 0
        ldp1 = 0
        ldp2 = 0
        bad = 0

        #print each row
        for row in range(0,6):
            lp1 = 0
            lp2 = 0
            for column  in range(0,6):
                if(board[row][column] != board[row][column+1]):
                    if((lp2==3)and(board[row][column+1] == 0)):
                        bad = 1
                    if((lp2==3)and(column>=3)):
                         if(board[row][column-3]==0):
                             bad = 1
                    if(board[row][column+1])==0:
                        if((lp2==2)and(column<5)):
                            if(board[row][column+2]==other):
                                bad = 1
                        if(board[row][column] == other):
                            if(lp2==0):
                                lp2 = 1
                        if((lp2==1)and(column<4)):
                            if((board[row][column+2]==other)and board[row][column+3]==other):
                                bad = 1
                                #print("NO")
                        

                    lp1 = 0
                    lp2 = 0
                elif(board[row][column] == self.player_number):
                    if(lp1 == 0):
                        lp1 = 1
                    lp1+=1

                elif(board[row][column] == other):
                    if(lp2 == 0):
                        lp2 = 1
                    lp2+=1

                if(lp1>rp1):
                    rp1 = lp1
                if(lp2>rp2):
                    rp2 = lp2

        for column in range(0,7):
            lp1 = 0
            lp2 = 0
            for row  in range(5,0, -1):
                if(board[row-1][column] != board[row][column]):
                    if((lp2==3)and(board[row-1][column] == 0)):
                        bad = 1
                    lp1 = 0
                    lp2 = 0
                elif(board[row-1][column] == self.player_number):
                    if(lp1 == 0):
                        lp1 = 1
                    lp1+=1

                elif(board[row-1][column] == other):
                    if(lp2 == 0):
                        lp2 = 1
                    lp2+=1

                if(lp1>cp1):
                    cp1 = lp1
                if(lp2>cp2):
                    cp2 = lp2


            

        p1 = rp1 + cp1 + rdp1 + ldp1
        p2 = max(rp2, cp2, rdp2, ldp2)



        # for row in range(0,6):
        #     for column  in range(0,7):
        #         print(board[row][column], end = "")
        #     print('\n')
        

        if((rp1 == 4)or(cp1 == 4)or(rdp1 == 4)or(ldp1 == 4)):
             return 400

        if bad:
            return -float('inf')


        return p1-p2


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

