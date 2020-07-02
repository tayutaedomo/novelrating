import os
import datetime

from .novel import NovelInfo, NovelPages

ROOT_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..')


class BookmarkDataMaker:
    def __init__(self):
        self.ncode_list = []
        self.inputs_list = []
        self.unique_keywords = []
        self.unique_word_classes = []
        self.rows = []

    def load(self, ncode_list):
        self.ncode_list = ncode_list

        for i, ncode in enumerate(self.ncode_list):
            novel_info = NovelInfo()
            novel_info.load(ncode)

            novel_pages = NovelPages()
            novel_pages.load_summary(ncode)

            self.inputs_list.append({
                'novel_info': novel_info,
                'novel_pages': novel_pages
            })

    def make(self):
        self.create_unique_keywords()

        self.create_unique_word_classes()

        for inputs in self.inputs_list:
            row = {}

            novel_info = inputs['novel_info']
            novel_pages = inputs['novel_pages']

            row['title'] = novel_info.info['title']
            row['category'] = novel_info.info['category']
            row['created_at'] = self.exchange_to_datetime(novel_info.info['created_at']).timestamp()
            row['updated_at'] = self.exchange_to_datetime(novel_info.info['updated_at']).timestamp()

            for keyword in self.unique_keywords:
                row[keyword] = 0

            for keyword in self.extract_keywors(novel_info):
                row[keyword] = 1

            for word_class in self.unique_word_classes:
                row[word_class] = 0

            sum_word_classes = novel_pages.summary['sum']['word_class']
            for word_class in sum_word_classes.keys():
                row[word_class] += sum_word_classes[word_class]

            self.rows.append(row)

        return self.rows

    def create_unique_keywords(self):
        keywords = []

        for inputs in self.inputs_list:
            novel_info = inputs['novel_info']
            keywords.extend(self.extract_keywors(novel_info))

        self.unique_keywords = list(set(keywords))

        return self.unique_keywords

    def extract_keywors(self, novel_info):
        keyword_list = []

        for keyword in novel_info.info['keywords'].split(' '):
            keyword = keyword.strip()
            if keyword != '':
                keyword_list.append(keyword)

        return keyword_list

    def create_unique_word_classes(self):
        word_classes = []

        for inputs in self.inputs_list:
            novel_pages = inputs['novel_pages']
            sum_word_classes = novel_pages.summary['sum']['word_class']
            word_classes.extend(sum_word_classes.keys())

        self.unique_word_classes = list(set(word_classes))

        return self.unique_word_classes

    def exchange_to_datetime(self, str_date):
        return datetime.datetime.strptime(str_date, '%Y年 %m月%d日 %H時%M分')

    def save(self):
        dest_path = self.create_dest_path()

        with open(dest_path, 'w') as f:
            # TODO
            pass

        return dest_path

    def create_dest_path(self):
        dir_path = self.create_dir_path()
        file_name = self.create_file_name()
        return os.path.join(dir_path, file_name)

    def create_dir_path(self):
        return os.path.join(ROOT_PATH, 'data')

    def create_file_name(self):
        return 'train_bookmark.csv'

