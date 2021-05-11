from keras.models import load_model
import keras
import pandas as pd
import matplotlib.pyplot as plt
from tensorflow.keras.preprocessing.text import Tokenizer
from tensorflow.keras.preprocessing.sequence import pad_sequences
from konlpy.tag import Okt

train = pd.read_csv('./vincenzo.csv', names=['label', 'document'])
okt = Okt()

class preprocessing():
    def __init__(self):
        # 스포일러 포함 감상평 문구 제거
        def reduce_spoil(self):
            train.document = train.document.apply(lambda x: str(x).replace('스포일러가 포함된 감상평입니다. 감상평 보기', ''))
            return train

        self.train = reduce_spoil(train)

    def analysis(self):
        def tokenize2(doc):
            # 조사 관련 형태소는 없애주기 위함
            word = ['/'.join(t) for t in okt.pos(doc, norm=True, stem=True) if 'Josa' not in t]
            return word

        train['comment'] = train['document'].apply(tokenize2)
        return train


preprocess = preprocessing()
train = preprocess.analysis()

X_train = train['comment'].values

    # 정수인코딩
tokenizer = Tokenizer(oov_token="<OOV>")
tokenizer.fit_on_texts(X_train)

threshold = 2
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

def padding(max_len):
    x_train = pad_sequences(X_train, maxlen = max_len)
    return x_train,max_len

X_train,max_len = padding(55)

"""
for i in range(len(X_train)):
    print(train['comment'][i])
    print(X_train[i])
    print("\n")
"""

loaded_model = load_model('oss.h5')

def sentiment_predict(sentence):
    print(sentence)
    new_sentence = okt.morphs(sentence, stem=True) # 토큰화
    stopwords = ['의', '가', '이', '은', '들', '는', '좀', '잘', '걍', '과', '도', '를', '으로', '자', '에', '와', '한', '하다']
    new_sentence = [word for word in new_sentence if not word in stopwords] # 불용어 제거
    encoded = tokenizer.texts_to_sequences([new_sentence]) # 정수 인코딩
    pad_new = pad_sequences(encoded, maxlen = max_len) # 패딩
    print(new_sentence)
    score = float(loaded_model.predict(pad_new)) # 예측
    if(score > 0.5):
        print("{:.2f}% 확률로 긍정 리뷰입니다.\n".format(score * 100))
        return score, 1
    else:
        print("{:.2f}% 확률로 부정 리뷰입니다.\n".format((1 - score) * 100))
        return score, 0
positive = 0
negative = 0
sum = 0
l = ["송혜교와 이혼하고 첫드라마인가?? 박근혜정부때 sbs가에서 사이코패스 드라마 나오더니..이번엔 종편에서 사이코패스 드라마네..요즘 피디 연출력이 많이 딸려...족집게로 대학드러간 애들의 수준이 이정도니...일본드라마 그만 배껴..",
     "매국노들 많네~",
     "돌아온 송중기는 매력 터져 너무 섹시해~♡",
     "현 정부에 시사하는 점이 많다고 느낌...정말 재밌게 잘 봤습니다",
     "러브라인 많이없어서 재밌다가... 16화 넘어가면서 부터 러브라인 너무 심해서 ... 노잼으로 변함.... 억지설정은 알겠는데... 그리고 마지막에 장한석이 동생 포함 세명 죽이려고 할때.. 동생이 장한석 공격 하면서 기회 만들었는데... 기회만들어준 동생 버리고 도망치다가 같이 도망치는 홍변 총 맞고나서야 도와주는 걸 보고 그냥 껐음... 처음은 좋은데 뒤가 되게 노잼엔딩...",
     "매회가 주옥 같은 명장면 하나 이상은 꼭있구만 ㅋㄷㅋㄷ",
     ]
for i in range(1,len(l)):
    score,emo = sentiment_predict(l[i])
    if emo == 1:
        positive+=1
    else:
        negative+=1
    sum += 1-score
print('sum : %d' % sum)
print('len : %d ' % len(train))

print(sum/len(train) * 100)
ratio = [positive,negative]
labels = ['Good', 'Bad']

plt.pie(ratio, labels=labels, autopct='%.1f%%')
plt.show()
