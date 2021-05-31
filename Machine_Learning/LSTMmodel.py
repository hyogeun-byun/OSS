import csv
from konlpy.tag import Okt
import json
import os
from pprint import pprint
import nltk
import matplotlib.pyplot as plt
from matplotlib import font_manager,rc
import numpy as np
from matplotlib import pyplot as plt
from sklearn.model_selection import train_test_split
import seaborn as sns
import pandas as pd



train = pd.read_csv('train.csv', names=['comments', 'score'])
#train = train['comments']
train_label,test_label,train_data,test_data= train_test_split(train['comments'], train['score'], test_size=0.25, random_state=42)

train_data = list(train_data)
train_label = list(train_label)
test_data = list(test_data)
test_label = list(test_label)


#print(train_data)
#print(train_label)
#print(test_data)
#print(test_label)

okt = Okt()
stopwords = ['의', '가', '이', '은', '들', '는', '좀', '잘', '걍', '과', '도', '를', '으로', '자', '에', '와', '한', '하다']

train_pos = []
test_pos = []

train_index = []
test_index = []
for i in range(len(train_data)):
    temp_X = []
    try:
        temp_X = okt.morphs(train_data[i],norm=True,stem=True)  # 토큰화
        temp_X = [word for word in temp_X if not word in stopwords]  # 불용어 제거
        train_pos.append(temp_X)
    except:
        train_index.append(i)

for i in reversed(range(len(train_index))):
    del train_label[train_index[i]]

for i in range(len(test_data)):
    temp_X = []
    try:
        temp_X = okt.morphs(test_data[i],norm=True,stem=True)  # 토큰화
        temp_X = [word for word in temp_X if not word in stopwords]  # 불용어 제거
        test_pos.append(temp_X)
    except:
        test_index.append(i)

for i in reversed(range(len(test_index))):
    del test_label[test_index[i]]


##########
from keras.preprocessing.text import Tokenizer
max_words = 35000
tokenizer = Tokenizer(num_words = max_words)
tokenizer.fit_on_texts(test_pos)
X_train = tokenizer.texts_to_sequences(train_pos)
X_test = tokenizer.texts_to_sequences(test_pos)


##########
import numpy as np
#score_train
#score_test
#2 긍정
#1 보통
#0 부정
y_train = []
y_test = []
for i in range(len(train_label)):
  if train_label[i] == "2":
    y_train.append([0, 0, 1])
  elif train_label[i] == "1":
    y_train.append([0, 1, 0])
  else:
    y_train.append([1, 0, 0])

for i in range(len(test_label)):
  if test_label[i] == "2":
    y_test.append([0, 0, 1])
  elif test_label[i] == "1":
    y_test.append([0, 1, 0])
  else:
    y_test.append([1, 0, 0])

y_train = np.array(y_train)
y_test = np.array(y_test)

###################

from keras.layers import Embedding, Dense, LSTM , GRU
from keras.models import Sequential
from keras.preprocessing.sequence import pad_sequences
from keras import models
from keras import layers
from keras import optimizers
from keras import losses
from keras import metrics

max_len = 20 # 전체 데이터의 길이를 20로 맞춘다

X_train = pad_sequences(X_train, maxlen=max_len)
X_test = pad_sequences(X_test, maxlen=max_len)

#print(len(X_train))
#print(len(y_train))
#print(len(X_test))
#print(len(y_test))

model = Sequential()
model.add(Embedding(max_words, 100))
model.add(LSTM(128)) #or gru

model.add(Dense(3, activation='softmax'))

model.compile(optimizer='rmsprop', loss='categorical_crossentropy', metrics=['accuracy']) #or adam
history = model.fit(X_train, y_train, epochs=10, batch_size=10, validation_split=0.1)

print("\n 테스트 정확도 : {:.2f}%" .format(model.evaluate(X_test, y_test)[1]*100))

###############
predict = model.predict(X_test)
import numpy as np
predict_labels = np.argmax(predict, axis = 1)
original_labels = np.argmax(y_test, axis = 1)
for i in range(len(test_pos)):
  print(test_data[i], "/////원래라벨: ",test_label[i],"예측한라벨: ",predict_labels[i] )

stopwords = ['의', '가', '이', '은', '들', '는', '좀', '잘', '걍', '과', '도', '를', '으로', '자', '에', '와', '한', '하다']


def tokenizing(data):
    pos = []
    temp_X = []
    temp_X = okt.morphs(data, stem=True)  # 토큰화
    temp_X = [word for word in temp_X if not word in stopwords]  # 불용어 제거
    pos.append(temp_X)
    return pos


def predict_pos_text(text):
    pos = tokenizing(text)  # okt.pos로 토큰화한 단어를 정리
    # print(pos)
    max_words = 35000
    tokenizer = Tokenizer(num_words=max_words)
    tokenizer.fit_on_texts(test_pos)
    data = tokenizer.texts_to_sequences(pos)
    # print(data)
    predict_score = model.predict(data)
    print(predict_score)
    # print(max(predict_score[0]))
    a = max(predict_score[0])

    if (a == predict_score[0][0]):
        print("[{}]는 {:.2f}% 확률로 부정 리뷰입니다.\n".format(text, a * 100))
    elif (a == predict_score[0][1]):
        print("[{}]는 {:.2f}% 확률로 보통 리뷰입니다.\n".format(text, a * 100))
    else:
        print("[{}]는 {:.2f}% 확률로 긍정 리뷰입니다.\n".format(text, a * 100))

model.save('best_model.h5')