from keras.models import load_model
import keras
import pandas as pd
import matplotlib.pyplot as plt
from tensorflow.keras.preprocessing.text import Tokenizer
from tensorflow.keras.preprocessing.sequence import pad_sequences
from konlpy.tag import Okt

train = pd.read_csv('./vincenzo.csv', names=['label', 'document'])
okt = Okt()

test = []
for i in train['document']:
    try:
        new_sentence = okt.morphs(i, stem=True)  # 토큰화
        stopwords = ['의', '가', '이', '은', '들', '는', '좀', '잘', '걍', '과', '도', '를', '으로', '자', '에', '와', '한', '하다']
        new_sentence = [word for word in new_sentence if not word in stopwords]  # 불용어 제거
        test.append(new_sentence)
    except:
        continue


tokenizer = Tokenizer(oov_token="<OOV>")
tokenizer.fit_on_texts(test)
test = tokenizer.texts_to_sequences(test)
test = pad_sequences(test, maxlen = 20)

loaded_model = load_model('oss.h5')

def sentiment_predict(sentence):
    try:
        new_sentence = okt.morphs(sentence, stem=True) # 토큰화
        stopwords = ['의', '가', '이', '은', '들', '는', '좀', '잘', '걍', '과', '도', '를', '으로', '자', '에', '와', '한', '하다']
        new_sentence = [word for word in new_sentence if not word in stopwords] # 불용어 제거
        encoded = tokenizer.texts_to_sequences([new_sentence]) # 정수 인코딩
        pad_new = pad_sequences(encoded, maxlen = 20) # 패딩
        print(new_sentence)
        score = float(loaded_model.predict(pad_new)) # 예측
        if(score > 0.5):
            print("{:.2f}% 확률로 긍정 리뷰입니다.\n".format(score * 100))
            return score, 1
        else:
            print("{:.2f}% 확률로 부정 리뷰입니다.\n".format((1 - score) * 100))
            return score, 0
    except:
        return 0,0
positive = 0
negative = 0
sum = 0

for i in train['document']:
    score,emo = sentiment_predict(i)
    if score==0: continue
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
