import os
import sys
import datetime

ROOT_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..')

sys.path.append(ROOT_PATH)

from scripts.utils.novel import NovelPage


if __name__ == '__main__':
    ncode = 'n0022gd'
    page_num = 1

    page = NovelPage()
    page.load(ncode, page_num)

    import pprint as pp
    print(page.get_char_count())
    print(page.get_new_line_count())
    print(page.get_talk_char_count())
    print(page.get_word_count())
    pp.pprint(page.get_word_summary())

