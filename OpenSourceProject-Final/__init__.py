from flask import Flask, render_template
from oss_database import Database
from oss_predict import Chat_Data
import math

app = Flask(__name__,static_folder='templates/static')

db_class = Database()
c=[]
for i in range(15):
    c.append(Chat_Data(id=i))
    c[i].get_data()

@app.route('/')
def home():
    sql = "SELECT * \
                FROM drama"
    row = db_class.executeAll(sql)

    return render_template('home.html', resultData=row)


# 여기부터 추가
@app.route('/이미테이션')
def info_0():
    sql = "SELECT * \
                FROM drama WHERE id = 0"
    row = db_class.executeAll(sql)

    sql_actor = "SELECT * FROM actor WHERE id = 0"
    actors = db_class.executeAll(sql_actor)

    if round((c[0].positive+(c[0].normal*0.5))/(c[0].positive+c[0].normal+c[0].negative),2)*100 > 90: rank = "A"
    elif round((c[0].positive+(c[0].normal*0.5))/(c[0].positive+c[0].normal+c[0].negative),2)*100 > 80: rank = "B"
    elif round((c[0].positive+(c[0].normal*0.5))/(c[0].positive+c[0].normal+c[0].negative),2)*100 > 70: rank = "C"
    else: rank = "D"

    return render_template('이미테이션.html', resultData=row[0], actor = actors,
                           chat=c[0].chat ,predict = c[0].predict,
                           pos = round(c[0].positive/(c[0].positive+c[0].normal+c[0].negative),2)*100,
                           nor = round(c[0].normal/(c[0].positive+c[0].normal+c[0].negative),2)*100,
                           neg = 100 - round((c[0].positive+c[0].normal)/(c[0].positive+c[0].normal+c[0].negative),2)*100,
                           sum = round(c[0].sum/(c[0].positive+c[0].normal+c[0].negative),2)*100,
                           rank = rank)

@app.route('/멸망')
def info_1():
    sql = "SELECT * \
                FROM drama WHERE id = 1"
    row = db_class.executeAll(sql)

    sql_actor = "SELECT * FROM actor WHERE id = 1"
    actors = db_class.executeAll(sql_actor)

    if round((c[1].positive+(c[1].normal*0.5))/(c[1].positive+c[1].normal+c[1].negative),2)*100 > 90: rank = "A"
    elif round((c[1].positive+(c[1].normal*0.5))/(c[1].positive+c[1].normal+c[1].negative),2)*100 > 80: rank = "B"
    elif round((c[1].positive+(c[1].normal*0.5))/(c[1].positive+c[1].normal+c[1].negative),2)*100 > 70: rank = "C"
    else: rank = "D"

    return render_template('멸망.html', resultData=row[0], actor = actors,
                           chat=c[1].chat ,predict = c[1].predict,
                           pos = round(c[1].positive/(c[1].positive+c[1].normal+c[1].negative),2)*100,
                           nor = round(c[1].normal/(c[1].positive+c[1].normal+c[1].negative),2)*100,
                           neg = 100 - round((c[1].positive+c[1].normal)/(c[1].positive+c[1].normal+c[1].negative),2)*100,
                           sum = round(c[1].sum/(c[1].positive+c[1].normal+c[1].negative),2)*100,
                           rank = rank)
@app.route('/오월의청춘')
def info_2():
    sql = "SELECT * \
                FROM drama WHERE id = 2"
    row = db_class.executeAll(sql)
    sql_actor = "SELECT * FROM actor WHERE id = 2"
    actors = db_class.executeAll(sql_actor)

    if round((c[2].positive+(c[2].normal*0.5))/(c[2].positive+c[2].normal+c[2].negative),2)*100 > 90: rank = "A"
    elif round((c[2].positive+(c[2].normal*0.5))/(c[2].positive+c[2].normal+c[2].negative),2)*100 > 80: rank = "B"
    elif round((c[2].positive+(c[2].normal*0.5))/(c[2].positive+c[2].normal+c[2].negative),2)*100 > 70: rank = "C"
    else: rank = "D"


    return render_template('오월의청춘.html', resultData=row[0], actor = actors,
                           chat=c[2].chat ,predict = c[2].predict,
                           pos = round(c[2].positive/(c[2].positive+c[2].normal+c[2].negative),2)*100,
                           nor = round(c[2].normal/(c[2].positive+c[2].normal+c[2].negative),2)*100,
                           neg = 100 - round((c[2].positive+c[2].normal)/(c[2].positive+c[2].normal+c[2].negative),2)*100,
                           sum = round(c[2].sum/(c[2].positive+c[2].normal+c[2].negative),2)*100,
                           rank = rank)

@app.route('/로스쿨')
def info_3():
    sql = "SELECT * \
                FROM drama WHERE id = 3"
    row = db_class.executeAll(sql)
    sql_actor = "SELECT * FROM actor WHERE id = 3"
    actors = db_class.executeAll(sql_actor)

    if round((c[3].positive+(c[3].normal*0.5))/(c[3].positive+c[3].normal+c[3].negative),2)*100 > 90: rank = "A"
    elif round((c[3].positive+(c[3].normal*0.5))/(c[3].positive+c[3].normal+c[3].negative),2)*100 > 80: rank = "B"
    elif round((c[3].positive+(c[3].normal*0.5))/(c[3].positive+c[3].normal+c[3].negative),2)*100 > 70: rank = "C"
    else: rank = "D"

    return render_template('로스쿨.html', resultData=row[0], actor = actors,
                           chat=c[3].chat ,predict = c[3].predict,
                           pos = round(c[3].positive/(c[3].positive+c[3].normal+c[3].negative),2)*100,
                           nor = round(c[3].normal/(c[3].positive+c[3].normal+c[3].negative),2)*100,
                           neg=100 - round((c[3].positive + c[3].normal) / (c[3].positive + c[3].normal + c[3].negative),2) * 100,
                           sum = round(c[3].sum/(c[3].positive+c[3].normal+c[3].negative),2)*100,
                           rank = rank)

@app.route('/대박부동산')
def info_4():
    sql = "SELECT * \
                FROM drama WHERE id = 4"
    row = db_class.executeAll(sql)
    sql_actor = "SELECT * FROM actor WHERE id = 4"
    actors = db_class.executeAll(sql_actor)

    if round((c[4].positive+(c[4].normal*0.5))/(c[4].positive+c[4].normal+c[4].negative),2)*100 > 90: rank = "A"
    elif round((c[4].positive+(c[4].normal*0.5))/(c[4].positive+c[4].normal+c[4].negative),2)*100 > 80: rank = "B"
    elif round((c[4].positive+(c[4].normal*0.5))/(c[4].positive+c[4].normal+c[4].negative),2)*100 > 70: rank = "C"
    else: rank = "D"

    return render_template('대박부동산.html', resultData=row[0], actor = actors,
                           chat=c[4].chat ,predict = c[4].predict,
                           pos = round(c[4].positive/(c[4].positive+c[4].normal+c[4].negative),2)*100,
                           nor = round(c[4].normal/(c[4].positive+c[4].normal+c[4].negative),2)*100,
                           neg = 100 - round((c[4].positive+c[4].normal)/(c[4].positive+c[4].normal+c[4].negative),2)*100,
                           sum = round(c[4].sum/(c[4].positive+c[4].normal+c[4].negative),2)*100,
                           rank = rank)

@app.route('/모범택시')
def info_5():
    sql = "SELECT * \
                FROM drama WHERE id = 5"
    row = db_class.executeAll(sql)
    sql_actor = "SELECT * FROM actor WHERE id = 5"
    actors = db_class.executeAll(sql_actor)


    if round((c[5].positive+(c[5].normal*0.5))/(c[5].positive+c[5].normal+c[5].negative),2)*100 > 90: rank = "A"
    elif round((c[5].positive+(c[5].normal*0.5))/(c[5].positive+c[5].normal+c[5].negative),2)*100 > 80: rank = "B"
    elif round((c[5].positive+(c[5].normal*0.5))/(c[5].positive+c[5].normal+c[5].negative),2)*100 > 70: rank = "C"
    else: rank = "D"

    return render_template('모범택시.html', resultData=row[0], actor = actors,
                           chat=c[5].chat ,predict = c[5].predict,
                           pos = round(c[5].positive/(c[5].positive+c[5].normal+c[5].negative),2)*100,
                           nor = round(c[5].normal/(c[5].positive+c[5].normal+c[5].negative),2)*100,
                           neg=100 - round((c[5].positive + c[5].normal) / (c[5].positive + c[5].normal + c[5].negative),2) * 100,
                           sum = round(c[5].sum/(c[5].positive+c[5].normal+c[5].negative),2)*100,
                           rank = rank)

@app.route('/다크홀')
def info_6():
    sql = "SELECT * \
                FROM drama WHERE id = 6"
    row = db_class.executeAll(sql)
    sql_actor = "SELECT * FROM actor WHERE id = 6"
    actors = db_class.executeAll(sql_actor)

    if round((c[6].positive+(c[6].normal*0.5))/(c[6].positive+c[6].normal+c[6].negative),2)*100 > 90: rank = "A"
    elif round((c[6].positive+(c[6].normal*0.5))/(c[6].positive+c[6].normal+c[6].negative),2)*100 > 80: rank = "B"
    elif round((c[6].positive+(c[6].normal*0.5))/(c[6].positive+c[6].normal+c[6].negative),2)*100 > 70: rank = "C"
    else: rank = "D"

    return render_template('다크홀.html', resultData=row[0], actor = actors,
                           chat=c[6].chat ,predict = c[6].predict,
                           pos = round(c[6].positive/(c[6].positive+c[6].normal+c[6].negative),2)*100,
                           nor = round(c[6].normal/(c[6].positive+c[6].normal+c[6].negative),2)*100,
                           neg = 100 - round((c[6].positive+c[6].normal)/(c[6].positive+c[6].normal+c[6].negative),2)*100,
                           sum = round(c[6].sum/(c[6].positive+c[6].normal+c[6].negative),2)*100,
                           rank = rank)

@app.route('/언더커버')
def info_7():
    sql = "SELECT * \
                FROM drama WHERE id = 7"
    row = db_class.executeAll(sql)
    sql_actor = "SELECT * FROM actor WHERE id = 7"
    actors = db_class.executeAll(sql_actor)

    if round((c[7].positive+(c[7].normal*0.5))/(c[7].positive+c[7].normal+c[7].negative),2)*100 > 90: rank = "A"
    elif round((c[7].positive+(c[7].normal*0.5))/(c[7].positive+c[7].normal+c[7].negative),2)*100 > 80: rank = "B"
    elif round((c[7].positive+(c[7].normal*0.5))/(c[7].positive+c[7].normal+c[7].negative),2)*100 > 70: rank = "C"
    else: rank = "D"

    return render_template('언더커버.html', resultData=row[0], actor = actors,
                           chat=c[7].chat ,predict = c[7].predict,
                           pos = round(c[7].positive/(c[7].positive+c[7].normal+c[7].negative),2)*100,
                           nor = round(c[7].normal/(c[7].positive+c[7].normal+c[7].negative),2)*100,
                           neg = 100 - round((c[7].positive+c[7].normal)/(c[7].positive+c[7].normal+c[7].negative),2)*100,
                           sum = round(c[7].sum/(c[7].positive+c[7].normal+c[7].negative),2)*100,
                           rank = rank)

@app.route('/오케이광자매')
def info_8():
    sql = "SELECT * \
                FROM drama WHERE id = 8"
    row = db_class.executeAll(sql)
    sql_actor = "SELECT * FROM actor WHERE id = 8"
    actors = db_class.executeAll(sql_actor)

    if round((c[8].positive+(c[8].normal*0.5))/(c[8].positive+c[8].normal+c[8].negative),2)*100 > 90: rank = "A"
    elif round((c[8].positive+(c[8].normal*0.5))/(c[8].positive+c[8].normal+c[8].negative),2)*100 > 80: rank = "B"
    elif round((c[8].positive+(c[8].normal*0.5))/(c[8].positive+c[8].normal+c[8].negative),2)*100 > 70: rank = "C"
    else: rank = "D"

    return render_template('오케이광자매.html', resultData=row[0], actor = actors,
                           chat=c[8].chat ,predict = c[8].predict,
                           pos = round(c[8].positive/(c[8].positive+c[8].normal+c[8].negative),2)*100,
                           nor = round(c[8].normal/(c[8].positive+c[8].normal+c[8].negative),2)*100,
                           neg = 100 - round((c[8].positive+c[8].normal)/(c[8].positive+c[8].normal+c[8].negative),2)*100,
                           sum = round(c[8].sum/(c[8].positive+c[8].normal+c[8].negative),2)*100,
                           rank = rank)

@app.route('/마인')
def info_9():
    sql = "SELECT * \
                FROM drama WHERE id = 9"
    row = db_class.executeAll(sql)
    sql_actor = "SELECT * FROM actor WHERE id = 9"
    actors = db_class.executeAll(sql_actor)

    if round((c[9].positive+(c[9].normal*0.5))/(c[9].positive+c[9].normal+c[9].negative),2)*100 > 90: rank = "A"
    elif round((c[9].positive+(c[9].normal*0.5))/(c[9].positive+c[9].normal+c[9].negative),2)*100 > 80: rank = "B"
    elif round((c[9].positive+(c[9].normal*0.5))/(c[9].positive+c[9].normal+c[9].negative),2)*100 > 70: rank = "C"
    else: rank = "D"

    return render_template('마인.html', resultData=row[0], actor = actors,
                           chat=c[9].chat ,predict = c[9].predict,
                           pos = round(c[9].positive/(c[9].positive+c[9].normal+c[9].negative),2)*100,
                           nor = round(c[9].normal/(c[9].positive+c[9].normal+c[9].negative),2)*100,
                           neg = 100 - round((c[9].positive+c[9].normal)/(c[9].positive+c[9].normal+c[9].negative),2)*100,
                           sum = round(c[9].sum/(c[9].positive+c[9].normal+c[9].negative),2)*100,
                           rank = rank)

@app.route('/보쌈')
def info_10():
    sql = "SELECT * \
                FROM drama WHERE id = 10"
    row = db_class.executeAll(sql)
    sql_actor = "SELECT * FROM actor WHERE id = 10"
    actors = db_class.executeAll(sql_actor)

    if round((c[10].positive+(c[10].normal*0.5))/(c[10].positive+c[10].normal+c[10].negative),2)*100 > 90: rank = "A"
    elif round((c[10].positive+(c[10].normal*0.5))/(c[10].positive+c[10].normal+c[10].negative),2)*100 > 80: rank = "B"
    elif round((c[10].positive+(c[10].normal*0.5))/(c[10].positive+c[10].normal+c[10].negative),2)*100 > 70: rank = "C"
    else: rank = "D"

    return render_template('보쌈.html', resultData=row[0], actor = actors,
                           chat=c[10].chat ,predict = c[10].predict,
                           pos = round(c[10].positive/(c[10].positive+c[10].normal+c[10].negative),2)*100,
                           nor = round(c[10].normal/(c[10].positive+c[10].normal+c[10].negative),2)*100,
                           neg = 100 - round((c[10].positive+c[10].normal)/(c[10].positive+c[10].normal+c[10].negative),2)*100,
                           sum = round(c[10].sum/(c[10].positive+c[10].normal+c[10].negative),2)*100,
                           rank = rank)

@app.route('/아모르파티')
def info_11():
    sql = "SELECT * \
                FROM drama WHERE id = 11"
    row = db_class.executeAll(sql)
    sql_actor = "SELECT * FROM actor WHERE id = 11"
    actors = db_class.executeAll(sql_actor)

    if round((c[11].positive+(c[11].normal*0.5))/(c[11].positive+c[11].normal+c[11].negative),2)*100 > 90: rank = "A"
    elif round((c[11].positive+(c[11].normal*0.5))/(c[11].positive+c[11].normal+c[11].negative),2)*100 > 80: rank = "B"
    elif round((c[11].positive+(c[11].normal*0.5))/(c[11].positive+c[11].normal+c[11].negative),2)*100 > 70: rank = "C"
    else: rank = "D"

    return render_template('아모르파티.html', resultData=row[0], actor = actors,
                           chat=c[11].chat ,predict = c[11].predict,
                           pos = round(c[11].positive/(c[11].positive+c[11].normal+c[11].negative),2)*100,
                           nor = round(c[11].normal/(c[11].positive+c[11].normal+c[11].negative),2)*100,
                           neg = 100 - round((c[11].positive+c[11].normal)/(c[11].positive+c[11].normal+c[11].negative),2)*100,
                           sum = round(c[11].sum/(c[11].positive+c[11].normal+c[11].negative),2)*100,
                           rank = rank)

@app.route('/밥이되어라')
def info_12():
    sql = "SELECT * \
                FROM drama WHERE id = 12"
    row = db_class.executeAll(sql)
    sql_actor = "SELECT * FROM actor WHERE id = 12"
    actors = db_class.executeAll(sql_actor)

    if round((c[12].positive+(c[12].normal*0.5))/(c[12].positive+c[12].normal+c[12].negative),2)*100 > 90: rank = "A"
    elif round((c[12].positive+(c[12].normal*0.5))/(c[12].positive+c[12].normal+c[12].negative),2)*100 > 80: rank = "B"
    elif round((c[12].positive+(c[12].normal*0.5))/(c[12].positive+c[12].normal+c[12].negative),2)*100 > 70: rank = "C"
    else: rank = "D"

    return render_template('밥이되어라.html',resultData=row[0], actor = actors,
                           chat=c[12].chat ,predict = c[12].predict,
                           pos = round(c[12].positive/(c[12].positive+c[12].normal+c[12].negative),2)*100,
                           nor = round(c[12].normal/(c[12].positive+c[12].normal+c[12].negative),2)*100,
                           neg = 100 - round((c[12].positive+c[12].normal)/(c[12].positive+c[12].normal+c[12].negative),2)*100,
                           sum = round(c[12].sum/(c[12].positive+c[12].normal+c[12].negative),2)*100,
                           rank = rank)

@app.route('/미스몬테크리스토')
def info_13():
    sql = "SELECT * \
                FROM drama WHERE id = 13"
    row = db_class.executeAll(sql)
    sql_actor = "SELECT * FROM actor WHERE id = 13"
    actors = db_class.executeAll(sql_actor)

    if round((c[13].positive+(c[13].normal*0.5))/(c[13].positive+c[13].normal+c[13].negative),2)*100 > 90: rank = "A"
    elif round((c[13].positive+(c[13].normal*0.5))/(c[13].positive+c[13].normal+c[13].negative),2)*100 > 80: rank = "B"
    elif round((c[13].positive+(c[13].normal*0.5))/(c[13].positive+c[13].normal+c[13].negative),2)*100 > 70: rank = "C"
    else: rank = "D"

    return render_template('미스몬테크리스토.html', resultData=row[0], actor = actors,
                           chat=c[13].chat ,predict = c[13].predict,
                           pos = round(c[13].positive/(c[13].positive+c[13].normal+c[13].negative),2)*100,
                           nor = round(c[13].normal/(c[13].positive+c[13].normal+c[13].negative),2)*100,
                           neg = 100 - round((c[13].positive+c[13].normal)/(c[13].positive+c[13].normal+c[13].negative),2)*100,
                           sum = round(c[13].sum/(c[13].positive+c[13].normal+c[13].negative),2)*100,
                           rank = rank)

@app.route('/속아도꿈결')
def info_14():
    sql = "SELECT * \
                FROM drama WHERE id = 14"
    row = db_class.executeAll(sql)
    sql_actor = "SELECT * FROM actor WHERE id = 14"
    actors = db_class.executeAll(sql_actor)

    if round((c[14].positive+(c[14].normal*0.5))/(c[14].positive+c[14].normal+c[14].negative),2)*100 > 90: rank = "A"
    elif round((c[14].positive+(c[14].normal*0.5))/(c[14].positive+c[14].normal+c[14].negative),2)*100 > 80: rank = "B"
    elif round((c[14].positive+(c[14].normal*0.5))/(c[14].positive+c[14].normal+c[14].negative),2)*100 > 70: rank = "C"
    else: rank = "D"

    return render_template('속아도꿈결.html', resultData=row[0], actor = actors,
                           chat=c[14].chat ,predict = c[14].predict,
                           pos = round(c[14].positive/(c[14].positive+c[14].normal+c[14].negative),2)*100,
                           nor = round(c[14].normal/(c[14].positive+c[14].normal+c[14].negative),2)*100,
                           neg = 100 - round((c[14].positive+c[14].normal)/(c[14].positive+c[14].normal+c[14].negative),2)*100,
                           sum = round(c[14].sum/(c[14].positive+c[14].normal+c[14].negative),2)*100,
                           rank = rank)
# 여기까지 추가
@app.route('/about')
def about():
    return render_template('about.html')

if __name__=='__main__':
    app.run(debug=True)
