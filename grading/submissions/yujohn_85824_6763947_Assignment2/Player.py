import numpy as np

class AIPlayer:
    def __init__(self, player_number):
        self.player_number = player_number
        self.type = 'ai'
        self.player_string = 'Player {}:ai'.format(player_number)

    def get_possible_moves(self, board):
      moves = []
      for col in range(7):
        for row in range(5, -1, -1):
          if(board[row][col] == 0):
            moves.append(col)
            break
      
      return moves

    def next_board(self, board, move, player):
      tempBoard = [np.copy(row) for row in board]
      # print("MOVE:", move)
      for row in range(len(board)-1, -1, -1):
        if(tempBoard[row][move] == 0):
          tempBoard[row][move] = player
          return tempBoard
      return tempBoard
      
    def max_value_alpha(self, board, depth, alpha, beta):
        possible_moves = self.get_possible_moves(board)
        value = float("-inf")
        myAlpha = alpha
        player = self.player_number

        if self.game_end(board) or depth == 0 or len(possible_moves) == 0:
          return self.evaluation_function(board)
        
        for move in possible_moves:
          if(myAlpha < beta):
            nextBoard = self.next_board(board, move, player)
            value = max(value, self.min_value_beta(nextBoard, depth-1, myAlpha, beta))
          if(value > beta):
            return value
          if(value > myAlpha):
            myAlpha = value
        return myAlpha


    def min_value_beta(self, board, depth, alpha, beta):
        possible_moves = self.get_possible_moves(board)
        myBeta = beta
        value = float("inf")
        player = self.player_number
        if(player == 1):
          player = 2
        else:
          player = 1

        if self.game_end(board) or depth == 0 or len(possible_moves) == 0:
          return self.evaluation_function(board)
        
        for move in possible_moves:
          if(alpha < myBeta):
            nextBoard = self.next_board(board, move, player)
            value = min(value, self.max_value_alpha(nextBoard, depth-1, alpha, myBeta))
          if(value < alpha):
            return value
          if(value < myBeta):
            myBeta = value
        return myBeta



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
        possible_moves = self.get_possible_moves(board)
        value = float("-inf")
        chosenMove = possible_moves[0]
        depth = 4
        player = self.player_number

        alpha = float("-inf")
        beta = float("inf")

        for move in possible_moves:
          beta_score = self.min_value_beta(self.next_board(board, move, player), depth-1, alpha, beta)
          
          if(beta_score > value):
            value = beta_score
            chosenMove = move

          if(value > beta):
            return value
        
          if(value > alpha):
            alpha = value

        return chosenMove

    def expect_max(self, board, depth):
        possible_moves = self.get_possible_moves(board)
        value = float("-inf")
        player = self.player_number

        if depth == 0 or len(possible_moves) == 0 or self.game_end(board):
          return self.evaluation_function(board)          
        
        for move in possible_moves:
          expectMove = self.expect_value(self.next_board(board, move, player), depth-1)

          if(expectMove > value):
            value = expectMove
                    
        return value

    def expect_value(self, board, depth):
        possible_moves = self.get_possible_moves(board)
        player = self.player_number
        if(player == 1):
          player = 2
        else:
          player = 1
        
        if depth == 0 or len(possible_moves) == 0 or self.game_end(board):
          return self.evaluation_function(board)
        
        sum = 0
        for move in possible_moves:
          sum += self.expect_max(self.next_board(board, move, player), depth-1)
        return sum/len(possible_moves)

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
        possible_moves = self.get_possible_moves(board)
        value = float("-inf")
        depth = 4
        chosenMove = possible_moves[0]
        player = self.player_number
        for move in possible_moves:
          expectMove = self.expect_value(self.next_board(board, move, player), depth-1)

          if(expectMove > value):
            value = expectMove
            chosenMove = move

        return chosenMove
        


    def readBackDiag(self, board, row, col):
      c = col
      seqLen = 0
      for r in range(row, len(board)):
        if(board[r][c] == board[row][col]):
          seqLen += 1
          c -= 1
        else:
          break
        if(seqLen >= 4):
          return 4
        if(c < 0):
          return seqLen
      
      if(seqLen >= 4):
        return 4
      return seqLen

    def readForwDiag(self, board, row, col):
      c = col
      seqLen = 0
      
      for r in range(row, len(board)):
        if(board[r][c] == board[row][col]):
          seqLen += 1
          c += 1
        else:
          break
        if(seqLen >= 4):
          return 4
        if(c >= len(board[0])):
          return seqLen
      
      return seqLen

    def readHoriSeq(self, board, row, col):
      seqLen = 0
      for c in range(col, len(board[0])):
        if(board[row][c] == board[row][col]):
          seqLen += 1
        else:
          break
        if(seqLen >= 4):
          return 4
      return seqLen

    def readVertSeq(self, board, row, col):
      seqLen = 0
      for r in range(row, len(board)):
        if(board[r][col] == board[row][col]):
          seqLen += 1
        else:
          break
        if(seqLen >= 4):
          return 4
      return seqLen

    def game_end(self, board):
      play1Moves = {1: 0, 2: 0, 3: 0, 4: 0}
      play2Moves = {1: 0, 2: 0, 3: 0, 4: 0}

      for row in range(len(board)):
        for col in range(len(board[0])):
          if(board[row][col] == 1):
            play1Moves[self.readBackDiag(board, row, col)] += 1
            play1Moves[self.readForwDiag(board, row, col)] += 1
            play1Moves[self.readHoriSeq(board, row, col)] += 1
            play1Moves[self.readVertSeq(board, row, col)] += 1
          if(board[row][col] == 2):
            play2Moves[self.readBackDiag(board, row, col)] += 1
            play2Moves[self.readForwDiag(board, row, col)] += 1
            play2Moves[self.readHoriSeq(board, row, col)] += 1
            play2Moves[self.readVertSeq(board, row, col)] += 1
          if(play1Moves[4] > 0 or play2Moves[4] > 0):
            return True
      return False

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
        play1Moves = {1: 0, 2: 0, 3: 0, 4: 0}
        play2Moves = {1: 0, 2: 0, 3: 0, 4: 0}

        for row in range(len(board)):
          for col in range(len(board[0])):
            if(board[row][col] == 1):
              play1Moves[self.readBackDiag(board, row, col)] += 1
              play1Moves[self.readForwDiag(board, row, col)] += 1
              play1Moves[self.readHoriSeq(board, row, col)] += 1
              play1Moves[self.readVertSeq(board, row, col)] += 1
            if(board[row][col] == 2):
              play2Moves[self.readBackDiag(board, row, col)] += 1
              play2Moves[self.readForwDiag(board, row, col)] += 1
              play2Moves[self.readHoriSeq(board, row, col)] += 1
              play2Moves[self.readVertSeq(board, row, col)] += 1

        player1Score = play1Moves[1] * 1 + play1Moves[2] * 5 + play1Moves[3] * 50 + play1Moves[4] * 500
        player2Score = play2Moves[1] * 1 + play2Moves[2] * 5 + play2Moves[3] * 50 + play2Moves[4] * 500

        if(self.player_number == 1):
          return player1Score - player2Score
        else:
          return player2Score - player1Score

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

