# 241220 intel AISW Academy
#
# preprocessing data
# use java and konlpy

import pandas as pd
import numpy as np
import pickle
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder
from keras.utils import to_categorical
from konlpy.tag import Okt                                  # Open korea tokenizer / need install Java jdk21
from tensorflow.keras.preprocessing.text import Tokenizer
from tensorflow.keras.preprocessing.sequence import pad_sequences


# open CSV
df = pd.read_csv('./crawling_data/naver_headline_news_result_20241220.csv')
df.drop_duplicates(inplace = True)                          # Remove duplicate
df.reset_index(drop = True, inplace = True)                 # Drop default index
print(df.head())
df.info()
print(df.category.value_counts())


# Makes Dataframe
X = df['titles']
Y = df['category']
print(X[0])


# Y : labeling
encoder = LabelEncoder()
labeled_y = encoder.fit_transform(Y)                        # fit_transform = only use first time transform
print(labeled_y[:3])

label = encoder.classes_
print(label)


# save encoder
with open('./models/encoder.pickle', 'wb') as f:            # wb = write binary
    pickle.dump(encoder, f)


# onehot encode
onehot_Y = to_categorical(labeled_y)
print(onehot_Y)



# X : morpheme separation
okt = Okt()
for i in range(len(X)):
    X[i] = okt.morphs(X[i], stem = True)
print(X)


# open korean stopword
stopwords = pd.read_csv('./crawling_data/stopwords.csv', index_col = 0)
print(stopwords)


# replace stopword to ' '
for sentence in range(len(X)):
    words = []
    for word in range(len(X[sentence])):
        if len(X[sentence][word]) > 1:
            if X[sentence][word] not in list(stopwords['stopword']):
                words.append(X[sentence][word])
    X[sentence] = ' '.join(words)
print(X[:5])



token = Tokenizer()
token.fit_on_texts(X)
tokened_X = token.texts_to_sequences(X)
wordsize = len(token.word_index) + 1                # max length + ' '

print(wordsize)
print(tokened_X[:5])


# find max length
max = 0
for i in range(len(tokened_X)):
    if max < len(tokened_X[i]):
        max = len(tokened_X[i])
print(max)

X_pad = pad_sequences(tokened_X, max)               # keras package, padding == fill '0'
print(X_pad)
print(len(X_pad[0]))


X_train, X_test, Y_train, Y_test = train_test_split(X_pad, onehot_Y, test_size = 0.1)
print(X_train.shape, Y_train.shape)
print(X_test.shape, Y_test.shape)

np.save('./crawling_data/news_data_X_train_max_{}_wordsize_{}'.format(max, wordsize), X_train)      # .npy
np.save('./crawling_data/news_data_X_test_max_{}_wordsize_{}'.format(max, wordsize), X_test)
np.save('./crawling_data/news_data_Y_train_max_{}_wordsize_{}'.format(max, wordsize), Y_train)
np.save('./crawling_data/news_data_Y_test_max_{}_wordsize_{}'.format(max, wordsize), Y_test)





















# from konlpy.tag import Kkma


# okt = Okt()
# okt_x = okt.morphs(X[0], stem = True)
# print('Okt :', okt_x)
# kkma = Kkma()
# kkma_x = kkma.morphs(X[0])
# print('kkma', kkma_x)








