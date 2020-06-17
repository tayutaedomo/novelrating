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
    ncode = None
    page_start = 1
    page_count = 1

    if len(sys.argv) > 3:
        ncode = sys.argv[1]
        page_start = int(sys.argv[2])
        page_count = int(sys.argv[3])

    if len(sys.argv) > 2:
        ncode = sys.argv[1]
        page_start = int(sys.argv[2])

    elif len(sys.argv) > 1:
        ncode = sys.argv[1]

    if not ncode:
        print(datetime.datetime.now().isoformat(), 'ncode is required.')
        pass

    page_end = page_start + page_count - 1
    print(datetime.datetime.now().isoformat(), 'ncode:', ncode, ', Page:', page_start, 'to', page_end)

    options = Options()
    options.add_argument('--headless')
    options.add_argument('--incognito')
    driver = webdriver.Chrome(options=options)

    crawler = NarouPageCrawler(driver, DEST_ROOT_PATH, 3)
    crawler.crawl(ncode, page_start, page_end)

    # Capture
    #file_path = os.path.join(ROOT_PATH, 'tmp', 'capture.png')
    #driver.save_screenshot(file_path)

