import os
import sys
import glob

ROOT_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..')

sys.path.append(ROOT_PATH)

from scripts.utils.novel import NOVELS_ROOT_PATH


if __name__ == '__main__':
    file_paths = glob.glob(os.path.join(NOVELS_ROOT_PATH, '*', '*_summary.json'))

    for i, file_path in enumerate(file_paths):
        os.remove(file_path)
        print(i, file_path, 'Removed')

