import MeCab


def wakati(text):
    #mecab = MeCab.Tagger('-Owakati')
    mecab = MeCab.Tagger('-Owakati -d /usr/local/Cellar/mecab/0.996/lib/mecab/dic/mecab-ipadic-neologd')
    return mecab.parse(text)


def chasen(text):
    #mecab = MeCab.Tagger('-Ochasen')
    mecab = MeCab.Tagger('-Ochasen -d /usr/local/Cellar/mecab/0.996/lib/mecab/dic/mecab-ipadic-neologd')
    return mecab.parse(text)

