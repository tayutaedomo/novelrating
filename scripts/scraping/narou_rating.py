import os
import csv
import sys
import time
import datetime
import chromedriver_binary
from selenium import webdriver
from selenium.webdriver.chrome.options import Options

ROOT_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..')
BOOKMARK_CSV_PATH = os.path.join(ROOT_PATH, 'data', 'narou', 'my_bookmark.csv')

sys.path.append(ROOT_PATH)

from scripts.utils.novel import login_narou


def load_bookmark_csv():
    bookmarks = []

    if not os.path.exists(BOOKMARK_CSV_PATH):
        return bookmarks

    with open(BOOKMARK_CSV_PATH, 'r', encoding='utf-8') as f:
        for row in csv.reader(f):
            bookmarks.append({
                'category': row[0],
                'ncode': row[1],
                'title': row[2],
            })

    return bookmarks


def get_rating(driver, ncode):
    url = 'https://ncode.syosetu.com/{}/1/'.format(ncode)
    print(datetime.datetime.now().isoformat(), 'GET:', url)

    driver.get(url)

    try:
        no_point_elem = driver.find_element_by_css_selector('div.p-novelpoint-form__note')
        print(no_point_elem.text)
        if no_point_elem.text == '評価受付停止中の作品です。':
            return None
    except Exception:
        pass

    rating = 0.0

    try:
        full_elem_list = driver.find_elements_by_css_selector('#novelpoint_form i.is-full')
        rating += len(full_elem_list)

        full_elem_list = driver.find_elements_by_css_selector('#novelpoint_form i.is-half')
        rating += len(full_elem_list) * 0.5
    except Exception as e:
        print(e)
        pass

    return rating


if __name__ == '__main__':
    bookmarks = load_bookmark_csv()
    print(datetime.datetime.now().isoformat(), 'Bookmark Count:', len(bookmarks))

    email = os.getenv('NAROU_EMAIL')
    password = os.getenv('NAROU_PASSWORED')

    options = Options()
    options.add_argument('--headless')
    options.add_argument('--incognito')
    driver = webdriver.Chrome(options=options)

    login_narou(driver, email, password)

    #ncode = 'n7951ei'
    #ncode = 'n7787eq'
    ncode = 'n6859du'
    rating = get_rating(driver, ncode)
    print(rating)

    # Capture
    #file_path = os.path.join(ROOT_PATH, 'tmp', 'capture.png')
    #driver.save_screenshot(file_path)

