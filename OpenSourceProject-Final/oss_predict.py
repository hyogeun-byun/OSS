from oss_database import Database
from keras.models import load_model
from tensorflow.keras.preprocessing.text import Tokenizer
from tensorflow.keras.preprocessing.sequence import pad_sequences
from PIL import Image
from konlpy.tag import Okt
from wordcloud import WordCloud
import matplotlib.pyplot as plt
import numpy as np

class Chat_Data:
    def __init__(self,id):
        self.db = Database()                                            # 데이터 베이스를 연동
        self.test = []                                                  # 예측할 데이터를 저장
        self.tokenizer = Tokenizer(oov_token="<OOV>",num_words=35000)   # 토근화 하기 위한 Tonenizer 변수
        self.okt = Okt()                                                # 자연어 처리를 위한 OKT 클래스-> KONLPY
        self.text = " "                                                 # WordCould를 위한 String 변수
        self.chat = []                                                  # 예측할 문장 -> 하나도 처리 안된것.
        self.predict = []                                               # 예측 결과
        self.positive = 0                                               # 긍정댓글 개수를 저장할 변수
        self.normal = 0                                                 # 보통댓글 개수를 저장할 변수
        self.negative = 0                                               # 부정댓글 개수를 저장할 변수
        self.sum = 0                                                    # 모든 댓글의 정확도를 저장.
        self.id = id                                                    # 드라마의 ID를 저장할 변수

    def get_data(self):             #Query를 통해 데이터를 가져온 후 예측함.
        if self.db:
            sql = "select talk from drama_talks where id =" + str(self.id) +";"    #드라마의 댓글들을 가져올 MySQL 쿼리
            train = self.db.executeAll(sql)                                        #쿼리 실행 후 데이터를 train변수에 저장.
            self.predict_data(train)                                               #train 데이터를 예측

    def predict_data(self,train):   #예측과 Wordcloud실행 함수.
        for i in train:                         # train의 데이터를 하나씩 가져옴.
            for key,value in i.items():         # train은 (key:value)의 딕셔너리형식이므로 train하나의 값을 key,value값으로 나누어서 가져옴.
                try:                            # 에러 해결을 위한 try catch문
                    new_sentence = self.okt.morphs(value, stem=True)  # 어간추출 및 토큰화
                                                                      # ex) 재밌네 -> 재밌다 (어간 추출), 드라마 재밌다 -> "드라마" "재밌다"(토큰화)
                    stopwords = ['의', '가', '이', '은', '들', '는', '좀', '잘', '걍', '과', '도', '를', '으로', '자', '에', '와', '한', '하다']
                    #조사를 포함한 불필요한 단어들
                    new_sentence = [word for word in new_sentence if not word in stopwords]  # 불필요한 단어들 제거
                    self.test.append(new_sentence) # 전처리된 문장을 test변수에 저장.
                except:  # 에러 해결을 위한 try catch문.
                    continue   # 에러 발견 시 그 문장은 skip함.

        self.tokenizer.fit_on_texts(self.test) # 토큰화 숫자로 바꾸기 -> 벡터화
        self.loaded_model = load_model('best_model.h5')  # 모델을 가져옴.



        for i in train:                                  # train 데이터를 가져옴.
            for key, value in i.items():                 # train은 (key:value)의 딕셔너리형식이므로 train하나의 값을 key,value값으로 나누어서 가져옴.
               self.sentiment_predict(self.text,value)   # 문장 하나하나 모델을 통해 예측함.

        wordcloud = WordCloud(font_path='C:/Windows/Fonts/batang.ttc', # WordCloud를 위한 변수 선언.
                              background_color="#0E111B",
                              max_font_size=100)

        #print(self.text)
        wordcloud.generate(str(self.text)) #WordCloud실행.


        plt.imshow(wordcloud, interpolation='bilinear')                                   # 이미지 출력
        plt.axis('off')                                                                   # 축 설정 -> off
        plt.savefig("./templates/static/wordcloud/wordcloud_"+str(self.id)+".png")        # WordCloud 사진을 저장.

        image = Image.open("./templates/static/wordcloud/wordcloud_"+str(self.id)+".png") # WordCloud 사진을 가져옴.
        croppedImage = image.crop((80,120,575,365))                                       # 이미지를 자름. -> Wordcloud 사진의 불필요한 부분을 자름.
        croppedImage.save("./templates/static/wordcloud/wordcloud_"+str(self.id)+".png")  # 자른 이미지 다시 저장.

        #print(round(self.positive/(self.positive+self.normal+self.negative),4)*100)
        #print(round(self.normal/(self.positive+self.normal+self.negative),4)*100)
        #print(round(self.negative/(self.positive+self.normal+self.negative),4)*100)
        #print(round(self.sum/(self.positive+self.normal+self.negative),4)*100)

        #ratio = [self.positive, self.negative]
        #labels = ['Good', 'Bad']

    def sentiment_predict(self,text,sentence): # 모델을 통해 데이터 결과 예측.
        try:
            new_sentence = self.okt.morphs(sentence,norm=True, stem=True) # 정규화, 어간추출, 토큰화
            stopwords = ['의', '가', '이', '은', '들', '는', '좀', '잘', '걍', '과', '도', '를', '으로', '자', '에', '와', '한', '하다']
            #불필요 단어
            new_sentence = [word for word in new_sentence if not word in stopwords] # 불필요단어 제거
            encoded = self.tokenizer.texts_to_sequences(new_sentence) # 정수 인코딩
            pad_new = pad_sequences(encoded, maxlen = 20) # 패딩
            predict_score = self.loaded_model.predict(pad_new) # 예측
            a = max(predict_score[0]) # 예측값
            # 예측을 긍정 보통 부정 3개로 하였기에 2차원배열의 형식으로 결과가나옴.
            # 그중 가장 값이 큰 확률을 가져와 비교하여 긍정인지 부정인지 보통인지를 판단
            if a == predict_score[0][0]:#부정
                self.chat.append(sentence) # chat에 전처리안된 데이터 입력
                self.predict.append("{:.2f}% 확률로 부정 리뷰입니다.\n".format(a * 100)) # 그 데이터의 확률 또한 입력.
                self.negative += 1 # 부정 개수 1 추가
                self.sum += a      # 정확도 추가.

            elif a == predict_score[0][1]: #보통
                self.chat.append(sentence) # chat에 전처리안된 데이터 입력
                self.predict.append("{:.2f}% 확률로 보통 리뷰입니다.\n".format(a * 100))# 그 데이터의 확률 또한 입력.
                self.normal += 1     # 보통 개수 1추가
                self.sum += a*0.5    # 정확도 추가

            elif a == predict_score[0][2] and a > 0.85: # 긍정
                self.chat.append(sentence) # chat에 전처리안된 데이터 입력
                self.predict.append("{:.2f}% 확률로 긍정 리뷰입니다.\n".format(a * 100))# 그 데이터의 확률 또한 입력.
                self.positive += 1   # 긍정 개수 1 추가
                self.sum += a        # 정확도 추가
            w = ' '.join(new_sentence) # w는 모든 데이터들을 하나의 String변수에 저장해둠.
            self.text = self.text + w + " " # 띄어쓰기 추가.
            return
        except:
            return