import numpy as np
import time

class AIPlayer:
    def __init__(self, player_number):
        self.player_number = player_number
        self.type = 'ai'
        self.player_string = 'Player {}:ai'.format(player_number)

    def value(self,board,alpha,beta,depth,t,column):
        if(depth == 0):
            return self.evaluation_function(board,column)
        elif(t):
            return self.max_value(board,alpha,beta,depth)
        else:
            return self.min_value(board,alpha,beta,depth)

    def max_value(self,board,alpha,beta,depth):

        # print("max:",depth)
        # print(board)

        # Initialize 'v'
        v = (-np.inf,-1)
        
        # Genereate successors of the board, based on where a disc can be placed
        for i in range(len(board[0])):
            for j in reversed(range(len(board))):

                # If there exists an empty slot for the disc
                if(board[j,i] == 0):

                    # Generate a temporary board and put in the disc
                    temp_board = board
                    temp_board[j,i] = self.player_number

                    # print("max:",depth,"temp_board:")
                    # print(temp_board)

                    # Determine 'v' and 'alpha' values
                    prev_max = v[0]
                    LL = list(v)
                    LL[0] = max(LL[0],self.value(temp_board,alpha,beta,depth-1,0,i)[0])
                    if(prev_max != LL[0]):
                        LL[1] = i
                    v = tuple(LL)

                    # if(depth == 1):
                    #     print("should compare now..? v[0] = ",v[0],"v[1] = ",v[1])

                    temp_board[j,i] = 0
                    
                    # print("still in max...",depth)

                    # Comparison
                    if(v[0] >= beta):
                        # print("max-early return")
                        # print("v[0]: ",v[0])
                        # print("beta: ",beta)
                        return v
                    alpha = max(alpha,v[0])

                    # Move to next column
                    break

        # Default exit
        # print("max return")
        return v

    def min_value(self,board,alpha,beta,depth):

        # print("min:",depth)
        # print(board)
        
        # Initialize 'v'
        v = (np.inf,-1)
        
        # Genereate successors of the board, based on where a disc can be placed
        for i in range(len(board[0])):
            for j in reversed(range(len(board))):

                # If there exists an empty slot for the disc
                if(board[j,i] == 0):

                    # Generate a temporary board and put in the disc
                    temp_board = board

                    if(self.player_number == 1):
                        temp_board[j,i] = 2
                    else:
                        temp_board[j,i] = 1

                    # print("min:",depth,"temp_board:")
                    # print(temp_board)

                    # Determine 'v' and 'beta' values
                    prev_max = v[0]
                    LL = list(v)
                    LL[0] = min(LL[0],self.value(temp_board,alpha,beta,depth-1,1,i)[0])
                    if(prev_max != LL[0]):
                        LL[1] = i
                    v = tuple(LL)

                    temp_board[j,i] = 0
                    
                    # print("still in min...",depth)

                    # Comparison
                    if(v[0] <= alpha):
                        # print("min-early return")
                        return v
                    beta = min(beta,v[0])

                    # Move to next column
                    break

        # Default exit
        # print("min-return")
        return v

    def get_alpha_beta_move(self, board):

        # Optimal chip placement
        if(self.chip_count(board) < 1):
            return 3

        # alpha-beta algorithm
        else:

            # t1 = time.time()
            # data = self.max_value(board,-np.inf,np.inf,8)[1]
            # t2 = time.time()
            # print(t2-t1)
            # return data
            
            return self.max_value(board,-np.inf,np.inf,3)[1]
            
    def get_expectimax_move(self, board):
        return self.expectimax_maxValues(board,3)[1]

    def expectimax_value(self,board,depth,t,column):
        if(depth == 0):
            return self.evaluation_function(board,column)
        elif(t):
            return self.expectimax_maxValues(board,depth)
        else:
            return self.expectimax_expValues(board,depth,column)

    def expectimax_maxValues(self,board,depth):

        # Initialize 'v'
        v = (0,-1)

        # Genereate successors of the board, based on where a disc can be placed
        for i in range(len(board[0])):
            for j in reversed(range(len(board))):

                # If there exists an empty slot for the disc
                if(board[j,i] == 0):

                    # Generate a temporary board and put in the disc
                    temp_board = board
                    temp_board[j,i] = self.player_number

                    # Determine the max 'v'
                    prev_max = v[0]
                    LL = list(v)
                    LL[0] = max(LL[0],self.expectimax_value(temp_board,depth-1,0,i)[0])
                    if(prev_max != LL[0]):
                        LL[1] = i
                    v = tuple(LL)

                    # Move to next column
                    break

        # Default exit
        return v

    def expectimax_expValues(self,board,depth,column):
        
        # Initialize 'v'
        v = (0,-1)

        # Counter of open slots
        open_slot = 0

        # List of successor values
        successor_values = []

        # Genereate successors of the board, based on where a disc can be placed
        for i in range(len(board[0])):
            for j in reversed(range(len(board))):

                # If there exists an empty slot for the disc
                if(board[j,i] == 0):

                    # Increment to represent the number of open slots
                    open_slot += 1

                    # Generate a temporary board and put in the disc
                    temp_board = board
                    temp_board[j,i] = self.player_number

                    # Determine the 'v'
                    prev_value = v[0]
                    LL = list(v)
                    LL[0] = self.expectimax_value(temp_board,depth-1,1,i)[0]
                    if(prev_value != LL[0]):
                        LL[1] = i
                    v = tuple(LL)

                    # Append 'v' to successor list
                    successor_values.append(LL[0])

                    # Move to next column
                    break

        # Default exit
        return self.expectimax_expectation(successor_values,open_slot,column)

    def expectimax_expectation(self,successor_values,open_slot,column):
        if(column > 0):
            return((sum(successor_values)/open_slot),column)
        else:
            return (0,column)

    def evaluation_function(self, board, column):

        # print(board)

        # Determine the number of different types of connections on the board

        # NOTE: We can tweak the how_many functions to account for how many different connections our opponent has and from there
        #       determine how strong the board is in their favor! Technique is to copy the functions but change the comparsion to
        #       be != self.player_number, to represent our opponent!
        opponent_number = 0
        if(self.player_number == 1):
            opponent_number = 2
        else:
            opponent_number = 1

        player_num_of_4_conn = self.evaluation_function_how_many_4_connected(board,self.player_number)
        player_num_of_3_conn = self.evaluation_function_how_many_3_connected(board,self.player_number)
        player_num_of_2_conn = self.evaluation_function_how_many_2_connected(board,self.player_number)
        player_num_of_1_conn = self.evaluation_function_how_many_1_open(board,self.player_number)

        opponent_num_of_4_conn = self.evaluation_function_how_many_4_connected(board,opponent_number)
        opponent_num_of_3_conn = self.evaluation_function_how_many_3_connected(board,opponent_number)
        opponent_num_of_2_conn = self.evaluation_function_how_many_2_connected(board,opponent_number)
        opponent_num_of_1_conn = self.evaluation_function_how_many_1_open(board,opponent_number)

        # Convert the different types of connections into points
        point_value = 5
        # total = ((num_of_4_conn * pow(point_value,3)) + 
        #          (num_of_3_conn * pow(point_value,2)) + 
        #          (num_of_2_conn * pow(point_value,1)) + 
        #          (num_of_1_conn * pow(point_value,0)))

        if(player_num_of_4_conn > 1):
            total = 1000
        elif(opponent_num_of_4_conn > 1):
            total = -1000
        else:
            total = (((player_num_of_3_conn - opponent_num_of_3_conn) * pow(point_value,2)) + 
                     ((player_num_of_2_conn - opponent_num_of_2_conn) * pow(point_value,1)) + 
                     ((player_num_of_1_conn - opponent_num_of_1_conn) * pow(point_value,0)))
        
        # print("Utility evaluated as:",total)
        # print(self.count_board(board))
        # print(board)

        # print("# of num_of_4_conn:",num_of_4_conn)
        # print("# of num_of_2_conn:",num_of_3_conn)
        # print("# of num_of_3_conn:",num_of_2_conn)
        # print("# of num_of_1_conn:",num_of_1_conn) 
       
        # Return the determined utility of the board
        return (total,column)

    def evaluation_function_how_many_4_connected(self,board,target_chip): 
        
        # Running sum
        num_of_4_conn = 0

        # Horizontal Check
        # Checks from (0,0) to (5,3)
        for i in range (len(board)):
            for j in range (len(board[0])-3):
                if(board[i][j] != 0):
                    if(board[i][j] == target_chip and
                       board[i][j+1] == target_chip and
                       board[i][j+2] == target_chip and
                       board[i][j+3] == target_chip):
                        num_of_4_conn += 1

        # Vertical Check
        # Checks from (0,0) to (2,6)
        for i in range (len(board)-3):
            for j in range (len(board[0])):
                if(board[i][j] != 0):
                    if(board[i][j] == target_chip and
                       board[i+1][j] == target_chip and
                       board[i+2][j] == target_chip and
                       board[i+3][j] == target_chip):
                        num_of_4_conn += 1

        # Descending Diagonal Check
        # Checks from (0,3) to (2,6)
        for i in range (len(board)-3):
            for j in range(3,len(board[0])):
                if(board[i][j] != 0):
                        if(board[i][j] == target_chip and
                           board[i+1][j-1] == target_chip and
                           board[i+2][j-2] == target_chip and
                           board[i+3][j-3] == target_chip):
                            num_of_4_conn += 1

        # Ascending Diagonal Check
        # Checks from (3,0) to (2,6)
        for i in range (3,len(board)):
            for j in range(len(board[0])-3):
                if(board[i][j] != 0):
                        if(board[i][j] == target_chip and
                           board[i-1][j+1] == target_chip and
                           board[i-2][j+2] == target_chip and
                           board[i-3][j+3] == target_chip):
                            num_of_4_conn += 1

        return num_of_4_conn

    def evaluation_function_how_many_3_connected(self,board,target_chip):

        # Running sum
        num_of_3_conn = 0

        # Horizontal Check
        # Checks from (0,0) to (5,4)
        for i in range (len(board)):
            for j in range (len(board[0])-2):
                if(board[i][j] != 0):
                    if(board[i][j] == target_chip and
                       board[i][j+1] == target_chip and
                       board[i][j+2] == target_chip):
                        num_of_3_conn += 1

        # Vertical Check
        # Checks from (0,0) to (3,6)
        for i in range (len(board)-2):
            for j in range (len(board[0])):
                if(board[i][j] != 0):
                    if(board[i][j] == target_chip and
                       board[i+1][j] == target_chip and
                       board[i+2][j] == target_chip):
                        num_of_3_conn += 1

        # Descending Diagonal Check
        # Checks from (0,2) to (3,6)
        for i in range (len(board)-2):
            for j in range(2,len(board[0])):
                if(board[i][j] != 0):
                        if(board[i][j] == target_chip and
                           board[i+1][j-1] == target_chip and
                           board[i+2][j-2] == target_chip):
                            num_of_3_conn += 1

        # Ascending Diagonal Check
        # Checks from (2,0) to (5,4)
        for i in range (2,len(board)):
            for j in range(len(board[0])-2):
                if(board[i][j] != 0):
                        if(board[i][j] == target_chip and
                           board[i-1][j+1] == target_chip and
                           board[i-2][j+2] == target_chip):
                            num_of_3_conn += 1

        return num_of_3_conn

    def evaluation_function_how_many_2_connected(self,board,target_chip):

        # Running sum
        num_of_2_conn = 0

        # Horizontal Check
        # Checks from (0,0) to (5,5)
        for i in range (len(board)):
            for j in range (len(board[0])-1):
                if(board[i][j] != 0):
                    if(board[i][j] == target_chip and
                       board[i][j+1] == target_chip):
                        num_of_2_conn += 1

        # Vertical Check
        # Checks from (0,0) to (4,6)
        for i in range (len(board)-1):
            for j in range (len(board[0])):
                if(board[i][j] != 0):
                    if(board[i][j] == target_chip and
                       board[i+1][j] == target_chip):
                        num_of_2_conn += 1

        # Descending Check
        # Checks from (0,1) to (4,6)
        for i in range (len(board)-1):
            for j in range(1,len(board[0])):
                if(board[i][j] != 0):
                        if(board[i][j] == target_chip and
                           board[i+1][j-1] == target_chip):
                            num_of_2_conn += 1
        # Ascending Check
        # Checks from (1,0) to (5,5)
        for i in range (1,len(board)):
            for j in range(len(board[0])-1):
                if(board[i][j] != 0):
                        if(board[i][j] == target_chip and
                           board[i-1][j+1] == target_chip):
                            num_of_2_conn += 1

        return num_of_2_conn

    def evaluation_function_how_many_1_open(self,board,target_chip):
        
        # Running sum
        num_of_1_conn = 0

        for i in range (len(board)):
            for j in range (len(board[0])):
                if(board[i][j] == target_chip):

                    # Grounded '1'
                    if(i == len(board)-1):

                        # Check statement
                        # print("Grounded '1' at",i,j,"Checking coordinates...")
                        
                        # Check for an open space @ 3 o' clock
                        if(j+1 < len(board[0])):
                            if(board[i,j+1] == 0):
                                # print("open space at",i,j+1)
                                num_of_1_conn += 1

                        # Check for an open space @ 9 o' clock
                        if(j-1 >= 0):
                            if(board[i,j-1] == 0):
                                # print("open space at",i,j-1)
                                num_of_1_conn += 1

                        # Check for an open space @ 12 o' clock
                        if(board[i-1,j] == 0):
                            # print("open space at",i-1,j)
                            num_of_1_conn += 1

                        # Check for an open space ascending right
                        if(j+1 < len(board[0])):
                            if((board[i-1,j+1] == 0) and board[i][j+1] != 0):
                                # print("open space at",i-1,j+1)
                                num_of_1_conn += 1

                        # Check for an open space ascending left
                        if(j-1 >= 0):
                            if((board[i-1][j-1] == 0) and board[i][j-1]):
                                # print("open space at",i-1,j-1)
                                num_of_1_conn += 1

                    # Flying '1'
                    else:

                        # Check statement
                        # print("Flying '1' at",i,j,"Checking coordinates...")

                        # Check for an open space @ 3 o' clock
                        if((j+1 < len(board[0])) and (i-1 >= 0)):
                            if((board[i,j+1] == 0) and (board[i-1,j+1] != 0)):
                                # print("open space at",i,j+1)
                                num_of_1_conn += 1

                        # Check for an open space @ 9 o' clock
                        if((j-1 >= 0) and (i-1 >= 0)):
                            if((board[i,j-1] == 0) and (board[i-1,j-1] != 0)):
                                # print("open space at",i,j-1)
                                num_of_1_conn += 1

                        # Check for an open space @ 12 o' clock
                        if(i-1 >= 0):
                            if(board[i-1,j] == 0):
                                # print("open space at",i-1,j)
                                num_of_1_conn += 1

                        # Check for an open space ascending right
                        if((j+1 < len(board[0])) and i-1 >= 0):
                            if((board[i-1,j+1] == 0) and board[i][j+1] != 0):
                                # print("open space at",i-1,j+1)
                                num_of_1_conn += 1

                        # Check for an open space ascending left
                        if((j-1 >= 0) and (i-1 >= 0)):
                            if((board[i-1][j-1] == 0) and board[i][j-1]):
                                # print("open space at",i-1,j-1)
                                num_of_1_conn += 1

                        # Check for an open space descending right
                        if((i+1 < len(board)) and (j+1 < len(board[0]))):
                            if(board[i+1][j+1] != 0):
                                # print("open space at",i+1,j+1)
                                num_of_1_conn += 1

                        # Check for an open space descending left
                        if((i+1 < len(board)) and (j-1 >= 0)):
                            if(board[i+1][j-1] != 0):
                                # print("open space at",i+1,j-1)
                                num_of_1_conn += 1
        return num_of_1_conn

    def chip_count(self,board):
        count = 0
        for i in range(len(board[0])):
            for j in range(1,3):
                if(board[len(board)-j,i] != 0):
                    count += 1
                    if(count > 2):
                        return count
        return count

    def count_board(self,board):
        
        p1 = 0
        p1_chip = self.player_number
        
        p2 = 0
        p2_chip = 0
        if(p1_chip == 1):
            p2_chip = 2
        else:
            p2_chip = 1

        for i in range(len(board)):
            for j in (range(len(board[0]))):
                if(board[i][j] == p1_chip):
                    p1 += 1
                elif(board[i][j] == p2_chip):
                    p2 += 1

        return(p1,p2)

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