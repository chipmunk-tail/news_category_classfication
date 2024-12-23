# 241223 intel AISW Academy
#
# 검증 자료를 만들어서 모델 정확도 검증


import pandas as pd
import numpy as np
import pickle
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder
from keras.utils import to_categorical
from konlpy.tag import Okt
from tensorflow.keras.preprocessing.text import Tokenizer
from tensorflow.keras.preprocessing.sequence import pad_sequences
from keras.models import load_model

from bs4 import BeautifulSoup
import requests
import re
import datetime


# make predict data
# category = ['Politics', 'Economic', 'Social', 'Culture', 'World', 'IT']
#
#
# # Get headlines
# for i in range(6):                                              # Sub_domain : 100 ~ 105
#     url = 'https://news.naver.com/section/10{}'. format(i)      # OR '/10%d' %i
#     resp = requests.get(url)                                    # url request == HTML
#     soup = BeautifulSoup(resp.text, 'html.parser')              # Using bs4 for HTML parsing
#     title_tags = soup.select('.sa_text_strong')                 # '.sa_text_strong' == news headline class def name
#     titles = []                                                 # Create empty list for save headline
#
#     for title_tag in title_tags:                                # all headlines
#         title = title_tag.text                                  # Crawling headlines
#         title = re.compile('[^가-힣 ]').sub(' ', title)            # Repalce all to 'null' execpt "가 ~ 힣" && " "
#         titles.append(title)
#
#     df_section_titles = pd.DataFrame(titles, columns = ['titles'])  # Create columns 'titles'
#     df_section_titles['category'] = category[i]
#     df_titles = pd.concat([df_titles, df_section_titles], axis = 'rows', ignore_index = True)
#
# print(df_titles.head())
# df_titles.info()
# print(df_titles['category'].value_counts())
# df_titles.to_csv('./crawling_data_predict/naver_headline_news_{}.csv'.format(
#     datetime.datetime.now().strftime('%Y%m%d')), index = False) # Change time format to 'YYYYMMDD'
#                                                                 # index = False == 0, 1, 2 default index = False






# open CSV
df = pd.read_csv('crawling_data_predict/naver_headline_news_20241223.csv')
df.drop_duplicates(inplace = True)                          # Remove duplicate
df.reset_index(drop = True, inplace = True)                 # Drop default index
print(df.head())
df.info()
print(df.category.value_counts())


# Makes Dataframe
X = df['titles']
Y = df['category']

with open('format_files/encoder.pickle', 'rb') as f:            # rb = read binary
    encoder = pickle.load(f)


label = encoder.classes_
print(label)


# onehot encode
labeled_y = encoder.transform(Y)
onehot_Y = to_categorical(labeled_y)
print(onehot_Y)



# X : morpheme separation
okt = Okt()
for i in range(len(X)):
    X[i] = okt.morphs(X[i], stem = True)
print(X)


# open korean stopword
stopwords = pd.read_csv('format_files/stopwords.csv', index_col = 0)
print(stopwords)


# replace stopword to ' '
for sentence in range(len(X)):
    words = []
    for word in range(len(X[sentence])):
        if len(X[sentence][word]) > 1:              # drop useless word
            if X[sentence][word] not in list(stopwords['stopword']):
                words.append(X[sentence][word])
    X[sentence] = ' '.join(words)
print(X[:5])


# new token not in model = 0

with open('format_files/news_token_max_16.pickle', 'rb') as f:
    token = pickle.load(f)

tokened_X = token.texts_to_sequences(X)
print(tokened_X[:5])


# if token over 16
for i in range(len(tokened_X)):
    if len(tokened_X[i]) > 16:
        tokened_X[i] = tokened_X[i][:16]
X_pad = pad_sequences(tokened_X, 16)


print(X_pad[:5])




model = load_model('./models/news_category_classification_model_0.6238532066345215.h5')
preds = model.predict(X_pad)

predicts = []
for pred in preds:
    most = label[np.argmax(pred)]
    pred[np.argmax(pred)] = 0
    second = label[np.argmax(pred)]
    predicts.append([most, second])


df['predict'] = predicts

print(df.head(30))


score = model.evaluate(X_pad, onehot_Y)
print(score[1])

df['OX'] = 0
for i in range(len(df)):
    if df.loc[i, 'category'] == df.loc[i, 'predict']:
        df.loc[i, 'OX'] = 1

print(df.OX.mean())
























