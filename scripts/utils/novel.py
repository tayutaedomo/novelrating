import os
import time
import datetime
import re
import csv
import copy
import json

from .mecab import chasen

ROOT_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..')
NOVELS_ROOT_PATH = os.path.join(ROOT_PATH, 'data', 'novels')
NOVELS_BAK_ROOT_PATH = os.path.join(ROOT_PATH, 'data', 'novels.bak')
BOOKMARK_CSV_PATH = os.path.join(ROOT_PATH, 'data', 'bookmark.csv')
BOOKMARK_RATING_CSV_PATH = os.path.join(ROOT_PATH, 'data', 'bookmark_rating.csv')
RANKING_CSV_PATH = os.path.join(ROOT_PATH, 'data', 'ranking.csv')


def login_narou(driver, email, password):
    url = 'https://ssl.syosetu.com/login/input/'
    print(datetime.datetime.now().isoformat(), 'GET:', url)

    driver.get(url)

    id_elem = driver.find_element_by_css_selector('input[name="narouid"]')
    id_elem.send_keys(email)

    pass_elem = driver.find_element_by_css_selector('input[name="pass"]')
    pass_elem.send_keys(password)

    driver.find_element_by_css_selector('#mainsubmit').click()


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


def load_ranking_csv():
    novels = []

    if not os.path.exists(RANKING_CSV_PATH):
        return novels

    with open(RANKING_CSV_PATH, 'r', encoding='utf-8') as f:
        for row in csv.reader(f):
            novels.append({
                'ncode': row[0],
                'ranking_path': row[1],
                'rank': row[2],
                'author': row[3],
                'updated_at': row[4],
                'pt': row[5],
                'page': row[6],
                'word': row[7],
                'category': row[8],
                'keywords': row[9],
                'title': row[10],
            })

    return novels


class NarouPageCrawler:
    def __init__(self, driver, dest_root_path, sleep=3):
        self.driver = driver
        self.dest_root_path = dest_root_path
        self.sleep = sleep

    def crawl(self, ncode, page_start, page_end):
        for page in range(page_start, page_end + 1):
            if self.is_txt_presents(ncode, page):
                print(datetime.datetime.now().isoformat(), ncode, page, 'Skip')
                continue

            novel = self.get_novel(ncode, page)

            if not novel['downloaded']:
                print(datetime.datetime.now().isoformat(), ncode, page, 'Failed')
            else:
                if self.write_novel_to_txt(ncode, page, novel):
                    print(datetime.datetime.now().isoformat(), ncode, page, 'New')

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

        self.create_ncode_dir(ncode)

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

    def create_dir_path(self, ncode):
        return os.path.join(self.dest_root_path, ncode)

    def create_txt_path(self, ncode, page):
        dir_path = self.create_dir_path(ncode)
        file_name = self.create_txt_name(ncode, page)
        return os.path.join(dir_path, file_name)

    def create_txt_name(self, ncode, page):
        return '{}_p{}.txt'.format(ncode, page)

    def create_ncode_dir(self, ncode):
        dir_path = self.create_dir_path(ncode)
        os.makedirs(dir_path, exist_ok=True)


class NarouRanking:
    def __init__(self, driver, limit=100):
        self.driver = driver
        self.limit = limit

    def get_list(self, ranking_path):
        novels = []

        base_url = 'https://yomou.syosetu.com/rank/{}'
        url = base_url.format(ranking_path)
        print(datetime.datetime.now().isoformat(), 'GET:', url)

        self.driver.get(url)

        ranking_elem_list = self.driver.find_elements_by_css_selector('div.ranking_list')

        for i, ranking_elem in enumerate(ranking_elem_list[:self.limit]):
            ranking = {
                'rank': i + 1,
                'ranking_path': ranking_path,
                'ncode': self.extract_ncode(ranking_elem),
                'title': self.extract_title(ranking_elem),
                'author': self.extract_author_id(ranking_elem),
                'pt': self.extract_point(ranking_elem),
                'page': self.extract_page(ranking_elem),
                'category': self.extract_category(ranking_elem),
                'keywords': self.extract_keywords(ranking_elem),
                'updated_at': self.extract_last_updated_at(ranking_elem),
                'word': self.extract_word_count(ranking_elem)
            }
            novels.append(ranking)

        return novels

    def extract_ncode(self, parent_elem):
        title_elem = parent_elem.find_element_by_css_selector('div.rank_h a')
        return self.extract_ncode_from_url(title_elem.get_attribute('href'))

    def extract_ncode_from_url(self, url):
        matched = re.match(r'^https:\/\/ncode\.syosetu\.com\/(.+)\/$', url)
        if matched:
            return matched.group(1)
        else:
            return ''

    def extract_title(self, parent_elem):
        title_elem = parent_elem.find_element_by_css_selector('div.rank_h a')
        return title_elem.text

    def extract_author_id(self, parent_elem):
        elem_list = parent_elem.find_elements_by_css_selector('td.h_info a')
        author_elem = elem_list[-1]
        return self.extract_author_id_from_url(author_elem.get_attribute('href'))

    def extract_author_id_from_url(self, url):
        matched = re.match(r'^https:\/\/mypage.syosetu.com\/(.+)\/$', url)
        if matched:
            return matched.group(1)
        else:
            return ''

    def extract_point(self, parent_elem):
        return parent_elem.find_element_by_css_selector('span.point').text

    def extract_page(self, parent_elem):
        td_elem = parent_elem.find_element_by_css_selector('td.left')
        point = self.extract_point(parent_elem)
        return td_elem.text.replace(point, '').replace('\n', '').strip()

    def extract_category(self, parent_elem):
        elem_list = parent_elem.find_elements_by_css_selector('tr')
        category_elem = elem_list[2]
        return category_elem.text

    def extract_keywords(self, parent_elem):
        keywords = []

        try:
            pass
            a_elem_list = parent_elem.find_elements_by_css_selector('td.keyword a')
            keywords = [elem.text for elem in a_elem_list]
        except Exception:
            pass

        return ' '.join(keywords)

    def extract_last_updated_at(self, parent_elem):
        elem_list = parent_elem.find_elements_by_css_selector('tr')
        last_elem = elem_list[-1]
        word_count = self.extract_word_count(parent_elem)
        return last_elem.text.replace(word_count, '').replace('最終更新日：', '').strip()

    def extract_word_count(self, parent_elem):
        elem_list = parent_elem.find_elements_by_css_selector('tr')
        last_elem = elem_list[-1]
        count_elem = last_elem.find_element_by_css_selector('span')
        return count_elem.text


class NovelPages:
    def __init__(self, page_count=30):
        self.page_count = page_count
        self.ncode = None
        self.pages = []

    def exist_json(self, ncode):
        json_path = self.create_json_path(ncode)
        return os.path.exists(json_path)

    def load(self, ncode):
        self.ncode = ncode

        for page_num in range(1, self.page_count+1):
            page = NovelPage()
            page.load(ncode, page_num)

            if page.loaded:
                self.pages.append(page)

    def get_summary(self):
        summary = {
            'count': 0,
            'sum': {
                'char_count': 0,
                'new_line_count': 0,
                'talk_char_count': 0,
                'word_count': 0,
                'word_class': {},
            },
            # 'avg': {},
        }

        for page in self.pages:
            summary['sum']['char_count'] += page.get_char_count()
            summary['sum']['new_line_count'] += page.get_new_line_count()
            summary['sum']['talk_char_count'] += page.get_talk_char_count()
            summary['sum']['word_count'] += page.get_word_count()

            word_classes = page.get_word_classes()
            self.add_word_class_to(word_classes, summary['sum']['word_class'])

        summary['count'] = len(self.pages)

        if summary['count'] > 0:
            summary['avg'] = copy.deepcopy(summary['sum'])

            summary['avg']['char_count'] /= summary['count']
            summary['avg']['new_line_count'] /= summary['count']
            summary['avg']['talk_char_count'] /= summary['count']
            summary['avg']['word_count'] /= summary['count']

            for key in summary['avg']['word_class'].keys():
                summary['avg']['word_class'][key] /= summary['count']

        return summary

    def add_word_class_to(self, src, dest):
        for key, value in src.items():
            if dest.get(key):
                dest[key] += value
            else:
                dest[key] = value

    def save(self):
        if not self.ncode:
            return None

        dest_path = self.create_json_path(self.ncode)

        with open(dest_path, 'w') as f:
            json.dump(self.get_summary(), f, indent=2, ensure_ascii=False)

        return dest_path

    def create_json_path(self, ncode):
        novel_dir_path = os.path.join(NOVELS_ROOT_PATH, ncode)
        file_name = '{}_summary.json'.format(ncode)
        return os.path.join(novel_dir_path, file_name)


class NovelPage:
    def __init__(self):
        self.ncode = None
        self.page_num = None
        self.loaded = False
        self.url = ''
        self.novel_title = ''
        self.page_title = ''
        self.page_body = ''

    def load(self, ncode, page_num):
        self.ncode = ncode
        self.page_num = page_num

        novel_dir_path = os.path.join(NOVELS_ROOT_PATH, self.ncode)
        page_file_name = '{}_p{}.txt'.format(self.ncode, 1)
        page_file_path = os.path.join(novel_dir_path, page_file_name)

        if not os.path.exists(page_file_path):
            return

        with open(page_file_path, 'r', encoding='utf-8') as f:
            self.url = f.readline().replace('\n', '')
            self.novel_title = f.readline().replace('\n', '')
            self.page_title = f.readline().replace('\n', '')
            self.page_body = f.read()

        self.loaded = True

    def get_char_count(self):
        return len(self.page_body)

    def get_new_line_count(self):
        return self.page_body.count(r'\n')

    def get_split_body_lines(self):
        lines = self.page_body.split('\\n')
        return [line for line in lines if line.strip() != '']

    def get_talk_lines(self):
        lines = []

        for line in self.get_split_body_lines():
            line = line.replace('『', '')
            line = line.replace('』', '')
            line = line.replace(r'\u3000', '')
            line = re.sub(r'\s', '', line)
            matched = re.match('(「)(.+?)(」)', line)
            if matched:
                lines.append(matched.groups()[1])

        return lines

    def get_talk_char_count(self):
        return len(''.join(self.get_talk_lines()))

    def get_normalized_body(self):
        body = re.sub(r'(\\n|\\u3000)', '', self.page_body)
        return body

    def get_body_chasen(self):
        return chasen(self.get_normalized_body())

    def get_word_count(self):
        parsed = self.get_body_chasen()
        return len(parsed)

    def get_chasen_word_classes(self):
        summary = {}

        parsed = self.get_body_chasen()
        for row in parsed.split('\n')[:-2]:  # Exclude EOS
            cols = row.split('\t')
            word_class = cols[3]

            if summary.get(word_class):
                summary[word_class] += 1
            else:
                summary[word_class] = 1

        return summary

    def get_word_classes(self):
        return self.get_chasen_word_classes()


class NovelInfo:
    def __init__(self):
        self.ncode = None
        self.raw = {'result': 0}

    def exist_json(self, ncode):
        json_path = self.create_json_path(ncode)
        return os.path.exists(json_path)

    def scrape(self, driver, ncode):
        self.ncode = ncode

        self.raw = {
            'result': 0,
            'ncode': ncode,
            'title': '',
            'overview': '',
            'author': '',
            'keywords': '',
            'category': '',
            'created_at': '',
            'updated_at': '',
            'comment_count': '',
            'review_count': '',
            'bookmark_count': '',
            'rating_total': '',
            'rating': '',
            'report': '',
            'public': '',
            'word_count': '',
            'time': '',
        }

        if not ncode:
            return self.raw

        url = 'https://ncode.syosetu.com/novelview/infotop/ncode/{}/'.format(ncode)
        print(datetime.datetime.now().isoformat(), 'GET:', url)

        driver.get(url)

        try:
            h1_elem = driver.find_element_by_css_selector('h1')
            self.raw['title'] = h1_elem.text

            td_list = driver.find_elements_by_css_selector('table#noveltable1 td')

            if td_list:
                self.raw['overview'] = self.strip_text(td_list[0])
                self.raw['author'] = self.extract_author_id(td_list[1])
                self.raw['keywords'] = self.strip_text(td_list[2])
                self.raw['category'] = self.strip_text(td_list[3])

            td_list = driver.find_elements_by_css_selector('table#noveltable2 td')

            if td_list:
                self.raw['created_at'] = self.strip_text(td_list[0])
                self.raw['updated_at'] = self.strip_text(td_list[1])
                self.raw['comment_count'] = self.strip_text(td_list[2])
                self.raw['review_count'] = self.strip_text(td_list[3])
                self.raw['bookmark_count'] = self.strip_text(td_list[4])
                self.raw['rating_total'] = self.strip_text(td_list[5])
                self.raw['rating'] = self.strip_text(td_list[6])
                self.raw['report'] = self.strip_text(td_list[7])
                self.raw['public'] = self.strip_text(td_list[8])
                self.raw['word_count'] = self.strip_text(td_list[9])
                self.raw['time'] = datetime.datetime.now().isoformat()

                self.raw['result'] = 1    # Completed all successfully

        except Exception as e:
            print(datetime.datetime.now().isoformat(), e)

        return self.raw

    def strip_text(self, elem):
        if not elem:
            return None

        if not elem.text:
            return None

        text = elem.text.replace('\n', ',').replace('\r\n', ',')
        text.lstrip().rstrip()
        return text

    def extract_author_id(self, parent_elem):
        try:
            author_elem = parent_elem.find_element_by_css_selector('a')
            return self.extract_author_id_from_url(author_elem.get_attribute('href'))
        except Exception:
            return parent_elem.text

    def extract_author_id_from_url(self, url):
        matched = re.match(r'^https:\/\/mypage.syosetu.com\/(.+)\/$', url)
        if matched:
            return matched.group(1)
        else:
            return ''

    def save(self):
        if not self.ncode or self.raw['result'] != 1:
            return None

        dest_path = self.create_json_path(self.ncode)

        self.create_ncode_directory(self.ncode)

        with open(dest_path, 'w') as f:
            json.dump(self.raw, f, indent=2, ensure_ascii=False)

        return dest_path

    def create_json_path(self, ncode):
        dir_path = self.create_dir_path(ncode)
        file_name = '{}_info.json'.format(ncode)
        return os.path.join(dir_path, file_name)

    def create_ncode_directory(self, ncode):
        dir_path = self.create_dir_path(ncode)
        os.makedirs(dir_path, exist_ok=True)

    def create_dir_path(self, ncode):
        return os.path.join(NOVELS_ROOT_PATH, ncode)

