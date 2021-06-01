import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from konlpy.tag import Okt
from konlpy.tag import Mecab
from sklearn.model_selection import train_test_split
from tensorflow.keras.preprocessing.text import Tokenizer
from tensorflow.keras.preprocessing.sequence import pad_sequences

from tensorflow.keras import models
from tensorflow.keras import layers
from tensorflow.keras import optimizers
from tensorflow.keras import losses
from tensorflow.keras import metrics
from tensorflow.keras.layers import Embedding, Dense, LSTM, Bidirectional, Dropout,BatchNormalization
from tensorflow.keras.models import Sequential
from tensorflow.keras.models import load_model
from tensorflow.keras.callbacks import EarlyStopping, ModelCheckpoint

train = pd.read_csv('train.csv', names=['label', 'document'])
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
        def tokenize1(doc):
            # norm은 정규화, stem은 근어로 표시하기를 나타냄
            return ['/'.join(t) for t in okt.pos(doc, norm=True, stem=True)]

        def tokenize2(doc):
            # 조사 관련 형태소는 없애주기 위함
            word = ['/'.join(t) for t in okt.pos(doc, norm=True, stem=True) if 'Josa' not in t]
            return word

        train['token_okt1'] = train['document'].apply(tokenize1)
        train['token_okt2'] = train['document'].apply(tokenize2)

        # 조사 및 괄호를 불용어로 정의
        stopwords = ['(', ')', '도', '는', '다', '의', '가', '이', '은', '한', '에', '하', '고', '을', '를', '인', '듯', '과', '와', '네',
                     '들', '듯', '지', '임', '게', '만', '음', '면']
        train['token_mecab1'] = train['document'].apply(mecab.morphs)
        train['token_mecab2'] = train['token_mecab1'].apply(lambda x: [item for item in x if item not in stopwords])
        return train


preprocess = preprocessing()
train = preprocess.analysis()


def train_test(self):
    train_data, test_data = train_test_split(train, train['label'], test_size=0.25, random_state=42)
    print('훈련용 리뷰의 개수 :', len(train_data))
    print('테스트용 리뷰의 개수 :', len(test_data))
    return train_data, test_data


train_data, test_data = train_test_split(train)


# 토큰 방법을 입력, 단어 빈도 수
def convert_input(token_analysis, how_many):
    X_train = train_data[token_analysis].values
    y_train = train_data['label']
    X_test = test_data[token_analysis].values
    y_test = test_data['label']
    print('X_train, y_Train, X_test, y_test', X_train.shape, y_train.shape, X_test.shape, y_test.shape)

    # 정수인코딩
    tokenizer = Tokenizer(oov_token="<OOV>")
    tokenizer.fit_on_texts(X_train)

    threshold = how_many
    total_cnt = len(tokenizer.word_index)  # 단어의 수
    rare_cnt = 0  # 등장 빈도수가 threshold보다 작은 단어의 개수를 카운트
    total_freq = 0  # 훈련 데이터의 전체 단어 빈도수 총 합
    rare_freq = 0  # 등장 빈도수가 threshold보다 작은 단어의 등장 빈도수의 총 합

    # 단어와 빈도수의 쌍(pair)을 key와 value로 받는다.
    for key, value in tokenizer.word_counts.items():
        total_freq = total_freq + value

        # 단어의 등장 빈도수가 threshold보다 작으면
        if (value < threshold):
            rare_cnt = rare_cnt + 1
            rare_freq = rare_freq + value

    print('\n단어 집합(vocabulary)의 크기 :', total_cnt)
    print('등장 빈도가 %s번 이하인 희귀 단어의 수: %s' % (threshold - 1, rare_cnt))
    print("단어 집합에서 희귀 단어의 비율:", (rare_cnt / total_cnt) * 100)
    print("전체 등장 빈도에서 희귀 단어 등장 빈도 비율:", (rare_freq / total_freq) * 100)

    # 전체 단어 개수 중 빈도수 2이하인 단어 개수는 제거.
    # 0번 패딩 토큰과 1번 OOV 토큰을 고려하여 +2
    vocab_size = total_cnt - rare_cnt + 2
    print('\nvocab size :', vocab_size)

    tokenizer = Tokenizer(vocab_size, oov_token='OOV')
    tokenizer.fit_on_texts(X_train)
    X_train = tokenizer.texts_to_sequences(X_train)
    X_test = tokenizer.texts_to_sequences(X_test)

    print('\n리뷰의 최대 길이 :', max(len(l) for l in X_train))
    print('리뷰의 평균 길이 :', sum(map(len, X_train)) / len(X_train))
    plt.hist([len(s) for s in X_train], bins=50)
    plt.xlabel('length of samples')
    plt.ylabel('number of samples')
    plt.show()

    return X_train, y_train, X_test, y_test, vocab_size


X_train, y_train, X_test, y_test, vocab_size = convert_input('token_okt1', 2)

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

def DNN():
    # 모델 구조 정의하기
    model = models.Sequential()
    model.add(Embedding(vocab_size, 100,input_length = max_len))
    model.add(layers.Dense(128, activation='relu'))
    model.add(layers.Dense(128, activation='relu')) #ReLU 활성화함수 채택
    model.add(layers.Dense(1, activation='sigmoid'))
    es = EarlyStopping(monitor='val_loss', mode='min', verbose=1, patience=10)
    mc = ModelCheckpoint('best_model.h5', monitor='val_acc', mode='max', verbose=1, save_best_only=True)
    model.compile(optimizer='adam', loss='binary_crossentropy', metrics=['acc'])
    history = model.fit(X_train, y_train, epochs=30, callbacks=[es, mc], batch_size=32, validation_split=0.2)
    loaded_model = load_model('best_model.h5')
    score = loaded_model.evaluate(X_test, y_test)[1]
    print("테스트 정확도: %.4f" % (score))
    test_result.append((token, 'DNN',score))


def lstm():
    model = Sequential()
    model.add(Embedding(vocab_size, 100,input_length = max_len))
    model.add(LSTM(128))
    model.add(Dense(1, activation='sigmoid'))

    es = EarlyStopping(monitor='val_loss', mode='min', verbose=1, patience=10)
    mc = ModelCheckpoint('best_model.h5', monitor='val_acc', mode='max', verbose=1, save_best_only=True)
    model.compile(optimizer='adam', loss='binary_crossentropy', metrics=['acc'])
    history = model.fit(X_train, y_train, epochs=30, callbacks=[es, mc], batch_size=32, validation_split=0.2)
    loaded_model = load_model('best_model.h5')
    score = loaded_model.evaluate(X_test, y_test)[1]
    print("테스트 정확도: %.4f" % (score))
    test_result.append((token, 'LSTM',score))

def lstm_2_layer():
    model = Sequential()
    model.add(Embedding(vocab_size, 100,input_length = max_len))
    model.add(LSTM(128, return_sequences=True,activation='relu'))
    model.add(LSTM(128, activation='relu'))
    model.add(Dense(1, activation='sigmoid'))

    es = EarlyStopping(monitor='val_loss', mode='min', verbose=1, patience=10)
    mc = ModelCheckpoint('best_model.h5', monitor='val_acc', mode='max', verbose=1, save_best_only=True)
    model.compile(optimizer='adam', loss='binary_crossentropy', metrics=['acc'])
    history = model.fit(X_train, y_train, epochs=30, callbacks=[es, mc], batch_size=32, validation_split=0.2)
    loaded_model = load_model('best_model.h5')
    score = loaded_model.evaluate(X_test, y_test)[1]
    print("테스트 정확도: %.4f" % (score))
    test_result.append((token, 'LSTM_2layer',score))


def bidirectional_lstm():
    model = Sequential()
    model.add(Embedding(vocab_size, 100,input_length = max_len))
    model.add(Bidirectional(LSTM(128,activation='relu')))
    model.add(Dense(1, activation='sigmoid'))

    es = EarlyStopping(monitor='val_loss', mode='min', verbose=1, patience=10)
    mc = ModelCheckpoint('best_model.h5', monitor='val_acc', mode='max', verbose=1, save_best_only=True)
    model.compile(optimizer='adam', loss='binary_crossentropy', metrics=['acc'])
    history = model.fit(X_train, y_train, epochs=30, callbacks=[es, mc], batch_size=32, validation_split=0.2)
    loaded_model = load_model('best_model.h5')
    score = loaded_model.evaluate(X_test, y_test)[1]
    print("테스트 정확도: %.4f" % (score))
    test_result.append((token, 'Bi-LSTM',score))

def bidirectional_lstm_2():
    model = Sequential()
    model.add(Embedding(vocab_size, 100,input_length = max_len))
    model.add(Bidirectional(LSTM(128, return_sequences=True,activation='relu')))
    model.add(Bidirectional(LSTM(128,activation='relu')))
    model.add(Dense(1, activation='sigmoid'))

    es = EarlyStopping(monitor='val_loss', mode='min', verbose=1, patience=10)
    mc = ModelCheckpoint('best_model.h5', monitor='val_acc', mode='max', verbose=1, save_best_only=True)
    model.compile(optimizer='adam', loss='binary_crossentropy', metrics=['acc'])
    history = model.fit(X_train, y_train, epochs=30, callbacks=[es, mc], batch_size=32, validation_split=0.2)
    loaded_model = load_model('best_model.h5')
    score = loaded_model.evaluate(X_test, y_test)[1]
    print("테스트 정확도: %.4f" % (score))
    test_result.append((token, 'Bi-LSTM-2',score))

from tensorflow.keras.layers import Embedding, Dropout, Conv1D, GlobalMaxPooling1D, Dense

def cnn_1D():
    model = Sequential()
    model.add(Embedding(vocab_size, 100,input_length = max_len))
    model.add(Conv1D(256, 3, padding='valid', activation='relu'))
    model.add(GlobalMaxPooling1D())
    model.add(Dense(128, activation='relu'))
    model.add(Dropout(0.5))
    model.add(Dense(1, activation='sigmoid'))
    es = EarlyStopping(monitor='val_loss', mode='min', verbose=1, patience=10)
    mc = ModelCheckpoint('best_model.h5', monitor='val_acc', mode='max', verbose=1, save_best_only=True)
    model.compile(optimizer='adam', loss='binary_crossentropy', metrics=['acc'])
    history = model.fit(X_train, y_train, epochs=30, callbacks=[es, mc], batch_size=32, validation_split=0.2)
    loaded_model = load_model('best_model.h5')
    score = loaded_model.evaluate(X_test, y_test)[1]
    print("테스트 정확도: %.4f" % (score))
    test_result.append((token, '1D-CNN',score))


test_result = []
token_name = ['token_okt1', 'token_okt2', 'token_mecab1', 'token_mecab2']
for token in token_name:
    print(token, "방식 진행합니다.\n")
    X_train, y_train, X_test, y_test, vocab_size = convert_input(token, 2)
    padding_len(55, X_train)
    padding_len(55, X_test)
    X_train, X_test, max_len = padding(55)

    if token == 'token_okt1':
        token = "okt"
    elif token == 'token_okt2':
        token = "okt_조사제거"
    elif token == 'token_mecab1':
        token = "mecab"
    elif token == 'token_mecab2':
        token = "mecab_조사제거"

    print("\nDNN 모델 진행합니다.")
    DNN()
    print("\nLSTM 모델 진행합니다.")
    lstm()
    print("\nLSTM_2layer 모델 진행합니다.")
    lstm_2_layer()
    print("\nBi-LSTM 모델 진행합니다.")
    bidirectional_lstm()
    print("\nBi-LSTM 2층 모델 진행합니다.")
    bidirectional_lstm_2()
    print("\1D-CNN 모델 진행합니다.")
    cnn_1D()