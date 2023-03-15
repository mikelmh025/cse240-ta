import os
import csv

# File system utils
MODEL_EXTENSIONS = [
   '.py'
]

def is_image_file(filename):
    return any(filename.endswith(extension) for extension in MODEL_EXTENSIONS)

# Customezed for this grading scrip
def make_pyset(dir):
    images = []
    assert os.path.isdir(dir), '%s is not a valid directory' % dir
    for root, _, fnames in sorted(os.walk(dir)):
        for fname in fnames:
            if is_image_file(fname):
                path = os.path.join(root, fname)
                if '__MACOSX' in path or '.Player' in path or 'ConnectFour' in path:
                    continue
                assert os.path.isfile(path), '%s is not a valid file' % path
                images.append(path)
        # break
    return images


def load_grading_csv(csv_path):
    with open(csv_path, 'r') as f:
        reader = csv.reader(f)
        grade_dict = {}
        header = next(reader)

        for row in reader:
            # make sure value is not nan
            if row[1] == 'nan': continue
            grade_dict[row[0]] = [row[1], row[2]]

    return grade_dict