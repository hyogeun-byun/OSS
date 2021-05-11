
from bs4 import BeautifulSoup
import urllib
import requests
import pymysql

#drama basic info
#drama_name ex)어느+날+우리+집+현관으로+멸망이+들어왔다  // drama_english_name ex) myulmang
def search_info_to_db(drama_name, drama_english_name):
    # Open database connection
    db = pymysql.connect(host='localhost', port=3306, user='findrama', passwd='findrama', db='findrama', charset='utf8',
                         autocommit=True)
    # prepare a cursor object using cursor() method
    cursor = db.cursor()
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 6.3; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.132 Safari/537.36'}
    url = "https://search.naver.com/search.naver?query=" + drama_name
    html = requests.get(url, headers=headers).text
    soup = BeautifulSoup(html, 'html.parser')

    # 기본 정보 저장
    name = soup.find('strong', class_='_text').text
    ch = soup.find('dd')
    chanel = ch.find('a').text
    start = ch.find_all('span')[0].text
    day = ch.find_all('span')[1].text
    plot = soup.find('span', class_='desc _text').text
    # print(name, chanel, start, day, plot, sep='//')

    url = "https://search.naver.com/search.naver?query=" + drama_name + "+등장인물"
    html = requests.get(url, headers=headers).text
    soup = BeautifulSoup(html, 'html.parser')

    characters = soup.find('div', class_='list_image_info _content').find_all('li')
    idx = 0
    character = []
    for ch in characters:
        atags = ch.find_all('a')
        role = atags[1].text
        actor = atags[2].text
        character.append(role + " : " + actor)
        # print(character[idx])
        idx += 1
        if idx == 5: break

    sql = "insert into myulmang_info values (" + "'" + name + "'" + "," + "'" + chanel + "'" + "," + "'" + start + "'," + "'" + day + "'," + "'" + \
          character[0] + "'," + "'" + character[1] + "'," + "'" + character[2] + "'," + "'" + character[
              3] + "'," + "'" + character[4] + "'," + "'" + plot + "')"
    cursor.execute(sql)

#사용 예시
#search_info_to_db( "어느+날+우리+집+현관으로+멸망이+들어왔다", "myulmang")