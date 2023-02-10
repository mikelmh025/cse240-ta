import numpy as np
import time
class AIPlayer:
    def __init__(self, player_number):
        self.player_number = player_number
        self.type = 'ai'
        self.player_string = 'Player {}:ai'.format(player_number)
        self.matrix_value = []
        self.maxDepth = 4
        self.WinMove = False
        self.LoseMove = False
        self.startTime = 0

    def get_alpha_beta_move(self, board):
        self.startTime = time.time()
        movecol = 3
        initValue = -float('inf')
        #valid_cols = self.validCol(board)

        for i in range(0,7):
            if self.notFullCol(board, i):
                currentRow = self.validRow(board, i) 
                board[currentRow, i] = self.player_number
                val = self.recMinMax(board, 1, -float('inf'), float('inf'), False)
                board[currentRow, i ] = 0
                if val > initValue:
                    initValue = val
                    movecol = i

        #print(movecol)
        end = time.time()
        print(self.startTime)
        print(end)
        print("time taken for play")

        print(end-self.startTime)
        return movecol
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
    def notFullCol(self, board, col):
        if board[0][col] == 0 :
            return True
        return False
    def recMinMax(self, board, depth, alpha, beta, maxplayer):

        if depth == 4 or self.filledBoard(board) or self.WinMove or self.LoseMove:
            eval = self.evaluation_function(board)
            #print("this is the last value of the branch")

            if self.WinMove:
                eval += 9999999999999999
                self.WinMove =False
            elif self.LoseMove:
                print("lose score")
                eval -= 9999999999999999
                self.LoseMove =False      
                print(eval)         
            #print(eval)    
            return eval
        
        if maxplayer:
            bestScore = -float('inf')
            for col in range(0,7):

                currentRow = self.validRow(board,col)
                board[currentRow, col] = self.player_number
                val = self.recMinMax(board, depth+1, alpha, beta, False)
                board[currentRow, col] = 0
                bestScore = max(val, bestScore)
                alpha = max(bestScore,alpha)

                if beta <= alpha:
                    
                    break
            return bestScore

        else:
            bestScore = float('inf')
            for col in range(0,7):

                currentRow = self.validRow(board,col)
                if(self.player_number == 1):
                    board[currentRow, col] = 2
                else:
                    board[currentRow, col] = 1
                val = self.recMinMax(board, depth+1, alpha, beta, True)
                board[currentRow, col] = 0
                bestScore = min(val, bestScore)
                beta = min(bestScore,beta)

                if beta <= alpha:
                    
                    break
            return bestScore
        
    def validCol(self, board, row):
        opencol = []
        for col in range(0,7):
            if board[0][col] == 0:
                opencol.append(col)
        return opencol
    
    def validRow(self,board, col):
        for i in range(5,-1,-1):
            if board[i][col] == 0:
                return i

    def filledBoard(self, board):
        for col in range(0,7):
            if board[0,col] == 0:
                return False
        return True
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
        self.startTime = time.time()
        movecol = 3
        initValue = -float('inf')
        #valid_cols = self.validCol(board)

        for i in range(0,7):
            if self.notFullCol(board, i):
                currentRow = self.validRow(board, i) 
                board[currentRow, i] = self.player_number
                val = self.recExpectiMax(board, 1, -float('inf'), 0, False)
                board[currentRow, i ] = 0
                if val > initValue:
                    initValue = val
                    movecol = i

        #print(movecol)
        end = time.time()
        print("start time")
        print(self.startTime)

        print("End time")
        print(end)
        
        print("time taken for play")

        print(self.startTime-end)
        return movecol
        raise NotImplementedError('Whoops I don\'t know what to do')

    def recExpectiMax(self, board, depth, alpha,beta,isMaxVal):

        if depth == 4 or self.filledBoard(board) or self.WinMove or self.LoseMove:
            eval = self.evaluation_function(board)
            #print("this is the last value of the branch")

            if self.WinMove:
                eval += 9999999999999999
                self.WinMove =False
            elif self.LoseMove:
                print("lose score")
                eval -= 9999999999999999
                self.LoseMove =False      
                print(eval)         
            #print(eval)    
            return eval
        if isMaxVal:
            bestScore = -float('inf')
            for col in range(0,7):

                currentRow = self.validRow(board,col)
                board[currentRow, col] = self.player_number
                val = self.recMinMax(board, depth+1, alpha, beta, False)
                board[currentRow, col] = 0
                bestScore = max(val, bestScore)
                alpha = max(bestScore,alpha)

                if beta <= alpha:
                    
                    break
            return bestScore
        else:
            bestScore = 0
            for col in range(0,7):

                currentRow = self.validRow(board,col)
                if(self.player_number == 1):
                    board[currentRow, col] = 2
                else:
                    board[currentRow, col] = 1
                val = self.recMinMax(board, depth+1, alpha, beta, True)
                board[currentRow, col] = 0
                bestScore = min(val, bestScore)
                beta = bestScore/len(self.validCol(board, currentRow))

                if beta <= alpha:
                    
                    break
            return bestScore

        



    def evaluation_function(self, board):

        utility_value = 0

        p1_score = 0
        p2_score = 0
        empty_row = 0

        self.WinMove == False
        self.LoseMove == False
        firstRow = False
        
        enemy_player = 2
        if self.player_number == 2: enemy_player = 1
        
        for i in range(5,-1,-1):
        #for i in range(0,6):
            for j in range(0,7):
                #print("the index is ")
                #print(i)
                piece = board[i][j]
                if piece == 0:
                    empty_row+=1
                elif piece == self.player_number:
                    p1_score += self.row_potential(self.player_number,enemy_player,board,i,j)
                    p1_score += self.column_potential(self.player_number,enemy_player,board,i,j)
                    p1_score += self.diag_potential_rigth(self.player_number,enemy_player,board,i,j)
                    p1_score += self.diag_potential_left(self.player_number,enemy_player,board,i,j)


                elif piece == enemy_player:
                    p2_score += self.row_potential(enemy_player,self.player_number,board,i,j)
                    p2_score += self.column_potential(enemy_player,self.player_number,board,i,j)
                    p2_score += self.diag_potential_rigth(enemy_player,self.player_number,board,i,j)
                    p2_score += self.diag_potential_left(enemy_player,self.player_number,board,i,j)
            #if empty_row == 7:
             #   firstRow = True
             #   break
        if firstRow:
            p1_score = 10 
        print("My score")
        print(p1_score)
        print("enemy score")
        print(p2_score)
        if(p1_score >= 10000):
            self.WinMove = True   
        if(p2_score >= 10000):
            print("Im going to lose")
            self.LoseMove = True
        #if(self.player_number == 1 and p2_score >= 10000):
        #    self.LoseMove = True                  
        utility_value = p1_score - p2_score

        return utility_value
    

    def row_potential(self, player, opp, board, current_row, current_col):
        #How many potential lines there are in the row for the player or opponent
        pScore = 10
        numbPieces = 0

        for i in range(current_col,7):
            if(board[current_row][i] == player):
                numbPieces+=1
            elif board[current_row][i] == opp:
                numbPieces = 0
                break
            else:
                break
        if numbPieces == 4:
            pScore+=10000
        elif numbPieces == 3:
            pScore+=30
        elif numbPieces == 2:
            pScore +=15
        numbPieces = 0

        for i in range(current_col, -1,-1):
            if board[current_row][i] == player:
                numbPieces+=1
            elif board[current_row][i] == opp:
                numbPieces = 0
                break
            else:
                break
        if numbPieces == 4:
            pScore+=10000
        elif numbPieces == 3:
            pScore+=30
        elif numbPieces == 2:
            pScore +=15                
        return pScore
        
    def column_potential(self, player, opp, board, current_row, current_col):
        #How many potential lines there are in the column for the player or opponent
        pScore = 10
        numbPieces = 0

        for i in range(current_row,6):
            if(board[i][current_col] == player):
                numbPieces+=1
            elif(board[i][current_col] == opp):
                numbPieces = 0
                break
            else:
                break
        if numbPieces == 4:
            pScore+=10000
        elif numbPieces == 3:
            pScore+=30
        elif numbPieces == 2:
            pScore +=15


        
        return pScore

    def diag_potential_rigth(self, player,opp, board, current_row, current_col):
        #How many potential lines there are in the diag for the player or opponent
        pScore = 10
        numbPieces = 0

        for i in range(current_col,7):
            for j in range(current_row,6):
                if(board[j][i] == player):
                    numbPieces+=1
                elif (board[j][i] == opp):
                    numbPieces = 0
                else:
                    break
        if numbPieces == 4:
            pScore+=10000
        elif numbPieces == 3:
            pScore+=30
        elif numbPieces == 2:
            pScore +=15

        numbPieces = 0    

        for i in range(current_col,-1,-1):
            for j in range(current_row,-1,-1):
                if(board[j][i] == player):
                    numbPieces+=1
                elif (board[j][i] == opp):
                    numbPieces = 0
                else:
                    break
        if numbPieces == 4:
            pScore+=10000
        elif numbPieces == 3:
            pScore+=30
        elif numbPieces == 2:
            pScore +=15        

        return pScore
    def diag_potential_left(self, player, opp, board, current_row, current_col):
        #How many potential lines there are in the diag for the player or opponent
        pScore = 10
        numbPieces = 0

        for i in range(current_row,6):
            for j in range (current_col,-1,-1 ):
                if(board[i][j] == player):
                    numbPieces+=1
                elif (board[i][j] == opp):
                    numbPieces = 0
                else:
                    break
        
        if numbPieces == 4:
            pScore+=10000
        elif numbPieces == 3:
            pScore+=30
        elif numbPieces == 2:
            pScore +=15
        numbPieces = 0

        for i in range(current_row,-1,-1):
            for j in range (0,current_col):
                if(board[i][j] == player):
                    numbPieces+=1
                elif (board[i][j] == opp):
                    numbPieces = 0
                    numbPieces = 0
                else:
                    break

        if numbPieces == 4:
            pScore+=10000
        elif numbPieces == 3:
            pScore+=30
        elif numbPieces == 2:
            pScore +=15
        return pScore
    
    



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

