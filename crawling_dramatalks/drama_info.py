from bs4 import BeautifulSoup
import urllib
import requests
import pymysql
import re

# 드라마 기본 정보 크롤링 , DB 저장
def search_info_to_db(idex,drama_name):
    # Open database connection
    db = pymysql.connect(host='localhost', port=3306, user='findrama', passwd='findrama', db='findrama', charset='utf8',
                         autocommit=True)
    # prepare a cursor object using cursor() method
    cursor = db.cursor()   # DB 접근
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 6.3; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.132 Safari/537.36'}
    url = "https://search.naver.com/search.naver?query=" + drama_name
    html = requests.get(url, headers=headers).text
    soup = BeautifulSoup(html, 'html.parser')

    # 기본 정보 저장
    title = soup.find('strong', class_='_text').text      # 제목
    ch = soup.find('dd')
    chanel = ch.find('a').text                            #방송사
    start_date = ch.find_all('span')[0].text
    day = ch.find_all('span')[1].text                     #방영일자
    plot = soup.find('span', class_='desc _text').text    #줄거리
    plot = plot.replace('\'','')
    img = soup.find('div',class_='detail_info')           #이미지
    img_url = img.find('img').get('src')
    
    # 등장인물
    url = "https://search.naver.com/search.naver?query=" + drama_name + "+등장인물"
    html = requests.get(url, headers=headers).text
    soup = BeautifulSoup(html, 'html.parser')
    characters = soup.find('div', class_='list_image_info _content').find_all('li') 
    sql = "insert into drama values (" + str(
        idex) + ",'" + title + "','" + chanel + "','" + start_date + "','" + day + "','" + img_url + "'," + "'" + plot + "')"
    cursor.execute(sql)
    idx = 0
    character = []
    for ch in characters:
        atags = ch.find_all('a')
        role = atags[1].text
        try:
            actor = atags[2].text
        except:
            actor = ch.find('span', class_='_text').text
        sql = "insert into actor values ("+str(idex)+",'" + role +"','"+actor + "')"

        #print(sql)
        cursor.execute(sql)
