import os
import sys
import time
import datetime
import pprint as pp
import chromedriver_binary
from selenium import webdriver
from selenium.webdriver.chrome.options import Options

ROOT_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..')

sys.path.append(ROOT_PATH)

from scripts.utils.novel import load_bookmark_csv, load_ranking_csv
from scripts.utils.novel import NovelInfo


if __name__ == '__main__':
    mode = None
    ncode_list = []

    if len(sys.argv) > 1:
        mode = sys.argv[1]

    if mode == 'bookmark':
        ncode_list = [bookmark['ncode'] for bookmark in load_bookmark_csv()]
        print(datetime.datetime.now().isoformat(), 'Bookmark Count:', len(ncode_list))

    elif mode == 'ranking':
        ncode_list = [novel['ncode'] for novel in load_ranking_csv()]
        print(datetime.datetime.now().isoformat(), 'Ranking Count:', len(ncode_list))

    elif mode == 'ncode':
        ncode = sys.argv[2]
        ncode_list.append(ncode)

    else:
        ncode_list = ['n6316bn', 'n9669bk']

    options = Options()
    options.add_argument('--headless')
    options.add_argument('--incognito')
    driver = webdriver.Chrome(options=options)

    for i, ncode in enumerate(ncode_list):
        novel_info = NovelInfo()

        if novel_info.exist_json(ncode):
            print(datetime.datetime.now().isoformat(), i, ncode, 'Skip')
            continue

        print(datetime.datetime.now().isoformat(), i, ncode, 'New')
        novel_info.scrape(driver, ncode)
        novel_info.save()

        print(datetime.datetime.now().isoformat(), i, ncode, 'Saved info')

        if i < len(ncode_list) - 1:
            print(datetime.datetime.now().isoformat(), 'Sleep(3)')
            time.sleep(3)

    # Capture
    #file_path = os.path.join(ROOT_PATH, 'tmp', 'capture.png')
    #driver.save_screenshot(file_path)

