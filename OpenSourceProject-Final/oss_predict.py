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
        self.tokenizer = Tokenizer(oov_token="<OOV>",num_words=35000)
        self.okt = Okt()
        self.text = " "
        self.chat = []
        self.predict = []
        self.positive = 0
        self.normal = 0
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
        self.loaded_model = load_model('best_model.h5')



        for i in train:
            for key, value in i.items():
               self.sentiment_predict(self.text,value)

        wordcloud = WordCloud(font_path='C:/Windows/Fonts/batang.ttc',
                              background_color="#0E111B",
                              max_font_size=100)

        print(self.text)
        wordcloud.generate(str(self.text))


        plt.imshow(wordcloud, interpolation='bilinear')
        plt.axis('off')
        plt.savefig("./templates/static/wordcloud/wordcloud_"+str(self.id)+".png")

        image = Image.open("./templates/static/wordcloud/wordcloud_"+str(self.id)+".png")
        croppedImage = image.crop((80,120,575,365))
        croppedImage.save("./templates/static/wordcloud/wordcloud_"+str(self.id)+".png")

        print(round(self.positive/(self.positive+self.normal+self.negative),4)*100)
        print(round(self.normal/(self.positive+self.normal+self.negative),4)*100)
        print(round(self.negative/(self.positive+self.normal+self.negative),4)*100)
        print(round(self.sum/(self.positive+self.normal+self.negative),4)*100)

        #ratio = [self.positive, self.negative]
        #labels = ['Good', 'Bad']

    def sentiment_predict(self,text,sentence):
        try:
            new_sentence = self.okt.morphs(sentence,norm=True, stem=True) # 토큰화
            stopwords = ['의', '가', '이', '은', '들', '는', '좀', '잘', '걍', '과', '도', '를', '으로', '자', '에', '와', '한', '하다']

            new_sentence = [word for word in new_sentence if not word in stopwords] # 불용어 제거
            encoded = self.tokenizer.texts_to_sequences(new_sentence) # 정수 인코딩
            pad_new = pad_sequences(encoded, maxlen = 20) # 패딩
            predict_score = self.loaded_model.predict(pad_new) # 예측
            a = max(predict_score[0])
            if a == predict_score[0][0]:
                self.chat.append(sentence)
                self.predict.append("{:.2f}% 확률로 부정 리뷰입니다.\n".format(a * 100))
                self.negative += 1
                self.sum += a

            elif a == predict_score[0][1]:
                self.chat.append(sentence)
                self.predict.append("{:.2f}% 확률로 보통 리뷰입니다.\n".format(a * 100))
                self.normal += 1
                self.sum += a*0.5

            elif a == predict_score[0][2] and a > 0.85:
                self.chat.append(sentence)
                self.predict.append("{:.2f}% 확률로 긍정 리뷰입니다.\n".format(a * 100))
                self.positive += 1
                self.sum += a
            w = ' '.join(new_sentence)
            self.text = self.text + w + " "
            return
        except:
            return