import os
import sys
import datetime
import time
import chromedriver_binary
from selenium import webdriver
from selenium.webdriver.chrome.options import Options

ROOT_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..')
DEST_ROOT_PATH = os.path.join(ROOT_PATH, 'data', 'narou')


def get_novel(driver, ncode, page):
    url = 'https://ncode.syosetu.com/{}/{}/'.format(ncode, page)
    print(datetime.datetime.now().isoformat(), 'GET:', url)

    novel = {
        'url': url,
        'title': '',
        'subtitle': '',
        'body': '',
        'downloaded': False,
    }

    driver.get(url)

    now_str = datetime.datetime.now().isoformat()

    try:
        title_elem = driver.find_element_by_css_selector('div.contents1 a')
        novel['title'] = title_elem.text

        subtitle_elem = driver.find_element_by_class_name('novel_subtitle')
        novel['subtitle'] = subtitle_elem.text

        body_elem = driver.find_element_by_css_selector('div#novel_honbun')
        novel['body'] = body_elem.text

        novel['time'] = now_str
        novel['downloaded'] = True

    except Exception as e:
        print(datetime.datetime.now().isoformat(), e, novel['url'])

    return novel


def write_novel_to_txt(ncode, page, novel):
    file_name = '{}-p{}.txt'.format(ncode, page)
    dest_path = os.path.join(DEST_ROOT_PATH, file_name)

    if os.path.exists(dest_path):
        print(datetime.datetime.now().isoformat(), 'Skip:', ncode, page)
        return False

    lines = [
        novel['url'],
        repr(novel['title']),
        repr(novel['subtitle']),
        repr(novel['body']),
    ]

    with open(dest_path, 'w') as f:
        f.write('\n'.join(lines))

    return True


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

    for page in range(page_start, page_end + 1):
        novel = get_novel(driver, ncode, page)

        if not novel['downloaded']:
            print(datetime.datetime.now().isoformat(), 'Failed:', ncode, page)
        else:
            if write_novel_to_txt(ncode, page, novel):
                print(datetime.datetime.now().isoformat(), 'New:', ncode, page)

        if page < page_end:
            print(datetime.datetime.now().isoformat(), 'Sleep(3)')
            time.sleep(3)

    # Capture
    #file_path = os.path.join(ROOT_PATH, 'tmp', 'capture.png')
    #driver.save_screenshot(file_path)

