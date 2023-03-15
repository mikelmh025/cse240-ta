import os
import importlib.util


def grade_assignment(submissions_folder_path, main_file_name, grade_file_name):
    # Get a list of all the subfolders in the submissions folder
    submissions = os.listdir(submissions_folder_path)

    # Loop through each subfolder (each student's submission)
    for submission in submissions:
        submission_path = os.path.join(submissions_folder_path, submission)

        # Check if the submission is a folder
        if os.path.isdir(submission_path):
            # Load the main file from the submission folder
            main_file_path = os.path.join(submission_path, main_file_name)

            # Check if the main file exists
            if os.path.isfile(main_file_path):
                # Load the helper function files from the submission folder
                helper_file_1_path = os.path.join(submission_path, 'helper1.py')
                helper_file_2_path = os.path.join(submission_path, 'helper2.py')
                helper_file_3_path = os.path.join(submission_path, 'helper3.py')

                # Check if all the helper files exist
                if (os.path.isfile(helper_file_1_path)
                        and os.path.isfile(helper_file_2_path)
                        and os.path.isfile(helper_file_3_path)):
                    # Load the main file module
                    spec = importlib.util.spec_from_file_location("main", main_file_path)
                    main_module = importlib.util.module_from_spec(spec)
                    spec.loader.exec_module(main_module)

                    # Call the main function to get the grade
                    grade = main_module.main()

                    # Write the grade to the grade file
                    grade_file_path = os.path.join(submission_path, grade_file_name)
                    with open(grade_file_path, 'w') as f:
                        f.write(str(grade))
                else:
                    print(f"Error: Helper files not found in {submission_path}")
            else:
                print(f"Error: Main file not found in {submission_path}")
        else:
            print(f"Error: {submission} is not a folder")


if __name__ == '__main__':
    submissions_folder = "submissions"
    main_file = "main.py"
    grade_file = "grade.txt"
    grade_assignment(submissions_folder, main_file, grade_file)
