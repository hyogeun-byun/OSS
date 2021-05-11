from selenium import webdriver
import time
from bs4 import BeautifulSoup
import pandas as pd

driver = webdriver.Chrome(r'C:\Users\paqgl\Downloads\chromedriver.exe')
drama_list_tvN = ['tvNmouse','MINE','myulmang','NAVILLERA']
driver.get('https://tv.naver.com/cjenm.vincenzo/talks')
time.sleep(3) #웹 페이지 로드를 보장하기 위해 3초 쉬기

l = []
for i in range(10):
    idx = 4
    for j in range(5):
        text = driver.page_source
        soup = BeautifulSoup(text, 'html.parser')

        for li in soup.select('div.u_cbox_area'):
            nickname = li.select_one('span.u_cbox_nick').text
            try:
                talk = li.select_one('span.u_cbox_contents').text
            except:
                talk = 'clean boat cleaned it'
            l.append([nickname,talk])
            #print(nickname,' :  ',talk)
        #page = 5*i+j+1
        #print('page:',page,' --------------------------------',idx)
        select = '#cbox_module_talk > div > div.u_cbox_paginate > div > a:nth-child(' + str(idx) + ')'
        button = driver.find_elements_by_css_selector(select)[0]
        button.click()
        idx += 1
        time.sleep(3)

df = pd.DataFrame(l,columns=['nickname','talk'])
df.to_excel('vincenzo_talks.xlsx', index=False)