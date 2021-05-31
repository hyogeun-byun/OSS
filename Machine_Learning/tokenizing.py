from konlpy.tag import Okt
import json
import os
from pprint import pprint
import nltk
import matplotlib.pyplot as plt
from matplotlib import font_manager,rc
import numpy as np

def read_train_data(filename):
    with open(filename,'r',encoding='UTF8') as f:
        data = [line.split(' ',maxsplit=1) for line in f.read().splitlines()]

    return data

def read_test_data(filename):
    with open(filename,'r',encoding='UTF8') as f:
        data = [line.split('\t') for line in f.read().splitlines()]
        data = data[1:]
    return data

train_df = read_test_data('naver_movie.txt')
test_df = read_test_data('naver_movie4.txt')
print(type(train_df))
print(train_df[0])
okt = Okt()

def tokenizing(docs):
    return ['/'.join(t) for t in okt.pos(docs,norm=True, stem=True)]

train_pos = []
test_pos = []
for row in train_df:
    try:
        train_pos0 = [tokenizing(row[1]),row[2]]
        print(train_pos0)
        train_pos.append(train_pos0)
    except:
        pass

for row in test_df:
    try:
        test_pos0 = [tokenizing(row[1]), row[2]]
        test_pos.append(test_pos0)
    except:
        pass

print(train_pos[0])

tokens = [t for d in train_pos for t in d[0]]

text = nltk.Text(tokens,name='NMSC')
len(set(text.tokens))
text.vocab().most_common(10)

plt.rc('font',family='D2Coding')
plt.figure(figsize=(20,10))
text.plot(100)
plt.show()

selected_words = [f[0] for f in text.vocab().most_common(10000)]

def term_frequency(doc):
    return [doc.count(word) for word in selected_words]

train_x = [term_frequency(d) for d, _ in train_pos]

test_x = [term_frequency(d) for d, _ in test_pos]
train_y = [c for _, c in train_pos]
test_y = [c for _, c in test_pos]

print(len(train_x))
print(len(train_x[0]))
print(len(train_y))

x_train = np.asarray(train_x).astype('float32')
x_test = np.asarray(test_x).astype('float32')
y_train = np.asarray(train_y).astype('float32')
y_test = np.asarray(test_y).astype('float32')

