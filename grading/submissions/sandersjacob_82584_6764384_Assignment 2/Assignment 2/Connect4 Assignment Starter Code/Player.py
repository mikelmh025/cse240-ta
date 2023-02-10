import numpy as np

class AIPlayer:

    def __init__(self, player_number):
        self.player_number = player_number
        self.type = 'ai'
        self.player_string = 'Player {}:ai'.format(player_number)

    def get_alpha_beta_move(self, board):
        # initialize best_move as a random move from the list of valid moves
        best_move = np.random.choice(self.get_valid_moves(board))
        # initialize best_value as negative infinity
        best_value = -float('inf')
        # set the depth for the search
        depth = 6

        # iterate through each move in the list of valid moves
        for move in self.get_valid_moves(board):
            # create a child board after making the move
            child_board = self.make_move(board, move, self.player_number)
            # get the value of the move using the alpha_beta_search function
            value = self.alpha_beta_search(child_board, depth, -float('inf'), float('inf'), False)
            # update the best_value and best_move if the value is greater than the current best_value
            if value > best_value:
                best_value = value
                best_move = move
        # return the best move found
        return best_move

    def alpha_beta_search(self, board, depth, alpha, beta, maximizing_player):
        # check if the board is a terminal state (depth is 0, win, or tie)
        if depth == 0 or self.check_win(board, self.player_number) or self.check_win(board, 3 - self.player_number) or self.check_tie(board):
            # return the evaluation value of the board
            return self.evaluation_value(board)

        # if it is the maximizing player's turn
        if maximizing_player:
            # initialize value as negative infinity
            value = -float('inf')
            # iterate through each move in the list of valid moves
            for move in self.get_valid_moves(board):
                # create a child board after making the move
                child_board = self.make_move(board, move, self.player_number)
                # update value as the maximum of value and the result of the alpha_beta_search of the child board
                value = max(value, self.alpha_beta_search(child_board, depth - 1, alpha, beta, False))
                # update alpha as the maximum of alpha and value
                alpha = max(alpha, value)
                # if beta is less than or equal to alpha, break out of the loop
                if beta <= alpha:
                    break
            # return value
            return value
        # if it is the minimizing player's turn
        else:
            # initialize value as 0
            value = 0
            # iterate through each move in the list of valid moves
            for move in self.get_valid_moves(board):
                # create a child board after making the move
                child_board = self.make_move(board, move, 3 - self.player_number)
                # update value as the average of value and the result of the alpha_beta_search of the child board divided by the number of valid moves
                value += self.alpha_beta_search(child_board, depth - 1, alpha, beta, True) / len(self.get_valid_moves(board))
                # update beta as the minimum of beta and value
                beta = min(beta, value)
                # if beta is less than or equal to alpha, break out of the loop
                if beta <= alpha:
                    break
            # return value
            return value


    def get_expectimax_move(self, board):
        # recursive function that implements the expectimax algorithm
        def expectimax(board, depth, maximizing_player):
            # check if depth has been reached or the opponent has won
            if depth == 0 or self.check_win(board, 3 - self.player_number):
                # return the evaluation value for the board
                return self.evaluation_value(board)

            # if it's the maximizing player's turn
            if maximizing_player:
                max_value = -float('inf')
                # loop through each column
                for column in range(board.shape[1]):
                    # if the move is valid
                    if self.is_valid_move(board, column):
                        # make a new board after making the move
                        new_board = self.make_move(board, column, self.player_number)
                        # calculate the expectimax value for the new board
                        value = expectimax(new_board, depth-1, False)
                        # update the max value if the new value is greater
                        max_value = max(max_value, value)
                return max_value
            else:
                # if it's the minimizing player's turn
                values = []
                # loop through each column
                for column in range(board.shape[1]):
                    # if the move is valid
                    if self.is_valid_move(board, column):
                        # make a new board after making the move
                        new_board = self.make_move(board, column, 3 - self.player_number)
                        # calculate the expectimax value for the new board
                        value = expectimax(new_board, depth-1, True)
                        # if the value is a number, append it to the list of values
                        if np.isnan(value) == False:
                            values.append(value)
                # if there are no valid moves, return 0
                if not values:
                    return 0
                # calculate the expected value for the list of values
                expected_value = np.mean(values)
                
                return expected_value

        # initializations for the best value and best column
        best_value = -float('inf')
        best_column = None
        # set the depth for the expectimax algorithm
        depth = 4

        # loop through each column
        for column in range(board.shape[1]):
            # if the move is valid
            if self.is_valid_move(board, column):
                # make a new board after making the move
                new_board = self.make_move(board, column, self.player_number)
                # calculate the expectimax value for the new board
                value = expectimax(new_board, depth, False)
                # if the new value is greater than the current best value
                if value > best_value:
                    # update the best value and best column
                    best_value = value
                    best_column = column
        # return the best column
        return best_column


    def make_move(self, board, move, player):
        # Copy the board to a new board object
        new_board = np.copy(board)

        # Loop through the columns of the board, starting from the bottom-most row
        for row in range(6-1, -1, -1):
            # If the current position in the column is empty
            if new_board[row][move] == 0:
                # Place the player's piece in the current position
                new_board[row][move] = player
                # Break out of the loop once a valid move has been made
                break
        # Return the updated board
        return new_board

    def get_valid_moves(self, board):
        # Initialize an empty list to store the valid moves
        valid_moves = []

        # Loop through all columns of the board
        for col in range(7):
            # If the top-most row in the current column is empty
            if board[0][col] == 0:
                # Add the current column index to the list of valid moves
                valid_moves.append(col)
        # Return the list of valid moves
        return valid_moves

    def is_valid_move(self, board, col):
        # Check if the move is within the boundaries of the board
        if col < 0 or col >= board.shape[1]:
            # If the move is not within the boundaries, return False
            return False
        # Check if the top-most row in the given column is empty
        return board[0][col] == 0

    def evaluation_value(self, board):
        # Check if AI player has won the game
        if self.check_win(board, self.player_number):
            # Return positive infinity if AI player has won
            return float('inf')
        # Check if opponent player has won the game
        if self.check_win(board, 3 - self.player_number):
            # Return negative infinity if opponent player has won
            return -float('inf')
        # Check if neither AI nor opponent player has won the game
        if self.check_tie(board):
            # Return 0 if neither player has won
            return 0
        return 0

    def check_win(self, board, player):
        # Check if the player has won the game
        for row in range(6):
            for col in range(7-3):
                # Check for horizontal wins
                if board[row][col] == player and board[row][col+1] == player and board[row][col+2] == player and board[row][col+3] == player:
                    return True
        for row in range(6-3):
            for col in range(7):
                # Check for vertical wins
                if board[row][col] == player and board[row+1][col] == player and board[row+2][col] == player and board[row+3][col] == player:
                    return True
        for row in range(6-3):
            for col in range(7-3):
                # Check for diagonal wins (top left to bottom right)
                if board[row][col] == player and board[row+1][col+1] == player and board[row+2][col+2] == player and board[row+3][col+3] == player:
                    return True
        for row in range(6-3):
            for col in range(3, 7):
                # Check for diagonal wins (bottom left to top right)
                if board[row][col] == player and board[row+1][col-1] == player and board[row+2][col-2] == player and board[row+3][col-3] == player:
                    return True
        # No wins found
        return False

    def check_tie(self, board):
        # Check if the game has ended in a tie
        for col in range(7):
            # Check if there is an empty space in the top row
            if board[0][col] == 0:
                return False
        # No empty spaces found, game is a tie
        return True


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

