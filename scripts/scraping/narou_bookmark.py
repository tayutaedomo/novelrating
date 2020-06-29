import os
import sys
import re
import time
import datetime
import chromedriver_binary
from selenium import webdriver
from selenium.webdriver.chrome.options import Options

ROOT_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..')
CSV_PATH = os.path.join(ROOT_PATH, 'data', 'bookmark.csv')

sys.path.append(ROOT_PATH)

from scripts.utils.novel import login_narou


def get_bookmarks_all(driver):
    bookmark_page_list = [
        {'category': 1, 'num': 1},
        {'category': 2, 'num': 1},
        {'category': 2, 'num': 2},
        {'category': 3, 'num': 1},
        {'category': 3, 'num': 2},
        {'category': 3, 'num': 3},
        {'category': 4, 'num': 1},
    ]

    bookmarks = []

    for i, page in enumerate(bookmark_page_list):
        ret = get_bookmarks(driver, page['category'], page['num'])
        print(datetime.datetime.now().isoformat(), 'Bookmark Count:', len(ret))

        bookmarks.extend(ret)

        if i < len(bookmark_page_list) - 1:
            print(datetime.datetime.now().isoformat(), 'Sleep(3)')
            time.sleep(3)

    return bookmarks


def get_bookmarks(driver, category, page_num):
    bookmarks = []

    base_url = 'https://syosetu.com/favnovelmain/list/index.php?nowcategory={}&order=new&p={}'
    url = base_url.format(category, page_num)
    print(datetime.datetime.now().isoformat(), 'GET:', url)

    driver.get(url)

    for a_elem in driver.find_elements_by_css_selector('a.title'):
        bookmark = {
            'category': category,
            'ncode': '',
            'title': a_elem.text,
        }

        matched = re.match(r'^https:\/\/ncode\.syosetu\.com\/(.+)\/$', a_elem.get_attribute('href'))

        if matched:
            bookmark['ncode'] = matched.group(1)

        bookmarks.append(bookmark)

    return bookmarks


def save_to_csv(bookmarks):
    print(datetime.datetime.now().isoformat(), 'Write, ', len(bookmarks))

    with open(CSV_PATH, 'w') as f:
        for bookmark in bookmarks:
            csv_line = '"{}","{}","{}"'.format(
                bookmark.get('category'),
                bookmark.get('ncode'),
                bookmark.get('title'),
            )

            f.write(csv_line + '\n')


if __name__ == '__main__':
    email = os.getenv('NAROU_EMAIL')
    password = os.getenv('NAROU_PASSWORED')

    options = Options()
    options.add_argument('--headless')
    options.add_argument('--incognito')
    driver = webdriver.Chrome(options=options)

    login_narou(driver, email, password)

    bookmarks = get_bookmarks_all(driver)

    save_to_csv(bookmarks)

    # Capture
    #file_path = os.path.join(ROOT_PATH, 'tmp', 'capture.png')
    #driver.save_screenshot(file_path)

