import os
import sys
import glob

ROOT_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..')

sys.path.append(ROOT_PATH)

from scripts.utils.novel import NOVELS_ROOT_PATH, NOVELS_BAK_ROOT_PATH


if __name__ == '__main__':
    dir_paths = glob.glob(os.path.join(NOVELS_ROOT_PATH, '*'))

    for dir_path in dir_paths:
        if not os.path.isdir(dir_path):
            continue

        file_paths = glob.glob(os.path.join(dir_path, '*_p*.txt'))

        #print(dir_path, len(file_paths))

        if len(file_paths) < 30:
            print(dir_path, len(file_paths))

            dest_path = dir_path.replace(NOVELS_ROOT_PATH, NOVELS_BAK_ROOT_PATH)
            os.rename(dir_path, dest_path)
            print('Rename to', dest_path)

