import os
import time
import datetime


def login_narou(driver, email, password):
    url = 'https://ssl.syosetu.com/login/input/'
    print(datetime.datetime.now().isoformat(), 'GET:', url)

    driver.get(url)

    id_elem = driver.find_element_by_css_selector('input[name="narouid"]')
    id_elem.send_keys(email)

    pass_elem = driver.find_element_by_css_selector('input[name="pass"]')
    pass_elem.send_keys(password)

    driver.find_element_by_css_selector('#mainsubmit').click()


class NarouPageCrawler:
    def __init__(self, driver, dest_root_path, sleep=3):
        self.driver = driver
        self.dest_root_path = dest_root_path
        self.sleep = sleep

    def crawl(self, ncode, page_start, page_end):
        for page in range(page_start, page_end + 1):
            if self.is_txt_presents(ncode, page):
                print(datetime.datetime.now().isoformat(), 'Skip:', ncode, page)
                continue

            novel = self.get_novel(ncode, page)

            if not novel['downloaded']:
                print(datetime.datetime.now().isoformat(), 'Failed:', ncode, page)
            else:
                if self.write_novel_to_txt(ncode, page, novel):
                    print(datetime.datetime.now().isoformat(), 'New:', ncode, page)

            if page < page_end:
                print(datetime.datetime.now().isoformat(), 'Sleep({})'.format(self.sleep))
                time.sleep(self.sleep)

    def get_novel(self, ncode, page):
        url = 'https://ncode.syosetu.com/{}/{}/'.format(ncode, page)
        print(datetime.datetime.now().isoformat(), 'GET:', url)

        novel = {
            'url': url,
            'title': '',
            'subtitle': '',
            'body': '',
            'downloaded': False,
        }

        self.driver.get(url)

        now_str = datetime.datetime.now().isoformat()

        try:
            title_elem = self.driver.find_element_by_css_selector('div.contents1 a')
            novel['title'] = title_elem.text

            subtitle_elem = self.driver.find_element_by_class_name('novel_subtitle')
            novel['subtitle'] = subtitle_elem.text

            body_elem = self.driver.find_element_by_css_selector('div#novel_honbun')
            novel['body'] = body_elem.text

            novel['time'] = now_str
            novel['downloaded'] = True

        except Exception as e:
            print(datetime.datetime.now().isoformat(), e, novel['url'])

        return novel

    def write_novel_to_txt(self, ncode, page, novel):
        # if self.is_txt_presents(ncode, page):
        #     print(datetime.datetime.now().isoformat(), 'Skip:', ncode, page)
        #     return False

        lines = [
            novel['url'],
            repr(novel['title']),
            repr(novel['subtitle']),
            repr(novel['body']),
        ]

        dest_path = self.create_txt_path(ncode, page)

        with open(dest_path, 'w') as f:
            f.write('\n'.join(lines))

        return True

    def is_txt_presents(self, ncode, page):
        dest_path = self.create_txt_path(ncode, page)
        return os.path.exists(dest_path)

    def create_txt_path(self, ncode, page):
        file_name = self.create_txt_name(ncode, page)
        return os.path.join(self.dest_root_path, file_name)

    def create_txt_name(self, ncode, page):
        return '{}-p{}.txt'.format(ncode, page)

