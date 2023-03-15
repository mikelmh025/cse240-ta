
import data_utils
import os
import importlib.util
import sys
import time
import csv


class NoStdStreams(object):
    def __init__(self,stdout = None, stderr = None):
        self.devnull = open(os.devnull,'w')
        self._stdout = stdout or self.devnull or sys.stdout
        self._stderr = stderr or self.devnull or sys.stderr

    def __enter__(self):
        self.old_stdout, self.old_stderr = sys.stdout, sys.stderr
        self.old_stdout.flush(); self.old_stderr.flush()
        sys.stdout, sys.stderr = self._stdout, self._stderr

    def __exit__(self, exc_type, exc_value, traceback):
        self._stdout.flush(); self._stderr.flush()
        sys.stdout = self.old_stdout
        sys.stderr = self.old_stderr
        self.devnull.close()


def grade_submission(submission_dir,required_files,required_main_files,show_game=False):
    student_name = submission_dir.split('/')[-2]
    print("start grading %s" % student_name)

    with NoStdStreams():
        submission_files = [os.path.join(submission_dir, item) for item in required_files]
        sumission_main_files = [os.path.join(submission_dir, item) for item in required_main_files][0]

        sys.path.insert(0, submission_dir)
        spec = importlib.util.spec_from_file_location("main", sumission_main_files)
        main_module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(main_module)

        main_args = main_module.helper.make_args()
        main_args.NUM_TRAIN_ITER = 10
        print(main_args)
        game1 = main_module.SnakeGame(main_args)

        if game1.args.NUM_TRAIN_ITER != 0:
            game1.do_training()

        # Instead of using their do_testing() function, we will use our own
        def do_testing(game1):
            INITIALIZATION=0
            print("Test Phase:")
            game1.agent.set_eval()
            game1.agent.load_model()
            points_results = []
            start = time.time()
            for game in range(1, game1.args.NUM_TEST_ITER + 1):
                print("TESTING NUMBER: " + str(game))
                isAgentDead = False
                action = game1.agent.agent_action(game1.env.get_state(), INITIALIZATION, isAgentDead)
                while True:
                    if isAgentDead:
                        break
                    state, points, isAgentDead = game1.env.step(action)
                    action = game1.agent.agent_action(state, points, isAgentDead)
                points_results.append(game1.env.get_points())
                game1.env.reset()

            return time.time() - start, len(points_results), sum(points_results)/len(points_results), max(points_results), min(points_results)

        test_time, num_games, avg_points, max_points, min_points = do_testing(game1)

    print("Testing takes", test_time, "seconds")
    print("Number of Games:", num_games)
    print("Average Points:", avg_points)
    print("Max Points:", max_points)
    print("Min Points:", min_points)
    if show_game: game1.show_games()

    grade = 100

    return [test_time, num_games, avg_points, max_points, min_points,grade]

if __name__=='__main__':
    submission_dir_path = './submissions' #'regrade' #'submissions'

    required_files = ['board.py', 'game.py', 'helper.py', 'snake_agent.py']
    required_main_files = ['game.py']

    if submission_dir_path == 'submissions':
        grading_report_name = 'grading_report.csv' 
    else:
        grading_report_name = '%s_report.csv' % (submission_dir_path)

    submission_files = data_utils.make_pyset(submission_dir_path)


    # TODO: Fix this to to fit this grading script
    grade_dict = {}
    if os.path.exists(grading_report_name):
        grade_dict = data_utils.load_grading_csv(grading_report_name)

    submission_dirs = [item.replace(item.split('/')[-1], '') for item in submission_files]
    submission_dirs = list(set(submission_dirs))

    for submission_dir in submission_dirs:
        student_name = submission_dir.split('/')[-2]

        File_missing_flag = False
        for required_file in required_files:
            if not os.path.exists(os.path.join(submission_dir, required_file)):
                print('Submission %s does not have %s' % (submission_dir, required_file))
                File_missing_flag = True

        if File_missing_flag: 
            grade_data_list = [0,0,0,0,0,-100]
        else:
            grade_data_list = grade_submission(submission_dir,required_files,required_main_files)

        # Grade the assignment
        grade_dict[student_name] = grade_data_list
    

    header = ['student_name', 'test_time', 'num_games', 'avg_points', 'max_points', 'min_points', 'grade']
    with open(grading_report_name, 'w') as f:
        writer = csv.writer(f)
        writer.writerow(header)
        for student_name, grade_data_list in grade_dict.items():
            writer.writerow([student_name] + grade_data_list)


    # for submission_file in submission_files:
    #     submission_dirs.append(submission_file.split('/')[-2])


    #     file_name = submission_file.split('/')[-1]
    #     if file_name != 'game.py':continue

    #     student_name = submission_file.split('/')[-2]
    #     print("start grading %s" % student_name)

        
    # a=1