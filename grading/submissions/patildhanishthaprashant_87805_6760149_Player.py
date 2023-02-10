import numpy as np
from operator import itemgetter

class_win=0

class AIPlayer:
    def __init__(self, player_number):
        self.player_number = player_number
        self.type = 'ai'
        self.player_string = 'Player {}:ai'.format(player_number)

    def validMoves(self, board):
        moves_output = []
        for col in range(7):
            for row in range(5,-1,-1):
                 if board[row][col] == 0:
                     moves_output.append([row, col])
                     break
        return moves_output

    def class_count_values(self, board, num, player_num):
            class_no_of_wins = 0 
            first_player_win_str = '{0}' * num 
            first_player_win_str = first_player_win_str.format(player_num)
            str_convert = lambda a: ''.join(a.astype(str))
            
            def class_check_horizontal(board):
                count = 0
                for row in board:
                    if first_player_win_str in str_convert(row):
                        count += str_convert(row).count(first_player_win_str) 
                return count

            def class_check_verticle(board):
                return class_check_horizontal(board.T)

            def class_check_diagonal(board):
                count = 0 
                for op in [None, np.fliplr]:
                    op_board = op(board) if op else board
                    root_diag = np.diagonal(op_board, offset=0).astype(np.int)
                    if first_player_win_str in str_convert(root_diag):
                        count += str_convert(root_diag).count(first_player_win_str) 

                for i in range(1, board.shape[1]-3):
                    for offset in [i, -i]:
                        diag = np.diagonal(op_board, offset=offset)
                        diag = str_convert(diag.astype(np.int))
                        if first_player_win_str in diag:
                            count += diag.count(first_player_win_str) 
                return count 
            class_no_of_wins = class_check_horizontal(board) + class_check_verticle(board) + class_check_diagonal(board)
            return class_no_of_wins

    def get_alpha_beta_move(self, board):

        value = []
    
        def alphabeta( board, depth, alpha, beta, player, opponent):
            for row, col in self.validMoves(board):
                board[row][col] = player
                alpha = max(alpha, min_value(board,alpha, beta,depth + 1 , player, opponent))
                value.append((alpha,col))
                board[row][col] = 0
            max_value = (max(value,key=itemgetter(1))[0]) 
            for item in value:
                if max_value in item:
                    max_index = item[1]
                    break

            return max_index

        def min_value(board, alpha, beta, depth, player, opponent):
            move_valid = self.validMoves(board)
            if(depth == 4 or not move_valid):
                return (self.evaluation_function(board))
            for row,col in move_valid:
                board[row][col] = opponent 
                result = max_value(board, alpha, beta, depth+1, player, opponent)
                beta = min (beta, result)
                board[row][col] = 0
                if beta<= alpha:
                    return beta 
            return beta
        def max_value(board, alpha, beta, depth, player, opponent):
            move_valid = self.validMoves(board)
            if(depth == 4 or not move_valid):
                return (self.evaluation_function(board))
            for row, col in move_valid:
                board[row][col] = player 
                result = min_value(board, alpha, beta, depth+1, player, opponent)
                alpha = max(alpha, result)
                board[row][col] = 0
                if alpha >= beta:
                    return alpha
            return alpha

        player = self.player_number
        if (player == 1): 
            opponent = 2
        else: 
            opponent = 1
        return (alphabeta(board, 0, -100000,+100000, player, opponent)) 
        

        raise NotImplementedError('Whoops I don\'t know what to do')

    def get_expectimax_move(self, board):

        value = []
        def expectimax(board, depth, player, opponent):
            alpha = - 1000000
            for row, col in self.validMoves(board):
                board[row][col] = player
                alpha = max(alpha, exp_val(board,depth - 1 , player, opponent))
                value.append((alpha,col))
                board[row][col] = 0

            max_value = (max(value,key=itemgetter(1))[0]) 
            for item in value:
                if max_value in item:
                    max_index = item[1]
                    break

            return max_index
        def max_val(board, depth, player,opponent):
            move_valid = self.validMoves(board)
            if (depth == 0 or not move_valid): 
                return (self.evaluation_function(board))
            best_value = -100000
            for row,col in move_valid:
                board[row][col] = player 
                val = exp_val(board, depth - 1, player, opponent)
                best_value = max(best_value, val);
            return best_value
        def exp_val(board, depth, player, opponent): 
            move_valid = self.validMoves(board)
            move_length = len(move_valid)
            print (move_length)
            if (depth == 0 or not move_valid): 
                return (self.evaluation_function(board))
            expectedValue = 0
            for row,col in move_valid:
                board[row][col] = opponent 
                val = max_val(board , depth-1, player, opponent)
                expectedValue += val


            return (expectedValue/move_length)

        player = self.player_number
        if (player == 1): 
            opponent = 2
        else: 
            opponent = 1
        return (expectimax(board, 8 , player, opponent))
        raise NotImplementedError('Whoops I don\'t know what to do')




    def evaluation_function(self, board):

        reply = 0
        player = self.player_number
        if (player == 1): 
            opponent = 2
        else: 
            opponent = 1
        reply = self.class_count_values( board, 4, player) * 1000
        reply += self.class_count_values( board, 3, player) * 100
        reply += self.class_count_values( board, 2, player) * 10

        reply -= self.class_count_values( board, 4, opponent) * 950 
        reply -= self.class_count_values( board, 3, opponent) * 100 
        reply -= self.class_count_values( board, 2, opponent) * 10

        return reply
       
        #return 0


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

