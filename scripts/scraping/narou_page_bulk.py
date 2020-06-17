import os
import sys
import datetime
import chromedriver_binary
from selenium import webdriver
from selenium.webdriver.chrome.options import Options

ROOT_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..')
DEST_ROOT_PATH = os.path.join(ROOT_PATH, 'data', 'narou')

sys.path.append(ROOT_PATH)

from scripts.utils.novel import NarouPageCrawler


if __name__ == '__main__':
    ncode_list = [
        'n6316bn',
        'n9669bk',
        'n7855ck',
    ]

    page_start = 1
    page_count = 30
    page_end = page_start + page_count - 1

    options = Options()
    options.add_argument('--headless')
    options.add_argument('--incognito')
    driver = webdriver.Chrome(options=options)

    crawler = NarouPageCrawler(driver, DEST_ROOT_PATH, 3)

    print(datetime.datetime.now().isoformat(), 'ncode Count:', len(ncode_list), ', Page:', page_start, 'to', page_end)

    for i, ncode in enumerate(ncode_list):
        crawler.crawl(ncode, page_start, page_end)

    # Capture
    #file_path = os.path.join(ROOT_PATH, 'tmp', 'capture.png')
    #driver.save_screenshot(file_path)

