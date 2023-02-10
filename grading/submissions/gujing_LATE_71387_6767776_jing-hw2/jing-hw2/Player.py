import numpy as np

HORIZON = 1
VERTICAL = 2

class AIPlayer:
    def __init__(self, player_number):
        self.player_number = player_number
        self.type = 'ai'
        self.player_string = 'Player {}:ai'.format(player_number)
        self.directions = [HORIZON, VERTICAL]
        self.visited = 0
        self.Score = {
            1: 1, 2: 11, 3: 111, 4: 1111,
            5: 11111, 6: 111111, 7: 1111111,
            8: 11111111, 9: 111111111
        }
        
    def _available_moves(self, table):
        next_move = []
        for col in range(table.shape[1]):
            if 0 in table[:,col]:
                next_move.append((table.shape[0] - 1 - np.flip(table[:,col]).tolist().index(0), col))
        return next_move
    
    def game_finish(self, cc):
        for item in cc:
            data = item[0]
            for d in data:
                if d[1] >= 4:
                    return True
        return False

    def count(self, table, direction=HORIZON):
        L_list = []
        if direction == HORIZON:
            for i in range(table.shape[0]):
                s = table[i][0] 
                count = 1
                actions = [(i, 0)]
                for j in range(1, table.shape[1]):
                    if s == table[i][j]:
                        count += 1
                        actions.append((i,j))
                    else:
                        if s != 0:
                            L_list.append((s, count, actions))
                        s = table[i][j]
                        count = 1
                        actions=[(i, j)]
                    if j == table.shape[1] - 1 and s != 0:
                        L_list.append((s, count, actions))
        else:
            for j in range(table.shape[1]):
                s = table[0][j]
                count = 1
                actions = [(0, j)]
                for i in range(1, table.shape[0]):
                    if s == table[i][j]:
                        count += 1
                        actions.append((i,j))
                    else:
                        if s != 0:
                            L_list.append((s, count, actions))
                        s = table[i][j]
                        count = 1
                        actions=[(i, j)]
                    if i == table.shape[0] - 1 and s != 0:
                        L_list.append((s, count, actions))
        return L_list
    
    def heuristic(self, table, c, actions, direction=HORIZON):
        if direction == HORIZON:
            r, min_c, max_c = actions[0][0], actions[0][1], actions[len(actions)-1][1]
            available = []
            for i in range(min_c-1, -1, -1):
                if table[r][i] == 0:
                    available.append((r, i))
                else:
                    break
            for j in range(max_c+1, table.shape[1]):
                if table[r][j] == 0:
                    available.append((r, j))
                else:
                    break
            return available
        elif direction == VERTICAL:
            c, min_r, _ = actions[0][1], actions[0][0], actions[len(actions)-1][0]
            available = []
            for i in range(min_r-1, -1, -1):
                if table[i][c] == 0:
                    available.append((i, c))
                else:
                    break
            return available
            
    def calculate(self, table, player, cc, next_move):

        for r in cc:
            hs = [(t[0], t[1]) for t in r[0] if t[1] == 4]
            if len(hs) > 0:
                if hs[0][0] == player:
                    return 999999
                else:
                    return -999999
        score = 0
        for data, dp in cc:
            for p, c, actions in data:
                available = self.heuristic(table, c, actions, direction=dp)
                value = 0
                for i, j in next_move:
                    if (i, j) in available:
                        value += 1
                if p == player:
                    score += (self.Score[c] + value * 10 if c + value >= 4 else value * -10)
                else:
                    score -= (self.Score[c] + value * 10 if c + value >= 4 else value * -10)
        return score

    def _Max_Value(self, player, table, depth, alpha, beta):
        v = float('-inf')
        action = None
        next_move = self._available_moves(table)
        cc = [(self.count(table, di), di) for di in [HORIZON, VERTICAL]]
        if depth == 0 or len(next_move) == 0 or self.game_finish(cc):
            if depth == 0:
                self.visited += 1
                print(f"finished depth 5, {self.visited}")
            return self.calculate(table, player, cc, next_move), None
        for i, j in next_move:
            table[i][j] = player
            cur_value, _ = self._Min_Value(3-player, table, depth-1, alpha, beta)
            if cur_value > v:
                v = cur_value
                action = (i, j)
            table[i][j] = 0
            if v >= beta:
                return v, None
            alpha = max(alpha, v)
        return v, action

    def _Min_Value(self, player, table, depth, alpha, beta):
        v = float('inf')
        action = None
        next_move = self._available_moves(table)
        cc = [(self.count(table, di), di) for di in [HORIZON, VERTICAL]]
        if depth == 0 or len(next_move) == 0 or self.game_finish(cc):
            if depth == 0:
                self.visited += 1
                print(f"finished one tree with depth = 5 with times = {self.visited}")
            return self.calculate(table, player, cc, next_move), None
        for i, j in next_move:
            table[i][j] = player
            cur_value, _ = self._Max_Value(3-player, table, depth-1, alpha, beta)
            if cur_value < v:
                v = cur_value
                action = (i, j)
            table[i][j] = 0
            if v <= alpha:
                return v, None
            beta = min(beta, v)
        return v, action

    
    def _expecti_Max_Value(self, player, table, depth):
        v = float('-inf')
        action = None
        next_move = self._available_moves(table)
        cc = [(self.count(table, di), di) for di in [HORIZON, VERTICAL]]
        if depth == 0 or len(next_move) == 0 or self.game_finish(cc):
            if depth == 0:
                self.visited += 1
                print(f"finished one tree with depth = 5 with times = {self.visited}")
            return self.calculate(table, player, cc, next_move), None
        for i, j in next_move:
            table[i][j] = player
            cur_value, _ = self._expecti_exp_value(3-player, table, depth-1)
            if cur_value > v:
                v = cur_value
                action = (i, j)
            table[i][j] = 0
        return v, action
    
    def _expecti_exp_value(self, player, table, depth):

        v = 0
        action = -1
        next_move = self._available_moves(table)
        cc = [(self.count(table, di), di) for di in [HORIZON, VERTICAL]]
        if depth == 0 or len(next_move) == 0 or self.game_finish(cc):
            if depth == 0:
                self.visited += 1
                print(f"Job done depth 5, with times {self.visited}")
            return self.calculate(table, player, cc, next_move), None
        for i, j in next_move:
            table[i][j] = player
            cur_value, action = self._expecti_Max_Value(3-player, table, depth-1)
            table[i][j] = 0
            v += 1/len(next_move) * cur_value
        return v, action

    def get_expectimax_move(self, table):

        depth = 5
        self.visited = 0
        _, action = self._expecti_Max_Value(self.player_number, table, depth)
        return action[1]



    def evaluation_function(self, table):

        return self.calculate(table, self.player_number)



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
        # go through each column and put chest into it
        for i, col in enumerate(board.T):
            if 0 in col:
                valid_cols.append(i)

        move = int(input('Enter your move: '))

        while move not in valid_cols:
            print('Column full, choose from:{}'.format(valid_cols))
            move = int(input('Enter your move: '))

        return move

