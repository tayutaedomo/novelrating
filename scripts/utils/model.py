import os
import datetime
import csv

from .novel import load_bookmark_rating_csv, load_ranking_csv
from .novel import NovelInfo, NovelPages

ROOT_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..')


class DataMaker:
    def __init__(self):
        self.ncode_list = []
        self.inputs_list = []
        self.unique_keywords = UniqueCounter()
        self.rows = []

    def load(self, ncode_list):
        self.ncode_list = ncode_list

        self._create_novel_inputs()
        self._create_unique_keywords()

    def _create_novel_inputs(self):
        self.inputs_list = []

        for i, ncode in enumerate(self.ncode_list):
            novel_info = NovelInfo()
            novel_info.load(ncode)

            novel_pages = NovelPages()
            novel_pages.load_summary(ncode)

            if novel_info.info['result'] == 1 and novel_pages.summary['result'] == 1:
                self.inputs_list.append({
                    'novel_info': novel_info,
                    'novel_pages': novel_pages
                })

            else:
                print(datetime.datetime.now().isoformat(), i, ncode, 'Skipped in Maker.load')

    def _create_unique_keywords(self):
        self.unique_keywords = UniqueCounter(50)

        for inputs in self.inputs_list:
            novel_info = inputs['novel_info']
            for keyword in self._extract_keywors(novel_info):
                self.unique_keywords.set(keyword, 1)

        return self.unique_keywords.get_unique_keys()

    def _extract_keywors(self, novel_info):
        keyword_list = []

        for keyword in novel_info.info['keywords'].split(' '):
            keyword = keyword.strip()
            if keyword != '':
                keyword_list.append(keyword)

        return keyword_list

    def make(self):
        for i, inputs in enumerate(self.inputs_list):
            row = {}

            novel_info = inputs['novel_info']
            novel_pages = inputs['novel_pages']
            ncode = novel_info.info['ncode']

            print(datetime.datetime.now().isoformat(), i, ncode, 'in Maker.make')

            row['ncode'] = novel_info.info['ncode']
            row['title'] = novel_info.info['title']
            row['category'] = novel_info.info['category']
            row['bookmark_cat'] = self._get_bookmark_category(ncode)
            row['created_at'] = self._exchange_to_datetime(
                novel_info.info['created_at']).timestamp()
            row['updated_at'] = self._exchange_to_datetime(
                novel_info.info['updated_at']).timestamp()

            self._extend_summary_data(novel_pages.summary['sum'], row, 'sum')

            avg_data = novel_pages.create_average(novel_pages.summary)
            self._extend_summary_data(avg_data, row, 'avg')

            for keyword in self.unique_keywords.get_unique_keys():
                key = self._create_keyword_column_name(keyword)
                row[key] = 0

            for keyword in self._extract_keywors(novel_info):
                key = self._create_keyword_column_name(keyword)
                if key in row:
                    row[key] = 1

            word_class_summary = WordClassSummary(
                novel_pages.summary['sum']['word_classes'])

            for key, value in word_class_summary.get_sum_items():
                row[key] = value

            for key, value in word_class_summary.get_rate_items():
                row[key] = value

            row['rating'] = self._get_rating(ncode)

            self.rows.append(row)

        return self.rows

    def _exchange_to_datetime(self, str_date):
        return datetime.datetime.strptime(str_date, '%Y年 %m月%d日 %H時%M分')

    def _extend_summary_data(self, src, dest, prefix):
        keys = [
            'char_count',
            'new_line_count',
            'talk_char_count',
            'word_count',
        ]

        for key in keys:
            new_key = '{}_{}'.format(prefix, key)
            dest[new_key] = src[key]

        return dest

    def _create_keyword_column_name(self, keyword):
        return 'kw_' + keyword

    def _get_bookmark_category(self, ncode):
        return -1  # Return dummy data

    def _get_rating(self, ncode):
        return -1  # Return dummy data

    def save(self):
        dest_path = self._create_dest_path()

        if len(self.rows) == 0:
            return None

        with open(dest_path, 'w') as f:
            writer = csv.DictWriter(f, fieldnames=self.rows[0].keys(), delimiter=",",
                                    quotechar='"', quoting=csv.QUOTE_ALL)
            writer.writeheader()
            writer.writerows(self.rows)

        return dest_path

    def _create_dest_path(self):
        dir_path = self._create_dir_path()
        file_name = self._create_file_name()
        return os.path.join(dir_path, file_name)

    def _create_dir_path(self):
        return os.path.join(ROOT_PATH, 'data')

    def _create_file_name(self):
        return 'data.csv'


class BookmarkDataMaker(DataMaker):
    def __init__(self):
        super(BookmarkDataMaker, self).__init__()

        self.bookmarks = {}
        self.rating_gradient = {
            '1': 1.0,
            '2': 1.5,
            '3': 0.5,
            '4': 1.0,
        }

    def load(self, ncode_list):
        self.bookmarks = load_bookmark_rating_csv()
        filtered_list = [ncode for ncode in ncode_list
                         if int(self._get_bookmark_category(ncode)) < 4]
        super(BookmarkDataMaker, self).load(filtered_list)

    def _get_bookmark_category(self, ncode):
        bookmark = [bookmark for bookmark in self.bookmarks if bookmark['ncode'] == ncode][0]
        if bookmark:
            return bookmark['category']
        else:
            return -1

    def _get_rating(self, ncode):
        bookmark = [bookmark for bookmark in self.bookmarks if bookmark['ncode'] == ncode][0]

        if bookmark:
            rating = (float)(bookmark['rating'])
            gradient = (float)(self.rating_gradient.get(bookmark['category'], 0.0))
            return rating * gradient
        else:
            return 0.0

    def _create_file_name(self):
        return 'bookmark_train_data.csv'


class RankingDataMaker(DataMaker):
    def __init__(self):
        super(RankingDataMaker, self).__init__()

    def load(self, ncode_list):
        filtered_list = self._filter_ncode_list(ncode_list)
        super(RankingDataMaker, self).load(filtered_list)

    def _filter_ncode_list(self, ncode_list):
        bookmark_ncode_list = self._get_bookmark_ncode_list()
        return [ncode for ncode in ncode_list if ncode not in bookmark_ncode_list]

    def _get_bookmark_ncode_list(self):
        return [bookmark['ncode'] for bookmark in load_bookmark_rating_csv()]

    def _create_file_name(self):
        return 'ranking_test_data.csv'


class UniqueCounter:
    def __init__(self, limit=100):
        self.data = {}
        self.limit = limit

    def set(self, key, count):
        if not self.data.get(key):
            self.data[key] = 0

        self.data[key] += count

    def get_unique_keys(self):
        sorted_list = self.get_sorted_items()

        if self.limit > 0:
            sorted_list = sorted_list[:self.limit]

        keys = [items[0] for items in sorted_list]

        return list(set(keys))

    def get_sorted_items(self, debug=False):
        if debug:
            return sorted(self.data.items())
        else:
            return sorted(self.data.items(), key=lambda x: x[1], reverse=True)


class WordClassSummary:
    WORD_CLASSES = [
        'その他',
        'フィラー',
        '副詞',
        '助動詞',
        '助詞',
        '動詞',
        '名詞',
        '形容詞',
        '感動詞',
        '接続詞',
        '接頭詞',
        '記号',
        '連体詞',
    ]

    def __init__(self, word_classes):
        self.input_wc = word_classes

        self.summary = dict(zip(WordClassSummary.WORD_CLASSES,
                                [0] * len(WordClassSummary.WORD_CLASSES)))

        for key, value in word_classes.items():
            for word_class in WordClassSummary.WORD_CLASSES:
                if key.find(word_class) != -1:
                    self.summary[word_class] += value

        self.total = sum(self.summary.values())

    def get_sum_items(self):
        for key, value in self.summary.items():
            key = self._create_column_name(key, 'sum')
            yield key, value

    def get_rate_items(self):
        for key, value in self.summary.items():
            key = self._create_column_name(key, 'rate')

            if self.total > 0:
                value = value / self.total

            yield key, value

    def _create_column_name(self, word_class, prefix):
        return 'wc_{}_{}'.format(prefix, word_class)

