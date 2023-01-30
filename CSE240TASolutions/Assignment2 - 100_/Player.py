import numpy as np

# https://numpy.org/doc/stable/reference/generated/numpy.pad.html
# Function used to add padding to a numpy matrix
def pad_with(vector, pad_width, iaxis, kwargs):
    pad_value = kwargs.get('padder', 10)
    vector[:pad_width[0]] = pad_value
    vector[-pad_width[1]:] = pad_value

class SearchNode:

    def __init__(self, value, position, optionsLength):
        self.value = value
        self.position = position
        self.optionsLength = optionsLength
        self.nodeDict = dict()
        

    def addNode(self, node, position):
        self.nodeDict[position] = node


    def isTerminal(self):
        if len(self.nodeDict.keys()) == 0:
            return True
        for value in self.nodeDict.values():
            if(value is None):
                return True
        return False

    def getPossiblePositions(self, board):
        posList = []
        for pos in range(0, self.optionsLength):
            column = board[:, pos]
            if 0 in column:
                posList.append(pos)
        return posList



class AIPlayer:


    def __init__(self, player_number):
        self.player_number = player_number
        self.type = 'ai'
        self.player_string = 'Player {}:ai'.format(player_number)
        self.searchLimit = 3



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


        # get search limit and construct graph
        limit = self.searchLimit
        optionLength = board.shape[-1]

        graph = SearchNode(self.evaluation_function(board), 0, optionLength)

        val = graph.getPossiblePositions(board)[0]

        graph.value = val


        increment = 0
        nodesAtIncrement = [(graph, board)]
        # construct graph
        isPlayer = True
        while increment != limit:
            newNodeSet = []
            for g, b in nodesAtIncrement:

                for child in g.getPossiblePositions(b):
                    # update board
                    newBoard = AIPlayer.updateBoard(b, child, isPlayer)

                    newNode = SearchNode(self.evaluation_function(newBoard), child, optionLength)
                    


                    g.addNode(newNode, child)
                    if newNode not in newNodeSet:
                        newNodeSet.append((newNode, newBoard))

            nodesAtIncrement = newNodeSet
            increment += 1
            isPlayer = not(isPlayer)

        return AIPlayer.alpha_beta_search(graph)


    def alpha_beta_search(node):
        position, value = AIPlayer.max_value(node, -np.inf, np.inf)
        return position

    def max_value(node, alpha, beta):
        if node.isTerminal():
            return (node.position, node.value)
        value = -np.inf
        currentAction = node.position
        
        for action, resultNode in node.nodeDict.items():
            minAction, minValue = AIPlayer.min_value(resultNode, alpha, beta)
            currentAction, value = max([(minAction, minValue), (currentAction, value)], key = lambda tup: tup[1])
            if value >= beta:
                return (currentAction, value)
            alpha = max(alpha, value)

        return (currentAction, value)

    def min_value(node, alpha, beta):
        if node.isTerminal():
            return (node.position, node.value)
        value = np.inf
        currentAction = node.position
        for action, resultNode in node.nodeDict.items():
            maxAction, maxValue = AIPlayer.max_value(resultNode, alpha, beta)

            currentAction, value = min([(maxAction, maxValue), (currentAction, value)], key=lambda tup: tup[1])
            if value <= alpha:
                return (currentAction, value)
            beta = min(beta, value)
        return (currentAction, value)

    def updateBoard(board, move, isPlayer):
        # assume move is legal, update the board with move and send new copy of board
        column = np.copy(board[:, move])
        
        column[np.where(column == 0)[-1][-1]] = 1 if isPlayer else 2
        newBoard = np.copy(board)
        newBoard[:, move] = column
        return newBoard

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
        limit = self.searchLimit
        optionLength = board.shape[-1]

        graph = SearchNode(self.evaluation_function(board), 0, optionLength)

        val = graph.getPossiblePositions(board)[0]

        graph.value = val


        increment = 0
        nodesAtIncrement = [(graph, board)]
        # construct graph using dls

        isPlayer = True
        while increment != limit:
            newNodeSet = []
            for g, b in nodesAtIncrement:

                for child in g.getPossiblePositions(b):
                    # update board
                    newBoard = AIPlayer.updateBoard(b, child, isPlayer)

                    newNode = SearchNode(self.evaluation_function(newBoard), child, optionLength)
                    

                    g.addNode(newNode, child)
                    if newNode not in newNodeSet:
                        newNodeSet.append((newNode, newBoard))

            nodesAtIncrement = newNodeSet
            increment += 1
            isPlayer = not(isPlayer)

        position, value = AIPlayer.expectimax(graph, True)

        return position


    def expectimax(node, isPlayer):
        """
            Given root, will return the (expectimax value, the position chosen)
        """

        if node.isTerminal():
            return (node.position, node.value)

        if isPlayer:
            # max nodes
            expectimaxValues = [AIPlayer.expectimax(value, False) for value in node.nodeDict.values()]
            position, exp = max(expectimaxValues, key = lambda tup: tup[1])

            return (position, exp)
        else:
            # chance nodes
            expectimaxValues = [AIPlayer.expectimax(value, True) for value in node.nodeDict.values()]
            return (node.position, sum(tup[0] for tup in expectimaxValues) / len(expectimaxValues))


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

        userPathSets = set({})
        opponentPathSets = set({})

        for x in range(0, board.shape[-1]):
            for y in range(0, board.shape[0]):
                value = board[y, x]
                
                if value == 1 or value == 2:

                    paths = self.find_largest_paths(board, x, y, value)

                    if value == self.player_number:
                        for a in paths:
                            userPathSets.add(a)
                    else:
                        for a in paths:
                            opponentPathSets.add(a)
        
        playerValue = 0.5 * len([len(s) == 1 for s in userPathSets]) + 1 * len([len(s) == 2 for s in userPathSets]) + 5 * len([len(s) == 3 for s in userPathSets]) + 30.0 * len([len(s) == 4 for s in userPathSets])
        opponentValue = 0.5 * len([len(s) == 1 for s in opponentPathSets]) + 1 * len([len(s) == 2 for s in opponentPathSets]) + 20.0 * len([len(s) == 3 for s in opponentPathSets])

        return playerValue - opponentValue

    def extract_path(arr, player):

        """
            Helper function to get the longest consecutive path of a player, given a diagonal, horizontal or vertical line
        """
        middle = int(len(arr) / 2)
        
        left = arr[0:middle]
        right = arr[middle+1:]

        leftBoundary = len(left)
        for i in range(len(left) - 1, -1, -1):
            if left[i][-1] != player:
                break
            else:
                leftBoundary = i

        rightBoundary = -1
        for i in range(0, len(right)):
            if right[i][-1] != player:
                break
            else:
                rightBoundary = i

        leftSide = [] if leftBoundary == len(left) else left[leftBoundary:]
        rightSide = [] if rightBoundary == -1 else right[:rightBoundary+1]

        result = []
        result.extend(leftSide)
        result.append(arr[middle])
        result.extend(rightSide)

        return result



    def find_largest_paths(self, board, x, y, player_number):
        """
        Helper method to find largest paths in form { {(0, 1), (0, 2)}, ... }
        Each inner set is a path

        """

        newX = x + 3
        newY = y + 3

        paddedBoard = np.pad(board, 3, pad_with, padder=5)
        
        
        horizontal = paddedBoard[newY, newX-3:newX+4]

        horizontal = [((newX - 3 + idx, newY), h) for idx, h in enumerate(horizontal)]

        vertical = paddedBoard[newY-3:newY+4, newX]
        vertical = [((newX, newY-3 + idx), h) for idx, h in enumerate(vertical)]


        rightDiagonal = [] 
        leftDiagonal = []
    
        for i, j in zip(list(range(newX-3, newX+4)), list(range(newY+3, newY-4, -1))):
            rightDiagonal.append(((i, j), paddedBoard[j, i]))

        for i, j in zip(list(range(newX+3, newX-4, -1)), list(range(newY+3, newY-4, -1))):
            leftDiagonal.append(((i, j), paddedBoard[j, i]))

        horizontal = AIPlayer.extract_path(horizontal, player_number)
        vertical = AIPlayer.extract_path(vertical, player_number)
        rightDiagonal = AIPlayer.extract_path(rightDiagonal, player_number)
        leftDiagonal = AIPlayer.extract_path(leftDiagonal, player_number)

        finalSet = set({})


        if (horizontal[0][0][0] - 1 >= 0 and paddedBoard[newY, horizontal[0][0][0] - 1] == 0) or (horizontal[-1][0][0] + 1 < paddedBoard.shape[1] and paddedBoard[newY, horizontal[-1][0][0] + 1] == 0):
            finalSet.add(frozenset(horizontal))

        if (vertical[0][0][0] - 1 >= 0 and paddedBoard[vertical[0][0][0] - 1, newX] == 0) or (vertical[-1][0][0] + 1 < paddedBoard.shape[0] and paddedBoard[vertical[-1][0][0] + 1, newX] == 0):
            finalSet.add(frozenset(vertical))
        if (rightDiagonal[0][0][1] + 1 < paddedBoard.shape[0] and rightDiagonal[0][0][0] - 1 >= 0 and paddedBoard[rightDiagonal[0][0][1] + 1, rightDiagonal[0][0][0] - 1] == 0)  or (rightDiagonal[-1][0][0] - 1 >= 0 and rightDiagonal[-1][0][1] + 1 < paddedBoard.shape[0] and paddedBoard[rightDiagonal[-1][0][0] - 1, rightDiagonal[-1][0][1] + 1] == 0):
            finalSet.add(frozenset(rightDiagonal))
        if (leftDiagonal[0][0][1] - 1 >= 0 and leftDiagonal[0][0][1] - 1 >= 0 and paddedBoard[leftDiagonal[0][0][1] - 1, leftDiagonal[0][0][1] - 1] == 0) or (leftDiagonal[-1][0][0] + 1 < paddedBoard.shape[1] and leftDiagonal[-1][0][1] + 1 < paddedBoard.shape[0] and paddedBoard[leftDiagonal[-1][0][0] + 1, leftDiagonal[-1][0][1] + 1] == 0):
            finalSet.add(frozenset(leftDiagonal))

        
        return finalSet





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

