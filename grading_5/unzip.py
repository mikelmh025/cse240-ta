# unzip all the files in the current directory
# convert to individual folders
import os
import zipfile

root = 'submissions'
zipfile_paths = [f for f in os.listdir(root) if f.endswith('.zip')]

for zipfile_path in zipfile_paths:
    print('Unzipping {}'.format(zipfile_path))
    with zipfile.ZipFile(os.path.join(root, zipfile_path), 'r') as z:
        # unzip to a folder with the same name as the zipfile
        z.extractall(os.path.join(root, zipfile_path[:-4]))
        
        # z.extractall(root)
    # os.remove(os.path.join(root, zipfile_path))



# rarfile_paths = [f for f in os.listdir(root) if f.endswith('.rar')]

# for rarfile_path in rarfile_paths:
#     print('Unzipping {}'.format(rarfile_path))
#     with zipfile.ZipFile(os.path.join(root, rarfile_path), 'r') as z:
#         # unzip to a folder with the same name as the zipfile
#         z.extractall(os.path.join(root, rarfile_path[:-4]))
        
#         # z.extractall(root)
#     # os.remove(os.path.join(root, zipfile_path))