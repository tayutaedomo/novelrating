import os
import sys
import glob
import datetime

ROOT_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..')

sys.path.append(ROOT_PATH)

from scripts.utils.novel import load_bookmark_csv, load_ranking_csv
from scripts.utils.novel import NovelPages
from scripts.utils.novel import NOVELS_ROOT_PATH


def get_all_summary_paths():
    path_name = os.path.join(NOVELS_ROOT_PATH, '*')
    return [os.path.basename(dir_path) for dir_path in glob.glob(path_name)]


if __name__ == '__main__':
    mode = None
    ncode_list = []

    if len(sys.argv) > 1:
        mode = sys.argv[1]

    if mode == 'all':
        ncode_list = get_all_summary_paths()
        print(datetime.datetime.now().isoformat(), 'All Count:', len(ncode_list))

    elif mode == 'bookmark':
        ncode_list = [bookmark['ncode'] for bookmark in load_bookmark_csv()]
        print(datetime.datetime.now().isoformat(), 'Bookmark Count:', len(ncode_list))

    elif mode == 'ranking':
        ncode_list = [novel['ncode'] for novel in load_ranking_csv()]
        print(datetime.datetime.now().isoformat(), 'Ranking Count:', len(ncode_list))

    elif mode == 'ncode':
        ncode = sys.argv[2]
        ncode_list.append(ncode)

    else:
        ncode_list = ['n0022gd', 'n0074em']

    print(datetime.datetime.now().isoformat(), 'Count:', len(ncode_list))

    for i, ncode in enumerate(ncode_list):
        pages = NovelPages()

        if pages.exist_json(ncode):
            print(datetime.datetime.now().isoformat(), i, ncode, 'Skip')
            continue

        print(datetime.datetime.now().isoformat(), i, ncode, 'New')
        pages.load(ncode)
        pages.save()

        print(datetime.datetime.now().isoformat(), i, ncode, 'Saved summary')

