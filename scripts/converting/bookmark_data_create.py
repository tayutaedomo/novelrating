import os
import sys
import datetime
import pprint as pp

ROOT_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..')

sys.path.append(ROOT_PATH)

from scripts.utils.novel import load_bookmark_rating_csv
from scripts.utils.model import BookmarkDataMaker


if __name__ == '__main__':
    mode = None
    ncode_list = []

    if len(sys.argv) > 1:
        mode = sys.argv[1]

    if mode == 'ncode':
        ncode = sys.argv[2]
        ncode_list.append(ncode)

    else:
        ncode_list = [bookmark['ncode'] for bookmark in load_bookmark_rating_csv()]
        print(datetime.datetime.now().isoformat(), 'Bookmark Count:', len(ncode_list))

    maker = BookmarkDataMaker()
    maker.load(ncode_list)

    # pp.pprint(maker.unique_keywords.get_sorted_items(True))
    # pp.pprint(maker.unique_word_classes.get_sorted_items(True))
    # pp.pprint(maker.unique_keywords.get_unique_keys())
    # pp.pprint(maker.unique_word_classes.get_unique_keys())
    # print(len(ncode_list), len(maker.inputs_list))

    maker.make()
    maker.save()

