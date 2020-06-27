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
BOOKMARK_RATING_CSV_PATH = os.path.join(ROOT_PATH, 'data', 'narou', 'my_bookmark_rating.csv')

sys.path.append(ROOT_PATH)

from scripts.utils.novel import login_narou, load_bookmark_csv


def create_cache():
    cache = {}

    if not os.path.exists(BOOKMARK_RATING_CSV_PATH):
        return cache

    with open(BOOKMARK_RATING_CSV_PATH, 'r', encoding='utf-8') as f:
        for row in csv.reader(f):
            cache[row[0]] = row[2]  # { ncode: rating, ... }

    return cache


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
        pass

    return rating


def append_to_csv(bookmark):
    csv_line = '"{}","{}","{}","{}"'.format(
        bookmark.get('ncode'),
        bookmark.get('category'),
        bookmark.get('rating'),
        bookmark.get('title'),
    )

    with open(BOOKMARK_RATING_CSV_PATH, 'a') as f:
        f.write(csv_line + '\n')


if __name__ == '__main__':
    bookmarks = load_bookmark_csv()
    print(datetime.datetime.now().isoformat(), 'Bookmark Count:', len(bookmarks))

    cache = create_cache()
    print(datetime.datetime.now().isoformat(), 'Cache Count:', len(cache))

    email = os.getenv('NAROU_EMAIL')
    password = os.getenv('NAROU_PASSWORED')

    options = Options()
    options.add_argument('--headless')
    options.add_argument('--incognito')
    driver = webdriver.Chrome(options=options)

    login_narou(driver, email, password)

    for i, bookmark in enumerate(bookmarks):
        #ncode = 'n7951ei'  # No Rating
        #ncode = 'n6859du'  # is-half
        ncode = bookmark['ncode']

        if cache.get(ncode):
            print(datetime.datetime.now().isoformat(), i, ncode, ', Skip')
            continue

        rating = get_rating(driver, ncode)

        if rating is None:
            print(datetime.datetime.now().isoformat(), i, ncode, ', No Rating')
        else:
            print(datetime.datetime.now().isoformat(), i, ncode, ', Rating:', rating)
            bookmark['rating'] = rating
            append_to_csv(bookmark)

        if i < len(bookmarks) - 1:
            print(datetime.datetime.now().isoformat(), 'Sleep(3)')
            time.sleep(3)

    # Capture
    #file_path = os.path.join(ROOT_PATH, 'tmp', 'capture.png')
    #driver.save_screenshot(file_path)

