import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from konlpy.tag import Okt
from konlpy.tag import Mecab
from sklearn.model_selection import train_test_split
from tensorflow.keras.preprocessing.text import Tokenizer
from tensorflow.keras.preprocessing.sequence import pad_sequences

from tensorflow.keras.layers import Embedding, Dense, LSTM, Bidirectional, Dropout,BatchNormalization
from tensorflow.keras.models import Sequential
from tensorflow.keras.models import load_model
from tensorflow.keras.callbacks import EarlyStopping, ModelCheckpoint
from tensorflow.keras.layers import Embedding, Dropout, Conv1D, GlobalMaxPooling1D, Dense

train = pd.read_csv('best_train.csv', names=['label', 'document'])
worst_train = pd.read_csv('worst_train.csv', names=['label', 'document'])

class data():
    def best_data(self):
        # 5만개 수집만개 수집 (별점 7점이상)
        best_train = train[train.label == 1]
        best_train = best_train.dropna()
        best_df = best_train[:3998]  # 수집한 부정 데이터와 개수 동일 유지
        return best_df

    def worst_data(self):
        worst_df = worst_train.dropna()
        return worst_df

    def train_test_merge(self, best_df1, worst_df1):
        train = pd.concat([best_df1, worst_df1])
        train.reset_index(drop=True, inplace=True)
        print("데이터의 shape : ", train.shape)
        print("데이터의 긍정 부정 비율 : \n", train['label'].value_counts())
        return train


data = data()
best_df = data.best_data()
worst_df = data.worst_data()
train = data.train_test_merge(best_df, worst_df)

okt = Okt()
mecab = Mecab(dicpath=r"C:\mecab\mecab-ko-dic")

class preprocessing():
    def __init__(self):
        # 스포일러 포함 감상평 문구 제거
        def reduce_spoil(self):
            train.document = train.document.apply(lambda x: x.replace('스포일러가 포함된 감상평입니다. 감상평 보기', ''))
            return train

        self.train = reduce_spoil(train)
        self.train2 = reduce_spoil(train)

    def analysis(self):
        def tokenize2(doc):
            # 조사 관련 형태소는 없애주기 위함
            word = ['/'.join(t) for t in okt.pos(doc, norm=True, stem=True) if 'Josa' not in t]
            return word

        train['token_okt2'] = train['document'].apply(tokenize2)
        return train


preprocess = preprocessing()
train = preprocess.analysis()


def train_test(self):
    train_data, test_data = train_test_split(train, train['label'], test_size=0.25, random_state=42)
    return train_data, test_data

train_data, test_data = train_test_split(train)


# 토큰 방법을 입력, 단어 빈도 수
def convert_input(token_analysis, how_many):
    X_train = train_data[token_analysis].values
    y_train = train_data['label']
    X_test = test_data[token_analysis].values
    y_test = test_data['label']

    # 정수인코딩
    tokenizer = Tokenizer(oov_token="<OOV>")
    tokenizer.fit_on_texts(X_train)

    threshold = how_many
    total_cnt = len(tokenizer.word_index)  # 단어의 수
    rare_cnt = 0  # 등장 빈도수가 threshold보다 작은 단어의 개수를 카운트
    total_freq = 0  # 훈련 데이터의 전체 단어 빈도수 총 합

    # 단어와 빈도수의 쌍(pair)을 key와 value로 받는다.
    for key, value in tokenizer.word_counts.items():
        total_freq = total_freq + value

        if (value < threshold):
            rare_cnt = rare_cnt + 1

    vocab_size = total_cnt - rare_cnt + 2

    tokenizer = Tokenizer(vocab_size, oov_token='OOV')
    tokenizer.fit_on_texts(X_train)
    X_train = tokenizer.texts_to_sequences(X_train)
    X_test = tokenizer.texts_to_sequences(X_test)

    return X_train, y_train, X_test, y_test, vocab_size


X_train, y_train, X_test, y_test, vocab_size = convert_input('token_okt2', 2)
print("---------------------------------------")
print(X_train)
print(y_train)
print("---------------------------------------")
def padding_len(max_len, sentences):
    cnt = 0
    for s in sentences:
        if(len(s) <= max_len):
            cnt = cnt + 1
    print('전체 샘플 중 길이가 %s 이하인 샘플의 비율: %s'%(max_len, (cnt / len(sentences))*100))
    return max_len
padding_len(55, X_train)
padding_len(55, X_test)

def padding(max_len):
    x_train = pad_sequences(X_train, maxlen = max_len)
    x_test = pad_sequences(X_test, maxlen = max_len)
    print(x_train.shape, x_test.shape)
    return x_train, x_test, max_len

X_train, X_test, max_len = padding(55)

def lstm():
    model = Sequential()
    model.add(Embedding(vocab_size, 100,input_length = max_len))
    model.add(LSTM(128))
    model.add(Dense(1, activation='sigmoid'))

    es = EarlyStopping(monitor='val_loss', mode='min', verbose=1, patience=10)
    mc = ModelCheckpoint('best_model.h5', monitor='val_acc', mode='max', verbose=1, save_best_only=True)
    model.compile(optimizer='adam', loss='binary_crossentropy', metrics=['acc'])
    model.fit(X_train, y_train, epochs=30, callbacks=[es, mc], batch_size=32, validation_split=0.2)
    loaded_model = load_model('best_model.h5')
    score = loaded_model.evaluate(X_test, y_test)[1]
    print("테스트 정확도: %.4f" % (score))
    test_result.append((token, 'LSTM',score))
    model.save("my_h5_model.h5")

test_result = []
token = 'token_okt2'
X_train, y_train, X_test, y_test, vocab_size = convert_input('token_okt2', 2)
padding_len(55, X_train)
padding_len(55, X_test)
X_train, X_test, max_len = padding(55)

lstm()
