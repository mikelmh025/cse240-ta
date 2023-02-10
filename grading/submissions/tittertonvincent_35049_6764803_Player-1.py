import numpy as np

MAXR = 10000
MINR = -10000

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
        depth = 6

        if self.player_number == 1:
            bestRating = float('-inf')
        else:
            bestRating = float('inf')
        bestCol = None
        for j in range(7):
            if board[0][j] == 0: # col j is not full
                r = self.ab_dfs_rating(board, depth - 2, self.player_number, self.player_number, j)
                if self.player_number == 1:
                    if r > bestRating:
                        bestRating = r
                        bestCol = j
                else:
                    if r < bestRating:
                        bestRating = r
                        bestCol = j

        if bestRating < MINR + 10:
            if self.player_number == 1:
                print('player 1 gives up')
            else:
                print('player 2 guarenteed win')
        if bestRating > MAXR - 10:
            if self.player_number == 1:
                print('player 1 guarenteed win')
            else:
                print('player 2 gives up')

        return bestCol


    def ab_dfs_rating(self, board, depth, player, nextPlayer, col):
        i = self.drop(board, col, nextPlayer)

        if depth == 0:
            curRating = self.evaluation_function(board)
            self.remove(board, i, col)
            return curRating

        if self.winning_space(board, i, col):
            self.remove(board, i, col)
            if nextPlayer == 1:
                return MAXR
            else:
                return MINR

        if nextPlayer == 1:
            bestRating = float('inf')
        else:
            bestRating = float('-inf')

        boardFull = True
        for j in range(7):
            if board[0][j] == 0: # col j is not full
                boardFull = False
                if nextPlayer == 1:
                    bestRating = min(self.ab_dfs_rating(board, depth - 1, player, 2, j), bestRating)
                else:
                    bestRating = max(self.ab_dfs_rating(board, depth - 1, player, 1, j), bestRating)
        self.remove(board, i, col)
        if boardFull:
            return 0 # tie

        # this modification makes it so:
        # if multiple moves guarentee a win, returns the fastest win (least moves needed)
        # if all moves lose allow opponent to win, returns the longest loss (most moves needed)
        if bestRating < MINR + 10:
            return bestRating + 1
        if bestRating > MAXR - 10:
            return bestRating - 1
        return bestRating
        


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
        depth = 5

        if self.player_number == 1:
            bestRating = float('-inf')
        else:
            bestRating = float('inf')
        bestCol = None
        for j in range(7):
            if board[0][j] == 0: # col j is not full
                r = self.em_dfs_rating(board, depth - 2, self.player_number, self.player_number, j)
                if self.player_number == 1:
                    if r > bestRating:
                        bestRating = r
                        bestCol = j
                else:
                    if r < bestRating:
                        bestRating = r
                        bestCol = j

        if bestRating < MINR + 10:
            if self.player_number == 1:
                print('player 1 gives up')
            else:
                print('player 2 guarenteed win')
        if bestRating > MAXR - 10:
            if self.player_number == 1:
                print('player 1 guarenteed win')
            else:
                print('player 2 gives up')

        return bestCol


    def em_dfs_rating(self, board, depth, player, nextPlayer, col):
        i = self.drop(board, col, nextPlayer)

        if depth == 0:
            curRating = self.evaluation_function(board)
            self.remove(board, i, col)
            return curRating

        if self.winning_space(board, i, col):
            self.remove(board, i, col)
            if nextPlayer == 1:
                return MAXR
            else:
                return MINR

        if player == nextPlayer:
            # avg loop
            totalRating = 0
            numOptions = 0
            for j in range(7):
                if board[0][j] == 0: # col j is not full
                    numOptions += 1
                    if nextPlayer == 1:
                        totalRating += self.em_dfs_rating(board, depth - 1, player, 2, j)
                    else:
                        totalRating += self.em_dfs_rating(board, depth - 1, player, 1, j)
            self.remove(board, i, col)
            if numOptions == 0:
                return 0 # tie
            return totalRating / numOptions

        else:
            # min/max loop
            if nextPlayer == 1:
                bestRating = float('inf')
            else:
                bestRating = float('-inf')

            boardFull = True
            for j in range(7):
                if board[0][j] == 0: # col j is not full
                    boardFull = False
                    if nextPlayer == 1:
                        bestRating = min(self.em_dfs_rating(board, depth - 1, player, 2, j), bestRating)
                    else:
                        bestRating = max(self.em_dfs_rating(board, depth - 1, player, 1, j), bestRating)
            self.remove(board, i, col)
            if boardFull:
                return 0 # tie
            # this modification makes it so:
            # if multiple moves guarentee a win, returns the fastest win (least moves needed)
            # if all moves lose allow opponent to win, returns the longest loss (most moves needed)
            if bestRating < MINR + 10:
                return bestRating + 1
            if bestRating > MAXR - 10:
                return bestRating - 1
            return bestRating 


    def evaluation_function(self, board):
        """
        Given the current state of the board, return the scalar value that 
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
        poten, cBias = self.potential_wins(board)

        if poten is None: # winning state
            if cBias == 1:
                return MAXR # player 1 is winner
            return MINR # player 2 is winner

        pBias = 0
        for j in range(7): # TODO(vince): check over this
            prevPoten = 0
            i = 5
            while i >= 0: # bottom up
                if poten[i][j] == 1:
                    if prevPoten == 1:
                        pBias += 5
                        prevPoten = 0
                    else:
                        pBias += 1
                        prevPoten = 1
                        if i % 2 == 0: # TODO(vince): verify even/odd squares
                            pBias += 2

                elif poten[i][j] == 2:
                    if prevPoten == 2:
                        pBias -= 5
                        prevPoten = 0
                    else:
                        pBias -= 1
                        prevPoten = 2
                        if i % 2 == 0: # TODO(vince): verify even/odd squares
                            pBias -= 2

                elif poten[i][j] == 3:
                    if prevPoten == 1:
                        pBias += 3
                    elif prevPoten == 2:
                        pBias -= 3
                    prevPoten = 0

                else:
                    prevPoten = 0
                i -= 1

        return 20 * pBias - cBias


    def potential_wins(self, board):
        # returns (None, winning player) if board is on a winning state,
        # otherwise returns (poten, cBias)
        poten = np.zeros([6, 7]).astype(np.uint8)
        # poten is is a 2d array of potential wins with values as follows:
        # 0 -> neither player will win if they occupy the space
        # 1 -> player 1 will win if they occupy the space
        # 2 -> player 2 will win if they occupy the space
        # 3 -> either player will win if they occupy the space
        cBias = 0
        # cBias favors spaces closer to the center of board (col == 3)
        # cBias > 0 favors player 1, cBias < 0 favors player 2
        
        # horizontal 4? + poten
        for i in range(6):
            color = pColor = 0 # color and potential color
            streak = pStreak = 0 # streak and potential streak
            pSpace = None # potential space
            for j in range(7):
                if board[i][j] == 0:
                    pSpace = (i, j)
                    pStreak = streak + 1
                    color = 0
                    streak = 0
                elif board[i][j] == color:
                    streak += 1
                    pStreak += 1
                else:
                    color = board[i][j]
                    if color == pColor:
                        pStreak += 1
                    elif streak == 0 and pSpace != None:
                        pStreak = 2
                        pColor = color
                    else:
                        pStreak = 1
                        pColor = color
                    streak = 1
                if streak == 4: # game won
                    return (None, pColor)
                if pStreak == 4: # pSpace wins for player pColor
                    self.update_poten(pColor, pSpace, poten)

        # vertical 4? + cBias
        # no need to calculate poten here - looking 1 move ahead will show a win.
        for j in range(7):
            color = 0
            streak = 0
            i = 5
            while i >= 0: # bottom up so we can break after first empty space
                if board[i][j] == 0:
                    break
                elif board[i][j] == color:
                    streak += 1
                else:
                    color = board[i][j]
                    streak = 1
                if streak == 4: # game won
                    return (None, color)
                if board[i][j] == 1:
                    cBias += 3 * abs(j - 3) + abs(i - 2)
                else:
                    cBias -= 3 * abs(j - 3) + abs(i - 2)
                i -= 1
                    
        # diagonal (\) 4? + poten
        for j in range(-2, 4):
            color = pColor = 0 # color and potential color
            streak = pStreak = 0 # streak and potential streak
            pSpace = None # potential space
            if j < 0:
                x = 0
                y = 0 - j
            else:
                x = j
                y = 0
            while x < 7 and y < 6:
                if board[y][x] == 0:
                    pSpace = (y, x)
                    pStreak = streak + 1
                    color = 0
                    streak = 0
                elif board[y][x] == color:
                    streak += 1
                    pStreak += 1
                else:
                    color = board[y][x]
                    if color == pColor:
                        pStreak += 1
                    elif streak == 0 and pSpace != None:
                        pStreak = 2
                        pColor = color
                    else:
                        pStreak = 1
                        pColor = color
                    streak = 1
                if streak == 4: # game won
                    return (None, pColor)
                if pStreak == 4: # pSpace wins for player pColor
                    self.update_poten(pColor, pSpace, poten)
                x += 1
                y += 1

        # diagonal (/) 4? + poten
        for j in range(3, 9):
            color = pColor = 0 # color and potential color
            streak = pStreak = 0 # streak and potential streak
            pSpace = None # potential space
            if j > 6:
                x = 6
                y = j - 6
            else:
                x = j
                y = 0
            while x > -1 and y < 6:
                if board[y][x] == 0:
                    pSpace = (y, x)
                    pStreak = streak + 1
                    color = 0
                    streak = 0
                elif board[y][x] == color:
                    streak += 1
                    pStreak += 1
                else:
                    color = board[y][x]
                    if color == pColor:
                        pStreak += 1
                    elif streak == 0 and pSpace != None:
                        pStreak = 2
                        pColor = color
                    else:
                        pStreak = 1
                        pColor = color
                    streak = 1
                if streak == 4: # game won
                    return (None, pColor)
                if pStreak == 4: # pSpace wins for player pColor
                    self.update_poten(pColor, pSpace, poten)
                x -= 1
                y += 1

        return (poten, cBias)


    def update_poten(self, pColor, pSpace, poten):
        # helper function for potential_wins()
        if pColor == 1:
            if poten[pSpace[0]][pSpace[1]] == 0:
                poten[pSpace[0]][pSpace[1]] = 1
            elif poten[pSpace[0]][pSpace[1]] == 2:
                poten[pSpace[0]][pSpace[1]] = 3
        else:
            if poten[pSpace[0]][pSpace[1]] == 0:
                poten[pSpace[0]][pSpace[1]] = 2
            elif poten[pSpace[0]][pSpace[1]] == 1:
                poten[pSpace[0]][pSpace[1]] = 3


    def drop(self, board, j, player):
        # player drops piece into column j
        i = 5
        while i >= 0:
            if board[i][j] == 0:
                board[i][j] = player
                return i
            i -= 1
        raise Exception('drop: Column full')


    def remove(self, board, i, j):
        board[i][j] = 0


    def winning_space(self, board, i, j):
        # returns True if piece at i, j makes 4 in a row
        # faster than checking whole board
        color = board[i][j]

        # vertical 4
        if i <= 2:
            if board[i+1][j] == color and board[i+2][j] == color and board[i+3][j] == color:
                return True

        # horizontal 4
        conn = 1
        j2 = j - 1
        while j2 >= 0 and board[i][j2] == color:
            if conn == 3:
                return True
            conn += 1
            j2 -= 1
        j2 = j + 1
        while j2 < 7 and board[i][j2] == color:
            if conn == 3:
                return True
            conn += 1
            j2 += 1

        # diagonal (\) 4
        conn = 1
        i2 = i - 1
        j2 = j - 1
        while i2 >= 0 and j2 >= 0 and board[i2][j2] == color:
            if conn == 3:
                return True
            conn += 1
            i2 -= 1
            j2 -= 1
        i2 = i + 1
        j2 = j + 1
        while i2 < 6 and j2 < 7 and board[i2][j2] == color:
            if conn == 3:
                return True
            conn += 1
            i2 += 1
            j2 += 1

        # diagonal (/) 4
        conn = 1
        i2 = i - 1
        j2 = j + 1
        while i2 >= 0 and j2 < 7 and board[i2][j2] == color:
            if conn == 3:
                return True
            conn += 1
            i2 -= 1
            j2 += 1
        i2 = i + 1
        j2 = j - 1
        while i2 < 6 and j2 >= 0 and board[i2][j2] == color:
            if conn == 3:
                return True
            conn += 1
            i2 += 1
            j2 -= 1

        return False
            


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

