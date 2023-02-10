# system libs
import argparse
import multiprocessing as mp
import tkinter as tk

# 3rd party libs
import numpy as np
import importlib.util
import os
import csv
import sys
import data_utils

#https://stackoverflow.com/a/37737985
def turn_worker(board, send_end, p_func):
    send_end.send(p_func(board))


class Game:
    def __init__(self, player1, player2, time):
        self.players = [player1, player2]
        self.colors = ['yellow', 'red']
        self.current_turn = 0
        self.board = np.zeros([6,7]).astype(np.uint8)
        self.gui_board = []
        self.game_over = False
        self.ai_turn_limit = time

        #https://stackoverflow.com/a/38159672
        self.root = tk.Tk()
        self.root.title('Connect 4')
        self.player_string = tk.Label(self.root, text=student_name+": "+player1.player_string)
        self.player_string.pack()
        self.c = tk.Canvas(self.root, width=700, height=600)
        self.c.pack()

        for row in range(0, 700, 100):
            column = []
            for col in range(0, 700, 100):
                column.append(self.c.create_oval(row, col, row+100, col+100, fill=''))
            self.gui_board.append(column)

        tk.Button(self.root, text='Next Move', command=self.make_move).pack()
        tk.Button(self.root, text='Start', command=self.start).pack()

        self.score = []
        tk.Button(self.root, text='Good-Full', command=self.good).pack()
        tk.Button(self.root, text='Good-Parcial', command=self.good_parcial).pack()
        tk.Button(self.root, text='Not good -Parcial', command=self.not_good_parcial).pack()
        tk.Button(self.root, text='Zero', command=self.bad).pack()
        tk.Button(self.root, text='Try again', command=self.again).pack()
        tk.Button(self.root, text='Exit', command=self.exit).pack()

        self.root.mainloop()

    def start(self):
        while not self.game_over:
            self.make_move()
        # self.make_move()

    def good(self):
        self.score.append(1)
        self.root.destroy()
    
    def good_parcial(self):
        self.score.append(0.75)
        self.root.destroy()
    
    def not_good_parcial(self):
        self.score.append(0.5)
        self.root.destroy()
    
    def bad(self):
        self.score.append(0)
        self.root.destroy()
    
    def again(self):
        self.score.append(-1)
        self.root.destroy()

    def exit(self):
        sys.exit()
        
        

    def make_move(self):
        if not self.game_over:
            current_player = self.players[self.current_turn]

            if current_player.type == 'ai':
                
                if self.players[int(not self.current_turn)].type == 'random':
                    p_func = current_player.get_expectimax_move
                else:
                    p_func = current_player.get_alpha_beta_move
                
                try:
                    recv_end, send_end = mp.Pipe(False)
                    p = mp.Process(target=turn_worker, args=(self.board, send_end, p_func))
                    p.start()
                    if p.join(self.ai_turn_limit) is None and p.is_alive():
                        p.terminate()
                        raise Exception('Player Exceeded time limit')
                except Exception as e:
                    uh_oh = 'Uh oh.... something is wrong with Player {}'
                    print(uh_oh.format(current_player.player_number))
                    print(e)
                    raise Exception('Game Over')

                move = recv_end.recv()
            else:
                move = current_player.get_move(self.board)

            if move is not None:
                self.update_board(int(move), current_player.player_number)

            if self.game_completed(current_player.player_number):
                self.game_over = True
                self.player_string.configure(text=self.players[self.current_turn].player_string + ' wins!')
            elif self.full_board():
                self.game_over = True
                self.player_string.configure(text='Tie Game')
            else:
                self.current_turn = int(not self.current_turn)
                self.player_string.configure(text=self.players[self.current_turn].player_string)
        a=1

    def update_board(self, move, player_num):
        if 0 in self.board[:,move]:
            update_row = -1
            for row in range(1, self.board.shape[0]):
                update_row = -1
                if self.board[row, move] > 0 and self.board[row-1, move] == 0:
                    update_row = row-1
                elif row==self.board.shape[0]-1 and self.board[row, move] == 0:
                    update_row = row

                if update_row >= 0:
                    self.board[update_row, move] = player_num
                    self.c.itemconfig(self.gui_board[move][update_row],
                                      fill=self.colors[self.current_turn])
                    break
        else:
            err = 'Invalid move by player {}. Column {}'.format(player_num, move)
            raise Exception(err)


    def game_completed(self, player_num):
        player_win_str = '{0}{0}{0}{0}'.format(player_num)
        board = self.board
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

    def full_board(self):
        return not 0 in self.board


def main(player1, player2, time,submission_path):
    """
    Creates player objects based on the string paramters that are passed
    to it and calls play_game()

    INPUTS:
    player1 - a string ['ai', 'random', 'human']
    player2 - a string ['ai', 'random', 'human']
    """
    Player_spec = importlib.util.spec_from_file_location('submissions', submission_path)
    foo = importlib.util.module_from_spec(Player_spec)
    Player_spec.loader.exec_module(foo)
    AIPlayer = foo.AIPlayer
    RandomPlayer = foo.RandomPlayer
    HumanPlayer = foo.HumanPlayer


    def make_player(name, num):
        if name=='ai':
            return AIPlayer(num)
        elif name=='random':
            return RandomPlayer(num)
        elif name=='human':
            return HumanPlayer(num)

    record = Game(make_player(player1, 1), make_player(player2, 2), time)
    while -1 in record.score:
        record = Game(make_player(player1, 1), make_player(player2, 2), time)

    mean = np.mean(record.score)
    return mean


def play_game(player1, player2):
    """
    Creates a new game GUI and plays a game using the two players passed in.

    INPUTS:
    - player1 an object of type AIPlayer, RandomPlayer, or HumanPlayer
    - player2 an object of type AIPlayer, RandomPlayer, or HumanPlayer

    RETURNS:
    None
    """
    board = np.zeros([6,7])






if __name__=='__main__':
    player_types = ['ai', 'random', 'human']
    parser = argparse.ArgumentParser()
    parser.add_argument('player1', choices=player_types)
    parser.add_argument('player2', choices=player_types)
    parser.add_argument('--time',
                        type=int,
                        default=60,
                        help='Time to wait for a move in seconds (int)')
    args = parser.parse_args()

    # 1: Find out all the submissions
    # 2: Import submission models one by one
    # 3: Run the game with each submission
    # 4: Record the results

    # Local libs
    # submission_path = 'submissions/adlercoen_70406_6761435_Player.py'
    # submission_path = 'TA solution/Player.py'
    
    grading_report_name = 'grading_report%s.csv' % ("_"+args.player1 + '_' + args.player2)

    # Given a dir find all the py files
    submission_dir_path = 'submissions'
    # submission_files = [f for f in os.listdir(submission_dir_path) if f.endswith('.py')]

    submission_files = data_utils.make_pyset(submission_dir_path)

    # Create or load initial grading report
    grade_dict = {}
    if os.path.exists(grading_report_name):
        grade_dict = data_utils.load_grading_csv(grading_report_name)


    # Loop through all the submissions
    for submission_file in submission_files:
        if 'ConnectFour' in submission_file: continue
        if 'Player' not in submission_file: print('Skipping %s' % submission_file)
        if submission_file in grade_dict: 
            if grade_dict[submission_file][0] == 1:
                continue

        student_name = submission_file.replace(submission_dir_path+'/','').split('_')[0]
        print("start grading %s" % student_name)
        # student_name = submission_file.split('/')[-1].split('_')[0]
        
        # cur_submission_path = os.path.join(submission_dir_path, submission_file)
        # Grade one submission
        try:
            score = main(args.player1, args.player2, args.time,submission_path=submission_file)
        except:
            score = -1
        # score = 1 # default score

        grade_dict[submission_file] = [score, student_name]


        # Save the grading report

        if not os.path.exists(grading_report_name):
            header = ['file_name', 'score']
            writer = csv.writer(f)
            writer.writerow(header)
        
        with open(grading_report_name, 'a') as f:
            writer = csv.writer(f)
            # for name in grade_dict:
            name = submission_file
            if grade_dict[name] == 'nan': continue
            row = [name, grade_dict[name][0], grade_dict[name][1]]
            writer.writerow(row)

        temp_dict = data_utils.load_grading_csv (grading_report_name)
        a=1

    