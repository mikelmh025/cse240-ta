import numpy as np
from operator import itemgetter

win_count=0

class AIPlayer:
    def __init__(self, player_number):
        self.player_number = player_number
        self.type = 'ai'
        self.player_string = 'Player {}:ai'.format(player_number)

    def validMoves(self, board):
        moves = []
        for col in range(7):
            for row in range(5,-1,-1):
                if board[row][col] == 0:
                     moves.append([row, col])
                     break
        return moves

    def count_values(self, board, num, player_num):
        noofwins = 0 
        win_string = '{0}' * num 
        win_string = win_string.format(player_num)
        str_convert = lambda a: ''.join(a.astype(str))

        def horizontal(board):
            count = 0
            for row in board:
                if win_string in str_convert(row):
                    count += str_convert(row).count(win_string) 
            return count

        def verticle(board):
             return horizontal(board.T)

        def diagonal(board):
            count = 0 
            for op in [None, np.fliplr]:
                board_operation = op(board) if op else board
                diagram = np.diagonal(board_operation, offset=0).astype(np.int)
                if win_string in str_convert(diagram):
                    count += str_convert(diagram).count(win_string) 
                    for i in range(1, board.shape[1]-3):
                        for offset in [i, -i]:
                            diag = np.diagonal(board_operation, offset=offset)
                            diag = str_convert(diag.astype(np.int))
                            if win_string in diag:
                                count += diag.count(win_string) 
            return count 
        noofwins = horizontal(board) + verticle(board) + diagonal(board) 
        return noofwins

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

        response = 0
        player = self.player_number
        if (player == 1): 
            opponent = 2
        else: 
            opponent = 1
        response = self.count_values( board, 4, player) * 1000
        response += self.count_values( board, 3, player) * 100
        response += self.count_values( board, 2, player) * 10

        response -= self.count_values( board, 4, opponent) * 950 
        response -= self.count_values( board, 3, opponent) * 100 
        response -= self.count_values( board, 2, opponent) * 10

        return response


class RandomPlayer:
    def __init__(self, player_number):
        self.player_number = player_number
        self.type = 'random'
        self.player_string = 'Player {}:random'.format(player_number)

    def get_move(self, board):
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

        valid_cols = []
        for i, col in enumerate(board.T):
            if 0 in col:
                valid_cols.append(i)

        move = int(input('Enter your move: '))

        while move not in valid_cols:
            print('Column full, choose from:{}'.format(valid_cols))
            move = int(input('Enter your move: '))

        return move

