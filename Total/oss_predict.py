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
        self.db = Database()
        self.test = []
        self.tokenizer = Tokenizer(oov_token="<OOV>")
        self.okt = Okt()
        self.text = " "
        self.chat = []
        self.predict = []
        self.positive = 0
        self.negative = 0
        self.sum = 0
        self.image = np.array(Image.open("./templates/static/wordcloud/hanbando.png"))
        self.id = id

    def get_data(self):
        if self.db:
            sql = "select talk from drama_talks where id =" + str(self.id) +";"
            train = self.db.executeAll(sql)
            self.predict_data(train)

    def predict_data(self,train):
        for i in train:
            for key,value in i.items():
                try:
                    new_sentence = self.okt.morphs(value, stem=True)  # 토큰화
                    stopwords = ['의', '가', '이', '은', '들', '는', '좀', '잘', '걍', '과', '도', '를', '으로', '자', '에', '와', '한', '하다']
                    new_sentence = [word for word in new_sentence if not word in stopwords]  # 불용어 제거
                    self.test.append(new_sentence)
                except:
                    continue

        self.tokenizer.fit_on_texts(self.test) # 토큰화 숫자로 바꾸기
        self.loaded_model = load_model('oss.h5')



        for i in train:
            for key, value in i.items():
                self.text = self.sentiment_predict(self.text,value)

        wordcloud = WordCloud(font_path='C:/Windows/Fonts/batang.ttc',
                              mask=self.image,
                              background_color="#0E111B",
                              max_font_size=100)
        wordcloud.generate(self.text)


        plt.imshow(wordcloud, interpolation='bilinear')
        plt.axis('off')
        plt.savefig("./templates/static/wordcloud/wordcloud_"+str(self.id)+".png")

        image = Image.open("./templates/static/wordcloud/wordcloud_"+str(self.id)+".png")
        croppedImage = image.crop((140, 60, 515, 420))
        croppedImage.save("./templates/static/wordcloud/wordcloud_"+str(self.id)+".png")

        print(self.positive)
        print(self.negative)
        print(sum)
        #ratio = [self.positive, self.negative]
        #labels = ['Good', 'Bad']

    def sentiment_predict(self,text,sentence):
        try:
            new_sentence = self.okt.morphs(sentence, stem=True) # 토큰화
            stopwords = ['의', '가', '이', '은', '들', '는', '좀', '잘', '걍', '과', '도', '를', '으로', '자', '에', '와', '한', '하다']
            new_sentence = [word for word in new_sentence if not word in stopwords] # 불용어 제거
            encoded = self.tokenizer.texts_to_sequences([new_sentence]) # 정수 인코딩
            pad_new = pad_sequences(encoded, maxlen = 20) # 패딩
            score = float(self.loaded_model.predict(pad_new)) # 예측
            if(score > 0.5):
                self.chat.append(sentence)
                self.predict.append("{:.2f}% 확률로 긍정 리뷰입니다.".format(score * 100))
                self.positive+=1
                self.sum+= 1-score
            else:
                self.chat.append(sentence)
                self.predict.append("{:.2f}% 확률로 부정 리뷰입니다.".format((1 - score) * 100))
                self.negative += 1
                self.sum += 1 - score

            a = ' '.join(new_sentence)
            text = text + a + " "
            return text
        except:
            return