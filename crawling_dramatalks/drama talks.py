from selenium import webdriver
import time
from bs4 import BeautifulSoup
import urllib
import pymysql


#drama talks
#ex) cjenm , myulmang
def search_talks_into_db(drama_chanel, drama_name):
    # Open database connection
    db = pymysql.connect(host='localhost', port=3306, user='findrama', passwd='findrama', db='findrama', charset='utf8',
                         autocommit=True)
    # prepare a cursor object using cursor() method
    cursor = db.cursor()

    driver = webdriver.Chrome(r'C:\Users\paqgl\Downloads\chromedriver.exe')
    url = 'https://tv.naver.com/'+drama_chanel+'.'+ drama_name +'/talks'
    driver.get(url)
    time.sleep(3)  # 웹 페이지 로드를 보장하기 위해 3초 쉬기
    # 댓글 데이터베이스에 삽입
    while True:
        idx = 4
        for j in range(5):
            text = driver.page_source
            soup = BeautifulSoup(text, 'html.parser')

            for li in soup.select('div.u_cbox_area'):
                nickname = li.select_one('span.u_cbox_nick').text
                try:
                    talk = li.select_one('span.u_cbox_contents').text
                except:
                    continue

                # execute SQL query using execute() method.
                sql = "insert into myulmang_talks values (" + "'" + nickname + "'" + "," + "'" + talk + "'" + ")"
                try:
                    cursor.execute(sql)
                except:
                    continue

                # l.append([nickname,talk])
                #print(nickname, ' :  ', talk)
            #page = 5 * i + j + 1
            #print('page:', page, ' --------------------------------', idx)
            select = '#cbox_module_talk > div > div.u_cbox_paginate > div > a:nth-child(' + str(idx) + ')'
            try:
                button = driver.find_elements_by_css_selector(select)[0]
            except:
                break
            button.click()
            idx += 1
            time.sleep(3)
#사용 예시
#search_talks_into_db('cjenm', 'myulmang')