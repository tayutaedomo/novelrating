import os
import sys
import glob

ROOT_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..')

sys.path.append(ROOT_PATH)

from scripts.utils.novel import NOVELS_ROOT_PATH


if __name__ == '__main__':
    file_paths = glob.glob(os.path.join(NOVELS_ROOT_PATH, '*', '*_p*.txt'))

    for src_path in file_paths:
        dir_path = os.path.dirname(src_path)
        file_name = os.path.basename(src_path)
        file_name = file_name.replace('-p', '_p')
        dest_path = os.path.join(dir_path, file_name)

        os.rename(src_path, dest_path)

