import numpy as np
import pandas as pd
#import matplotlib.pyplot as plt
import sys
import os
import xgboost as xgb
import pickle
from sklearn.preprocessing import LabelEncoder


DATA_DIR_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..', 'data')


def data_preprocess(df):
    cat_le = LabelEncoder()
    cat_le.fit(df['category'])

    WORD_CLASSE_LABELS = ['その他', 'フィラー', '副詞', '助動詞', '助詞',
                          '動詞', '名詞', '形容詞', '感動詞', '接続詞',
                          '接頭詞', '記号', '連体詞', ]
    new_wc_columns = {}
    for (i, name) in enumerate(WORD_CLASSE_LABELS):
        new_wc_columns['wc_sum_{}'.format(name)] = 'wc_sum_{}'.format(i)
        new_wc_columns['wc_rate_{}'.format(name)] = 'wc_rate_{}'.format(i)

    new_df = df.drop(['ncode', 'title', 'bookmark_cat'], axis=1)

    new_df['category'] = cat_le.transform(new_df['category'])

    new_df['rating'] = new_df['rating'] * 10
    new_df = new_df.astype({'rating': 'int32'})

    #wc_columns = [col for col in new_df.columns if col.find('wc_') != -1]
    #new_df = new_df.drop(wc_columns, axis=1)
    wc_columns = [col for col in new_df.columns if col.find('wc_sum_') != -1]
    new_df = new_df.drop(wc_columns, axis=1)
    new_df = new_df.rename(columns=new_wc_columns)

    kw_columns = [col for col in new_df.columns if col.find('kw_') != -1]
    new_df = new_df.drop(kw_columns, axis=1)

    return new_df


def load_model():
    dump_path = os.path.join(DATA_DIR_PATH, 'xgb_model.pickle')
    loaded_bst = pickle.load(open(dump_path, 'rb'))
    return loaded_bst


def load_data(file_path):
    return pd.read_csv(file_path, header=0)


if __name__ == '__main__':
    if len(sys.argv) <= 1:
        print('Data path is required.')
        exit(1)

    data_path = sys.argv[1]

    bst = load_model()

    df_test = load_data(data_path)
    df_test2 = data_preprocess(df_test)

    X = df_test2.drop(['rating'], axis=1).values
    y = df_test2['rating'].values
    feature_names = df_test2.keys()[:-1]

    dtest = xgb.DMatrix(X, label=y, feature_names=feature_names)
    y_pred = bst.predict(dtest)

    #df_rating = pd.DataFrame(columns=['ncode', 'title', 'rating'])

    for i, y in enumerate(y_pred):
        row = df_test.loc[i]
        print('{}\t{}\t{}\t{}'.format(i, row.ncode, row.title, y))
        #df_rating = df_rating.append({'ncode': row.ncode, 'title': row.title, 'rating': y}, ignore_index=True)

