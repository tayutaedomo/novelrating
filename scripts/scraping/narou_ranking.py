import os
import sys
import time
import datetime
import csv
import chromedriver_binary
from selenium import webdriver
from selenium.webdriver.chrome.options import Options

ROOT_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..')
DEST_ROOT_PATH = os.path.join(ROOT_PATH, 'data', 'ranking.csv')

sys.path.append(ROOT_PATH)

from scripts.utils.novel import NarouRanking


def create_cache():
    cache = {}

    if not os.path.exists(DEST_ROOT_PATH):
        return cache

    with open(DEST_ROOT_PATH, 'r', encoding='utf-8') as f:
        for row in csv.reader(f):
            cache[create_cache_id(row[0], row[1])] = True  # { cache_id: True, ... }

    return cache


def create_cache_id(ncode, ranking_path):
    return '{}_{}'.format(ncode, ranking_path)


def append_to_csv(novel):
    csv_line = '"{}","{}","{}","{}","{}","{}","{}","{}","{}","{}","{}"'.format(
        novel.get('ncode'),
        novel.get('ranking_path'),
        novel.get('rank'),
        novel.get('author'),
        novel.get('updated_at'),
        novel.get('pt'),
        novel.get('page'),
        novel.get('word'),
        novel.get('category'),
        novel.get('keywords'),
        novel.get('title'),
    )

    with open(DEST_ROOT_PATH, 'a') as f:
        f.write(csv_line + '\n')


if __name__ == '__main__':
    cache = create_cache()
    print(datetime.datetime.now().isoformat(), 'Cache Count:', len(cache))

    options = Options()
    options.add_argument('--headless')
    options.add_argument('--incognito')
    driver = webdriver.Chrome(options=options)

    ranking_paths = [
        'genrelist/type/weekly_101',
        'genrelist/type/monthly_101',
        'genrelist/type/weekly_102',
        'genrelist/type/weekly_201',
        'genrelist/type/weekly_202',
        'genrelist/type/weekly_301',
        'genrelist/type/weekly_401',
        'list/type/weekly_total',
        'list/type/monthly_total',
        'isekailist/type/weekly_1',
        'isekailist/type/weekly_2',
        'isekailist/type/weekly_o',
        'isekailist/type/monthly_1',
        'isekailist/type/monthly_2',
        'isekailist/type/monthly_o',
        'isekailist/type/quarter_1',
    ]

    for i, ranking_path in enumerate(ranking_paths):
        ranking = NarouRanking(driver)
        novels = ranking.get_list(ranking_path)

        for novel in novels:
            ncode = novel['ncode']
            cache_id = create_cache_id(ncode, ranking_path)

            if cache.get(cache_id):
                print(datetime.datetime.now().isoformat(), i, ncode, ranking_path, 'Skip')
                continue

            print(datetime.datetime.now().isoformat(), i, ncode, ranking_path, 'New')
            append_to_csv(novel)
            cache[cache_id] = True

        if i < len(ranking_paths) - 1:
            print(datetime.datetime.now().isoformat(), 'Sleep(3)')
            time.sleep(3)

    # Capture
    #file_path = os.path.join(ROOT_PATH, 'tmp', 'capture.png')
    #driver.save_screenshot(file_path)

