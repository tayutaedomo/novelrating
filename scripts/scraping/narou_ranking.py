import os
import sys
import time
import datetime
import chromedriver_binary
from selenium import webdriver
from selenium.webdriver.chrome.options import Options

ROOT_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..')
DEST_ROOT_PATH = os.path.join(ROOT_PATH, 'data', 'narou')

sys.path.append(ROOT_PATH)

from scripts.utils.novel import NarouRanking


def get_ranking_list(driver):
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

    all_list = []

    for i, ranking_path in enumerate(ranking_paths):
        ranking = NarouRanking(driver, limit=1)
        ranking_list = ranking.get_list(ranking_path)
        all_list.extend(ranking_list)

        import pprint as pp
        pp.pprint(ranking_list)

        if i < len(ranking_paths) - 1:
            print(datetime.datetime.now().isoformat(), 'Sleep(3)')
            time.sleep(3)

    return all_list


if __name__ == '__main__':
    options = Options()
    options.add_argument('--headless')
    options.add_argument('--incognito')
    driver = webdriver.Chrome(options=options)

    ranking_list = get_ranking_list(driver)

    # Capture
    #file_path = os.path.join(ROOT_PATH, 'tmp', 'capture.png')
    #driver.save_screenshot(file_path)

