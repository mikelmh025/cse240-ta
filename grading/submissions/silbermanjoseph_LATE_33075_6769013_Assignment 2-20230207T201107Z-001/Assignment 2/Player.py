import numpy as np

class AIPlayer:
    def __init__(self, player_number):
        self.player_number = player_number
        self.type = 'ai'
        self.player_string = 'Player {}:ai'.format(player_number)

    def alphabeta(self, board, node, max_node, alpha, beta):
        if not node.children:
            to_delete = []
            on_node = 0
            for i in node.placements:
                if on_node % 2 == 0:
                    to_delete.append(self.place(board, i, self.player_number))
                else:
                    to_delete.append(self.place(board, i, self.other_player(self.player_number)))
                on_node += 1
            node.value = self.evaluation_function(board)
            for spot in to_delete:
                if spot:
                    board[spot[0]][spot[1]] = 0

            return node.value
        
        if max_node:
            best_value = float('-inf')
            for n in node.children:
                val = self.alphabeta(board, n, False, alpha, beta)
                best_value = max(best_value, val)
                alpha = max(alpha, best_value)
                if beta <= alpha:
                    break
            return best_value
            
        else:
            best_value = float('inf')
            for n in node.children:
                val = self.alphabeta(board, n, True, alpha, beta)
                best_value = min(best_value, val)
                beta = min(beta, best_value)
                if beta <= alpha:
                    break
            return best_value
        
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

        print("---------------------------------------------------------------------------------")
        maxdepth = 3

        options = []
        for i in range(7):
            options.append(self.Node(0, []))
            options[i].placements.append(i)

        values = []
        for node in options:
            self.populate(node, maxdepth)
            node.value = self.alphabeta(board, node, True, float('-inf'), float('inf'))
            values.append(node.value)

        print(values)
        maxval = max(options).placements[0]
        while board[0][maxval] != 0:
            options.remove(max(options))
            maxval = max(options).placements[0]

        return maxval

        raise NotImplementedError('Whoops I don\'t know what to do')

    class Node:
        def __init__(self, value, placements):
            self.value = value
            self.placements = placements
            self.children = []

        def __gt__(self, other):
            return self.value > other.value

        def __ge__(self, other):
            return self.value >= other.value

    def other_player(self, plnum):
        if plnum == 1: return 2
        else: return 1

    def avg(self, a, b, c, d, e, f, g):
        return (a+b+c+d+e+f+g) /7

    def expectimax(self, board, node, max_node):
        if not node.children:
            to_delete = []
            on_node = 0
            for i in node.placements:
                if on_node % 2 == 0:
                    to_delete.append(self.place(board, i, self.player_number))
                else:
                    to_delete.append(self.place(board, i, self.other_player(self.player_number)))
                on_node += 1
            node.value = self.evaluation_function(board)
            for spot in to_delete:
                if spot:
                    board[spot[0]][spot[1]] = 0

            return node.value
        
        if max_node:
            return max(self.expectimax(board, node.children[0], False), self.expectimax(board, node.children[1], False), self.expectimax(board, node.children[2], False), self.expectimax(board, node.children[3], False), self.expectimax(board, node.children[4], False), self.expectimax(board, node.children[5], False), self.expectimax(board, node.children[6], False))

        else:
            return self.avg(self.expectimax(board, node.children[0], True), self.expectimax(board, node.children[1], True), self.expectimax(board, node.children[2], True), self.expectimax(board, node.children[3], True), self.expectimax(board, node.children[4], True), self.expectimax(board, node.children[5], True), self.expectimax(board, node.children[6], True))

    def populate(self, node, depthleft):
        if depthleft == 0:
            return
        
        for i in range(7):
            node.children.append(self.Node(0, node.placements))
            node.children[i].placements.append(i)
        
        for child in node.children:
            self.populate(child, depthleft-1)

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
        print("---------------------------------------------------------------------------------")
        maxdepth = 2

        options = []
        for i in range(7):
            options.append(self.Node(0, []))
            options[i].placements.append(i)

        values = []
        for node in options:
            self.populate(node, maxdepth)
            node.value = self.expectimax(board, node, False)
            values.append(node.value)

        print(values)
        maxval = max(options).placements[0]
        while board[0][maxval] != 0:
            options.remove(max(options))
            maxval = max(options).placements[0]

        return maxval

    def place(self, board, column, plnum):
        row = 5
        placed = False
        while row >= 0:
            if board[row][column] == 0:
                board[row][column] = plnum
                placed = True
                break
            row -= 1
        if not(placed):
            return []

        return [row, column]

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
        
        if self.worst_horizontal(board) == 4:
            return -100
        if self.worst_vertical(board) == 4:
            return -100
        if self.worst_right_diagonal(board) == 4:
            return -100
        if self.worst_left_diagonal(board) == 4:
            return -100
        if self.best_horizontal(board) == 4:
            return 100
        if self.best_vertical(board) == 4:
            return 100
        if self.best_right_diagonal(board) == 4:
            return 100
        if self.best_left_diagonal(board) == 4:
            return 100
        
       
        return self.best_horizontal(board) + self.best_vertical(board) + self.best_right_diagonal(board) + self.best_left_diagonal(board) - self.worst_horizontal(board) - self.worst_vertical(board) - self.worst_right_diagonal(board) - self.worst_left_diagonal(board)

    def best_horizontal(self, board):
        # longest horizontal line made so far
        longest = 0
        measuring = False
        current_horizontal = 0
        for row in board:
            colnum = 0
            for col in row:
                if col == self.player_number and not(measuring):
                    measuring = True
                    current_horizontal = 1
                    if current_horizontal > longest:
                        longest = current_horizontal
                elif col == self.player_number:
                    current_horizontal += 1
                    if current_horizontal > longest:
                        longest = current_horizontal
                else:
                    current_horizontal = 0
                    measuring = False
                colnum += 1

        return longest

    def worst_horizontal(self, board):
        # longest horizontal line made so far by opponent
        longest = 0
        measuring = False
        current_horizontal = 0
        for row in board:
            colnum = 0
            for col in row:
                if col == self.other_player(self.player_number) and not(measuring):
                    measuring = True
                    current_horizontal = 1
                    if current_horizontal > longest:
                        longest = current_horizontal
                elif col == self.other_player(self.player_number):
                    current_horizontal += 1
                    if current_horizontal > longest:
                        longest = current_horizontal
                else:
                    current_horizontal = 0
                    measuring = False
                colnum += 1

        return longest

    def best_vertical(self, board):
        # longest vertical line made so far
        longest = 0
        measuring = False
        current_vertical = 0
        for column in range(7):
            for row in reversed(range(6)):
                spot = board[row][column]
                if spot == self.player_number and not(measuring):
                    measuring = True
                    current_vertical = 1
                    if current_vertical > longest:
                        longest = current_vertical
                elif spot == self.player_number:
                    current_vertical += 1
                    if current_vertical > longest:
                        longest = current_vertical
                else:
                    current_vertical = 0
                    measuring = False

        return longest

    def worst_vertical(self, board):
        # longest vertical line made so far
        longest = 0
        measuring = False
        current_vertical = 0
        for column in range(7):
            for row in reversed(range(6)):
                spot = board[row][column]
                if spot == self.other_player(self.player_number) and not(measuring):
                    measuring = True
                    current_vertical = 1
                    if current_vertical > longest:
                        longest = current_vertical
                elif spot == self.other_player(self.player_number):
                    current_vertical += 1
                    if current_vertical > longest:
                        longest = current_vertical
                else:
                    current_vertical = 0
                    measuring = False

        return longest

    def best_right_diagonal(self, board):
        # longest right diagonal line made so far
        longest = 0
        current_vertical = 0
        for column in range(7):
            for row in reversed(range(6)):
                spot = board[row][column]
                if spot == self.player_number:
                    current_vertical = 1
                    iteration = 1
                    while row - iteration >= 0 and column + iteration < 7:
                        if board[row-iteration][column+iteration] == self.player_number:
                            current_vertical += 1
                        else: break
                        iteration += 1
                    if current_vertical > longest:
                        longest = current_vertical
                current_vertical = 0

        return longest

    def worst_right_diagonal(self, board):
        # longest right diagonal line made so far
        longest = 0
        current_vertical = 0
        for column in range(7):
            for row in reversed(range(6)):
                spot = board[row][column]
                if spot == self.other_player(self.player_number):
                    current_vertical = 1
                    iteration = 1
                    while row - iteration >= 0 and column + iteration < 7:
                        if board[row-iteration][column+iteration] == self.other_player(self.player_number):
                            current_vertical += 1
                        else: break
                        iteration += 1
                    if current_vertical > longest:
                        longest = current_vertical
                current_vertical = 0

        return longest

    def best_left_diagonal(self, board):
        # longest left diagonal line made so far
        longest = 0
        current_vertical = 0
        for column in range(7):
            for row in reversed(range(6)):
                spot = board[row][column]
                if spot == self.player_number:
                    current_vertical = 1
                    iteration = 1
                    while row - iteration >= 0 and column - iteration >= 0:
                        if board[row-iteration][column-iteration] == self.player_number:
                            current_vertical += 1
                        else: break
                        iteration += 1
                    if current_vertical > longest:
                        longest = current_vertical
                current_vertical = 0

        return longest

    def worst_left_diagonal(self, board):
        # longest left diagonal line made so far
        longest = 0
        current_vertical = 0
        for column in range(7):
            for row in reversed(range(6)):
                spot = board[row][column]
                if spot == self.other_player(self.player_number):
                    current_vertical = 1
                    iteration = 1
                    while row - iteration >= 0 and column - iteration >= 0:
                        if board[row-iteration][column-iteration] == self.other_player(self.player_number):
                            current_vertical += 1
                        else: break
                        iteration += 1
                    if current_vertical > longest:
                        longest = current_vertical
                current_vertical = 0

        return longest

    

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

