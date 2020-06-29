import os
import glob

ROOT_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..')
NAROU_ROOT_PATH = os.path.join(ROOT_PATH, 'data', 'narou')
NAROU_BAK_ROOT_PATH = os.path.join(ROOT_PATH, 'data', 'narou.bak')


if __name__ == '__main__':
    dir_paths = glob.glob(os.path.join(NAROU_ROOT_PATH, '*'))

    for dir_path in dir_paths:
        if not os.path.isdir(dir_path):
            continue

        file_paths = glob.glob(os.path.join(dir_path, '*_p*.txt'))

        #print(dir_path, len(file_paths))

        if len(file_paths) < 30:
            print(dir_path, len(file_paths))

            dest_path = dir_path.replace(NAROU_ROOT_PATH, NAROU_BAK_ROOT_PATH)
            os.rename(dir_path, dest_path)
            print('Rename to', dest_path)

