import numpy as np

class AIPlayer:
    def __init__(self, player_number):
        self.player_number = player_number
        self.type = 'ai'
        self.player_string = 'Player {}:ai'.format(player_number)

    def game_completed(self, board, player_num):
        player_win_str = '{0}{0}{0}{0}'.format(player_num)
        board = board
        to_str = lambda a: ''.join(a.astype(str))

        def check_horizontal(b):
            for row in b:
                if player_win_str in to_str(row):
                    return True
            return False

        def check_verticle(b):
            return check_horizontal(b.T)

        def check_diagonal(b):
            for op in [None, np.fliplr]:
                op_board = op(b) if op else b
                
                root_diag = np.diagonal(op_board, offset=0).astype(np.int)
                if player_win_str in to_str(root_diag):
                    return True

                for i in range(1, b.shape[1]-3):
                    for offset in [i, -i]:
                        diag = np.diagonal(op_board, offset=offset)
                        diag = to_str(diag.astype(np.int))
                        if player_win_str in diag:
                            return True

            return False

        return (check_horizontal(board) or
                check_verticle(board) or
                check_diagonal(board))

    def result_board(self, board, move, player_num):
        result_board = board.copy()
        if 0 in result_board[:,move]:
            update_row = -1
            for row in range(1, result_board.shape[0]):
                update_row = -1
                if result_board[row, move] > 0 and result_board[row-1, move] == 0:
                    update_row = row-1
                elif row==result_board.shape[0]-1 and result_board[row, move] == 0:
                    update_row = row

                if update_row >= 0:
                    result_board[update_row, move] = player_num
                    # self.c.itemconfig(self.gui_result_board[move][update_row],
                                    #   fill=self.colors[self.current_turn])
                    break
        else:
            err = 'Invalid move by player {}. Column {}'.format(player_num, move)
            raise Exception(err)
        # print("returning board")
        return result_board

    def max_value(self, board, alpha, beta, d, act):
        if self.game_completed(board, self.player_number) or d==3:
            return self.evaluation_function(board), act
        v = np.NINF
        move = 0
        for a in range(7):
            try: 
                new_board = self.result_board(board, a, self.player_number)
            except Exception as e:
                continue
            min_v, action = self.min_value(new_board, alpha, beta, d+1, a)
            if min_v >= v:
                move = action
            v = max(v, min_v)
            if v >= beta:
                return v, move
            alpha = max(alpha, v)
        return v, move

    def min_value(self, board, alpha, beta, d, act):
        player_num = 1
        if self.player_number == 1:
            player_num = 2
        if self.game_completed(board, self.player_number) or d==3:
            return self.evaluation_function(board), act
        v = np.inf
        move = 0
        for a in range(7):
            try:
                new_board = self.result_board(board, a, player_num)
            except Exception as e:
                continue
            max_v, action = self.max_value(new_board, alpha, beta, d+1, a)
            if max_v <= v:
                move = action
            v = min(v, max_v)
            if v <= alpha:     
                return v, move
            beta = min(beta, v)
        return v, move

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
        v, action = self.max_value(board, np.NINF, np.inf, 0, 0)
        return action

    class Node:
        def __init__(self, board, utility, position, children):
            self.board = board
            self.utility = utility
            self.position = position
            self.children = []
        def set_children(self, children):
            self.children = children

    def expectimax(self, board, isPlayer, action, d):
        if self.game_completed(board, self.player_number) or d == 3:
            return self.evaluation_function(board), action
        if isPlayer:
            action = 0
            v = np.NINF
            for a in range(7):
                try:
                    child = self.result_board(board, a, self.player_number)
                except Exception as e:
                    continue
                ev, act = self.expectimax(child, False, a, d+1)
                if ev >= v:
                    v = ev
                    action = act
            return ev, action
        else:
            opponent_num = 1
            if self.player_number == 1:
                opponent_num = 2
            action = 0
            v = 0
            for a in range(7):
                try:
                    child = self.result_board(board, a, opponent_num)
                except Exception as e:
                    continue
                rv, action = self.expectimax(child, True, a, d+1)
                v = v + (1/7) * rv
            return v, action


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
        v, action = self.expectimax(board, True, 0, 0)
        return action

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
        # have a sliding window of varying sizes count neighbor occurrences
        two_count = 0
        triple_count = 0

        # check rows
        for row_indx in range(6):
            row = board[row_indx]
            for i in range(1, 6):
                if (row[i-1]==self.player_number and row[i]==self.player_number and row[i+1]==self.player_number):
                    # print(f"triple in row {row_indx}")
                    triple_count += 10
                elif (row[i-1]==self.player_number and 
                      row[i]==self.player_number) or (row[i]==self.player_number 
                                                      and row[i+1]==self.player_number):
                    # since players can put coins left or right in row, we'll double count doubles
                    # print(f"double in row {row_indx}")
                    two_count += 1
                
        # check columns
        for col_indx in range(7):
            col = board[:,col_indx]
            for i in range(1,5):
                if (col[i-1] == 0 and col[i] == self.player_number and col[i+1] == self.player_number):
                    # print(f"double in column {col_indx}") 
                    two_count += 1
                if (col[i-1] == self.player_number and col[i] == self.player_number and col[i+1] == self.player_number):
                    # print(f"triple in column {col_indx}")
                    triple_count += 10

        # TODO: check diagonals

        # check if opponent is close to three
        opponent_num = 1
        if self.player_number == 1:
            opponent_num = 2
        
        counter_score = 0
        for row_indx in range(1,6):
            row = board[row_indx]
            for i in range(1, 6):
                if (row[i-1]==self.player_number and row[i]==opponent_num and row[i+1]==opponent_num):
                    counter_score += 1
                elif (row[i-1]==opponent_num and row[i]==opponent_num and row[i+1]==self.player_number):
                    counter_score += 1
            for i in range(2,6):
                if (row[i-2] == self.player_number and row[i-1]==opponent_num and row[i]==opponent_num and row[i+1]==opponent_num):
                    counter_score += 10
                elif (row[i-2] == opponent_num and row[i-1]==opponent_num and row[i]==opponent_num and row[i+1]==self.player_number):
                    counter_score += 10

        for col_indx in range(7):
            col = board[:,col_indx]
            for i in range(1,5):
                if (col[i-1] == self.player_number and col[i] == opponent_num and col[i+1] == opponent_num):
                    counter_score += 2
            for i in range(2, 5):
                if (col[i-2] == self.player_number and col[i-1] == opponent_num and col[i] == opponent_num and col[i+1] == opponent_num):
                    counter_score += 10

        # print(f"Eval: {np.sum(triple_count) + np.sum(two_count)}")
        return np.sum(triple_count) + np.sum(two_count) + np.sum(counter_score)


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

