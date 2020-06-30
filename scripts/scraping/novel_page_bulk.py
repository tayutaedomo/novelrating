import os
import sys
import datetime
import chromedriver_binary
from selenium import webdriver
from selenium.webdriver.chrome.options import Options

ROOT_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..')

sys.path.append(ROOT_PATH)

from scripts.utils.novel import NarouPageCrawler, load_bookmark_csv, load_ranking_csv
from scripts.utils.novel import NOVELS_ROOT_PATH


if __name__ == '__main__':
    page_start = 1
    page_count = 30
    page_end = page_start + page_count - 1

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

    crawler = NarouPageCrawler(driver, NOVELS_ROOT_PATH, 3)

    print(datetime.datetime.now().isoformat(),
          'Count:', len(ncode_list), ', Page:', page_start, 'to', page_end)

    for i, ncode in enumerate(ncode_list):
        crawler.crawl(ncode, page_start, page_end)

    # Capture
    #file_path = os.path.join(ROOT_PATH, 'tmp', 'capture.png')
    #driver.save_screenshot(file_path)

