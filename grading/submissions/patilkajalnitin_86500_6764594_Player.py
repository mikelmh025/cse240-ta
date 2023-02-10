import numpy as np
from operator import itemgetter

w = 0        
class AIPlayer:
    def __init__(self, player_number):
        self.player_number = player_number
        self.type = 'ai'
        self.player_string = 'Player {}:ai'.format(player_number)


    def val_MOVES(self, board):
        moves = []
        for col in range(7):
            for row in range(5,-1,-1):
                if board[row][col] == 0:
                    moves.append([row, col])
                    break
        return moves

    def count_values(self, board, num, player_num):
        noofwins = 0 
        player_win_str = '{0}' * num 
        player_win_str = player_win_str.format(player_num)
        to_str = lambda a: ''.join(a.astype(str))

        def check_horizontal(b):
            count = 0
            for row in b:
                if player_win_str in to_str(row):
                    count += to_str(row).count(player_win_str) 
            return count

        def check_verticle(b):
            return check_horizontal(b.T)

        def check_diagonal(b):
            count = 0 
            for op in [None, np.fliplr]:
                op_board = op(b) if op else b
                root_diag = np.diagonal(op_board, offset=0).astype(np.int)
                if player_win_str in to_str(root_diag):
                    count += to_str(root_diag).count(player_win_str) 

                for i in range(1, b.shape[1]-3):
                    for offset in [i, -i]:
                        diag = np.diagonal(op_board, offset=offset)
                        diag = to_str(diag.astype(np.int))
                        if player_win_str in diag:
                            count += diag.count(player_win_str) 
            return count 
        noofwins = check_horizontal(board) + check_verticle(board) + check_diagonal(board) 
        return noofwins

    def evaluation_function(self, board):
        rlt = 0
        player = self.player_number
        if (player == 1): 
            opponent = 2
        else: 
            opponent = 1
        rlt = self.count_values( board, 4, player) * 1000
        rlt += self.count_values( board, 3, player) * 100
        rlt += self.count_values( board, 2, player) * 10

        rlt -= self.count_values( board, 4, opponent) * 950 
        rlt -= self.count_values( board, 3, opponent) * 100 
        rlt -= self.count_values( board, 2, opponent) * 10

        return (rlt)

    def get_alpha_beta_move(self, board):
        v = []
    
        def alphabeta( board, depth, alp, bet, player, opponent):
            for row, col in self.val_MOVES(board):
                board[row][col] = player
                alp = max(alp, min_value(board,alp, bet,depth + 1 , player, opponent))
                v.append((alp,col))
                board[row][col] = 0
            maxval = (max(v,key=itemgetter(1))[0]) 
            for item in v:
                if maxval in item:
                    maxin = item[1]
                    break

            return (maxin)

        def min_value(board,alp,bet,depth,player, opponent):
            valid_moves = self.val_MOVES(board)
            if(depth == 4 or not valid_moves):
                return (self.evaluation_function(board))
            for row,col in valid_moves:
                board[row][col] = opponent 
                rlt = max_value(board, alp, bet, depth+1, player, opponent)
                bet = min (bet, rlt)
                board[row][col] = 0
                if bet<= alp:
                    return bet 
            return bet
        def max_value(board,alp, bet, depth, player, opponent):
            valid_moves = self.val_MOVES(board)
            if(depth == 4 or not valid_moves):
                return (self.evaluation_function(board))
            for row, col in valid_moves:
                board[row][col] = player 
                rlt = min_value(board,alp,bet,depth+1, player, opponent)
                alp = max(alp, rlt)
                board[row][col] = 0
                if alp >= bet:
                    return alp
            return alp

        player = self.player_number
        if (player == 1): 
            opponent = 2
        else: 
            opponent = 1
        return (alphabeta(board, 0, -100000,+100000, player, opponent)) 
        raise NotImplementedError('Whoops I don\'t know what to do')


   
    def get_expectimax_move(self, board):
        v = []
        def expectimax(board, depth, player, opponent):
            alp = - 1000000
            for row, col in self.val_MOVES(board):
                board[row][col] = player
                alp = max(alp, exp_val(board,depth - 1 , player, opponent))
                v.append((alp,col))
                board[row][col] = 0

            maxval = (max(v,key=itemgetter(1))[0]) 
            for item in v:
                if maxval in item:
                    maxin = item[1]
                    break

            return (maxin)
        def max_val(board, depth, player,opponent):
            valid_moves = self.val_MOVES(board)
            if (depth == 0 or not valid_moves): 
                return (self.evaluation_function(board))
            bestValue = -100000
            for row,col in valid_moves:
                board[row][col] = player 
                val = exp_val(board, depth - 1, player, opponent)
                bestValue = max(bestValue, val);
            return bestValue
        def exp_val(board, depth, player, opponent): 
            valid_moves = self.val_MOVES(board)
            lengthmoves = len(valid_moves)
            print (lengthmoves)
            if (depth == 0 or not valid_moves): 
                return (self.evaluation_function(board))
            expectedValue = 0
            for row,col in valid_moves:
                board[row][col] = opponent 
                val = max_val(board , depth-1, player, opponent)
                expectedValue += val


            return (expectedValue/lengthmoves)

        player = self.player_number
        if (player == 1): 
            opponent = 2
        else: 
            opponent = 1
        return (expectimax(board, 8 , player, opponent))

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