import os
import sys
import datetime
import pprint as pp

ROOT_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..')

sys.path.append(ROOT_PATH)

from scripts.utils.novel import NovelPage, NovelPages


if __name__ == '__main__':
    ncode = 'n0022gd'

    # import pprint as pp
    # page = NovelPage()
    # page.load(ncode, 1)
    #
    # print(page.get_char_count())
    # print(page.get_new_line_count())
    # print(page.get_talk_char_count())
    # print(page.get_word_count())
    # pp.pprint(page.get_word_classes())

    pages = NovelPages()
    pages.load(ncode)
    # summary = pages.get_summary()
    # pp.pprint(summary)
    pages.save()

