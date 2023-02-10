import numpy as np
from enum import Enum
import logging

logger = logging.getLogger(__name__)
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s.%(msecs)03d %(levelname)s %(module)s - %(funcName)s: %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S',
    handlers=[
            logging.StreamHandler()
        ]
)

class Direction(Enum):
    HORIZON = 1
    VERTICAL = 2
    DIALOG = 3
    RDIALOG = 4

class AIPlayer:
    def __init__(self, player_number):
        self.player_number = player_number
        self.type = 'ai'
        self.player_string = 'Player {}:ai'.format(player_number)
        self.ctoScore = {
            1: 1,
            2: 11,
            3: 111,
            4: 1111,
            5: 11111,
            6: 111111,
            7: 1111111,
            8: 11111111,
            9: 111111111
        }
        self.directions = [Direction]
        self.tree_visited = 0

    def _switch_player(self, player):
        if player == 1:
            return 2
        else:
            return 1
        
    def _available_moves(self, board):
        next_move = []
        for col in range(board.shape[1]):
            if 0 in board[:,col]:
                next_move.append((board.shape[0] - 1 - np.flip(board[:,col]).tolist().index(0), col))
        return next_move
    
    def _isOver(self, cc):
        for data, _ in cc:
            for _, cc, _ in data:
                if cc >= 4:
                    return True
        return False

    def _connectNum(self, board, direction=Direction.HORIZON):
        playerToCntList = []
        if direction == Direction.HORIZON:
            for i in range(board.shape[0]):
                s = board[i][0]; cnt = 1; actions = [(i, 0)]
                for j in range(1, board.shape[1]):
                    if s == board[i][j]:
                        cnt += 1; actions.append((i,j))
                    else:
                        if s != 0:
                            playerToCntList.append((s, cnt, actions))
                        s = board[i][j]; cnt = 1; actions=[(i, j)]
                    if j == board.shape[1] - 1 and s != 0:
                        playerToCntList.append((s, cnt, actions))
        elif direction == Direction.VERTICAL:
            for j in range(board.shape[1]):
                s = board[0][j]; cnt = 1; actions = [(0, j)]
                for i in range(1, board.shape[0]):
                    if s == board[i][j]:
                        cnt += 1; actions.append((i,j))
                    else:
                        if s != 0:
                            playerToCntList.append((s, cnt, actions))
                        s = board[i][j]; cnt = 1; actions=[(i, j)]
                    if i == board.shape[0] - 1 and s != 0:
                        playerToCntList.append((s, cnt, actions))
        elif direction == Direction.DIALOG:
            playerToCntList = self.dialog(board)
        else:
            playerToCntList = self.dialog(board, direction=Direction.RDIALOG)
        return playerToCntList

    def dialog(self, board, direction=Direction.DIALOG):
        playerToCntList = []
        j = 0
        for i in range(board.shape[0]):
            si, sj = i, 0
            s = board[i][0]; cnt = 1; actions = [(si, sj)]
            if direction == Direction.DIALOG:
                si += 1; sj += 1
            else:
                si -= 1; sj += 1
            while si < board.shape[0] and sj < board.shape[1]:
                if s == board[si][sj]:
                    cnt += 1; actions.append((si,sj))
                else:
                    if s != 0:
                        playerToCntList.append((s, cnt, actions))
                    s = board[si][sj]; cnt = 1; actions=[(si, sj)]
                if (si == board.shape[0] - 1 or sj == board.shape[1] - 1) and s != 0:
                    playerToCntList.append((s, cnt, actions))
                if direction == Direction.DIALOG:
                    si += 1; sj += 1
                else:
                    si -= 1; sj += 1
        i = 0
        for j in range(1, board.shape[1]):
            si, sj = i, j
            s = board[i][0]; cnt = 1; actions = [(si, sj)]
            if direction == Direction.DIALOG:
                si += 1; sj += 1
            else:
                si -= 1; sj += 1
            while si < board.shape[0] and sj < board.shape[1]:
                if s == board[si][sj]:
                    cnt += 1; actions.append((si,sj))
                else:
                    if s != 0:
                        playerToCntList.append((s, cnt, actions))
                    s = board[si][sj]; cnt = 1; actions=[(si, sj)]
                if (si == board.shape[0] - 1 or sj == board.shape[1] - 1) and s != 0:
                    playerToCntList.append((s, cnt, actions))
                if direction == Direction.DIALOG:
                    si += 1; sj += 1
                else:
                    si -= 1; sj += 1
        return playerToCntList

    def _utility(self, board, player, cc, next_move):
        def heuristic(board, c, actions, direction=Direction.HORIZON):
            if direction == Direction.HORIZON:
                r, min_c, max_c = actions[0][0], actions[0][1], actions[len(actions)-1][1]
                available = []
                for i in range(min_c-1, -1, -1):
                    if board[r][i] == 0:
                        available.append((r, i))
                    else:
                        break
                for j in range(max_c+1, board.shape[1]):
                    if board[r][j] == 0:
                        available.append((r, j))
                    else:
                        break
                return available
            elif direction == Direction.VERTICAL:
                c, min_r, max_r = actions[0][1], actions[0][0], actions[len(actions)-1][0]
                available = []
                for i in range(min_r-1, -1, -1):
                    if board[i][c] == 0:
                        available.append((i, c))
                    else:
                        break
                return available
            elif direction == Direction.DIALOG:
                available = []
                si, sj = actions[0]
                ei, ej = actions[len(actions)-1]
                si -= 1; sj -= 1
                while si > -1 and sj > -1:
                    if board[si][sj] == 0:
                        available.append((si, sj))
                    else:
                        break
                    si -= 1; sj -= 1
                ei += 1; ej += 1
                while ei < board.shape[0] and ej < board.shape[1]:
                    if board[ei][ej] == 0:
                        available.append((ei, ej))
                    else:
                        break
                    ei += 1; ej += 1
                return available
            else:
                available = []
                si, sj = actions[0]
                ei, ej = actions[len(actions)-1]
                si += 1; sj -= 1
                while si < board.shape[0] and sj > -1:
                    if board[si][sj] == 0:
                        available.append((si, sj))
                    else:
                        break
                    si += 1; sj -= 1
                ei -= 1; ej += 1
                while ei > -1 and ej < board.shape[1]:
                    if board[ei][ej] == 0:
                        available.append((ei, ej))
                    else:
                        break
                    ei -= 1; ej += 1
                return available
            
        def overlap(next_move, available):
            cnt = 0
            for i, j in next_move:
                if (i, j) in available:
                    cnt += 1
            return cnt
        
        # see: game over check
        for r in cc:
            hs = [(t[0], t[1]) for t in r[0] if t[1] == 4]
            if len(hs) > 0:
                if hs[0][0] == player:
                    return 999999
                else:
                    return -999999
        # see: heuristic along every direction
        score = 0
        for data, dp in cc:
            for p, c, actions in data:
                available = heuristic(board, c, actions, direction=dp)
                ec = overlap(next_move, available)
                if p == player:
                    # c = 1 -> 1, c = 2 -> 11, c = 3 -> 111
                    score += (self.ctoScore[c] + ec * 10 if c + ec >= 4 else ec * -10)
                else:
                    score -= (self.ctoScore[c] + ec * 10 if c + ec >= 4 else ec * -10)
        return score

    def _max_value(self, player, board, depth, alpha, beta):
        v = float('-inf'); action = None
        next_move = self._available_moves(board)
        cc = [(self._connectNum(board, di), di) for di in [Direction.HORIZON, Direction.VERTICAL, Direction.DIALOG, Direction.RDIALOG]]
        if depth == 0 or len(next_move) == 0 or self._isOver(cc):
            if depth == 0:
                self.tree_visited += 1
                logger.info(f"finished one tree with depth = 5 with times = {self.tree_visited}")
            return self._utility(board, player, cc, next_move), None
        for i, j in next_move:
            board[i][j] = player
            cur_v, _ = self._min_value(self._switch_player(player), board, depth-1, alpha, beta)
            if cur_v > v:
                v = cur_v; action = (i, j)
            board[i][j] = 0
            if v >= beta:
                return v, None
            alpha = max(alpha, v)
        return v, action

    def _min_value(self, player, board, depth, alpha, beta):
        v = float('inf'); action = None
        next_move = self._available_moves(board)
        cc = [(self._connectNum(board, di), di) for di in [Direction.HORIZON, Direction.VERTICAL, Direction.DIALOG, Direction.RDIALOG]]
        if depth == 0 or len(next_move) == 0 or self._isOver(cc):
            if depth == 0:
                self.tree_visited += 1
                logger.info(f"finished one tree with depth = 5 with times = {self.tree_visited}")
            return self._utility(board, player, cc, next_move), None
        for i, j in next_move:
            board[i][j] = player
            cur_v, _ = self._max_value(self._switch_player(player), board, depth-1, alpha, beta)
            if cur_v < v:
                v = cur_v; action = (i, j)
            board[i][j] = 0
            if v <= alpha:
                return v, None
            beta = min(beta, v)
        return v, action

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
        self.tree_visited = 0
        alpha, beta = float('-inf'), float('inf')
        depth = 5
        _, action = self._max_value(self.player_number, board, depth, alpha, beta)
        return action[1]
    
    def _expecti_max_value(self, player, board, depth):
        v = float('-inf'); action = None
        next_move = self._available_moves(board)
        cc = [(self._connectNum(board, di), di) for di in [Direction.HORIZON, Direction.VERTICAL, Direction.DIALOG, Direction.RDIALOG]]
        if depth == 0 or len(next_move) == 0 or self._isOver(cc):
            if depth == 0:
                self.tree_visited += 1
                logger.info(f"finished one tree with depth = 5 with times = {self.tree_visited}")
            return self._utility(board, player, cc, next_move), None
        for i, j in next_move:
            board[i][j] = player
            cur_v, _ = self._expecti_exp_value(self._switch_player(player), board, depth-1)
            if cur_v > v:
                v = cur_v; action = (i, j)
            board[i][j] = 0
        return v, action
    
    def _expecti_exp_value(self, player, board, depth):
        """expecti algorithm to return action -1, which is randomly selected at this step

        Args:
            player (int): the player indicator
            board (np.array): the chess board
            depth (int): the depth limit

        Returns:
            tuple(v, action): the expectation value and action with -1 (random draw)
        """
        v = 0; action = -1
        next_move = self._available_moves(board)
        cc = [(self._connectNum(board, di), di) for di in [Direction.HORIZON, Direction.VERTICAL, Direction.DIALOG, Direction.RDIALOG]]
        if depth == 0 or len(next_move) == 0 or self._isOver(cc):
            if depth == 0:
                self.tree_visited += 1
                logger.info(f"finished one tree with depth = 5 with times = {self.tree_visited}")
            return self._utility(board, player, cc, next_move), None
        for i, j in next_move:
            board[i][j] = player
            cur_v, action = self._expecti_max_value(self._switch_player(player), board, depth-1)
            board[i][j] = 0
            v += 1/len(next_move) * cur_v
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
        depth = 5
        self.tree_visited = 0
        _, action = self._expecti_max_value(self.player_number, board, depth)
        return action[1]



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
        return self._utility(board, self.player_number)


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

if __name__ == "__main__":
    ai = AIPlayer(1)
    board = np.zeros((6,7))
    board[0][1] = 1
    board[0][2] = 1
    board[0][3] = 1
    board[1][1] = 2
    board[1][2] = 2
    board[1][3] = 2
    board[1][4] = 2
    ai._connectNum(board)
