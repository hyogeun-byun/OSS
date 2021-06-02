from selenium import webdriver
import time
from bs4 import BeautifulSoup
import urllib
import pymysql

# 드라마 댓글 크롤링, DB저장
def search_talks_into_db(index,drama_chanel, drama_name):
    count = 1
    # Open database connection
    db = pymysql.connect(host='localhost', port=3306, user='findrama', passwd='findrama', db='findrama', charset='utf8',
                         autocommit=True)
    # prepare a cursor object using cursor() method
    cursor = db.cursor()        #DB 접근
    
    #chrome driver 사용
    driver = webdriver.Chrome(r'C:\Users\paqgl\Downloads\chromedriver.exe')
    url = 'https://tv.naver.com/'+drama_chanel+'.'+ drama_name +'/talks'
    driver.get(url)
    time.sleep(3)  # 웹 페이지 로드를 보장하기 위해 3초 쉬기

    # 댓글 데이터베이스에 삽입 (임의로 100개)
    while count <= 2:
        idx = 4
        for j in range(5):

            text = driver.page_source
            soup = BeautifulSoup(text, 'html.parser')

            for li in soup.select('div.u_cbox_area'):
                nickname = li.select_one('span.u_cbox_nick').text   # 댓글 작성자 아이디 크롤링
                try:
                    talk = li.select_one('span.u_cbox_contents').text  
                except:
                    continue

                # execute SQL query using execute() method.
                sql = "insert into drama_talks values ("+str(index) + ",'" + nickname + "'" + "," + "'" + talk + "'" + ")"
                #print(count ,sql)

                try:
                    cursor.execute(sql)
                except:                                # 클린 로봇이 처리한 댓글은 가져오지 않음
                    continue
                #print(nickname, ' :  ', talk)
            select = '#cbox_module_talk > div > div.u_cbox_paginate > div > a:nth-child(' + str(idx) + ')'
            try:
                button = driver.find_elements_by_css_selector(select)[0]  # 페이지 2,3,4,5,다음페이지 버튼 클릭
            except:
                break
            button.click()
            idx += 1
            time.sleep(3)
        count += 1
