import numpy as np

class AIPlayer:
    def __init__(self, player_number):
        self.player_number = player_number
        self.type = 'ai'
        self.player_string = 'Player {}:ai'.format(player_number)

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
        # raise NotImplementedError('Whoops I don\'t know what to do')
        max_depth = 4
        alpha = -float('inf')
        beta = float('inf')

        move = self.alpha_move(board, alpha, beta, 0, max_depth, True)
        # move = self.max_move(board, 0, max_depth)
        print(self.player_number,"move:",move)
        return move

    def insert_board(self, board, column, player):
        board = np.copy(board)
        for i in reversed(range(len(board))):
            if board[i][column] == 0:
                board[i][column] = player
                return board
        return False

    def alpha_move(self, board, alpha, beta, depth, max_depth, game_over=False):
        if depth == max_depth:
            score = self.evaluation_function(board)
            return score
        column = 0
        for i in range(board.shape[1]):
            new_board = self.insert_board(board, i, self.player_number)
            if not isinstance(new_board, bool):
                
                if game_over and self.game_over(new_board, self.player_number) == True:
                    score = 100
                else:
                    score = self.beta_move(new_board, alpha, beta, depth+1, max_depth, game_over)
                if score > alpha:
                    alpha = score
                    column = i
                # if score > beta:
                #     break
        if depth == 0:
            print("score", score)
            return column
        return alpha

    def beta_move(self, board, alpha, beta, depth, max_depth, game_over):
        if depth == max_depth:
            score = self.evaluation_function(board)
            return score
        column = 0
        for i in range(board.shape[1]):
            new_board = self.insert_board(board, i, (0,2,1)[self.player_number])
            if not isinstance(new_board, bool):
                if game_over and self.game_over(new_board, [0,2,1][self.player_number]) == True:
                    score = -100
                else:
                    score = self.alpha_move(new_board, alpha, beta, depth+1, max_depth, game_over)
                if score < beta:
                    beta = score
                # if score < alpha:
                #     break
        if depth == 0:
            return column
        return beta

    def max_move(self, board, depth, max_depth, game_over=False):
        if depth == max_depth:
            score = self.evaluation_function(board)
            return score
        column = 0
        alpha = -float('inf')
        for i in range(board.shape[1]):
            new_board = self.insert_board(board, i, self.player_number)
            if not isinstance(new_board, bool):
                if game_over and self.game_over(new_board, self.player_number) == True:
                    score = 100
                else:
                    score = self.expected_move(new_board, depth+1, max_depth, game_over)
                if score > alpha:
                    alpha = score
                    column = i
        if depth == 0:
            print("score", score)
            return column
        return alpha

    def expected_move(self, board, depth, max_depth, game_over):
        if depth == max_depth:
            score = self.evaluation_function(board)
            return score
        score = 0
        for i in range(board.shape[1]):
            new_board = self.insert_board(board, i, self.player_number)
            if not isinstance(new_board, bool):
                if game_over and self.game_over(new_board, [0,2,1][self.player_number]) == True:
                    score += 100/board.shape[1]
                else:
                    score += self.max_move(new_board, depth+1, max_depth, game_over)/board.shape[1]
        # print("score:",score)
        return score






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
        # raise NotImplementedError('Whoops I don\'t know what to do')
        max_depth = 2

        move = self.max_move(board, 0, max_depth)
        print(self.player_number,"move:",move)
        return move


    def activation_function(self, x):
        return 12/(1+2.71**(-x/3))-6

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
        next_turn = np.argmin([np.count_nonzero(board == 1), np.count_nonzero(board == 2)])+1
        next_turn = next_turn == self.player_number
        # player = (sum(board == 1) >= sum(board == 2)) + 1
        # print(board)
        your_min_turns = 1000
        player_pieces = np.stack(np.where(board==self.player_number), axis=1)
        for position in player_pieces:
            your_min_turns = min(your_min_turns, self.turns_to_win(board, position))
        their_min_turns = 1000
        player_pieces = np.stack(np.where(board==(0,2,1)[self.player_number]), axis=1)
        for position in player_pieces:
            their_min_turns = min(their_min_turns, self.turns_to_win(board, position))
        # print("your turns:", your_min_turns, "their turns:", their_min_turns)
        if their_min_turns <= 1 and not next_turn:
            return -99
        elif your_min_turns <=1 and next_turn:
            return 99
        return -1*self.activation_function(your_min_turns)*[0.99, 1.01][next_turn] + self.activation_function(their_min_turns)

    def game_over(self, board, player):
        min_turns = float('inf')
        player_pieces = np.stack(np.where(board==player), axis=1)
        for position in player_pieces:
            min_turns = min(min_turns, self.turns_to_win(board, position))
            if min_turns == 0:
                # print("potential win for player:",player)
                return True
        return False


    def turns_to_win(self, board, pos):
        best_path = ""
        player = board[pos[0], pos[1]]
        if player == 0:
            print("player:", player)
        # down
        least_moves = 1000
        for i in range(4):
            num_moves = 0
            if pos[0]-i >= 0 and pos[0]-i+3 < board.shape[0]:
                for ix in range(0,4):
                    if board[pos[0]+ix-i][pos[1]] == 0:
                        num_moves += sum(board[pos[0]+ix-i:, pos[1]] == 0)
                    elif board[pos[0]+ix-i][pos[1]] == player:
                        continue
                    else:
                        break
                else:
                    # print(num_moves, "down", pos[0]-i, pos[1], "i:",i)
                    # if(num_moves == 0):
                    #     print(num_moves, "down", pos[0]-i, pos[1], "i:",i)
                    best_path = str(num_moves)+ " down "+ str(pos[0]-i) +" "+ str(pos[1])+ " i: "+str(i)
                    least_moves = min(num_moves, least_moves)

        # right
        for i in range(4):
            num_moves = 0
            if pos[1]-i >= 0 and pos[1]-i+3 < board.shape[1]:
                for iy in range(0,4):
                    if board[pos[0]][pos[1]+iy-i] == 0:
                        num_moves += sum(board[pos[0]:, pos[1]+iy-i] == 0)
                    elif board[pos[0]][pos[1]+iy-i] == player:
                        continue
                    else:
                        break
                else:
                    # print(num_moves, "right", pos[0], (pos[1]-i), "i:",i)
                    # if(num_moves == 0):
                    #     print(num_moves, "right", pos[0], (pos[1]-i), "i:",i)
                    best_path = str(num_moves)+ " right "+ str(pos[0]) +" "+ str(pos[1]-i)+ " i: "+str(i)
                    least_moves = min(num_moves, least_moves)

        # down right slope
        for i in range(4):
            num_moves = 0
            # pos[1] is column number HORIZONTAL
            # pos[0] is height inversed VERTICAL
            if pos[1]-i >= 0 and pos[1]-i+3 < board.shape[1] and pos[0]-i >= 0 and pos[0]-i+3 < board.shape[0]:
                for ixy in range(0,4):
                    if board[pos[0]+ixy-i][pos[1]+ixy-i] == 0:
                        num_moves += sum(board[pos[0]+ixy-i:, pos[1]+ixy-i] == 0)
                    elif board[pos[0]+ixy-i][pos[1]+ixy-i] == player:
                        continue
                    else:
                        break
                else:
                    # print(num_moves, "down right", pos[0]-i, (pos[1]-i), "i:",i)
                    # if(num_moves == 0):
                    #     print(num_moves, "down right", pos[0]-i, (pos[1]-i), "i:",i)
                    best_path = str(num_moves)+ " down right "+ str(pos[0]-i) +" "+ str(pos[1]-i)+ " i: "+str(i)
                    least_moves = min(num_moves, least_moves)

        # up right slope
        for i in range(4):
            num_moves = 0
            # pos[1] is column number
            # pos[0] is height inversed
            if pos[1]-i >= 0 and pos[1]-i+3 < board.shape[1] and pos[0]+i-3 >= 0 and pos[0]+i < board.shape[0]:
                for ixy in range(4):
                    if board[pos[0]-ixy+i][pos[1]+ixy-i] == 0:
                        num_moves += sum(board[pos[0]-ixy+i:, pos[1]+ixy-i] == 0)
                    elif board[pos[0]-ixy+i][pos[1]+ixy-i] == player:
                        continue
                    else:
                        break
                else:
                    # print(num_moves, "up right", pos[0]+i, (pos[1]-i), "i:",i)
                    # if(num_moves == 0):
                    #     print(num_moves, "up right", pos[0]+i, (pos[1]-i), "i:",i)
                    # best_path = str(num_moves)+ " up right "+ str(pos[0]+i) +" "+ str(pos[1]-i)+ " i: "+str(i)
                    least_moves = min(num_moves, least_moves)
        # print(best_path, "player:", player)         
        return least_moves


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

