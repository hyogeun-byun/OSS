from keras.models import load_model
import pymysql
from keras.models import load_model
import matplotlib.pyplot as plt
from tensorflow.keras.preprocessing.text import Tokenizer
from tensorflow.keras.preprocessing.sequence import pad_sequences
from konlpy.tag import Okt

class Chat_data:
    def __init__(self):
        self.db = pymysql.connect(host='localhost',
                                  user='root',
                                  password='byun0424',
                                  db='findrama',
                                  charset='utf8')
        self.cursor = self.db.cursor(pymysql.cursors.DictCursor)
        self.test = []
        self.tokenizer = Tokenizer(oov_token="<OOV>")
        self.okt = Okt()
        sql = "select talk from drama_talks where id = 0;"
        self.cursor.execute(sql)
        train = self.cursor.fetchall()
        print(train)
        self.chat = []
        self.predict = []
        for i in train:
            try:
                new_sentence = self.okt.morphs(i[0], stem=True)  # 토큰화
                stopwords = ['의', '가', '이', '은', '들', '는', '좀', '잘', '걍', '과', '도', '를', '으로', '자', '에', '와', '한', '하다']
                new_sentence = [word for word in new_sentence if not word in stopwords]  # 불용어 제거
                self.test.append(new_sentence)
            except:
                continue


        self.tokenizer.fit_on_texts(self.test)

        self.loaded_model = load_model('oss.h5')

        positive = 0
        negative = 0
        sum = 0

        """for i in train:
            score, emo = self.sentiment_predict(i[0])
            if score == 0: continue
            if emo == 1:
                positive += 1
            else:
                negative += 1
            sum += 1 - score"""


        #print('sum : %d' % sum)
        #print('len : %d ' % len(train))

        #print(sum / len(train) * 100)
        ratio = [positive, negative]
        labels = ['Good', 'Bad']
        #plt.pie(ratio, labels=labels, autopct='%.1f%%')
        #plt.show()

    def sentiment_predict(self,sentence):
        try:
            new_sentence = self.okt.morphs(sentence, stem=True) # 토큰화
            stopwords = ['의', '가', '이', '은', '들', '는', '좀', '잘', '걍', '과', '도', '를', '으로', '자', '에', '와', '한', '하다']
            new_sentence = [word for word in new_sentence if not word in stopwords] # 불용어 제거
            encoded = self.tokenizer.texts_to_sequences([new_sentence]) # 정수 인코딩
            pad_new = pad_sequences(encoded, maxlen = 20) # 패딩
            score = float(self.loaded_model.predict(pad_new)) # 예측
            if(score > 0.5):
                self.chat.append(sentence)
                self.predict.append("{:.2f}% 확률로 긍정 리뷰입니다.\n".format(score * 100))
                return score, 1
            else:
                self.chat.append(sentence)
                self.predict.append("{:.2f}% 확률로 부정 리뷰입니다.\n".format((1 - score) * 100))
                return score, 0
        except:
            return 0,0

chat = Chat_data()
