from bs4 import BeautifulSoup
import urllib
import requests
import pymysql
import numpy as np
from PIL import Image
from konlpy.tag import Okt
from wordcloud import WordCloud,ImageColorGenerator
import matplotlib.pyplot as plt

class word_cloud:
    def __init__(self):
        db = pymysql.connect(host='localhost', port=3306, user='root', passwd='byun0424', db='findrama', charset='utf8',
                              autocommit=True)
        self.cursor = db.cursor()
        self.train = []
        self.okt = Okt()
        self.text = " "
        self.image = np.array(Image.open("./hanbando.png"))
        self.execute()

    def sentiment_predict(self,text,sentence):
        print(sentence)
        new_sentence = self.okt.morphs(sentence, stem=True) # 토큰화
        print(new_sentence)
        stopwords = ['의', '가', '이', '은', '들', '는', '좀', '잘', '걍', '과', '도', '를', '으로', '자', '에', '와', '한', '하다']
        new_sentence = [word for word in new_sentence if not word in stopwords] # 불용어 제거
        print(new_sentence)
        a = ' '.join(new_sentence)
        text = text + a
        text = text + " "
        return text

    def execute(self):
        sql = "select * from drama_talks"
        self.cursor.execute(sql)
        result = self.cursor.fetchall()

        for i in range(100):
            self.text = self.sentiment_predict(self.text,result[i][2])


        wordcloud = WordCloud(font_path='C:/Windows/Fonts/batang.ttc',
                              mask=self.image,
                              background_color="#0E111B",
                              max_font_size=100)
        wordcloud.generate(self.text)

        fig = plt.figure()
        plt.imshow(wordcloud, interpolation='bilinear')
        plt.axis('off')
        plt.savefig('./templates/static/wordcloud/wordcloud1.png')
        image = Image.open('./templates/static/wordcloud/wordcloud1.png')
        croppedImage = image.crop((140,60,515,420))
        croppedImage.save('./templates/static/wordcloud/wordcloud1.png')

word = word_cloud()